describe ("Creating test list for unittests", () => {

    if ($("#my-lists li").length == 0) {
      window.location.href = "http://localhost:5000/users/testuser/lists/create"
      $('#name').val("testlist");
      $('#description').val("My test planets");
      $("button").trigger("click");
    }
})