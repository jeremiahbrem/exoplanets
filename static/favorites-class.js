class Favorites {

  // sends list id and array of planet names to database for adding a planet to a list
  static async addFavorites(listID, planetNames) {
    const data = { list_id: listID, planets: planetNames };
    const resp = await axios.post(
      `https://exoplanet-jbrem.herokuapp.com/users/${$("#username").text()}/favorites/add`,
      // `http://localhost:5000/users/${$("#username").text()}/favorites/add`,
      data
    );
    return resp;
  }

  // gathers list id from selected list and given planet to send delete request to database
  static async deleteFavorite(listID, planet) {
    const data = { list_id: listID, planet: planet };
    const resp = await axios.post(
      `https://exoplanet-jbrem.herokuapp.com/users/${$("#username").text()}/favorites/delete`,
      // `http://localhost:5000/users/${$("#username").text()}/favorites/delete`,
      data
    );
    return resp.data;
  }

  // creates new favorites list from results and planet details page
  static async createList(name) {
    const data = { name: name };
    const resp = await axios.post(
      `https://exoplanet-jbrem.herokuapp.com/users/${$("#username").text()}/favorites/create-list`,
      // `http://localhost:5000/users/${$("#username").text()}/favorites/create-list`,
      data
    );
    return resp.data;
  }
}