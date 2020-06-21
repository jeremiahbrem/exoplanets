$('#word-def').hide();

// event handler for select all
$("#all-check").click(function(){
  $(".checkboxes").prop('checked', $(this).prop('checked'));

});

const pageNum = parseInt($("#page-num").val());
const resultTotal = parseInt($("#result-length").val());

paginate(pageNum, resultTotal);

// displays page links on results page
function paginate(pageNum, resultTotal) {
  $("#next").text("").attr("href", "");
  $("#previous").text("").attr("href", "");
  $("#start").text("").attr("href", "");
  $("#last").text("").attr("href", "");
  $(".page-buttons").remove();
  const totalPages = getTotalPages(resultTotal);
  const start = getPageStart(totalPages, pageNum);
  let end = getPageEnd(totalPages, start);
  const next = getNextPageSet(totalPages, end);
  const previous = getPreviousPageSet(start);

  if (totalPages > end) {
    $("#next").text("Next10").attr("href", `/planets/results/${next}`);
    $("#last").text("Last").attr("href", `/planets/results/${totalPages}`);
  }

  if (pageNum >= 10) {
    $("#previous").text("Previous10").attr("href", `/planets/results/${previous}`);
    $("#start").text("Start").attr("href", `/planets/results/1`);
  }

  if (!end) {
    end = 2;
  }

  for (let i = start; i <= end; i++) {
    $("#pages").append(
      $(`<div class="page-buttons">
                <a href="/planets/results/${i}" id="${i}">${i}</a></div>`)
    );
  }
  $(`#${pageNum}`).removeAttr("href").parent().css("background-color", "rgb(68, 164, 228)");
}

// returns total number of pages (100 results each) depending on number of returned results
function getTotalPages(resultTotal) {
  let remainder = resultTotal % 100;
  if (resultTotal <= 100) {
    return 1;
  } else if (remainder > 0) {
    return Math.floor(resultTotal / 100) + 1;
  } else {
    return resultTotal / 100;
  }
}

// returns first page link of page set
function getPageStart(totalPages, pageNum) {
  if (totalPages <= 9 || pageNum <= 9) {
    return 1;
  } else {
    return Math.floor(pageNum / 10) * 10;
  }
}

// returns last page link of page set
function getPageEnd(totalPages, pageStart) {
  if (totalPages <= 9 && totalPages >= 1) {
    return totalPages;
  } else if (pageStart === 1) {
    return 9;
  } else {
    return pageStart + 9 <= totalPages ? pageStart + 9 : totalPages;
  }
}

// returns next set of 10 pages
function getNextPageSet(totalPages, pageEnd) {
  const nextTen = pageEnd + 1;
  if (totalPages >= 9 && pageEnd < totalPages) {
    if (totalPages < nextTen) return totalPages;
    return nextTen;
  }
}

// returns previous set of 10 pages
function getPreviousPageSet(pageStart) {
  if (pageStart > 10) {
    return pageStart - 10;
  }
  if (pageStart == 10) {
    return 1;
  }
}