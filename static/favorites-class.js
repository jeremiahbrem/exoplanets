class Favorites {

  // sends list id and array of planet names to database for adding a planet to a list
  static async addFavorites(listID, planetNames) {
    const data = { list_id: listID, planets: planetNames };
    const resp = await axios.post(
      `https://127.0.0.1:5000//users/${$("#username").text()}/favorites/add`,
      data
    );
    const list = resp.data.new_favorites.list;
    const planets = resp.data.new_favorites.planets;
    return { list: list, planets: planets };
  }

  // gathers list id from selected list and given planet to send delete request to database
  static async deleteFavorite(listID, planet) {
    const data = { list_id: listID, planet: planet };
    const resp = await axios.post(
      `https://127.0.0.1:5000/users/${$("#username").text()}/favorites/delete`,
      data
    );
    return resp.data;
  }
}