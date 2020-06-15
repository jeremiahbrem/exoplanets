// adds event listener to add button for adding planets to selected list
$("#add-planets").on("click", handleAdd);

// handles add button click for adding planets to selected list
async function handleAdd(evt) {
  const id = $('#lists').val();
  const checkboxes = $(".checkboxes").toArray();
  const checked = checkboxes.filter(
    (checkbox) => checkbox.checked == true
  );
  planets = checked.map((checkbox) => checkbox.id);
  const resp = await addFavorites(id, planets)
  if (planets.length > 1) {
    $("#message").text("Planets added to list.");
  } else if (planets.length == 1) {
    $("#message").text("Planet added to list.");
  }
  setTimeout(() => {
    $("#message").text("");
  }, 3000)
  
}

// sends list id and array of planet names to database for adding a planet to a list
async function addFavorites(listID, planetNames) {
  data = { list_id: listID, planets: planetNames };
  const resp = await axios.post(
    `http://localhost:5000/users/${$("#username").text()}/favorites/add`,
    data
  );
  const list = resp.data.new_favorites.list;
  const planets = resp.data.new_favorites.planets;
  return { list: list, planets: planets };
}

// add event listener to delete buttons
$(".delete-planet").on("click", handleDelete);

// handles delete button click, sends delete request to database, and deletes from page
async function handleDelete(evt) {
  const planet = evt.target.previousElementSibling.text;
  evt.target.parentElement.remove();
  await deleteFavorite(planet);
}

// gathers list id from selected list and given planet to send delete request to database
async function deleteFavorite(planet) {
  const listID = $("#list-id").val();
  data = { list_id: listID, planet: planet };

  const resp = await axios.post(
    `http://localhost:5000/users/${$("#username").text()}/favorites/delete`,
    data
  );
  return resp.data;
}
