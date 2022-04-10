from django.db.models import Max
from .models import TournamentMember, Match, Round
from ratings.models import FideRating, TITLE_TUPLE, THRESHOLD
from django.db.models import Q
from accounts.models import Account


results = {
    '1': 1,
    '0.5': 0.5,
    '0': 0,
    '+': 1,
    '-': 0,
}


def berger_system(n):
    def odd_players(x):
        if x % 2 == 0:
            return x
        return x + 1

    n = odd_players(n)

    matches_in_round = int(n / 2)
    games = int(n / 2 * (n - 1))
    rounds = int(games / matches_in_round)

    pairing = dict()

    for i in range(rounds):
        match_list = [[0, 0] for _ in range(matches_in_round)]

        if i == 0:
            for j in range(matches_in_round):
                match_list[j] = [1 + j, n - j]
        else:
            black_last_board = pairing[i][matches_in_round - 1][1]

            if i % 2 == 1:
                match_list[0] = [n, black_last_board]
            else:
                match_list[0] = [black_last_board, n]

            p = black_last_board + 1

            for j in range(1, matches_in_round):
                if p == n:
                    p = 1
                match_list[j][0] = p
                p += 1

            for j in range(matches_in_round - 1, 0, -1):
                if p == n:
                    p = 1
                match_list[j][1] = p
                p += 1
        pairing[i + 1] = match_list
    return pairing


def create_pairing(pk):
    players = TournamentMember.objects.filter(tournament_id=pk)
    players_count = len(players)
    odd_players = [False, 0]
    if len(players) % 2 == 1:
        players_count += 1
        odd_players = [True, 1]
    last_round = Round.objects.filter(tournament_id=pk).latest('round')

    pairing = berger_system(players_count)[last_round.round]

    for i in range(0 + odd_players[1], len(pairing)):
        Match(round_id=last_round.id, chessboard=i + 1 - odd_players[1],
              white_id=players[pairing[i][0] - 1].id, black_id=players[pairing[i][1] - 1].id).save()


def update_results(pk):
    rounds_id = [item.id for item in Round.objects.filter(tournament_id=pk)]
    matches = Match.objects.filter(round_id__in=rounds_id)

    for member in TournamentMember.objects.filter(tournament_id=pk):
        white_points = sum([results[x.white_result] for x in matches.filter(white_id=member.id)])
        black_points = sum([results[x.black_result] for x in matches.filter(black_id=member.id)])

        member.points = white_points + black_points
        member.save()


def create_round(pk):
    def set_round():
        if Round.objects.filter(tournament_id=pk):
            return Round.objects.filter(tournament_id=pk).aggregate(Max('round'))['round__max'] + 1
        return 1
    Round(tournament_id=pk, round=set_round()).save()


def get_fide_rating(account_id, tournament_type):
    if FideRating.objects.filter(person_id=account_id):
        rating = FideRating.objects.get(person_id=account_id)
        if rating:
            if tournament_type == 'błyskawiczny':
                if rating.blitz:
                    return rating.blitz
            elif tournament_type == 'szybki':
                if rating.rapid:
                    return rating.rapid
            elif tournament_type == 'klasyczny':
                if rating.classic:
                    return rating.classic
    return 0


def round_count(pk):
    member_count = len(TournamentMember.objects.filter(tournament=pk))
    if member_count % 2 == 0:
        return member_count - 1
    return member_count


def obtain_rating(tournament, member):
    rounds = [x.id for x in Round.objects.filter(tournament_id=tournament.id)]
    matches = Match.objects.filter(Q(white_id=member.id) | Q(black_id=member.id), round_id__in=rounds)

    rating_sum = 0
    for match in matches:
        if match.white.id == member.id:
            rating_sum += match.black.get_polish_rating()
        else:
            rating_sum += match.white.get_polish_rating()

    match_count = len(matches)
    person_rating = member.get_polish_rating()
    points = member.points

    calculate_rating = (1 / (match_count + 1)) * (person_rating + rating_sum + 400 * ((2 * points) - match_count))
    return round(calculate_rating)


def update_categories(tournament):
    for member in TournamentMember.objects.filter(tournament_id=tournament.id):
        acc = Account.objects.get(pk=member.person.id)
        begin = TITLE_TUPLE.index(acc.title) + 1
        end = len(TITLE_TUPLE) - 1

        rating = obtain_rating(tournament, member)

        if acc.gender == 'M':
            gender = 'male'
        else:
            gender = 'female'

        new_category = None
        for i in range(begin, end):
            if rating >= THRESHOLD[gender][TITLE_TUPLE[i]]:
                new_category = TITLE_TUPLE[i]

        if new_category:
            acc.title = new_category
            acc.save()
