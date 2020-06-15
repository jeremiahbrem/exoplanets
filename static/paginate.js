const pageNum = parseInt($("#page-num").val());
const resultTotal = parseInt($("#result-length").val());

paginate(pageNum, resultTotal);

// displays page links on results page
function paginate(pageNum, resultTotal) {
  $("#next").text("").attr("href", "");
  $("#previous").text("").attr("href", "");
  $(".page-buttons").remove();
  const totalPages = getTotalPages(resultTotal);
  const start = getPageStart(totalPages, pageNum);
  let end = getPageEnd(totalPages, start);
  const next = getNextPageSet(totalPages, end);
  const previous = getPreviousPageSet(next);

  if (totalPages > end) {
    $("#next").text("Next").attr("href", `/planets/results/${next}`);
  }

  if (pageNum >= 10) {
    $("#previous")
      .text("Previous")
      .attr("href", `/planets/results/${previous}`);
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
  $(`#${pageNum}`).removeAttr("href");
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
function getPreviousPageSet(nextSet) {
  if (nextSet == 20) {
    return 1;
  } else if (nextSet > 20) {
    return nextSet - 20;
  }
}