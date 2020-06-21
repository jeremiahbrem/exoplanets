// zoomout animation when planet clicked
$('.planet-list-items').on("click", () =>
{
  $('#pl-sn').css("transition", "transform 1s");
  $('#pl-sn').css("transform", "scale(.001)");
})

$('#go-to-list').on("click", () => {
  if ($('#lists').val()) {
    const username = $('#username').text();
    window.location.href = `/users/${username}/lists/${$('#lists').val()}`
  }
})

// adds event listener to add button for adding planets to selected list
$("#add-planets").on("click", handleAdd);

// sort select list
const myOptions = $("#lists option");
const selected = $("#lists").val();

myOptions.sort(function(a,b) {
    if (a.text > b.text) return 1;
    if (a.text < b.text) return -1;
    return 0
})

$("#lists").empty().append(myOptions);
$("#lists").val(selected);

// handles add button click for adding planets to selected list
async function handleAdd(evt) {
  const id = $('#lists').val();
  const checkboxes = $(".checkboxes").toArray();
  const checked = checkboxes.filter(
    (checkbox) => checkbox.checked == true
  );
  planets = checked.map((checkbox) => checkbox.id);
  const resp = await Favorites.addFavorites(id, planets)
  for (let entry in resp) {
    if (entry.slice(0,18) == "You already added") {
      $('#message').text(entry);
      setTimeout(() => {
        $('#message').text("")
      }, 4000);
    }
  }
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
$(".fas").on("click", handleDelete);

// handles delete button click, sends delete request to database, and deletes from page
async function handleDelete(evt) {
  const listID = $("#list-id").val();
  const planet = evt.target.nextElementSibling.text;
  evt.target.parentElement.remove();
  await Favorites.deleteFavorite(listID, planet);
}

