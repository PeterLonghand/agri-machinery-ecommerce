$(document).ready(function () {
  console.log("Document ready, checking modal...");
  $("#inquiryModal").on("shown.bs.modal", function () {
    console.log("Modal shown, initializing sliders...");

    if ($("#customerNeedSelect").val() === "Лизинг") {
      $("#purchaseInfo").hide();
      $("#leasingCalculator").show();
      console.log("Leasing selected, initializing calculator...");
      initializeCalculator();
    }
  });

  $("#customerNeedSelect").change(function () {
    var selectedOption = $(this).val();

    if (selectedOption === "Лизинг") {
      $("#purchaseInfo").hide();
      $("#leasingCalculator").show();

      initializeCalculator();
    } else {
      $("#purchaseInfo").show();
      $("#leasingCalculator").hide();
    }
  });

  //обработчик переключения типа графика платежей
  $("input[name='paymentScheduleType']").change(function () {
    var paymentType = $(this).val();
    $("#leasingPaymentTypeInput").val(paymentType);

    if (paymentType === "equal") {
      $("#equalPaymentsResults").show();
      $("#decreasingPaymentsResults").hide();
    } else {
      $("#equalPaymentsResults").hide();
      $("#decreasingPaymentsResults").show();
    }

    calculatePayments();
  });

  //Инициализация при открытии модального окна
  $("#inquiryModal").on("shown.bs.modal", function () {
    if ($("#customerNeedSelect").val() === "Лизинг") {
      $("#purchaseInfo").hide();
      $("#leasingCalculator").show();
      initializeCalculator();
    }
  });

  function initializeCalculator() {
    var machinePrice = parseFloat($("#machinePrice").val()) || 0;

    if ($("#advancePaymentSlider").slider("instance")) {
      // если слайдер уже инициализирован, обновляем его значения
      $("#advancePaymentSlider").slider("option", "value", 20);
    } else {
      // иначе инициализируем новый слайдер
      $("#advancePaymentSlider").slider({
        range: "min",
        min: 5,
        max: 49,
        value: 20,
        slide: function (event, ui) {
          $("#advancePercent").text(ui.value);
          var advanceAmount = Math.round((machinePrice * ui.value) / 100);
          $("#advanceAmount").text(formatNumber(advanceAmount));
          $("#equalAdvanceAmount").text(formatNumber(advanceAmount));
          $("#decreasingAdvanceAmount").text(formatNumber(advanceAmount));
          $("#leasingAdvanceInput").val(ui.value);
          calculatePayments();
        },
      });
    }

    if ($("#leasingTermSlider").slider("instance")) {
      $("#leasingTermSlider").slider("option", "value", 36);
    } else {
      $("#leasingTermSlider").slider({
        range: "min",
        min: 12,
        max: 60,
        value: 36,
        slide: function (event, ui) {
          $("#leasingTerm").text(ui.value);
          $("#leasingTermInput").val(ui.value);
          calculatePayments();
        },
      });
    }

    // установка начальных значений
    var advancePercent = $("#advancePaymentSlider").slider("value");
    var advanceAmount = Math.round((machinePrice * advancePercent) / 100);
    $("#advancePercent").text(advancePercent);
    $("#advanceAmount").text(formatNumber(advanceAmount));
    $("#equalAdvanceAmount").text(formatNumber(advanceAmount));
    $("#decreasingAdvanceAmount").text(formatNumber(advanceAmount));
    $("#leasingTerm").text($("#leasingTermSlider").slider("value"));

    // установка значений в скрытые поля формы
    $("#leasingAdvanceInput").val(advancePercent);
    $("#leasingTermInput").val($("#leasingTermSlider").slider("value"));
    $("#leasingPaymentTypeInput").val(
      $("input[name='paymentScheduleType']:checked").val()
    );

    calculatePayments();
  }

  // ф-я расчета платежей
  function calculatePayments() {
    var machinePrice = parseFloat($("#machinePrice").val()) || 0;
    var advancePercent = $("#advancePaymentSlider").slider("value");
    var leasingTerm = $("#leasingTermSlider").slider("value");
    var paymentType = $("input[name='paymentScheduleType']:checked").val();

    var advanceAmount = Math.round((machinePrice * advancePercent) / 100);
    var remainingAmount = machinePrice - advanceAmount;

    // Базовые ставки удорожания (для 12 месяцев и минимального аванса 5%)
    var baseEqualRate = 9;
    var baseDecreasingRate = 8;

    // Коэффициенты влияния
    var yearlyIncrease = 1.0; // Увеличение ставки за каждый год срока
    var advanceDiscount = 0.1; // Снижение ставки за каждый 1% аванса сверх минимального

    // Минимальные значения параметров, от которых считаем отклонение
    var minAdvancePercent = 5; // Минимальный аванс
    var minTermMonths = 12; // Минимальный срок

    // рассчетскорректированных ставок удорожания
    var termAdjustment = (leasingTerm / 12 - 1) * yearlyIncrease;
    var advanceAdjustment =
      (advancePercent - minAdvancePercent) * advanceDiscount;
    var equalAppreciationRate = Math.max(
      3,
      baseEqualRate + termAdjustment - advanceAdjustment
    );
    var decreasingAppreciationRate = Math.max(
      2.5,
      baseDecreasingRate + termAdjustment - advanceAdjustment
    );

    // округляем ставки до одного 10го знака
    equalAppreciationRate = Math.round(equalAppreciationRate * 10) / 10;
    decreasingAppreciationRate =
      Math.round(decreasingAppreciationRate * 10) / 10;

    // для равномерного графика
    var equalTotalAmount =
      remainingAmount * (1 + equalAppreciationRate / 100) + advanceAmount;
    var equalMonthlyPayment = Math.round(
      (equalTotalAmount - advanceAmount) / leasingTerm
    );

    // расчет для убывающего графика
    var decreasingTotalAmount =
      remainingAmount * (1 + decreasingAppreciationRate / 100) + advanceAmount;
    var decreasingMaxPayment = Math.round(
      (2 * (decreasingTotalAmount - advanceAmount)) /
        (leasingTerm * (1 + 1 / leasingTerm))
    );
    var decreasingMinPayment = Math.round(decreasingMaxPayment / 2);

    $("#equalAppreciation").text(equalAppreciationRate.toFixed(1));
    $("#equalMonthlyPayment").text(formatNumber(equalMonthlyPayment));
    $("#equalTotalAmount").text(formatNumber(Math.round(equalTotalAmount)));

    $("#decreasingAppreciation").text(decreasingAppreciationRate.toFixed(1));
    $("#decreasingMonthlyPaymentMin").text(formatNumber(decreasingMinPayment));
    $("#decreasingMonthlyPaymentMax").text(formatNumber(decreasingMaxPayment));
    $("#decreasingTotalAmount").text(
      formatNumber(Math.round(decreasingTotalAmount))
    );

    // ----- УЛУЧШЕННЫЙ РАСЧЕТ НАЛОГОВЫХ ВЫГОД -----

    // Константы для налоговых расчетов
    var VAT_RATE = 0.2; // ставка НДС 20%
    var PROFIT_TAX_RATE = 0.2; // ставка налога на прибыль 20%

    // 1. Расчет возврата НДС
    // НДС возвращается со всей суммы договора лизинга (включая аванс)
    // НДС = Сумма договора * 20/120 = Сумма договора * 1/6
    var equalVatReturn = Math.round(
      (equalTotalAmount * VAT_RATE) / (1 + VAT_RATE)
    );
    var decreasingVatReturn = Math.round(
      (decreasingTotalAmount * VAT_RATE) / (1 + VAT_RATE)
    );

    // 2. Расчет экономии налога на прибыль
    // Экономия = (Общая сумма лизинговых платежей) * Ставка налога на прибыль
    var equalProfitTaxSaving = Math.round(equalTotalAmount * PROFIT_TAX_RATE);
    var decreasingProfitTaxSaving = Math.round(
      decreasingTotalAmount * PROFIT_TAX_RATE
    );

    // 3. Расчет совокупной налоговой выгоды
    var equalTotalTaxBenefit = equalVatReturn + equalProfitTaxSaving;
    var decreasingTotalTaxBenefit =
      decreasingVatReturn + decreasingProfitTaxSaving;

    // 4. Расчет реальной стоимости лизинга с учетом налоговых выгод
    var equalNetCost = equalTotalAmount - equalTotalTaxBenefit;
    var decreasingNetCost = decreasingTotalAmount - decreasingTotalTaxBenefit;

    // Обновление текстовых полей для налоговых выгод (равномерный график)
    $("#equalVatReturn").text(formatNumber(equalVatReturn));
    $("#equalProfitTaxSaving").text(formatNumber(equalProfitTaxSaving));

    if ($("#equalTotalTaxBenefit").length) {
      $("#equalTotalTaxBenefit").text(formatNumber(equalTotalTaxBenefit));
    }
    if ($("#equalNetCost").length) {
      $("#equalNetCost").text(formatNumber(Math.round(equalNetCost)));
    }

    // налоговые выгоды (убывающий график)
    $("#decreasingVatReturn").text(formatNumber(decreasingVatReturn));
    $("#decreasingProfitTaxSaving").text(
      formatNumber(decreasingProfitTaxSaving)
    );

    if ($("#decreasingTotalTaxBenefit").length) {
      $("#decreasingTotalTaxBenefit").text(
        formatNumber(decreasingTotalTaxBenefit)
      );
    }
    if ($("#decreasingNetCost").length) {
      $("#decreasingNetCost").text(formatNumber(Math.round(decreasingNetCost)));
    }

    if (paymentType === "equal") {
      $("#leasingMonthlyPaymentInput").val(equalMonthlyPayment);
      $("#leasingFullPaymentInput").val(Math.round(equalTotalAmount));
    } else {
      $("#leasingMonthlyPaymentInput").val(
        decreasingMaxPayment + "-" + decreasingMinPayment
      );
      $("#leasingFullPaymentInput").val(Math.round(decreasingTotalAmount));
    }
  }

  // Форматирование чисел с разделителями тысяч
  function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  }
});
