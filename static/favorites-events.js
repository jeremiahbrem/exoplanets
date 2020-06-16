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
  const resp = await Favorites.addFavorites(id, planets)
  if (planets.length > 1) {
    $("#message").text("Planets added to list.");
  } else if (planets.length == 1) {
    $("#message").text("Planet added to list.");
  }
  setTimeout(() => {
    $("#message").text("");
  }, 3000)
  $('.checkboxes').prop("checked",false);
}

// add event listener to delete buttons
$(".delete-planet").on("click", handleDelete);

// handles delete button click, sends delete request to database, and deletes from page
async function handleDelete(evt) {
  const listID = $("#list-id").val();
  const planet = evt.target.previousElementSibling.text;
  evt.target.parentElement.remove();
  await Favorites.deleteFavorite(listID, planet);
}