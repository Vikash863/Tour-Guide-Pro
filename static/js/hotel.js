const API_KEY = "7c52fb6c66464373a2bfc6512686a1e4"; // Geoapify key

let allHotels = [];
let allRestaurants = [];

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("hotelSearchForm");

  // Filter event listeners
  document.getElementById("ratingFilter")?.addEventListener("change", applyFilters);
  document.getElementById("priceFilter")?.addEventListener("change", applyFilters);
  document.getElementById("sortFilter")?.addEventListener("change", applyFilters);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const searchBtn = form.querySelector(".search-btn");
    const originalText = searchBtn.innerHTML;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    searchBtn.classList.add("loading");

    const place = document.getElementById("location").value.trim();
    if (!place) {
      searchBtn.innerHTML = originalText;
      searchBtn.classList.remove("loading");
      return;
    }

    // Update location display
    document.getElementById("currentLocation").textContent = place;

    document.getElementById("hotelResults").innerHTML = '<div class="spinner"></div>';
    document.getElementById("restaurantResults").querySelector(".hotel-cards").innerHTML = "";

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
        `https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=circle:${lon},${lat},5000&limit=12&apiKey=${API_KEY}`
      );

      if (!hotelsRes.ok) throw new Error("Hotels API error");

      const hotelsData = await hotelsRes.json();
      allHotels = hotelsData.features;
      
      // Update hotel count
      document.getElementById("hotelCount").textContent = allHotels.length;
      
      renderHotels(allHotels);
      
      // Clear restaurants
      allRestaurants = [];
      document.getElementById("restaurantResults").querySelector(".hotel-cards").innerHTML = "";
      
    } catch (err) {
      document.getElementById("hotelResults").innerHTML = `
        <div class="error">
          <i class="fas fa-exclamation-triangle"></i>
          <span>${err.message}</span>
        </div>
      `;
      console.error(err);
    } finally {
      searchBtn.innerHTML = originalText;
      searchBtn.classList.remove("loading");
    }
  });
});

function renderHotels(hotels) {
  const container = document.getElementById("hotelResults");

  if (!hotels || !hotels.length) {
    container.innerHTML = `
      <div class="placeholder-message">
        <i class="fas fa-bed"></i>
        <h3>No Hotels Found</h3>
        <p>Try searching for a different location or expanding your search area.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = hotels
    .map((h, index) => {
      const p = h.properties;
      const safeName = encodeURIComponent(p.name || "hotel");
      
      // Generate random rating for demo (in real app, this would come from API)
      const rating = (Math.random() * (5 - 3) + 3).toFixed(1);
      const stars = Math.floor(rating);
      
      // Generate distance
      const distance = (Math.random() * 2 + 0.1).toFixed(1);
      
      // Generate mock amenities
      const amenitiesList = [
        { icon: "fa-wifi", name: "Free WiFi" },
        { icon: "fa-parking", name: "Parking" },
        { icon: "fa-swimming-pool", name: "Pool" },
        { icon: "fa-concierge-bell", name: "Room Service" },
        { icon: "fa-dumbbell", name: "Gym" },
        { icon: "fa-spa", name: "Spa" },
        { icon: "fa-utensils", name: "Restaurant" },
        { icon: "fa-coffee", name: "Breakfast" }
      ];
      
      // Randomly select 3-5 amenities
      const shuffled = amenitiesList.sort(() => 0.5 - Math.random());
      const selectedAmenities = shuffled.slice(0, Math.floor(Math.random() * 3) + 3);
      
      // Determine if featured
      const isFeatured = index < 3;
      
      return `
        <div class="card" data-lat="${p.lat}" data-lon="${p.lon}" style="animation-delay: ${index * 0.1}s">
          ${isFeatured ? '<span class="card-badge">Featured</span>' : ''}
          <div class="card-header">
            <h3><i class="fas fa-hotel"></i> ${p.name || "Unnamed Hotel"}</h3>
            <div class="rating">
              ${Array(stars).fill('<i class="fas fa-star star"></i>').join('')}
              ${Array(5 - stars).fill('<i class="far fa-star star"></i>').join('')}
              <span class="rating-text">${rating}</span>
            </div>
          </div>
          <div class="card-body">
            <div class="address">
              <i class="fas fa-map-marker-alt"></i>
              <span>${p.address_line1 || p.formatted || "Address not available"}</span>
            </div>
            
            <div class="distance-badge">
              <i class="fas fa-location-arrow"></i>
              ${distance} km from search location
            </div>
            
            <div class="amenities">
              ${selectedAmenities.map(a => `
                <span class="amenity">
                  <i class="fas ${a.icon}"></i>
                  ${a.name}
                </span>
              `).join('')}
            </div>
            
            <div class="card-actions">
              <button class="book-btn" data-name="${safeName}" data-lat="${p.lat}" data-lon="${p.lon}">
                <i class="fas fa-calendar-check"></i> Book Now
              </button>
              <button class="view-restaurants" data-lat="${p.lat}" data-lon="${p.lon}">
                <i class="fas fa-utensils"></i> Restaurants
              </button>
            </div>
          </div>
        </div>
      `;
    })
    .join("");

  // Book buttons
  document.querySelectorAll(".book-btn").forEach((btn) => {
    btn.onclick = (e) => {
      e.stopPropagation();
      bookHotel(btn.dataset.name, btn.dataset.lat, btn.dataset.lon);
    };
  });

  // Restaurant buttons
  document.querySelectorAll(".view-restaurants").forEach((btn) => {
    btn.onclick = (e) => {
      e.stopPropagation();
      const card = btn.closest(".card");
      fetchRestaurants(card.dataset.lat, card.dataset.lon, card.querySelector("h3")?.textContent || "Hotel");
    };
  });
}

function bookHotel(hotelName, lat, lon) {
  const name = decodeURIComponent(hotelName);
  
  // Show confirmation
  if (confirm(`Do you want to book "${name}"?`)) {
    window.location.href = `/book-hotel?name=${encodeURIComponent(name)}&lat=${lat || ''}&lon=${lon || ''}`;
  }
}

async function fetchRestaurants(lat, lon) {
  const container = document.getElementById("restaurantResults").querySelector(".hotel-cards");
  container.innerHTML = '<div class="spinner"></div>';
  
  // Scroll to restaurants section
  document.getElementById("restaurantResults").scrollIntoView({ behavior: "smooth" });

  try {
    const res = await fetch(
      `https://api.geoapify.com/v2/places?categories=catering.restaurant&filter=circle:${lon},${lat},1500&limit=8&apiKey=${API_KEY}`
    );

    if (!res.ok) throw new Error("Restaurants API error");

    const data = await res.json();
    allRestaurants = data.features;

    if (!allRestaurants.length) {
      container.innerHTML = `
        <div class="placeholder-message" style="grid-column: 1 / -1;">
          <i class="fas fa-utensils"></i>
          <h3>No Restaurants Found</h3>
          <p>No restaurants found near this location.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = allRestaurants
      .map((r, index) => {
        const p = r.properties;
        const rating = (Math.random() * (5 - 3.5) + 3.5).toFixed(1);
        const stars = Math.floor(rating);
        
        // Generate mock price range
        const priceRanges = ["$", "$$", "$$$"];
        const priceRange = priceRanges[Math.floor(Math.random() * priceRanges.length)];
        
        // Generate mock cuisine types
        const cuisines = ["Indian", "Chinese", "Italian", "Thai", "Mexican", "Continental", "Local", "Multi-cuisine"];
        const cuisine = cuisines[Math.floor(Math.random() * cuisines.length)];
        
        return `
          <div class="card" data-lat="${p.lat}" data-lon="${p.lon}" style="animation-delay: ${index * 0.1}s">
            <div class="card-header">
              <h3><i class="fas fa-utensils"></i> ${p.name || "Unnamed Restaurant"}</h3>
              <div class="rating">
                ${Array(stars).fill('<i class="fas fa-star star"></i>').join('')}
                ${Array(5 - stars).fill('<i class="far fa-star star"></i>').join('')}
                <span class="rating-text">${rating}</span>
              </div>
            </div>
            <div class="card-body">
              <div class="address">
                <i class="fas fa-map-marker-alt"></i>
                <span>${p.address_line1 || p.formatted || "Address not available"}</span>
              </div>
              
              <div class="distance-badge">
                <i class="fas fa-walking"></i>
                Walking distance
              </div>
              
              <div class="amenities">
                <span class="amenity">
                  <i class="fas fa-tag"></i>
                  ${cuisine}
                </span>
                <span class="amenity">
                  <i class="fas fa-money-bill-wave"></i>
                  ${priceRange}
                </span>
                ${p.opening_hours ? `
                  <span class="amenity">
                    <i class="far fa-clock"></i>
                    Open Now
                  </span>
                ` : ''}
              </div>
              
              <div class="card-actions">
                ${p.website ? `
                  <a href="${p.website}" target="_blank" class="book-btn" style="text-decoration: none; display: inline-flex;">
                    <i class="fas fa-external-link-alt"></i> Visit Website
                  </a>
                ` : ''}
                <button class="view-restaurants" onclick="alert('Directions feature coming soon!')">
                  <i class="fas fa-directions"></i> Directions
                </button>
              </div>
            </div>
          </div>
        `;
      })
      .join("");
  } catch (err) {
    container.innerHTML = `
      <div class="error" style="grid-column: 1 / -1;">
        <i class="fas fa-exclamation-triangle"></i>
        <span>${err.message}</span>
      </div>
    `;
    console.error(err);
  }
}

function applyFilters() {
  if (!allHotels.length) return;

  const ratingFilter = document.getElementById("ratingFilter").value;
  const priceFilter = document.getElementById("priceFilter").value;
  const sortFilter = document.getElementById("sortFilter").value;

  let filtered = [...allHotels];

  // Apply rating filter (mock rating since API doesn't provide it)
  if (ratingFilter !== "all") {
    filtered = filtered.filter((_, index) => {
      const rating = (Math.random() * (5 - 3) + 3);
      return rating >= parseFloat(ratingFilter);
    });
  }

  // Apply sorting
  switch (sortFilter) {
    case "rating":
      filtered.sort((a, b) => {
        const ratingA = Math.random() * (5 - 3) + 3;
        const ratingB = Math.random() * (5 - 3) + 3;
        return ratingB - ratingA;
      });
      break;
    case "distance":
      // Already sorted by API distance
      break;
    case "name":
      filtered.sort((a, b) => {
        const nameA = a.properties.name || "";
        const nameB = b.properties.name || "";
        return nameA.localeCompare(nameB);
      });
      break;
  }

  // Update count
  document.getElementById("hotelCount").textContent = filtered.length;
  
  renderHotels(filtered);
}

function resetFilters() {
  document.getElementById("ratingFilter").value = "all";
  document.getElementById("priceFilter").value = "all";
  document.getElementById("sortFilter").value = "rating";
  
  if (allHotels.length) {
    document.getElementById("hotelCount").textContent = allHotels.length;
    renderHotels(allHotels);
  }
}

// Add smooth scroll behavior for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

// Mobile menu toggle (if implemented)
document.querySelector('.mobile-menu')?.addEventListener('click', () => {
  const navLinks = document.querySelector('.nav-links');
  navLinks.classList.toggle('active');
});
