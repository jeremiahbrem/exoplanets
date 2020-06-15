from habitable_zone import HabitableZoneCheck
from app import app
from unittest import TestCase

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

class HabitableZoneTestCase(TestCase):
    """Test HabitableZoneCheck functions."""

    def setUp(self):
        """Define test client"""

        self.client = app.test_client() 

        self.check_zone = HabitableZoneCheck(9.87,3.80,'M3.5', 0.09)

    def test_get_bolometric_correction(self):

        cor = HabitableZoneCheck.get_bolometric_correction("G2")

        self.assertEqual(cor, -0.4)

    def test_calculate_luminosity(self):

        lum = HabitableZoneCheck.calculate_luminosity(10.55,6.26,-2.0)  

        self.assertEqual("{:.3f}".format(lum), '0.012')  

    def test_in_habitable_zone(self):

        self.assertEqual(self.check_zone.in_habitable_zone(),True)

        self.check_zone.orbit = 1.99
        self.assertEqual(self.check_zone.in_habitable_zone(), False) 