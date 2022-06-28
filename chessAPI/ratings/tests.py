import django
import unittest
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chessAPI.settings')
django.setup()

from .views import fide_profile

# Create your tests here.


class FideProfileTest(unittest.TestCase):
    # test date: 23.06.2022

    def test_valid_fide_profile(self):
        fide_id = '21099421'
        result = ['std', '1287', 'rapid', '1284', 'blitz', 0, 'None']
        self.assertEqual(result, fide_profile(fide_id))

    def test_invalid_fide_profile(self):
        fide_id = '21099422'
        self.assertEqual(-1, fide_profile(fide_id))


if __name__ == '__main__':
    unittest.main()
