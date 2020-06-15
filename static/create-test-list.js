describe ("Creating test list for unittests", () => {

    if (!$('#testlist')) {
      window.location.href = "http://localhost:5000/users/testuser/lists/create"
      $('#name').val("testlist");
      $('#description').val("My test planets");
      $("button").trigger("click");
    }
})