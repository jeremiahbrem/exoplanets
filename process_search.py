class ProcessSearch:
    """Class for processing search form input data"""

    def __init__(self, parameters):
        "Creates instance for processing search inputs."
        
        self.parameters = parameters
        self.base_query = ("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?" +
                           "api_key=9GxYHa5XdrMcw1czzRmM7xtWyxHrEUS8dxHyNiK7&table=exoplanets" + 
                           "&select=pl_name,pl_hostname,st_dist,st_spstr,pl_orbsmax," +
                           "pl_rade,pl_masse,pl_pnum,st_rad,st_mass,st_bmvj,st_teff,st_optmag")

    def create_api_query(self):
        """Processes input data and returns a query for the api"""
       
        where = "&where="
        
        if self.parameters.get('all', None):
            return (f"{self.base_query}&format=json")

        if self.parameters.get('pl_name', None):
            if "+" in self.parameters.get('pl_name'):
                formatted_string = self.parameters.get('pl_name').replace("+", f"%2b")
                return (f"{self.base_query}&where=pl_name like '{formatted_string}%25'&order=pl_name&format=json")
            else:
                return (f"{self.base_query}&where=pl_name like '{self.parameters.get('pl_name')}%25'&order=pl_name&format=json")    

        if self.parameters.get('pl_hostname', None):
            return (f"{self.base_query}&where=pl_hostname like '{self.parameters['pl_hostname']}%25'&order=pl_hostname&format=json")

        count = 1
        for key,value in self.parameters.items():
            min_value = self.parameters.get(f"{key}_min", None)
            max_value = self.parameters.get(f"{key}_max", None)
            
            if key != "habitable":
                if value == 'on' and key == 'st_spstr' and self.parameters['st_spstr_type']:
                    if count > 1:
                        where = where + " and "
                    where = where + f"st_spstr like '{self.parameters['st_spstr_type']}%25'"
                if value == 'on' and (min_value or max_value):
                    if count > 1:
                        where = where + " and "
                    where = where + f"{key}"
                    if min_value and max_value:
                        where = where + f">{min_value} and {key}<{max_value}"
                    elif min_value:
                        where = where + f">{min_value}" 
                    elif max_value:
                        where = where + f"<{max_value}"
                count += 1        

        return f"{self.base_query}{where}&order=pl_name&format=json" 