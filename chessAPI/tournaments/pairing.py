import copy


class Swiss:
    def __init__(self, players, games, round):
        self.pairs = []
        self.players = players
        self.games = games
        self.round = round

    def order_players(self):
        sorted_list = sorted(self.players, key=lambda x: (x[2], x[1]), reverse=True)
        return sorted_list

    def pairing(self):
        self.players = self.order_players()
        if self.round == 1:
            self.first_round_pairing()
        else:
            self.round_pairing()

        print(f'\npairs(Round {self.round}):', self.pairs)

    def is_odd_players(self):
        if len(self.players) % 2 == 1:
            return True
        return False

    def first_round_pairing(self):
        games_count = len(self.players) // 2
        for i in range(games_count):
            self.pairs.append([self.players[i][0], self.players[i + games_count][0]])

    def round_pairing(self):
        def set_block_matches():
            block_matches = dict()
            for player in self.players:
                block_matches[player[0]] = []

            for game in self.games:
                block_matches[game['white']].append(game['black'])
                block_matches[game['black']].append(game['white'])

            return block_matches

        def pairs_in_groups():
            groups_copy = copy.deepcopy(groups)

            for i in range(len(groups_copy)):
                set_pairs(groups_copy[i])
                update_group(groups_copy, i)

        # set as many as possible pairs in single group
        def set_pairs(group):
            p = 0
            while p < len(group) - 1:
                increase = 1
                for j in range(p + 1, len(group)):
                    if group[j] not in block_matches[group[p]]:
                        self.pairs.append(set_colors([group[p], group[j]]))
                        # first remove opp, then player
                        group.remove(group[j])
                        group.remove(group[p])
                        p, increase = 0, 0
                        break

                p += increase

        # move players without pair from higher to lower group
        # they are moved in front of list in case they should be first paired
        def update_group(groups_copy, group_index):
            if group_index + 1 < len(groups_copy):
                for player in groups_copy[group_index]:
                    groups_copy[group_index + 1].insert(0, player)

        def set_colors(players_pair):
            p1, p2 = player_colors(players_pair[0]), player_colors(players_pair[1])
            # print(players_pair[0], p1, players_pair[1], p2)
            p1_len = len([x for x in p1[::-1] if x == p1[-1]])
            p2_len = len([x for x in p2[::-1] if x == p2[-1]])

            if len(p1) == 0:
                if p2[-1] == 'W':
                    return players_pair
                return players_pair[::-1]
            elif len(p2) == 0:
                if p1[-1] == 'W':
                    return players_pair[::-1]
                return players_pair
            else:
                if p1[-1] == 'W' and p2[-1] == 'B':
                    return players_pair[::-1]
                elif p1[-1] == 'B' and p2[-1] == 'W':
                    return players_pair
                else:
                    if p1[-1] == 'W':
                        if p1_len > p2_len:
                            return players_pair[::-1]
                        else:
                            return players_pair
                    else:
                        if p1_len > p2_len:
                            return players_pair
                        else:
                            return players_pair[::-1]

        def player_colors(player):
            colors = ''
            for j in range(self.round - 1):
                tmp_games = [game for game in self.games if game['round'] == j + 1]
                color = ''
                for game in tmp_games:
                    if game['white'] == player:
                        color = 'W'
                    elif game['black'] == player:
                        color = 'B'

                colors += color
            return colors

        even_players = self.set_even_players()
        groups = self.set_groups(even_players)
        block_matches = set_block_matches()
        # print('block matches', block_matches)

        pairs_in_groups()

    def set_even_players(self):
        even_players = self.players.copy()
        if self.is_odd_players():
            player_to_break = self.player_to_break()
            even_players = [x for x in even_players if x[0] != player_to_break]

        return even_players

    def score_groups(self):
        score_groups = []

        players_score = set([x[2] for x in self.players])
        for score in players_score:
            score_groups.append(score)

        score_groups = sorted(score_groups, reverse=True)
        # print('score groups:', score_groups)
        return score_groups

    def set_groups(self, players_list):
        groups = []
        for group in self.score_groups():
            tmp = []
            for player in players_list:
                if player[2] == group:
                    tmp.append(player[0])
            groups.append(tmp)
        # print('groups:', groups)
        return groups

    def player_to_break(self):
        # 1. Make list of players which doesn't already have break
        players_game_count = {}
        for player in self.players:
            players_game_count[player[0]] = 0

        for game in self.games:
            players_game_count[game['white']] += 1
            players_game_count[game['black']] += 1

        players_to_break = [x for x in players_game_count.keys() if players_game_count[x] == self.round - 1]

        # 2. Choose player with lowest score and rating
        for player in self.players[::-1]:
            if player[0] in players_to_break:
                return player[0]

        return -1


class Berger:
    def __init__(self, players, round_no):
        self.players = players
        self.round_no = round_no
        self.players_no = self.odd_players_no()
        self.pairs = []

    def paired_players_id(self):
        players_id = [[self.players[pair[0] - 1], self.players[pair[1] - 1]] for pair in self.pairs]

        # Remove match which will have only one player
        players_id = [pair for pair in players_id if None not in pair]

        return players_id

    def get_match_no(self):
        return self.players_no // 2

    def odd_players_no(self):
        if len(self.players) % 2 == 1:
            self.players.append(None)

        return len(self.players)

    def pairing(self):
        for r_n in range(self.round_no):
            if r_n == 0:
                self.first_round_pairs()
            else:
                self.next_round_pairs(r_n)

        return self.paired_players_id()

    def first_round_pairs(self):
        for m_n in range(self.get_match_no()):
            self.pairs.append([m_n + 1, self.players_no - m_n])

    def next_round_pairs(self, r_n):
        tmp_pairs = []
        black_last_board = self.get_black_last_board()

        if r_n % 2 == 1:
            tmp_pairs.append([self.players_no, black_last_board])
        else:
            tmp_pairs.append([black_last_board, self.players_no])

        next_player = black_last_board + 1

        for i in range(1, self.get_match_no()):
            if next_player == self.players_no:
                next_player = 1
            tmp_pairs.append([next_player, -1])
            next_player += 1

        for i in range(self.get_match_no() - 1, 0, -1):
            if next_player == self.players_no:
                next_player = 1
            tmp_pairs[i][1] = next_player
            next_player += 1

        self.pairs = tmp_pairs

    def get_black_last_board(self):
        return self.pairs[len(self.pairs) - 1][1]
