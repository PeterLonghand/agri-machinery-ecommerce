document.addEventListener("DOMContentLoaded", function () {
  setupFilterUI();
  // Now we can extract data directly from data attributes rather than parsing text content
  const machineryData = extractMachineryData();

  document
    .getElementById("filter-button")
    .addEventListener("click", function () {
      applyFilters(machineryData);
    });
});

function setupFilterUI() {
  const sidebarContent = `<div class="widget advanced-search2">
    <h3 class="sidebar-title">Filter Machinery</h3>
    <div class="filter-section">
      <h4>Производитель</h4>
      <div class="checkbox-group" id="manufacturer-filters"></div>
    </div>
    <div class="filter-section">
      <h4>Condition</h4>
      <div class="checkbox-group">
        <div class="form-check">
          <input type="checkbox" id="condition-new" class="form-check-input" value="new">
          <label for="condition-new" class="form-check-label">Новый</label>
        </div>
        <div class="form-check">
          <input type="checkbox" id="condition-used" class="form-check-input" value="used">
          <label for="condition-used" class="form-check-label">Б/у</label>
        </div>
      </div>
    </div>
    <div class="filter-section">
      <h4>Year</h4>
      <div class="range-inputs">
        <div class="range-slider-container">
          <div class="range-values">
            <input type="number" id="min-year" min="1960" max="2025" placeholder="From">
            <span>-</span>
            <input type="number" id="max-year" min="1960" max="2025" placeholder="To">
          </div>
          <div id="year-slider" class="range-slider"></div>
        </div>
      </div>
    </div>
    <div class="filter-section">
      <h4>Price (₽)</h4>
      <div class="range-inputs">
        <div class="range-slider-container">
          <div class="range-values">
            <input type="number" id="min-price" min="0" placeholder="From">
            <span>-</span>
            <input type="number" id="max-price" min="0" placeholder="To">
          </div>
          <div id="price-slider" class="range-slider"></div>
        </div>
      </div>
    </div>
    <div class="filter-section">
      <h4>Machinery Type</h4>
      <div class="machinery-type-filters">
        <div class="type-section">
          <div class="form-check type-header">
            <input type="checkbox" id="type-tractor" class="form-check-input type-toggle" value="Tractor">
            <label for="type-tractor" class="form-check-label">Трактор</label>
          </div>
          <div class="type-details" id="tractor-details">
            <div class="sub-filter">
              <h5>Тип</h5>
              <div class="checkbox-group">
                <div class="form-check">
                  <input type="checkbox" id="drive-wheeled" class="form-check-input" value="wheeled">
                  <label for="drive-wheeled" class="form-check-label">Колёсный</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="drive-tracked" class="form-check-input" value="tracked">
                  <label for="drive-tracked" class="form-check-label">Гусеничный</label>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Мощность (л.с.)</h5>
              <div class="range-inputs">
                <div class="range-slider-container">
                  <div class="range-values">
                    <input type="number" id="min-power" min="0" placeholder="From">
                    <span>-</span>
                    <input type="number" id="max-power" min="0" placeholder="To">
                  </div>
                  <div id="power-slider" class="range-slider"></div>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Объём двигателя (л)</h5>
              <div class="range-inputs">
                <div class="range-slider-container">
                  <div class="range-values">
                    <input type="number" id="min-engine" min="0" step="0.1" placeholder="From">
                    <span>-</span>
                    <input type="number" id="max-engine" min="0" step="0.1" placeholder="To">
                  </div>
                  <div id="engine-slider" class="range-slider"></div>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Тип КПП</h5>
              <div class="checkbox-group">
                <div class="form-check">
                  <input type="checkbox" id="transmission-manual" class="form-check-input" value="manual">
                  <label for="transmission-manual" class="form-check-label">Механическая</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="transmission-auto" class="form-check-input" value="auto">
                  <label for="transmission-auto" class="form-check-label">Автоматическая</label>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Тяговый класс</h5>
              <div class="checkbox-group">
                <div class="form-check">
                  <input type="checkbox" id="tow-class-0.2" class="form-check-input" value="0.2">
                  <label for="tow-class-0.2" class="form-check-label">Класс 0.2</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="tow-class-0.6" class="form-check-input" value="0.6">
                  <label for="tow-class-0.6" class="form-check-label">Класс 0.6</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="tow-class-1.4" class="form-check-input" value="1.4">
                  <label for="tow-class-1.4" class="form-check-label">Класс 1.4</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="tow-class-2" class="form-check-input" value="2">
                  <label for="tow-class-2" class="form-check-label">Класс 2</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="tow-class-3" class="form-check-input" value="3">
                  <label for="tow-class-3" class="form-check-label">Класс 3</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="tow-class-4" class="form-check-input" value="4">
                  <label for="tow-class-4" class="form-check-label">Класс 4</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="tow-class-5" class="form-check-input" value="5">
                  <label for="tow-class-5" class="form-check-label">Класс 5</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="tow-class-6" class="form-check-input" value="6">
                  <label for="tow-class-6" class="form-check-label">Класс 6</label>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="type-section">
          <div class="form-check type-header">
            <input type="checkbox" id="type-harvester" class="form-check-input type-toggle" value="Harvester">
            <label for="type-harvester" class="form-check-label">Комбайн</label>
          </div>
          <div class="type-details" id="harvester-details">
            <div class="sub-filter">
              <h5>Мощность (л.с.)</h5>
              <div class="range-inputs">
                <div class="range-slider-container">
                  <div class="range-values">
                    <input type="number" id="harvester-min-power" min="0" placeholder="From">
                    <span>-</span>
                    <input type="number" id="harvester-max-power" min="0" placeholder="To">
                  </div>
                  <div id="harvester-power-slider" class="range-slider"></div>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Объём бункера (л)</h5>
              <div class="range-inputs">
                <div class="range-slider-container">
                  <div class="range-values">
                    <input type="number" id="min-bunker" min="0" placeholder="From">
                    <span>-</span>
                    <input type="number" id="max-bunker" min="0" placeholder="To">
                  </div>
                  <div id="bunker-slider" class="range-slider"></div>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Тип молотильного аппарата</h5>
              <div class="checkbox-group">
                <div class="form-check">
                  <input type="checkbox" id="threshing-drum" class="form-check-input" value="drum">
                  <label for="threshing-drum" class="form-check-label">Барабан</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="threshing-rotor" class="form-check-input" value="rotor">
                  <label for="threshing-rotor" class="form-check-label">Ротор</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="threshing-hybrid" class="form-check-input" value="hybrid">
                  <label for="threshing-hybrid" class="form-check-label">Гибрид</label>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="type-section">
          <div class="form-check type-header">
            <input type="checkbox" id="type-sprayer" class="form-check-input type-toggle" value="SelfPropelledSprayer">
            <label for="type-sprayer" class="form-check-label">Опрыскиватель самоходный</label>
          </div>
          <div class="type-details" id="sprayer-details">
            <div class="sub-filter">
              <h5>Объём бака (л)</h5>
              <div class="range-inputs">
                <div class="range-slider-container">
                  <div class="range-values">
                    <input type="number" id="min-tank" min="0" placeholder="From">
                    <span>-</span>
                    <input type="number" id="max-tank" min="0" placeholder="To">
                  </div>
                  <div id="tank-slider" class="range-slider"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="type-section">
          <div class="form-check type-header">
            <input type="checkbox" id="type-plow" class="form-check-input type-toggle" value="Plow">
            <label for="type-plow" class="form-check-label">Плуг</label>
          </div>
          <div class="type-details" id="plow-details">
            <div class="sub-filter">
              <h5>Количество корпусов</h5>
              <div class="range-inputs">
                <div class="range-slider-container">
                  <div class="range-values">
                    <input type="number" id="min-bodies" min="0" placeholder="From">
                    <span>-</span>
                    <input type="number" id="max-bodies" min="0" placeholder="To">
                  </div>
                  <div id="bodies-slider" class="range-slider"></div>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Тип</h5>
              <div class="checkbox-group">
                <div class="form-check">
                  <input type="checkbox" id="plow-reversible" class="form-check-input" value="yes">
                  <label for="plow-reversible" class="form-check-label">Оборотный</label>
                </div>
                <div class="form-check">
                  <input type="checkbox" id="plow-non-reversible" class="form-check-input" value="no">
                  <label for="plow-non-reversible" class="form-check-label">Необоротный</label>
                </div>
              </div>
            </div>
            <div class="sub-filter">
              <h5>Мин. мощность трактора (л.с.)</h5>
              <div class="range-inputs">
                <div class="range-slider-container">
                  <div class="range-values">
                    <input type="number" id="min-min-power" min="0" placeholder="From">
                    <span>-</span>
                    <input type="number" id="max-min-power" min="0" placeholder="To">
                  </div>
                  <div id="min-power-slider" class="range-slider"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="form-group mt-4">
      <button id="filter-button" class="btn btn-block button-theme btn-md">
        <i class="fa fa-filter"></i> Filter
      </button>
    </div>
  </div>`;

  const sidebar = document.querySelector(".sidebar-right");
  if (sidebar) {
    sidebar.innerHTML = sidebarContent;
  }

  setupToggleBehavior();
  setupSliders();
  populateManufacturers();
}

function setupToggleBehavior() {
  document.querySelectorAll(".type-toggle").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      const details =
        this.closest(".type-section").querySelector(".type-details");
      if (this.checked) {
        details.style.display = "block";
      } else {
        details.style.display = "none";
      }
    });

    // Initially hide all type details
    const details = checkbox
      .closest(".type-section")
      .querySelector(".type-details");
    details.style.display = "none";
  });
}

function setupSliders() {
  // Year slider
  const yearSlider = document.getElementById("year-slider");
  if (yearSlider) {
    noUiSlider.create(yearSlider, {
      start: [1960, 2025],
      connect: true,
      step: 1,
      range: {
        min: 1960,
        max: 2025,
      },
    });

    const minYearInput = document.getElementById("min-year");
    const maxYearInput = document.getElementById("max-year");

    yearSlider.noUiSlider.on("update", function (values, handle) {
      if (handle === 0) {
        minYearInput.value = Math.round(values[0]);
      } else {
        maxYearInput.value = Math.round(values[1]);
      }
    });

    minYearInput.addEventListener("change", function () {
      yearSlider.noUiSlider.set([this.value, null]);
    });

    maxYearInput.addEventListener("change", function () {
      yearSlider.noUiSlider.set([null, this.value]);
    });
  }

  // Price slider
  const priceSlider = document.getElementById("price-slider");
  if (priceSlider) {
    noUiSlider.create(priceSlider, {
      start: [0, 10000000],
      connect: true,
      step: 10000,
      range: {
        min: 0,
        max: 10000000,
      },
    });

    const minPriceInput = document.getElementById("min-price");
    const maxPriceInput = document.getElementById("max-price");

    priceSlider.noUiSlider.on("update", function (values, handle) {
      if (handle === 0) {
        minPriceInput.value = Math.round(values[0]);
      } else {
        maxPriceInput.value = Math.round(values[1]);
      }
    });

    minPriceInput.addEventListener("change", function () {
      priceSlider.noUiSlider.set([this.value, null]);
    });

    maxPriceInput.addEventListener("change", function () {
      priceSlider.noUiSlider.set([null, this.value]);
    });
  }

  // Power slider
  const powerSlider = document.getElementById("power-slider");
  if (powerSlider) {
    noUiSlider.create(powerSlider, {
      start: [0, 600],
      connect: true,
      step: 10,
      range: {
        min: 0,
        max: 600,
      },
    });

    const minPowerInput = document.getElementById("min-power");
    const maxPowerInput = document.getElementById("max-power");

    powerSlider.noUiSlider.on("update", function (values, handle) {
      if (handle === 0) {
        minPowerInput.value = Math.round(values[0]);
      } else {
        maxPowerInput.value = Math.round(values[1]);
      }
    });

    minPowerInput.addEventListener("change", function () {
      powerSlider.noUiSlider.set([this.value, null]);
    });

    maxPowerInput.addEventListener("change", function () {
      powerSlider.noUiSlider.set([null, this.value]);
    });
  }

  // Engine slider
  const engineSlider = document.getElementById("engine-slider");
  if (engineSlider) {
    noUiSlider.create(engineSlider, {
      start: [0, 15],
      connect: true,
      step: 0.1,
      range: {
        min: 0,
        max: 15,
      },
    });

    const minEngineInput = document.getElementById("min-engine");
    const maxEngineInput = document.getElementById("max-engine");

    engineSlider.noUiSlider.on("update", function (values, handle) {
      if (handle === 0) {
        minEngineInput.value = parseFloat(values[0]).toFixed(1);
      } else {
        maxEngineInput.value = parseFloat(values[1]).toFixed(1);
      }
    });

    minEngineInput.addEventListener("change", function () {
      engineSlider.noUiSlider.set([this.value, null]);
    });

    maxEngineInput.addEventListener("change", function () {
      engineSlider.noUiSlider.set([null, this.value]);
    });
  }

  // Setup additional sliders for new filter sections
  setupAdditionalSliders();
}

function setupAdditionalSliders() {
  // Harvester power slider
  setupRangeSlider(
    "harvester-power-slider",
    "harvester-min-power",
    "harvester-max-power",
    [0, 600],
    10
  );

  // Bunker volume slider
  setupRangeSlider(
    "bunker-slider",
    "min-bunker",
    "max-bunker",
    [0, 15000],
    100
  );

  // Tank capacity slider
  setupRangeSlider("tank-slider", "min-tank", "max-tank", [0, 5000], 100);

  // Bodies slider for plows
  setupRangeSlider("bodies-slider", "min-bodies", "max-bodies", [1, 12], 1);

  // Min power slider for plows
  setupRangeSlider(
    "min-power-slider",
    "min-min-power",
    "max-min-power",
    [0, 600],
    10
  );
}

function setupRangeSlider(sliderId, minInputId, maxInputId, range, step) {
  const slider = document.getElementById(sliderId);
  if (!slider) return;

  noUiSlider.create(slider, {
    start: range,
    connect: true,
    step: step,
    range: {
      min: range[0],
      max: range[1],
    },
  });

  const minInput = document.getElementById(minInputId);
  const maxInput = document.getElementById(maxInputId);

  slider.noUiSlider.on("update", function (values, handle) {
    if (handle === 0) {
      minInput.value = Math.round(values[0]);
    } else {
      maxInput.value = Math.round(values[1]);
    }
  });

  minInput.addEventListener("change", function () {
    slider.noUiSlider.set([this.value, null]);
  });

  maxInput.addEventListener("change", function () {
    slider.noUiSlider.set([null, this.value]);
  });
}

function populateManufacturers() {
  // Use the data attributes to get manufacturers
  const manufacturers = [];
  document.querySelectorAll(".car-box-3").forEach((box) => {
    const manufacturer = box.getAttribute("data-manufacturer");
    if (manufacturer && !manufacturers.includes(manufacturer)) {
      manufacturers.push(manufacturer);
    }
  });

  // Sort manufacturers alphabetically
  manufacturers.sort();

  const manufacturerContainer = document.getElementById("manufacturer-filters");
  if (manufacturerContainer) {
    manufacturers.forEach((manufacturer) => {
      const checkboxDiv = document.createElement("div");
      checkboxDiv.className = "form-check";

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = `manufacturer-${manufacturer}`;
      checkbox.className = "form-check-input";
      checkbox.value = manufacturer;

      const label = document.createElement("label");
      label.htmlFor = `manufacturer-${manufacturer}`;
      label.className = "form-check-label";
      label.textContent = manufacturer;

      checkboxDiv.appendChild(checkbox);
      checkboxDiv.appendChild(label);
      manufacturerContainer.appendChild(checkboxDiv);
    });
  }
}

function extractMachineryData() {
  const machineryItems = [];

  document.querySelectorAll(".car-box-3").forEach((box) => {
    const item = {
      element: box, // Store the DOM element reference for later use
      type: box.getAttribute("data-type"),
      manufacturer: box.getAttribute("data-manufacturer"),
      model: box.getAttribute("data-model"),
      year: parseInt(box.getAttribute("data-year")),
      price: parseInt(box.getAttribute("data-price")),
      condition: box.getAttribute("data-condition"),
      attributes: {
        // Generic attributes that may be present on multiple machine types
        power: box.hasAttribute("data-power")
          ? parseInt(box.getAttribute("data-power"))
          : null,
        engineVolume: box.hasAttribute("data-engine-volume")
          ? parseFloat(box.getAttribute("data-engine-volume"))
          : null,
        width: box.hasAttribute("data-width")
          ? parseFloat(box.getAttribute("data-width"))
          : null,

        // Tractor specific attributes
        driveType: box.getAttribute("data-drive-type"),
        transmissionType: box.getAttribute("data-transmission"),
        towClass: box.getAttribute("data-tow-class"),

        // Sprayer specific attributes
        tankCapacity: box.hasAttribute("data-tank-capacity")
          ? parseInt(box.getAttribute("data-tank-capacity"))
          : null,

        // Plow specific attributes
        bodies: box.hasAttribute("data-bodies")
          ? parseInt(box.getAttribute("data-bodies"))
          : null,
        reversible: box.getAttribute("data-reversible") === "yes",
        minPower: box.hasAttribute("data-min-power")
          ? parseInt(box.getAttribute("data-min-power"))
          : null,

        // Harvester specific attributes
        bunkerVolume: box.hasAttribute("data-bunker-volume")
          ? parseInt(box.getAttribute("data-bunker-volume"))
          : null,
        threshingType: box.getAttribute("data-threshing-type"),
      },
    };

    machineryItems.push(item);
  });
  console.log(machineryItems);
  return machineryItems;
}

function applyFilters(machineryData) {
  // Step 1: Get filter values
  const filters = {
    manufacturers: getCheckedValues("manufacturer"),
    conditions: getCheckedValues("condition"),
    year: {
      min: getNumberInputValue("min-year", 1960),
      max: getNumberInputValue("max-year", 2025),
    },
    price: {
      min: getNumberInputValue("min-price", 0),
      max: getNumberInputValue("max-price", 10000000),
    },
    machineTypes: getMachineTypes(),
    // Tractor specific filters
    tractorFilters: {
      driveTypes: getCheckedValuesById(["drive-wheeled", "drive-tracked"]),
      power: {
        min: getNumberInputValue("min-power", 0),
        max: getNumberInputValue("max-power", 600),
      },
      engineVolume: {
        min: getNumberInputValue("min-engine", 0),
        max: getNumberInputValue("max-engine", 15),
      },
      transmissionTypes: getCheckedValuesById([
        "transmission-manual",
        "transmission-auto",
      ]),
      towClasses: getCheckedValuesById([
        "tow-class-0.2",
        "tow-class-0.6",
        "tow-class-1.4",
        "tow-class-2",
        "tow-class-3",
        "tow-class-4",
        "tow-class-5",
        "tow-class-6",
      ]),
    },
    // Harvester specific filters
    harvesterFilters: {
      power: {
        min: getNumberInputValue("harvester-min-power", 0),
        max: getNumberInputValue("harvester-max-power", 600),
      },
      bunkerVolume: {
        min: getNumberInputValue("min-bunker", 0),
        max: getNumberInputValue("max-bunker", 15000),
      },
      threshingTypes: getCheckedValuesById([
        "threshing-drum",
        "threshing-rotor",
        "threshing-hybrid",
      ]),
    },
    // Sprayer specific filters
    sprayerFilters: {
      tankCapacity: {
        min: getNumberInputValue("min-tank", 0),
        max: getNumberInputValue("max-tank", 5000),
      },
    },
    // Plow specific filters
    plowFilters: {
      bodies: {
        min: getNumberInputValue("min-bodies", 1),
        max: getNumberInputValue("max-bodies", 12),
      },
      reversible: getCheckedValuesById([
        "plow-reversible",
        "plow-non-reversible",
      ]),
      minPower: {
        min: getNumberInputValue("min-min-power", 0),
        max: getNumberInputValue("max-min-power", 600),
      },
    },
  };

  // Step 2: Apply filters to data
  const filteredItems = machineryData.filter((item) => {
    // First, check common filters
    // Manufacturer filter
    if (
      filters.manufacturers.length > 0 &&
      !filters.manufacturers.includes(item.manufacturer)
    ) {
      return false;
    }

    // Condition filter
    if (
      filters.conditions.length > 0 &&
      !filters.conditions.includes(item.condition)
    ) {
      return false;
    }

    // Year range filter
    if (item.year < filters.year.min || item.year > filters.year.max) {
      return false;
    }

    // Price range filter
    if (item.price < filters.price.min || item.price > filters.price.max) {
      return false;
    }

    // Machine type filter
    if (
      filters.machineTypes.length > 0 &&
      !filters.machineTypes.includes(item.type)
    ) {
      return false;
    }

    // Apply type-specific filters
    if (item.type === "Tractor" && filters.machineTypes.includes("Tractor")) {
      // Drive type filter
      if (
        filters.tractorFilters.driveTypes.length > 0 &&
        !filters.tractorFilters.driveTypes.includes(item.attributes.driveType)
      ) {
        return false;
      }

      // Power range filter
      if (
        item.attributes.power !== null &&
        (item.attributes.power < filters.tractorFilters.power.min ||
          item.attributes.power > filters.tractorFilters.power.max)
      ) {
        return false;
      }

      // Engine volume range filter
      if (
        item.attributes.engineVolume !== null &&
        (item.attributes.engineVolume <
          filters.tractorFilters.engineVolume.min ||
          item.attributes.engineVolume >
            filters.tractorFilters.engineVolume.max)
      ) {
        return false;
      }

      // Transmission type filter
      if (
        filters.tractorFilters.transmissionTypes.length > 0 &&
        !filters.tractorFilters.transmissionTypes.includes(
          item.attributes.transmissionType
        )
      ) {
        return false;
      }

      // Tow class filter
      if (
        filters.tractorFilters.towClasses.length > 0 &&
        !filters.tractorFilters.towClasses.includes(item.attributes.towClass)
      ) {
        return false;
      }
    }

    // Harvester specific filters
    if (
      item.type === "Harvester" &&
      filters.machineTypes.includes("Harvester")
    ) {
      // Power range filter
      if (
        item.attributes.power !== null &&
        (item.attributes.power < filters.harvesterFilters.power.min ||
          item.attributes.power > filters.harvesterFilters.power.max)
      ) {
        return false;
      }

      // Bunker volume filter
      if (
        item.attributes.bunkerVolume !== null &&
        (item.attributes.bunkerVolume <
          filters.harvesterFilters.bunkerVolume.min ||
          item.attributes.bunkerVolume >
            filters.harvesterFilters.bunkerVolume.max)
      ) {
        return false;
      }

      // Threshing type filter
      if (
        filters.harvesterFilters.threshingTypes.length > 0 &&
        !filters.harvesterFilters.threshingTypes.includes(
          item.attributes.threshingType
        )
      ) {
        return false;
      }
    }

    // Self-propelled sprayer specific filters
    if (
      item.type === "SelfPropelledSprayer" &&
      filters.machineTypes.includes("SelfPropelledSprayer")
    ) {
      // Tank capacity filter
      if (
        item.attributes.tankCapacity !== null &&
        (item.attributes.tankCapacity <
          filters.sprayerFilters.tankCapacity.min ||
          item.attributes.tankCapacity >
            filters.sprayerFilters.tankCapacity.max)
      ) {
        return false;
      }
    }

    // Plow specific filters
    if (item.type === "Plow" && filters.machineTypes.includes("Plow")) {
      // Bodies count filter
      if (
        item.attributes.bodies !== null &&
        (item.attributes.bodies < filters.plowFilters.bodies.min ||
          item.attributes.bodies > filters.plowFilters.bodies.max)
      ) {
        return false;
      }

      // Reversible filter
      if (filters.plowFilters.reversible.length > 0) {
        const isReversible = item.attributes.reversible ? "yes" : "no";
        if (!filters.plowFilters.reversible.includes(isReversible)) {
          return false;
        }
      }

      // Min power filter
      if (
        item.attributes.minPower !== null &&
        (item.attributes.minPower < filters.plowFilters.minPower.min ||
          item.attributes.minPower > filters.plowFilters.minPower.max)
      ) {
        return false;
      }
    }

    // If item passed all filters
    return true;
  });

  // Step 3: Update UI to show only filtered items
  updateUI(filteredItems, machineryData);
}

// Helper function to get checked values from checkboxes by manufacturer pattern
function getCheckedValues(type) {
  const values = [];
  const checkboxes = document.querySelectorAll(`input[id^="${type}-"]:checked`);

  checkboxes.forEach((checkbox) => {
    values.push(checkbox.value);
  });

  return values;
}

// Helper function to get checked values from checkboxes by explicit IDs
function getCheckedValuesById(ids) {
  const values = [];

  ids.forEach((id) => {
    const checkbox = document.getElementById(id);
    if (checkbox && checkbox.checked) {
      values.push(checkbox.value);
    }
  });

  return values;
}

// Helper function to get number input value with fallback
function getNumberInputValue(id, fallback) {
  const input = document.getElementById(id);
  return input && input.value ? parseFloat(input.value) : fallback;
}

// Helper function to get selected machine types
function getMachineTypes() {
  const types = [];
  const typeCheckboxes = document.querySelectorAll(".type-toggle:checked");

  typeCheckboxes.forEach((checkbox) => {
    types.push(checkbox.value);
  });

  return types;
}

// Function to update UI with filtered results
function updateUI(filteredItems, allItems) {
  // First, hide all items
  allItems.forEach((item) => {
    item.element.style.display = "none";
  });

  // Then show only filtered items
  filteredItems.forEach((item) => {
    item.element.style.display = "block";
  });

  // Show message if no results
  const resultsContainer = document.querySelector(".row");
  const noResultsMessage = document.getElementById("no-results-message");

  if (filteredItems.length === 0) {
    if (!noResultsMessage) {
      const message = document.createElement("div");
      message.id = "no-results-message";
      message.className = "col-12 text-center my-5";
      message.innerHTML = `
<h3>Нет результатов, соответствующих фильтрам</h3>
<p>Попробуйте изменить параметры фильтрации</p>
`;
      resultsContainer.appendChild(message);
    }
  } else if (noResultsMessage) {
    noResultsMessage.remove();
  }

  // Update counter if it exists
  const counter = document.querySelector(".filter-counter");
  if (counter) {
    counter.textContent = `Найдено: ${filteredItems.length}`;
  }
}
