jQuery(document).ready(function() {
  $('#carouselHacked').carousel();
  //this code is for animation nav
  // jQuery(window).scroll(function() {
  //   var windowScrollPosTop = jQuery(window).scrollTop();

  //   if(windowScrollPosTop >= 150) {
  //     jQuery(".header").css({"background": "#B193DD",});
  //     jQuery(".top-header img.logo").css({"margin-top": "-40px", "margin-bottom": "0"});
  //     jQuery(".navbar-default").css({"margin-top": "-15px",});
  //   }
  //   else{
  //     jQuery(".header").css({"background": "transparent",});
  //     jQuery(".top-header img.logo").css({"margin-top": "-12px", "margin-bottom": "25px"});
  //     jQuery(".navbar-default").css({"margin-top": "12px", "margin-bottom": "0"});
  //   }
  // });
});
// Javascript to enable link to tab
function changeToTab() {
  var url = document.location.toString();
  if (url.match('#')) {
    $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
    $('.nav-pills a[href="#' + url.split('#')[1] + '"]').tab('show');
  }
}
changeToTab();
$('.site-map-links').on('click', changeToTab);

// Change hash for page-reload
$('.nav-tabs a,.nav-pills a').on('shown.bs.tab', function (e) {
   window.location.hash = e.target.hash;
});
