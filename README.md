## Exoplanet App  
##### A discovery tool for anyone, whether an astronomy enthusiast or a casual observer, to search for and learn about exoplanets and their host stars. Data for the site is queried from the NASA Exoplanet API.

<https://exoplanet-jbrem.herokuapp.com>  

##### NASA Exoplanet API  
The NASA exoplanet data can be gathered by using SQL query url requests. An example query:  

    http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=st_spstr&where=st_spstr%20like%20%27M5%25%27&format=json  

The Exoplanet App allows a user to fill out a simple search form for chosen parameters, and the application uses Python algorithms to create complex queries based on the user's search inputs to return a table of results.  

##### Search parameter options:  
- Planet name, mass, radius, and orbit  
- Host star name, number of planets, mass, radius, and distance
- Host star optical magnitude, B-V color index, spectral type, and surface temperature  
- Habitability - calculated from optical magnitude, orbit, spectral-type, and distance, if available

##### User features  
- Account creation, editing, and deletion
- Password hashing and password email resetting  
- Planet favorites list creation, editing, and deleting  
- Sorting results table data and adding selected planets to user list   

##### Visual effects
Many people are unaware of how beautiful it is to view the color contrast between two stars with different surface temperatures.  A goal of this site was to give users a beautiful representation of star color contrast and how the view might look from an exoplanet with different properties than our own. Most stars on the site include visual simulations of color comparisons with the sun, based off B-V index, surface temperature, or spectral-type. If data is available, this site also includes visual simulations of star size comparisons with the sun, and planet size comparisons with the earth. Exoplanet images are simulated based off planet mass, radius, habitability, or orbital distance.  

##### Testing
This project was guided by test-driven development and includes Python-Flask and Jasmine-JavaScript unit and integration tests.  

##### Resources:  
- NASA Exoplanet API  
    <http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets>  
- Planetary Biology  
    <https://www.planetarybiology.com/>  

##### Tools:  
- Python
- JavaScript
- Flask
- SQLAlchemy  
- Bootstrap  
- HTML/CSS  
- JQuery
- Axios
