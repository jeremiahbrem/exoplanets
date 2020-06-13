paginate();
function paginate() {
  let totalPages;
  let pageStart;
  let pageEnd;
  const resultTotal = $('#result-length').val();
  let pageNum = $('#page-num').val();
  let remainder = resultTotal % 100;
  if (resultTotal <= 100) {
      totalPages = 1;
  }
  else if (remainder > 0) {
      totalPages = parseInt(resultTotal / 100) + 1;
  }
  else {
      totalPages = parseInt(resultTotal / 100);
  }
  
  if (totalPages <= 10) {
      pageStart = 1;
      pageEnd = totalPages;
  }
  else {
      pageStart = Math.floor(pageNum / 10) * 10 + 1;
      pageEnd = (pageStart + 10) <= totalPages ? (pageStart + 10) : totalPages;
  }

  for (let i = pageStart; i <= pageEnd; i++) {
      $('#pages').append($(`<div class="page-buttons">
                <a href="/planets/results/${i}" id="${i}">${i}</a></div>`));
  }
  $(`#${pageNum}`).removeAttr("href");
}