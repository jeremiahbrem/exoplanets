import math

class HabitableZoneCheck:
    """Class instance methods for calculating if planet is in habitable zone"""

    def __init__(self, opt_mag, distance, spec_type, orbit):
        "Creates instance for checking habitable zone."
        
        self.opt_mag = opt_mag
        self.distance = distance
        self.spec_type = spec_type
        self.orbit = orbit

    @classmethod
    def calculate_luminosity(cls, opt_mag, distance, bol_corr):
        """Calculates the solar luminosity from optical
           magnitude, distance(parsecs), and bolometric
           correction"""

        if not opt_mag or not distance or not bol_corr:
            return None
        
        abs_mag = (opt_mag - 5 * math.log10(distance/10))
        bol_mag = (abs_mag + bol_corr)
        
        return math.pow(10,((bol_mag - 4.72) / -2.5))

    @classmethod
    def get_bolometric_correction(cls, spec_type):
        """Bolometric correction factor depending on spectral type"""
        
        if not spec_type:
            return None
        
        if spec_type[0] == 'B':
            return -2.0
        
        if spec_type[0] == 'A':
            return -0.3
        
        if spec_type[0] == 'F':
            return -0.15
        
        if spec_type[0] == 'G':
            return -0.4
        
        if spec_type[0] == 'K':
            return -0.8
        
        if spec_type[0] == 'M':
            return -2.0        

    def in_habitable_zone(self):
        """Using class methods, calculates is planet is
           within habitable zone boundaries """

        bol_corr = self.get_bolometric_correction(self.spec_type)
        luminosity = self.calculate_luminosity(self.opt_mag, self.distance, bol_corr)

        if luminosity:
            inner_bound = math.sqrt(luminosity / 1.1)
            outer_bound = math.sqrt(luminosity / 0.53)

            if self.orbit >= inner_bound and self.orbit <= outer_bound:
                return True
            else:
                return False    

        return "Unknown"                 