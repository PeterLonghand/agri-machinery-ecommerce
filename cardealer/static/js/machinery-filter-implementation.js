let selectedTypes = [];

function getUrlParams() {
  const params = new URLSearchParams(window.location.search);
  return Object.fromEntries(params.entries());
}

// В функции initEventListeners() или сразу после нее добавьте:
function applyPresetFilters() {
  const params = getUrlParams();

  if (params.preset === "seeding") {
    // Отметить нужные типы техники
    const typesToSelect = ["Tractor", "Seeder", "Harrow", "Plow"];
    typesToSelect.forEach((type) => {
      const checkbox = document.getElementById(`type-${type.toLowerCase()}`);
      if (checkbox && !checkbox.checked) {
        checkbox.checked = true;

        // Показать детальный блок для этого типа техники
        const details = document.getElementById(
          `details-${type.toLowerCase()}`
        );
        if (details) {
          details.style.display = "block";
        }

        // Добавить в массив выбранных типов
        if (!selectedTypes.includes(type)) {
          selectedTypes.push(type);
        }
      }
    });

    // Если нужно исключить определенные тяговые классы тракторов
    if (document.getElementById("tow-class-options")) {
      const excludeClasses = ["0.6", "0.9", "1.4"];
      const towClassCheckboxes =
        document.querySelectorAll('[name="tow_class"]');

      towClassCheckboxes.forEach((checkbox) => {
        if (!excludeClasses.includes(checkbox.value)) {
          checkbox.checked = true;
        }
      });
    }

    // Загрузить технику с примененными фильтрами
    // Загрузку выполним чуть позже, после инициализации всех фильтров
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Глобальные переменные
  const apiUrl = "/catalog/api/machinery-combined/";
  const filterOptionsUrl = "/catalog/api/filter-options/";
  const machineryList = document.getElementById("machinery-list");
  const filterForm = document.getElementById("filter-form");
  const resultCount = document
    .getElementById("result-count")
    .querySelector("span");
  const filterButton = document.getElementById("filter-button");
  const resetButton = document.getElementById("reset-button");
  const sortSelect = document.getElementById("sort-select");
  const paginationContainer = document.getElementById("pagination-container");
  const template = document.getElementById("machinery-card-template");
  let currentPage = 1;
  let totalPages = 0;
  let filterOptions = {};
  //let selectedTypes = [];

  // Инициализация
  initFilterOptions();
  initEventListeners();

  function scrollToCatalogBeginning() {
    const targetElement = document.getElementById("machinery-container-area");
    const elementPosition =
      targetElement.getBoundingClientRect().top + window.pageYOffset;
    const offset = 80;
    const targetPosition = elementPosition - offset;

    // Текущая позиция скролла
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;

    // Адаптируем длительность в зависимости от расстояния
    // Меньшее расстояние - меньшая длительность для более естественного ощущения
    const distanceAbs = Math.abs(distance);
    const baseDuration = 800; // Базовая длительность в мс
    const duration = Math.min(
      baseDuration,
      (baseDuration * distanceAbs) / 1000
    );

    let startTime = null;

    function animation(currentTime) {
      if (startTime === null) startTime = currentTime;
      const timeElapsed = currentTime - startTime;
      const progress = Math.min(timeElapsed / duration, 1);

      // Улучшенная функция плавности
      const easeOutQuint = (t) => 1 + --t * t * t * t * t;

      window.scrollTo(0, startPosition + distance * easeOutQuint(progress));

      if (timeElapsed < duration) {
        requestAnimationFrame(animation);
      }
    }

    requestAnimationFrame(animation);
  }
  // Получение данных для фильтров
  function initFilterOptions() {
    fetch(filterOptionsUrl)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        filterOptions = data;
        populateManufacturers(data.manufacturers);
        initSliders(data);
        updateMachineryCounts(data.machinery_counts);
        populateTractorDetails(data.tractor_options);
        populateHarvesterDetails(data.harvester_options);
        populateSeederDetails(data.seeder_options);
        populateHarrowDetails(data.harrow_options);
        populateBalerDetails(data.baler_options);
        // Проверяем и применяем пресеты перед загрузкой техники
        applyPresetFilters();
        // Загрузка техники после инициализации фильтров
        loadMachinery();
      })
      .catch((error) =>
        console.error("Ошибка при загрузке опций фильтров:", error)
      );
  }

  // Заполнение производителей
  function populateManufacturers(manufacturers) {
    const container = document.getElementById("manufacturers-container");
    manufacturers.forEach((manufacturer) => {
      const div = document.createElement("div");
      div.className = "checkbox checkbox-theme";
      div.innerHTML = `
              <input type="checkbox" id="manufacturer-${manufacturer}" name="manufacturer_in" value="${manufacturer}">
              <label for="manufacturer-${manufacturer}">${manufacturer}</label>
          `;
      container.appendChild(div);
    });
  }

  // Инициализация слайдеров для числовых фильтров
  function initSliders(data) {
    // Год выпуска
    if (data.year_range && data.year_range.min && data.year_range.max) {
      initSlider("year", data.year_range.min, data.year_range.max);
    }

    // Цена
    if (data.price_range && data.price_range.min && data.price_range.max) {
      initSlider("price", 0 /* data.price_range.min */, data.price_range.max);
    }

    // Мощность для тракторов
    if (data.power_range && data.power_range.min && data.power_range.max) {
      initSlider("power", 0 /* data.power_range.min */, data.power_range.max);
      initSlider("harvester-power", data.power_range.min, data.power_range.max);
      initSlider(
        "self-sprayer-power",
        data.power_range.min,
        data.power_range.max
      );
    }

    // Объем двигателя
    if (
      data.engine_volume_range &&
      data.engine_volume_range.min &&
      data.engine_volume_range.max
    ) {
      initSlider(
        "engine-volume",
        data.engine_volume_range.min,
        data.engine_volume_range.max
      );
    }

    // Ширина для сельхозтехники
    if (data.width_range && data.width_range.min && data.width_range.max) {
      initSlider("plow-width", data.width_range.min, data.width_range.max);
      initSlider(
        "self-sprayer-width",
        data.width_range.min,
        data.width_range.max
      );
    }

    // Специфичные слайдеры
    initSlider("bunker-volume", 0, 15);
    initSlider("bodies", 0, 12);
    initSlider("self-sprayer-tank", 0, 6000);
  }

  // Инициализация конкретного слайдера
  function initSlider(id, min, max) {
    const slider = document.getElementById(`${id}-slider`);
    if (!slider) return;

    const minInput = document.getElementById(`${id}-min`);
    const maxInput = document.getElementById(`${id}-max`);

    // Сохраняем начальные значения как атрибуты
    slider.dataset.defaultMin = min;
    slider.dataset.defaultMax = max;

    $(slider).slider({
      range: true,
      min: min,
      max: max,
      values: [min, max],
      slide: function (event, ui) {
        minInput.value = ui.values[0];
        maxInput.value = ui.values[1];
      },
    });

    // Синхронизация ввода с ползунком
    minInput.value = min;
    maxInput.value = max;

    minInput.addEventListener("change", function () {
      const value = parseInt(this.value) || min;
      $(slider).slider("values", 0, value);
    });

    maxInput.addEventListener("change", function () {
      const value = parseInt(this.value) || max;
      $(slider).slider("values", 1, value);
    });
  }
  /* function initSlider(id, min, max) {
    const slider = document.getElementById(`${id}-slider`);
    if (!slider) return;

    const minInput = document.getElementById(`${id}-min`);
    const maxInput = document.getElementById(`${id}-max`);

    $(slider).slider({
      range: true,
      min: min,
      max: max,
      values: [min, max],
      slide: function (event, ui) {
        minInput.value = ui.values[0];
        maxInput.value = ui.values[1];
      },
    });

    // Синхронизация ввода с ползунком
    minInput.value = min;
    maxInput.value = max;

    minInput.addEventListener("change", function () {
      const value = parseInt(this.value) || min;
      $(slider).slider("values", 0, value);
    });

    maxInput.addEventListener("change", function () {
      const value = parseInt(this.value) || max;
      $(slider).slider("values", 1, value);
    });
  }
 */
  // Обновление счетчиков типов техники
  function updateMachineryCounts(counts) {
    for (const [type, count] of Object.entries(counts)) {
      const countElement = document.getElementById(
        `count-${type.toLowerCase()}`
      );
      if (countElement) {
        countElement.textContent = count;
      }
    }
  }

  // Заполнение деталей для тракторов
  function populateTractorDetails(options) {
    // Тип привода
    populateCheckboxOptions(
      "drive-type-options",
      options.drive_types,
      "drive_type",
      "Колёсный, полный",
      "Колёсный, задний",
      "Гусеничный"
    );

    // Тип КПП
    populateCheckboxOptions(
      "transmission-type-options",
      options.transmission_types,
      "transmission_type",
      "Механика",
      "Автомат",
      "Полуавтомат",
      "Вариатор"
    );

    // Тяговый класс
    populateCheckboxOptions(
      "tow-class-options",
      options.tow_classes,
      "tow_class",
      "0.6",
      "0.9",
      "1.4",
      "2",
      "3",
      "4",
      "5",
      "6"
    );
  }

  // Заполнение деталей для комбайнов
  function populateHarvesterDetails(options) {
    // Тип системы обмолота
    populateCheckboxOptions(
      "threshing-type-options",
      options.threshing_types,
      "threshing_type",
      "Барабанная",
      "Роторная",
      "Гибридная"
    );
  }

  // Заполнение деталей для сеялок
  function populateSeederDetails(options) {
    populateCheckboxOptions(
      "seed-type-options",
      options.seed_types,
      "seed_type",
      "Зерновая",
      "Пропашная",
      "Универсальная"
    );
  }

  // Заполнение деталей для борон
  function populateHarrowDetails(options) {
    // Типы борон заполняются из options.harrow_types
    if (document.getElementById("harrow-type-options")) {
      populateCheckboxOptions(
        "harrow-type-options",
        options.harrow_types,
        "harrow_type",
        "Дисковая",
        "Зубовая",
        "Пружинная",
        "Ротационная"
      );
    }
  }

  // Заполнение деталей для пресс-подборщиков
  function populateBalerDetails(options) {
    // Типы и размеры рулонов заполняются из options
    if (document.getElementById("baler-type-options")) {
      populateCheckboxOptions(
        "baler-type-options",
        options.baler_types,
        "baler_type",
        "Рулонный",
        "Тюковый"
      );
    }

    if (document.getElementById("bale-size-options")) {
      populateCheckboxOptions(
        "bale-size-options",
        options.bale_sizes,
        "bale_size",
        "Маленький",
        "Средний",
        "Большой"
      );
    }
  }

  // Общая функция для создания чекбоксов
  function populateCheckboxOptions(containerId, options, name, ...labels) {
    const container = document.getElementById(containerId);
    if (!container) return;

    options.forEach((option, index) => {
      const label = labels[index] || option;
      const div = document.createElement("div");
      div.className = "checkbox checkbox-theme";
      div.innerHTML = `
              <input type="checkbox" id="${name}-${option}" name="${name}" value="${option}">
              <label for="${name}-${option}">${label}</label>
          `;
      container.appendChild(div);
    });
  }

  // Обработчики событий
  function initEventListeners() {
    // Типы техники - показывать/скрывать специфичные фильтры
    document
      .querySelectorAll(".machinery-type-item > .checkbox > input")
      .forEach((checkbox) => {
        checkbox.addEventListener("change", function () {
          const type = this.id.replace("type-", "");
          const details = document.getElementById(`details-${type}`);

          if (details) {
            details.style.display = this.checked ? "block" : "none";
          }

          // Добавляем тип в выбранные
          if (this.checked) {
            selectedTypes.push(this.value);
          } else {
            const index = selectedTypes.indexOf(this.value);
            if (index > -1) {
              selectedTypes.splice(index, 1);
            }
          }
        });
      });

    // Кнопка применения фильтров
    filterButton.addEventListener("click", function () {
      currentPage = 1;
      loadMachinery();
      scrollToCatalogBeginning();
    });

    // кнопка сброса фильтров
    resetButton.addEventListener("click", function () {
      filterForm.reset();

      // сброс слайдеров
      document.querySelectorAll(".slider-range").forEach((slider) => {
        const id = slider.id.replace("-slider", "");
        const minInput = document.getElementById(`${id}-min`);
        const maxInput = document.getElementById(`${id}-max`);

        if (minInput && maxInput) {
          // использ. дефолтные значения, хранящиеся в наборе данных, или  0 для min и 100 для max
          const min = parseInt(slider.dataset.defaultMin) || 0;
          const max = parseInt(slider.dataset.defaultMax) || 100;

          // только если элемент был инициализирован
          try {
            $(slider).slider("values", 0, min);
            $(slider).slider("values", 1, max);
          } catch (e) {
            console.warn(`Slider ${id} not initialized yet`);
          }

          minInput.value = min;
          maxInput.value = max;
        }
      });

      // Закрытие всех разделов типов техники
      document.querySelectorAll(".machinery-details").forEach((details) => {
        details.style.display = "none";
      });

      selectedTypes = [];
      currentPage = 1;
      loadMachinery();
      scrollToCatalogBeginning();
    });

    // сортировка
    sortSelect.addEventListener("change", function () {
      loadMachinery();
    });
  }

  // Получение данных о технике
  function loadMachinery() {
    console.log(selectedTypes);
    const params = new URLSearchParams(getFilterParams());

    // Добавляем сортировку
    if (sortSelect.value) {
      params.append("ordering", sortSelect.value);
    }

    // Добавляем страницу
    params.append("page", currentPage);

    // Запрос к API
    fetch(`${apiUrl}?${params.toString()}`)
      .then((response) => response.json())
      .then((data) => {
        displayMachinery(data.results);
        resultCount.textContent = data.count;
        createPagination(data);
      })
      .catch((error) => console.error("Ошибка при загрузке техники:", error));
  }

  // Получение параметров фильтров
  // В функции getFilterParams() добавить преобразование имен параметров
  function getFilterParams() {
    const formData = new FormData(filterForm);
    const params = {};

    // Собираем все чекбоксы с одинаковыми именами
    const checkboxGroups = {};

    // Отслеживаем, какие слайдеры были изменены
    const slidersChanged = {};

    // Собираем значения всех полей формы
    const formValues = {};

    for (const [key, value] of formData.entries()) {
      if (value === "") continue;
      formValues[key] = value;

      // Проверяем, является ли это чекбоксом
      const input = filterForm.querySelector(`[name="${key}"]`);
      if (input && input.type === "checkbox") {
        if (!checkboxGroups[key]) {
          checkboxGroups[key] = [];
        }
        checkboxGroups[key].push(value);
      }
    }

    // Обработка слайдеров для каждого типа техники
    if (selectedTypes.includes("Plow")) {
      processSlider(params, "plow-width", "plow_width");
    }
    if (selectedTypes.includes("SelfPropelledSprayer")) {
      processSlider(params, "self-sprayer-width", "self_sprayer_width");
      processSlider(params, "self-sprayer-tank", "self_sprayer_tank");
      processSlider(params, "self-sprayer-power", "self_sprayer_power");
    }
    if (selectedTypes.includes("Tractor")) {
      processSlider(params, "power", "power");
      processSlider(params, "engine-volume", "engine_volume");
    }
    if (selectedTypes.includes("Harvester")) {
      processSlider(params, "harvester-power", "harvester_power");
      processSlider(params, "bunker-volume", "bunker_volume");
    }

    // Общие слайдеры
    processSlider(params, "year", "year");
    processSlider(params, "price", "price");
    processSlider(params, "bodies", "bodies");

    // Добавляем собранные группы чекбоксов
    for (const [key, values] of Object.entries(checkboxGroups)) {
      params[key] = values.join(",");
    }

    // Добавляем выбранные типы техники
    if (selectedTypes.length > 0) {
      params["machinery_type"] = selectedTypes.join(",");
    }

    return params;

    // Вспомогательная функция для обработки слайдеров
    function processSlider(params, htmlId, apiParam) {
      const minInput = document.getElementById(`${htmlId}-min`);
      const maxInput = document.getElementById(`${htmlId}-max`);
      const slider = document.getElementById(`${htmlId}-slider`);

      if (!minInput || !maxInput || !slider) return;

      const defaultMin =
        parseInt(slider.dataset.defaultMin) ||
        $(slider).slider("option", "min");
      const defaultMax =
        parseInt(slider.dataset.defaultMax) ||
        $(slider).slider("option", "max");
      const currentMin = parseInt(minInput.value);
      const currentMax = parseInt(maxInput.value);

      // Добавляем параметры только если значения изменились от дефолтных
      if (currentMin !== defaultMin) {
        params[`${apiParam}_min`] = currentMin;
      }
      if (currentMax !== defaultMax) {
        params[`${apiParam}_max`] = currentMax;
      }
    }
  }
  /* function getFilterParams() {
    const formData = new FormData(filterForm);
    const params = {};

    // Собираем все чекбоксы с одинаковыми именами
    const checkboxGroups = {};

    // Отслеживаем, какие слайдеры были изменены
    const slidersChanged = {};

    for (const [key, value] of formData.entries()) {
      if (value === "") continue;

      // Проверяем, является ли это чекбоксом
      const input = filterForm.querySelector(`[name="${key}"]`);
      if (input && input.type === "checkbox") {
        if (!checkboxGroups[key]) {
          checkboxGroups[key] = [];
        }
        checkboxGroups[key].push(value);
      } else if (key.endsWith("_min") || key.endsWith("_max")) {
        // Извлекаем базовое имя слайдера
        const baseName = key.replace(/_min$|_max$/, "");

        // Проверяем, было ли значение слайдера изменено
        const slider = document.getElementById(`${baseName}-slider`);
        if (slider) {
          const defaultMin = $(slider).slider("option", "min");
          const defaultMax = $(slider).slider("option", "max");
          const currentMin = parseInt(
            document.getElementById(`${baseName}-min`).value
          );
          const currentMax = parseInt(
            document.getElementById(`${baseName}-max`).value
          );

          // Если значение изменилось с дефолтного, отмечаем слайдер как измененный
          if (currentMin !== defaultMin || currentMax !== defaultMax) {
            slidersChanged[baseName] = true;
          }
        }

        // Добавляем значение только если слайдер был изменен
        if (slidersChanged[baseName]) {
          params[key] = value;
        }
      } else {
        params[key] = value;
      }
    }

    // Добавляем собранные группы чекбоксов
    for (const [key, values] of Object.entries(checkboxGroups)) {
      params[key] = values.join(",");
    }

    // Добавляем выбранные типы техники
    if (selectedTypes.length > 0) {
      params["machinery_type"] = selectedTypes.join(",");
    }

    return params;
  } */
  /*   function getFilterParams() {
    const formData = new FormData(filterForm);
    const params = {};

    // Собираем все чекбоксы с одинаковыми именами
    const checkboxGroups = {};

    for (const [key, value] of formData.entries()) {
      if (value === "") continue;

      // Проверяем, является ли это чекбоксом
      const input = filterForm.querySelector(`[name="${key}"]`);
      if (input && input.type === "checkbox") {
        if (!checkboxGroups[key]) {
          checkboxGroups[key] = [];
        }
        checkboxGroups[key].push(value);
      } else {
        params[key] = value;
      }
    }

    // Добавляем собранные группы чекбоксов
    for (const [key, values] of Object.entries(checkboxGroups)) {
      params[key] = values.join(",");
    }

    // Добавляем выбранные типы техники
    if (selectedTypes.length > 0) {
      params["machinery_type"] = selectedTypes;
    }

    return params;
  } */

  // Отображение техники
  function displayMachinery(machinery) {
    machineryList.innerHTML = "";

    machinery.forEach((item) => {
      const clone = template.content.cloneNode(true);

      // Заполняем шаблон данными
      const links = clone.querySelectorAll(".machinery-link");
      links.forEach((link) => {
        link.href = `/catalog/${item.id}`;
      });

      const title = clone.querySelector(".machinery-title");
      title.innerHTML = `${item.machinery_type_display} <strong> ${item.manufacturer} ${item.model_name} </strong>`;
      const location = clone.querySelector(".location a");
      location.textContent = `${item.year} г.в.`;

      const priceBox = clone.querySelector(".price-box .price-text");
      priceBox.textContent = `${new Intl.NumberFormat("ru-RU").format(
        item.price
      )} ₽`;

      const conditionTag = clone.querySelector(".condition-tag");
      conditionTag.textContent = item.condition_display;
      conditionTag.className = `tag-2 condition-tag ${
        item.condition === "new" ? "bg-success" : "bg-warning"
      }`;

      const image = clone.querySelector(".w-100");
      const mainPhotoLink = clone.querySelector(".overlap-btn");
      const mainPhotoImg = clone.querySelector(".hidden");

      if (item.photo) {
        image.src = item.photo;
        mainPhotoImg.src = item.photo;
        mainPhotoLink.href = item.photo;

        // Добавление дополнительных фотографий, если они есть
        const galleryContainer = clone.querySelector(".car-magnify-gallery");

        if (item.photo_1) {
          const additionalLink = document.createElement("a");
          additionalLink.href = item.photo_1;
          additionalLink.className = "hidden";

          const additionalImg = document.createElement("img");
          additionalImg.src = item.photo_1;
          additionalImg.className = "hidden";

          additionalLink.appendChild(additionalImg);
          galleryContainer.appendChild(additionalLink);
        }

        if (item.photo_2) {
          const additionalLink = document.createElement("a");
          additionalLink.href = item.photo_2;
          additionalLink.className = "hidden";

          const additionalImg = document.createElement("img");
          additionalImg.src = item.photo_2;
          additionalImg.className = "hidden";

          additionalLink.appendChild(additionalImg);
          galleryContainer.appendChild(additionalLink);
        }

        if (item.photo_3) {
          const additionalLink = document.createElement("a");
          additionalLink.href = item.photo_3;
          additionalLink.className = "hidden";

          const additionalImg = document.createElement("img");
          additionalImg.src = item.photo_3;
          additionalImg.className = "hidden";

          additionalLink.appendChild(additionalImg);
          galleryContainer.appendChild(additionalLink);
        }
        if (item.photo_4) {
          const additionalLink = document.createElement("a");
          additionalLink.href = item.photo_4;
          additionalLink.className = "hidden";

          const additionalImg = document.createElement("img");
          additionalImg.src = item.photo_4;
          additionalImg.className = "hidden";

          additionalLink.appendChild(additionalImg);
          galleryContainer.appendChild(additionalLink);
        }
      } else {
        image.src = "/static/img/no-image.jpg";
        mainPhotoImg.src = "/static/img/no-image.jpg";
        mainPhotoLink.href = "/static/img/no-image.jpg";
      }

      // Добавляем спецификации техники
      const specsList = clone.querySelector(".machinery-specs");

      // Общие спецификации
      //addSpec(specsList, "Состояние", item.condition_display);

      // Специфичные спецификации в зависимости от типа техники
      if (item.machinery_type === "Tractor") {
        addSpec(specsList, "Мощность", `${item.power} л.с.`);
        addSpec(specsList, "Привод", item.drive_type_display);
        addSpec(specsList, "КПП", item.transmission_type_display);
      } else if (item.machinery_type === "Harvester") {
        addSpec(specsList, "Мощность", `${item.power} л.с.`);
        addSpec(specsList, "Объем бункера", `${item.bunker_volume} м³`);
        addSpec(specsList, "Тип обмолота", item.threshing_type_display);
      } else if (item.machinery_type === "SelfPropelledSprayer") {
        addSpec(specsList, "Мощность", `${item.power} л.с.`);
        addSpec(specsList, "Ширина", `${item.width} м`);
        addSpec(specsList, "Объем бака", `${item.tank_capacity} л`);
      } else if (item.machinery_type === "Plow") {
        addSpec(specsList, "Ширина", `${item.width} м`);
        addSpec(specsList, "Корпусов", item.bodies);
        addSpec(specsList, "Оборотный", item.reversible ? "Да" : "Нет");
      } else if (item.machinery_type === "Seeder") {
        addSpec(specsList, "Тип", item.seed_type_display);
        addSpec(specsList, "Ширина", `${item.width} м`);
        addSpec(specsList, "Объем бункера", `${item.seed_tank_capacity} л`);
      } else if (item.machinery_type === "Harrow") {
        addSpec(specsList, "Ширина", `${item.width} м`);
        addSpec(specsList, "Тип", item.harrow_type_display);
      } else if (item.machinery_type === "TrailedSprayer") {
        addSpec(specsList, "Ширина", `${item.width} м`);
        addSpec(specsList, "Объем бака", `${item.tank_capacity} л`);
      } else if (item.machinery_type === "Mower") {
        addSpec(specsList, "Ширина", `${item.width} м`);
      } else if (item.machinery_type === "Baler") {
        addSpec(specsList, "Тип", item.baler_type_display);
        addSpec(specsList, "Размер тюка", item.bale_size_display);
      }

      machineryList.appendChild(clone);
    });
    $(".car-magnify-gallery").lightGallery({
      selector: "a", // Изменить на этот селектор, чтобы включить все ссылки
      thumbnail: true,
      share: false,
      fullScreen: true,
      autoplay: false,
      autoplayControls: true,
      actualSize: false,
    });
  }

  // Добавление спецификаций в список
  function addSpec(list, label, value) {
    if (!value && value !== 0) return;

    const li = document.createElement("li");
    li.innerHTML = `<span>${label}:</span> ${value}`;
    list.appendChild(li);
  }

  // Создание пагинации
  function createPagination(data) {
    totalPages = Math.ceil(data.count / 8); // 10 - количество элементов на странице
    paginationContainer.innerHTML = "";

    if (totalPages <= 1) return;

    // Добавление "Предыдущая"
    if (currentPage > 1) {
      addPaginationItem("&laquo;", currentPage - 1);
    }

    // Номера страниц
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
      addPaginationItem(i, i, i === currentPage);
    }

    // Добавление "Следующая"
    if (currentPage < totalPages) {
      addPaginationItem("&raquo;", currentPage + 1);
    }
  }

  // Добавление элемента пагинации
  function addPaginationItem(text, page, isActive = false) {
    const li = document.createElement("li");
    li.className = `page-item${isActive ? " active" : ""}`;

    const a = document.createElement("a");
    a.className = "page-link";
    a.href = "#";
    a.innerHTML = text;

    a.addEventListener("click", function (e) {
      e.preventDefault();
      currentPage = page;
      loadMachinery();
      scrollToCatalogBeginning();
    });

    li.appendChild(a);
    paginationContainer.appendChild(li);
  }
});
