async function searchDestination() {
  const city = document.getElementById('destinationInput').value.trim();
  const resultDiv = document.getElementById('destinationResult');
  const weatherBox = document.getElementById('weather');
  const attractionsBox = document.getElementById('attractions');
  const restaurantsBox = document.getElementById('restaurants');

  resultDiv.innerHTML = 'Loading...';
  weatherBox.classList.add('hidden');
  attractionsBox.classList.add('hidden');
  restaurantsBox.classList.add('hidden');

  const weatherApiKey = 'e373769e2050490599b134019252909';
  const unsplashAccessKey = 'gpfwZz-jHdDm6SmUfqlF-vbGYw2x47T_IQA_8hS8OuQ'; // Replace this

  try {
    // Fetch weather
    const weatherRes = await fetch(`http://api.weatherapi.com/v1/current.json?key=${weatherApiKey}&q=${city}&aqi=no`);
    const weatherData = await weatherRes.json();

    // Fetch image
    const imageRes = await fetch(`https://api.unsplash.com/search/photos?query=${city}&client_id=${unsplashAccessKey}`);
    const imageData = await imageRes.json();
    const imageUrl = imageData.results[0]?.urls?.regular || '';

    // Display image and basic info
    resultDiv.innerHTML = `
      <h3>${city}</h3>
      <img src="${imageUrl}" alt="${city}" />
    `;

    // Display weather
    weatherBox.innerHTML = `
      <h2>Weather in ${city}</h2>
      <p><strong>Temperature:</strong> ${weatherData.current.temp_c}°C</p>
      <p><strong>Condition:</strong> ${weatherData.current.condition.text}</p>
      <p><strong>Humidity:</strong> ${weatherData.current.humidity}%</p>
      <p><strong>Wind:</strong> ${weatherData.current.wind_kph} km/h</p>
    `;
    weatherBox.classList.remove('hidden');

    // Simulated attractions
    const attractions = ['City Palace', 'Local Museum', 'Botanical Garden'];
    attractionsBox.innerHTML = `<h2>Top Attractions</h2><ul>${attractions.map(a => `<li>${a}</li>`).join('')}</ul>`;
    attractionsBox.classList.remove('hidden');

    // Simulated restaurants
    const restaurants = ['Spice Villa', 'Tandoori Treats', 'Café Delight'];
    restaurantsBox.innerHTML = `<h2>Popular Restaurants</h2><ul>${restaurants.map(r => `<li>${r}</li>`).join('')}</ul>`;
    restaurantsBox.classList.remove('hidden');

  } catch (error) {
    resultDiv.innerHTML = 'Error fetching data. Please try again.';
    console.error(error);
  }
}