// sort select list
const myLists = $("#my-lists li");
// const selected = $("#lists").val();

myLists.sort(function(a,b) {
    if (a.id > b.id) return 1;
    if (a.id < b.id) return -1;
    return 0
})

$("#my-lists").empty().append(myLists);
// $("#lists").val(selected);