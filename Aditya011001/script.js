// API Key from OpenWeatherMap
const apiKey = 'c21d00866eea22c35ad49cd16a6d3c79'; // Replace with your API key

// DOM Elements
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const weatherInfo = document.getElementById('weatherInfo');

// Function to fetch weather data
async function getWeather(city) {
  const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

  try {
    const response = await fetch(apiUrl);
    const data = await response.json();

    if (data.cod === 200) {
      displayWeather(data);
    } else {
      weatherInfo.innerHTML = `<p class="error">City not found. Please try again.</p>`;
    }
  } catch (error) {
    console.error('Error fetching weather data:', error);
    weatherInfo.innerHTML = `<p class="error">An error occurred. Please try again later.</p>`;
  }
}

// Function to display weather data
function displayWeather(data) {
  const { name, main, weather, wind, sys } = data;
  const temperature = main.temp;
  const feelsLike = main.feels_like;
  const humidity = main.humidity;
  const pressure = main.pressure;
  const windSpeed = wind.speed;
  const weatherDescription = weather[0].description;
  const icon = weather[0].icon;
  const country = sys.country;

  weatherInfo.innerHTML = `
    <div class="weather-card">
      <h2>${name}, ${country}</h2>
      <p class="temperature">${temperature}°C</p>
      <p class="weather-description">${weatherDescription}</p>
      <img src="http://openweathermap.org/img/wn/${icon}@2x.png" alt="${weatherDescription}">
      <div class="details">
        <p><span>Feels Like:</span> ${feelsLike}°C</p>
        <p><span>Humidity:</span> ${humidity}%</p>
        <p><span>Pressure:</span> ${pressure} hPa</p>
        <p><span>Wind Speed:</span> ${windSpeed} m/s</p>
      </div>
    </div>
  `;
}

// Event listener for the search button
searchBtn.addEventListener('click', () => {
  const city = cityInput.value.trim();
  if (city) {
    getWeather(city);
  } else {
    weatherInfo.innerHTML = `<p class="error">Please enter a city name.</p>`;
  }
});

// Optional: Allow pressing "Enter" to search
cityInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    searchBtn.click();
  }
});