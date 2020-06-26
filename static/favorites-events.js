// zoomout animation when planet clicked
$('.planet-list-items').on("click", () =>
{
  $(".loader").show();
  $('.exoplanet').css("transition", "transform 1s");
  $('.exoplanet').css("transform", "scale(.001)");
})

// redirect to list page
$('#go-to-list').on("click", () => {
  if ($('#lists').val()) {
    const username = $('#username').text();
    window.location.href = `/users/${username}/lists/${$('#lists').val()}`
  }
})

// enables text input to create list
$("#lists").change(() => {
  if ($('#lists').val() == "create-list") {
    $('#create-text').prop("hidden", false);
    $('#add-planets').prop("hidden", true);
    $('#add-planet').prop("hidden", true);
    $('#go-to-list').prop("hidden", true);
    $('#create-list-btn').prop("hidden", false);
  }
  else {
    $('#create-text').prop("hidden", true);
    $('#add-planets').prop("hidden", false);
    $('#add-planet').prop("hidden", false);
    $('#go-to-list').prop("hidden", false);
    $('#create-list-btn').prop("hidden", true);
  }
})

// handler for create list button click
$('#create-list-btn').on("click", async function() {
  let message;
  if ($('#create-text').val()) {
    const resp = await Favorites.createList($('#create-text').val());
    if (resp == "List already exists") {
      message = resp;
    }
    else {
      $('#lists').append(`<option value="${resp.list_id}"> 
          ${resp.list_name}</option>`);
      message = "List created";
      sortList()
      $('#create-text').prop("hidden", true);
      $('#add-planets').prop("hidden", false);
      $('#add-planet').prop("hidden", false);
      $('#go-to-list').prop("hidden", false);
      $('#create-list-btn').prop("hidden", true);
      $('#lists').val("");
    }
    $('#message').append(`<p>${message}</p>`).css("margin", "0");
    setTimeout(() => {
      $("#message").html("");
    }, 3000)
  }
})

// adds event listener to add button for adding planets to selected list
$("#add-planets").on("click", handleAdd);

// addes event lister for add button on planet details page
$("#add-planet").on("click", handleAddPlanet);

// sort select list
sortList()

function sortList() {
  const myOptions = $("#lists option");
  const selected = $("#lists").val();

  myOptions.sort(function(a,b) {
    if (a.text > b.text && a.text) return 1;
    if (a.text < b.text && b.text != "Create list") return -1;
    return 0
  })

  $("#lists").empty().append(myOptions);
  $("#lists").val(selected);
}

// handles add button click for adding planets to selected list
async function handleAdd(evt) {
  const id = $('#lists').val();
  const checkboxes = $(".checkboxes").toArray();
  const checked = checkboxes.filter(
    (checkbox) => checkbox.checked == true
  );
  planets = checked.map((checkbox) => checkbox.id);
  const resp = await Favorites.addFavorites(id, planets)

  for (let message of resp.data.messages) {
    $('#message').append(`<p>${message}</p>`).css("margin", "0");
  }
  setTimeout(() => {
    $("#message").html("");
  }, 3000)
  $('.checkboxes').prop("checked",false);
  $('#all-check').prop("checked",false); 
}

// handles add button click on planet details page
async function handleAddPlanet(evt) {
  const id = $('#lists').val();
  const planet = $('#planet-name').text();
  const planetArray = [planet]
  const resp = await Favorites.addFavorites(id, planetArray)
  for (let message of resp.data.messages) {
    $('#message').append(`<p>${message}</p>`).css("margin", "0");
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



