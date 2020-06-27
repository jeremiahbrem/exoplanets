// clear checkboxes on page load or cached load
window.onpageshow = () => {
  $('.check').prop('checked', false);
}

// adds event listener to check
$(".check").change(enableSearchOption);

$(".btn").on("click", () => {
  $(".loader").show();
})

// event listener for select all
$("#select-all").click(function(){
  $(".check").prop('checked', $(this).prop('checked'));
  if ($('#select-all').prop('checked') == true) {
    $('input').prop("disabled", false);
  }
  else if ($('#select-all').prop('checked') == false) {
    $('input').prop("disabled", true);
  }
  $('.check, #planet-name, #st-name, #all').prop("disabled", false);  
});  

// enables search options if parameter checkbox checked
function enableSearchOption(evt) {
    const id = evt.target.id;
    if ($(`#${id}`).prop("checked") == true) {
      $(`.${id}`).prop("disabled", false);
    } else if ($(`#${id}`).prop("checked") == false) {
      $(`.${id}`).prop("disabled", true);
    }
  }