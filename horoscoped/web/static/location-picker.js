(function () {
  const cities = [
    { city: "New York", country: "USA", region: "North America", timezone: "America/New_York" },
    { city: "Los Angeles", country: "USA", region: "North America", timezone: "America/Los_Angeles" },
    { city: "Chicago", country: "USA", region: "North America", timezone: "America/Chicago" },
    { city: "Houston", country: "USA", region: "North America", timezone: "America/Chicago" },
    { city: "Phoenix", country: "USA", region: "North America", timezone: "America/Phoenix" },
    { city: "Denver", country: "USA", region: "North America", timezone: "America/Denver" },
    { city: "Miami", country: "USA", region: "North America", timezone: "America/New_York" },
    { city: "Seattle", country: "USA", region: "North America", timezone: "America/Los_Angeles" },
    { city: "Toronto", country: "Canada", region: "North America", timezone: "America/Toronto" },
    { city: "Vancouver", country: "Canada", region: "North America", timezone: "America/Vancouver" },
    { city: "Montreal", country: "Canada", region: "North America", timezone: "America/Toronto" },
    { city: "Mexico City", country: "Mexico", region: "North America", timezone: "America/Mexico_City" },
    { city: "Guadalajara", country: "Mexico", region: "North America", timezone: "America/Mexico_City" },

    { city: "Sao Paulo", country: "Brazil", region: "Latin America", timezone: "America/Sao_Paulo" },
    { city: "Rio de Janeiro", country: "Brazil", region: "Latin America", timezone: "America/Sao_Paulo" },
    { city: "Buenos Aires", country: "Argentina", region: "Latin America", timezone: "America/Argentina/Buenos_Aires" },
    { city: "Lima", country: "Peru", region: "Latin America", timezone: "America/Lima" },
    { city: "Bogota", country: "Colombia", region: "Latin America", timezone: "America/Bogota" },
    { city: "Santiago", country: "Chile", region: "Latin America", timezone: "America/Santiago" },
    { city: "Caracas", country: "Venezuela", region: "Latin America", timezone: "America/Caracas" },
    { city: "San Juan", country: "Puerto Rico", region: "Latin America", timezone: "America/Puerto_Rico" },
    { city: "Havana", country: "Cuba", region: "Latin America", timezone: "America/Havana" },
    { city: "Kingston", country: "Jamaica", region: "Latin America", timezone: "America/Jamaica" },

    { city: "London", country: "United Kingdom", region: "Europe", timezone: "Europe/London" },
    { city: "Dublin", country: "Ireland", region: "Europe", timezone: "Europe/Dublin" },
    { city: "Paris", country: "France", region: "Europe", timezone: "Europe/Paris" },
    { city: "Madrid", country: "Spain", region: "Europe", timezone: "Europe/Madrid" },
    { city: "Barcelona", country: "Spain", region: "Europe", timezone: "Europe/Madrid" },
    { city: "Berlin", country: "Germany", region: "Europe", timezone: "Europe/Berlin" },
    { city: "Rome", country: "Italy", region: "Europe", timezone: "Europe/Rome" },
    { city: "Amsterdam", country: "Netherlands", region: "Europe", timezone: "Europe/Amsterdam" },
    { city: "Stockholm", country: "Sweden", region: "Europe", timezone: "Europe/Stockholm" },
    { city: "Oslo", country: "Norway", region: "Europe", timezone: "Europe/Oslo" },
    { city: "Warsaw", country: "Poland", region: "Europe", timezone: "Europe/Warsaw" },
    { city: "Athens", country: "Greece", region: "Europe", timezone: "Europe/Athens" },
    { city: "Istanbul", country: "Turkey", region: "Europe", timezone: "Europe/Istanbul" },
    { city: "Moscow", country: "Russia", region: "Europe", timezone: "Europe/Moscow" },

    { city: "Cairo", country: "Egypt", region: "Africa", timezone: "Africa/Cairo" },
    { city: "Lagos", country: "Nigeria", region: "Africa", timezone: "Africa/Lagos" },
    { city: "Kinshasa", country: "DR Congo", region: "Africa", timezone: "Africa/Kinshasa" },
    { city: "Johannesburg", country: "South Africa", region: "Africa", timezone: "Africa/Johannesburg" },
    { city: "Cape Town", country: "South Africa", region: "Africa", timezone: "Africa/Johannesburg" },
    { city: "Nairobi", country: "Kenya", region: "Africa", timezone: "Africa/Nairobi" },
    { city: "Casablanca", country: "Morocco", region: "Africa", timezone: "Africa/Casablanca" },
    { city: "Addis Ababa", country: "Ethiopia", region: "Africa", timezone: "Africa/Addis_Ababa" },
    { city: "Accra", country: "Ghana", region: "Africa", timezone: "Africa/Accra" },

    { city: "Dubai", country: "United Arab Emirates", region: "Middle East", timezone: "Asia/Dubai" },
    { city: "Riyadh", country: "Saudi Arabia", region: "Middle East", timezone: "Asia/Riyadh" },
    { city: "Jeddah", country: "Saudi Arabia", region: "Middle East", timezone: "Asia/Riyadh" },
    { city: "Doha", country: "Qatar", region: "Middle East", timezone: "Asia/Qatar" },
    { city: "Kuwait City", country: "Kuwait", region: "Middle East", timezone: "Asia/Kuwait" },
    { city: "Jerusalem", country: "Israel", region: "Middle East", timezone: "Asia/Jerusalem" },
    { city: "Baghdad", country: "Iraq", region: "Middle East", timezone: "Asia/Baghdad" },
    { city: "Tehran", country: "Iran", region: "Middle East", timezone: "Asia/Tehran" },

    { city: "Mumbai", country: "India", region: "South Asia", timezone: "Asia/Kolkata" },
    { city: "Delhi", country: "India", region: "South Asia", timezone: "Asia/Kolkata" },
    { city: "Bengaluru", country: "India", region: "South Asia", timezone: "Asia/Kolkata" },
    { city: "Kolkata", country: "India", region: "South Asia", timezone: "Asia/Kolkata" },
    { city: "Karachi", country: "Pakistan", region: "South Asia", timezone: "Asia/Karachi" },
    { city: "Lahore", country: "Pakistan", region: "South Asia", timezone: "Asia/Karachi" },
    { city: "Dhaka", country: "Bangladesh", region: "South Asia", timezone: "Asia/Dhaka" },
    { city: "Colombo", country: "Sri Lanka", region: "South Asia", timezone: "Asia/Colombo" },
    { city: "Kathmandu", country: "Nepal", region: "South Asia", timezone: "Asia/Kathmandu" },

    { city: "Tokyo", country: "Japan", region: "East Asia", timezone: "Asia/Tokyo" },
    { city: "Osaka", country: "Japan", region: "East Asia", timezone: "Asia/Tokyo" },
    { city: "Seoul", country: "South Korea", region: "East Asia", timezone: "Asia/Seoul" },
    { city: "Beijing", country: "China", region: "East Asia", timezone: "Asia/Shanghai" },
    { city: "Shanghai", country: "China", region: "East Asia", timezone: "Asia/Shanghai" },
    { city: "Hong Kong", country: "China", region: "East Asia", timezone: "Asia/Hong_Kong" },
    { city: "Taipei", country: "Taiwan", region: "East Asia", timezone: "Asia/Taipei" },
    { city: "Ulaanbaatar", country: "Mongolia", region: "East Asia", timezone: "Asia/Ulaanbaatar" },

    { city: "Singapore", country: "Singapore", region: "Southeast Asia", timezone: "Asia/Singapore" },
    { city: "Bangkok", country: "Thailand", region: "Southeast Asia", timezone: "Asia/Bangkok" },
    { city: "Jakarta", country: "Indonesia", region: "Southeast Asia", timezone: "Asia/Jakarta" },
    { city: "Manila", country: "Philippines", region: "Southeast Asia", timezone: "Asia/Manila" },
    { city: "Ho Chi Minh City", country: "Vietnam", region: "Southeast Asia", timezone: "Asia/Ho_Chi_Minh" },
    { city: "Hanoi", country: "Vietnam", region: "Southeast Asia", timezone: "Asia/Ho_Chi_Minh" },
    { city: "Kuala Lumpur", country: "Malaysia", region: "Southeast Asia", timezone: "Asia/Kuala_Lumpur" },
    { city: "Yangon", country: "Myanmar", region: "Southeast Asia", timezone: "Asia/Yangon" },

    { city: "Sydney", country: "Australia", region: "Oceania", timezone: "Australia/Sydney" },
    { city: "Melbourne", country: "Australia", region: "Oceania", timezone: "Australia/Melbourne" },
    { city: "Brisbane", country: "Australia", region: "Oceania", timezone: "Australia/Brisbane" },
    { city: "Perth", country: "Australia", region: "Oceania", timezone: "Australia/Perth" },
    { city: "Auckland", country: "New Zealand", region: "Oceania", timezone: "Pacific/Auckland" },
    { city: "Wellington", country: "New Zealand", region: "Oceania", timezone: "Pacific/Auckland" },
    { city: "Honolulu", country: "USA", region: "Oceania", timezone: "Pacific/Honolulu" },
    { city: "Suva", country: "Fiji", region: "Oceania", timezone: "Pacific/Fiji" },
  ];

  document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("[data-location-form]");
    const modal = document.querySelector("[data-location-modal]");
    const openButton = document.querySelector("[data-location-open]");
    const closeButtons = document.querySelectorAll("[data-location-close]");
    const searchInput = document.querySelector("[data-location-search]");
    const regionList = document.querySelector("[data-location-regions]");
    const results = document.querySelector("[data-location-results]");
    const placeInput = document.getElementById("place");
    const timezoneInput = document.getElementById("timezone");
    const label = document.querySelector("[data-location-label]");
    const meta = document.querySelector("[data-location-meta]");
    const validation = document.querySelector("[data-location-validation]");

    if (!form || !modal || !openButton || !searchInput || !regionList || !results || !placeInput || !timezoneInput) {
      return;
    }

    const regions = Array.from(new Set(cities.map((city) => city.region)));
    let activeRegion = regions[0];
    let lastFocusedElement = null;

    function cityLabel(city) {
      return `${city.city}, ${city.country}`;
    }

    function openModal() {
      lastFocusedElement = document.activeElement;
      modal.hidden = false;
      document.body.classList.add("modal-open");
      searchInput.focus();
      renderResults();
    }

    function closeModal() {
      modal.hidden = true;
      document.body.classList.remove("modal-open");
      if (lastFocusedElement) {
        lastFocusedElement.focus();
      }
    }

    function renderRegions() {
      regionList.innerHTML = "";
      regions.forEach((region) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "location-region";
        button.textContent = region;
        button.setAttribute("aria-pressed", String(region === activeRegion));
        button.addEventListener("click", () => {
          activeRegion = region;
          searchInput.value = "";
          renderRegions();
          renderResults();
        });
        regionList.appendChild(button);
      });
    }

    function matchingCities() {
      const query = searchInput.value.trim().toLowerCase();
      if (query) {
        return cities.filter((city) => {
          return [
            city.city,
            city.country,
            city.region,
            city.timezone,
          ].some((value) => value.toLowerCase().includes(query));
        });
      }

      return cities.filter((city) => city.region === activeRegion);
    }

    function renderResults() {
      const matches = matchingCities();
      results.innerHTML = "";

      if (matches.length === 0) {
        const empty = document.createElement("p");
        empty.className = "location-empty";
        empty.textContent = "No cities found. Try the nearest major city or browse by area.";
        results.appendChild(empty);
        return;
      }

      matches.forEach((city) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "location-result";
        button.innerHTML = `
          <span>
            <strong>${cityLabel(city)}</strong>
            <small>${city.region}</small>
          </span>
          <small>${city.timezone}</small>
        `;
        button.addEventListener("click", () => {
          placeInput.value = cityLabel(city);
          timezoneInput.value = city.timezone;
          label.textContent = cityLabel(city);
          meta.textContent = city.timezone;
          validation.hidden = true;
          closeModal();
        });
        results.appendChild(button);
      });
    }

    openButton.addEventListener("click", openModal);
    closeButtons.forEach((button) => button.addEventListener("click", closeModal));
    searchInput.addEventListener("input", renderResults);

    modal.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeModal();
      }
    });

    form.addEventListener("submit", (event) => {
      if (!timezoneInput.value.trim()) {
        event.preventDefault();
        validation.hidden = false;
        openModal();
      }
    });

    renderRegions();
    renderResults();
  });
})();
