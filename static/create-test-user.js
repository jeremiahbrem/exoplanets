describe ("Creating test user for unittests", () => {

   
    $('#username').val("testuser");
    $('#password').val("testpassword");
    $('#email').val("test@example.com");
    $('#first_name').val("First");
    $('#last_name').val("Last");
    $("button").trigger("click");
})