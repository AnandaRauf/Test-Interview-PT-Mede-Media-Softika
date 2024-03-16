// Menampilkan modal saat tombol DETAIL diklik
$('.modal-trigger').click(function() {
    $('#myModal').fadeIn();
  });
  
  // Menutup modal saat tombol Close (X) diklik
  $('.close').click(function() {
    $('#myModal').fadeOut();
  });
  
  // Menutup modal saat area di luar modal diklik
  $(window).click(function(event) {
    if (event.target == $('#myModal')[0]) {
      $('#myModal').fadeOut();
    }
  });
  