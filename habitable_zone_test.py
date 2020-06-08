from habitable_zone import HabitableZone
from app import app
from unittest import TestCase

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

class HabitableZoneTestCase(TestCase):
    """Test Data functions."""

    def setUp(self):
        """Define test client"""

        self.client = app.test_client()    

    def test_get_bolometric_correction(self):

        cor = HabitableZone.get_bolometric_correction("G2")

        self.assertEqual(cor, -0.4)

    def test_calculate_luminosity(self):

        lum = HabitableZone.calculate_luminosity(10.55,6.26,-2.0)  

        self.assertEqual("{:.3f}".format(lum), '0.012')  

    def test_habitable(self):

        self.assertEqual(HabitableZone.in_habitable_zone(.00794,.09),True)     