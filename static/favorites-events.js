// zoomout animation when planet clicked
$('.planet-list-items').on("click", () =>
{
  $(".loader").show();
  $('.exoplanet').css("transition", "transform 1s");
  $('.exoplanet').css("transform", "scale(.001)");
})

$('#go-to-list').on("click", () => {
  if ($('#lists').val()) {
    const username = $('#username').text();
    window.location.href = `/users/${username}/lists/${$('#lists').val()}`
  }
})

$("#lists").change(() => {
  if ($('#lists').val() == "create-list") {
    $('#create-text').prop("hidden", false);
  }
  else {
    $('#create-text').prop("hidden", true);
  }
})

// adds event listener to add button for adding planets to selected list
$("#add-planets").on("click", handleAdd);

// sort select list
const myOptions = $("#lists option");
const selected = $("#lists").val();

myOptions.sort(function(a,b) {
    if (a.text > b.text && a.text) return 1;
    if (a.text < b.text && b.text != "Create list") return -1;
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
 
  for (let message in resp.data.messages) {
    $('#message').append(`<p>${entry}</p>`).css("margin", "0");
  }
  setTimeout(() => {
    $("#message").html("");
  }, 3000)
  $('.checkboxes').prop("checked",false);
  $('#all-check').prop("checked",false);
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

