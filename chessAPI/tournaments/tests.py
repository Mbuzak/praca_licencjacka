import django
import unittest
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chessAPI.settings')
django.setup()

from .calculate import Berger, get_player_calculate_rating, is_match_result_valid


# Create your tests here.


class BergerTest(unittest.TestCase):
    def setUp(self):
        players = [x for x in range(1, 10)]
        round_no = 3
        self.berger = Berger(players, round_no)

    def test_odd_players_no(self):
        self.assertEqual(10, self.berger.players_no)

    def test_get_match_no(self):
        self.assertEqual(5, self.berger.get_match_no())

    def test_first_round_pairs(self):
        result = [[1, 10], [2, 9], [3, 8], [4, 7], [5, 6]]
        self.berger.first_round_pairs()
        self.assertEqual(result, self.berger.pairs)

    def test_get_black_last_board(self):
        self.berger.first_round_pairs()
        self.assertEqual(6, self.berger.get_black_last_board())

    def test_pairing(self):
        result = [[2, 10], [3, 1], [4, 9], [5, 8], [6, 7]]
        self.berger.pairing()
        self.assertEqual(result, self.berger.pairs)

    def test_players_id(self):
        players_id = [201, 205, 202, 203, 209, 208, 207, 200, 199]
        new_berger = Berger(players_id, 3)
        result = [[202, 201], [203, 199], [209, 200], [208, 207]]

        self.assertEqual(result, new_berger.pairing())


class PlayerCalculateRatingTest(unittest.TestCase):
    def setUp(self):
        self.opp_ratings = [1200, 1400, 1600, 1400, 1800, 1000]
        self.player_rating = 1600

    def test_get_rating_1(self):
        score = 4.5
        self.assertEqual(1600, get_player_calculate_rating(self.player_rating, self.opp_ratings, score))

    def test_get_rating_2(self):
        score = 5  # ((5 - 4,5) * 2) * 400 / 7 ~= 57
        self.assertAlmostEqual(1657, get_player_calculate_rating(self.player_rating, self.opp_ratings, score), delta=1)


class MatchResultTest(unittest.TestCase):
    def test_match_1(self):
        self.assertEqual(True, is_match_result_valid(0.5, 0.5))

    def test_match_2(self):
        self.assertEqual(False, is_match_result_valid(0.7, 0.3))

    def test_match_3(self):
        self.assertEqual(False, is_match_result_valid(-5, 5))


if __name__ == '__main__':
    unittest.main()
