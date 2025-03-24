document.addEventListener("DOMContentLoaded", function () {
  // Функция для форматирования числа с пробелами
  function formatNumberWithSpaces(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  }

  // Оригинальный метод создания слайдера
  var rangeSlider = function () {
    var slider = $(".range-slider-ui");
    slider.each(function () {
      var $this = $(this);
      var min = $this.data("min");
      var max = $this.data("max");
      var unit = $this.data("unit");
      var minName = $this.data("min-name");
      var maxName = $this.data("max-name");
      var disableOnReady = $this.data("disable-on-ready");

      $this.slider({
        range: true,
        min: min,
        max: max,
        values: [min, max],
        slide: function (event, ui) {
          // Форматируем числа с пробелами только для отображения
          $this
            .parent()
            .find(".min")
            .text(formatNumberWithSpaces(ui.values[0]) + " " + unit);
          $this
            .parent()
            .find(".max")
            .text(formatNumberWithSpaces(ui.values[1]) + " " + unit);
          $('input[name="' + minName + '"]').val(ui.values[0]);
          $('input[name="' + maxName + '"]').val(ui.values[1]);
        },
        create: function (event, ui) {
          // Добавляем элементы отображения мин/макс значений, если их еще нет
          if (!$this.parent().find(".min").length) {
            $this
              .parent()
              .append(
                '<span class="min">' +
                  formatNumberWithSpaces(min) +
                  " " +
                  unit +
                  "</span>"
              );
          } else {
            $this
              .parent()
              .find(".min")
              .text(formatNumberWithSpaces(min) + " " + unit);
          }

          if (!$this.parent().find(".max").length) {
            $this
              .parent()
              .append(
                '<span class="max">' +
                  formatNumberWithSpaces(max) +
                  " " +
                  unit +
                  "</span>"
              );
          } else {
            $this
              .parent()
              .find(".max")
              .text(formatNumberWithSpaces(max) + " " + unit);
          }

          // Добавляем скрытые поля для формы, если их еще нет
          if ($('input[name="' + minName + '"]').length === 0) {
            $("<input>")
              .attr({
                name: minName,
                type: "hidden",
                value: min,
              })
              .appendTo($this.parent());
          }

          if ($('input[name="' + maxName + '"]').length === 0) {
            $("<input>")
              .attr({
                name: maxName,
                type: "hidden",
                value: max,
              })
              .appendTo($this.parent());
          }
        },
      });

      if (disableOnReady) {
        $this.slider("disable");
      }
    });
  };

  // Запускаем функцию инициализации слайдера
  rangeSlider();
});
