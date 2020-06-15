// adds event listener to check
$(".check").change(enableSearchOption);

// enables search options if parameter checkbox checked
function enableSearchOption(evt) {
    const id = evt.target.id;
    if ($(`#${id}`).prop("checked") == true) {
      $(`.${id}`).prop("disabled", false);
    } else if ($(`#${id}`).prop("checked") == false) {
      $(`.${id}`).prop("disabled", true);
    }
  }