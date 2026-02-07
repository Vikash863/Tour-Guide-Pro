const API_KEY = "7c52fb6c66464373a2bfc6512686a1e4"; // Geoapify key

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("hotelSearchForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const place = document.getElementById("location").value.trim();
    if (!place) return;

    document.getElementById("hotelResults").innerHTML = '<div class="spinner"></div>';
    document.getElementById("restaurantResults").innerHTML = "";

    try {
      // 1. Geocode place
      const geoRes = await fetch(
        `https://api.geoapify.com/v1/geocode/search?text=${encodeURIComponent(place)}&format=json&limit=1&apiKey=${API_KEY}`
      );

      if (!geoRes.ok) throw new Error("Geocoding failed");
      const geoData = await geoRes.json();
      if (!geoData.results.length) throw new Error("Location not found");

      const { lat, lon } = geoData.results[0];

      // 2. Fetch hotels
      const hotelsRes = await fetch(
        `https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=circle:${lon},${lat},2000&limit=10&apiKey=${API_KEY}`
      );

      if (!hotelsRes.ok) throw new Error("Hotels API error");

      const hotelsData = await hotelsRes.json();
      renderHotels(hotelsData.features);
    } catch (err) {
      document.getElementById("hotelResults").innerHTML = `<p class="error">${err.message}</p>`;
      console.error(err);
    }
  });
});

function renderHotels(hotels) {
  const container = document.getElementById("hotelResults");

  if (!hotels.length) {
    container.innerHTML = "<p>No hotels found nearby.</p>";
    return;
  }

  container.innerHTML = hotels
    .map((h) => {
      const p = h.properties;
      const safeName = encodeURIComponent(p.name || "hotel");

      return `
        <div class="card" data-lat="${p.lat}" data-lon="${p.lon}">
          <h3>${p.name || "Unnamed Hotel"}</h3>
          <p>${p.address_line1 || p.formatted}</p>

          <button class="book-btn" data-name="${safeName}">
            Book Now
          </button>

          <button class="view-restaurants">View Restaurants Nearby</button>
        </div>
      `;
    })
    .join("");

  // Book buttons
  document.querySelectorAll(".book-btn").forEach((btn) => {
    btn.onclick = () => {
      bookHotel(btn.dataset.name);
    };
  });

  // Restaurant buttons
  document.querySelectorAll(".view-restaurants").forEach((btn) => {
    btn.onclick = () => {
      const card = btn.closest(".card");
      fetchRestaurants(card.dataset.lat, card.dataset.lon);
    };
  });
}

function bookHotel(hotelName) {
  const name = decodeURIComponent(hotelName);
  function bookHotel(hotelName) {
  window.location.href = "/book-hotel?name=" + encodeURIComponent(hotelName);
}

  window.location.href = "/book-hotel?name=" + hotelName;
}

async function fetchRestaurants(lat, lon) {
  const container = document.getElementById("restaurantResults");
  container.innerHTML = '<div class="spinner"></div>';

  try {
    const res = await fetch(
      `https://api.geoapify.com/v2/places?categories=catering.restaurant&filter=circle:${lon},${lat},1000&limit=8&apiKey=${API_KEY}`
    );

    if (!res.ok) throw new Error("Restaurants API error");

    const data = await res.json();

    if (!data.features.length) {
      container.innerHTML = "<p>No restaurants found nearby.</p>";
      return;
    }

    container.innerHTML = data.features
      .map((r) => {
        const p = r.properties;
        return `
          <div class="card">
            <h3>${p.name || "Unnamed Restaurant"}</h3>
            <p>${p.address_line1 || p.formatted}</p>
            ${p.website ? `<a href="${p.website}" target="_blank">Visit Site</a>` : ""}
          </div>
        `;
      })
      .join("");
  } catch (err) {
    container.innerHTML = `<p class="error">${err.message}</p>`;
    console.error(err);
  }
}
