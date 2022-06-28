from django.db.models import Max
from .models import TournamentMember, Match, Round, Promotion
from ratings.models import FideRating, TITLE_TUPLE, THRESHOLD
from accounts.models import Account, GENDER
from .pairing import Berger


def is_match_result_valid(white_result, black_result):
    if white_result is None or black_result is None:
        return False
    if white_result not in [0, 0.5, 1] or white_result + black_result != 1:
        return False
    return True


def create_pairing(pk):
    players = [player.id for player in TournamentMember.objects.filter(tournament_id=pk)]
    last_round = Round.objects.filter(tournament_id=pk).latest('round')
    berger = Berger(players, last_round.id)
    pairs = berger.pairing()

    for i in range(len(pairs)):
        Match(round_id=last_round.id, chessboard=i + 1, white_id=pairs[i][0], black_id=pairs[i][1]).save()


def update_results(pk):
    rounds_id = [item.id for item in Round.objects.filter(tournament_id=pk)]
    matches = Match.objects.filter(round_id__in=rounds_id)

    for member in TournamentMember.objects.filter(tournament_id=pk):
        white_points = sum([x.white_result for x in matches.filter(white_id=member.id)])
        black_points = sum([x.black_result for x in matches.filter(black_id=member.id)])

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
    if member_count % 2 == 1:
        return member_count - 1
    return member_count


def get_player_calculate_rating(player_rating, opp_ratings, score):
    games_no = len(opp_ratings)
    opp_ratings_sum = sum(opp_ratings)
    return (1 / (games_no + 1)) * (player_rating + opp_ratings_sum + 400 * ((2 * score) - games_no))


def verify_promotion(promotion):
    promotion.status = 'accepted'
    promotion.save()

    account = Account.objects.get(pk=promotion.participant.person.id)
    account.title = promotion.title
    account.save()


def set_participants_promotion(tournament):
    for member in TournamentMember.objects.filter(tournament_id=tournament.id):
        acc = Account.objects.get(pk=member.person.id)
        begin = TITLE_TUPLE.index(acc.title) + 1
        end = len(TITLE_TUPLE) - 1

        # calculate rating
        rounds = [x.id for x in Round.objects.filter(tournament_id=tournament.id)]
        opp_ratings = list()
        [opp_ratings.append(match.black.get_rating()) for match in Match.objects.filter(white_id=member.id, round_id__in=rounds)]
        [opp_ratings.append(match.white.get_rating()) for match in Match.objects.filter(black_id=member.id, round_id__in=rounds)]

        calculate_rating = get_player_calculate_rating(member.get_rating(), opp_ratings, member.points)

        new_title = None
        for i in range(begin, end):
            if calculate_rating >= THRESHOLD[GENDER[acc.gender]][TITLE_TUPLE[i]]:
                new_title = TITLE_TUPLE[i]

        if new_title:
            Promotion(participant=member, title=new_title, status='awaiting').save()
