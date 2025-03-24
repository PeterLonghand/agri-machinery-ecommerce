$(document).ready(function () {
  // Находим карусель по ID
  var carousel = $("#carouselExampleIndicators");

  // Инициализируем карусель с нужными параметрами
  carousel.carousel({
    interval: 5000, // время автопереключения в миллисекундах
    pause: false, // не останавливать при наведении мыши
    wrap: true, // зацикливание слайдов
  });

  // Настраиваем обработчики для кнопок навигации
  $(".carousel-control-prev").click(function (e) {
    e.preventDefault();
    carousel.carousel("prev");
  });

  $(".carousel-control-next").click(function (e) {
    e.preventDefault();
    carousel.carousel("next");
  });

  // Функция для анимации элементов при смене слайда (если нужно)
  function doAnimations(elements) {
    var animEndEv = "webkitAnimationEnd animationend";
    elements.each(function () {
      var $this = $(this);
      var $animationType = $this.data("animation");
      $this.addClass($animationType).one(animEndEv, function () {
        $this.removeClass($animationType);
      });
    });
  }

  // Анимируем элементы первого слайда при загрузке
  var firstSlideElements = carousel
    .find(".carousel-item:first")
    .find("[data-animation]");
  doAnimations(firstSlideElements);

  // Анимируем элементы при смене слайда
  carousel.on("slide.bs.carousel", function (e) {
    var nextSlideElements = $(e.relatedTarget).find("[data-animation]");
    doAnimations(nextSlideElements);
  });
});
