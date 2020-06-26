class Favorites {

  // sends list id and array of planet names to database for adding a planet to a list
  static async addFavorites(listID, planetNames) {
    const data = { list_id: listID, planets: planetNames };
    const resp = await axios.post(
      `https://exoplanet-jbrem.herokuapp.com/users/${$("#username").text()}/favorites/add`,
      data
    );
    return resp;
  }

  // gathers list id from selected list and given planet to send delete request to database
  static async deleteFavorite(listID, planet) {
    const data = { list_id: listID, planet: planet };
    const resp = await axios.post(
      `https://exoplanet-jbrem.herokuapp.com/users/${$("#username").text()}/favorites/delete`,
      data
    );
    return resp.data;
  }

//   static async createList(name, userID) {
//     const data = { name: name, user_id: userID};
//     const resp = await axios.post(
//       // `https://exoplanet-jbrem.herokuapp.com/users/${$("#username").text()}/lists/create`,
//       `https://localhost:5000/users/${$("#username").text()}/favorites/delete`,
//       data
//     );
//     return resp.data;
//   }
}