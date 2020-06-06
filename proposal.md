## Project Proposal
### Exoplanet Search App

**Goal**  
The goal of this project is to provide a user friendly application allowing a user to easily search for and save exoplanet/host star information and understand the basic planetary and host star properties, as compared to our own system. 

**Expected Users**  
The application will be useful for experienced amateur astronomers as well as anyone with a beginner's interest in astronomy. Seasoned astronomers can use this site to search for detailed host star and planetary system data, while beginners can learn about how these properties compare to our own Sun and Earth.

**Data**  
The data resource used for this site will be NASA's Exoplanet API. Extensive exoplanet and host star data can be queried from the api and be returned into a site database. I plan to narrow down the data into handpicked columns, such as planetary orbit, mass, size, and the distance from the host star, as well the host star's spectral class, mass, radius, temperature, luminosity, and distance, if available. 

**Outline**  
First of all, the data schema will consist of a table of host stars, each with solar property columns and a relationship to one or many exoplanets. A table for exoplanets will contain planetary property columns for each exoplanet, including a host star column. A user will be able to search the database for stars or exoplanets. Example queries include:

* Search for stars by solar property(if available), such as mass, luminosity, size, distance
* Search for exoplanets by planetary property(if available), such as size, mass, orbit
* Search for stars by number of exoplanets in the system
* Search for stars and exoplanets within a given distance
* Search for exoplanets with a given star property, such as sun-like stars with a G2 spectral class

Each individual star or exoplanet result will include a chart/graphic showing how it compares with our system. A visual simulation of the star/planet size comparison using the returned radius, or star color comparison using B-V index would be nice to have, although these could be challenging to implement.  

Also, the site will include additional user functionality, including creating, updating, and deleting accounts, with which the user can save, edit, and delete searches and favorites. Therefore, user tables will be created in the database along with a search result table. A user can have one or many searches, each with ID's of one or many stars/planets. Issues aligning all of these database relationships are certainly expected.  Each user will have unique login usernames and encrypted password authentication. Additional functionality could include challenging users to find exoplanet-hosting stars (with a bright enough visual magnitude), and uploading astrophotography images found with a telescope. A feed on the home page could display user images.
