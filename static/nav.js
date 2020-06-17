$(".nav-link").on("click", function(){
  $(".nav-link").find(".active").removeClass("active");
  $(this).addClass("active");
});