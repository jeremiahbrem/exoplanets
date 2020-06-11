class ProcessSearch:
    """Class for processing search form input data"""

    def __init__(self, parameter, search_input, min_num, max_num):
        "Creates instance for processing search inputs."
        
        self.parameter = parameter
        self.search_input = search_input
        self.min_num = min_num   
        self.max_num = max_num
        self.base_query = ("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?" +
                           "table=exoplanets&select=pl_name, pl_hostname, st_dist, st_spstr, pl_orbsmax," +
                           "pl_rade, pl_masse, st_rad, st_mass, st_bmvj, st_teff, st_optmag")

    def create_api_query(self):
        """Processes input data and returns a query for the api"""

        where = ""
        
        if self.parameter == 'all':
            return (f"{self.base_query}&format=json")

        if self.parameter == 'pl_name':
            return (f"{self.base_query}&where=pl_name like '{self.search_input}%25'&order={self.parameter}&format=json")

        if self.parameter == 'pl_hostname':
            return (f"{self.base_query}&where=pl_hostname like '{self.search_input}%25'&order={self.parameter}&format=json")

        if self.parameter == 'st_spstr':
            return (f"{self.base_query}&where=st_spstr like '{self.search_input}%25'&order={self.parameter}&format=json")        

        if self.min_num and self.max_num:
            where = f"&where={self.parameter}>{self.min_num} and {self.parameter}<{self.max_num}"
        elif self.min_num:
            where = f"&where={self.parameter}>{self.min_num}"
        elif self.max_num:
            where = f"&where={self.parameter}<{self.max_num}"

        return (f"{self.base_query}{where}&order={self.parameter}&format=json")    