let weather = {
  apiKey: "537d958674af08b22115d5e049b5a408",
  fetchWeather: function (city) {
    fetch(
      "https://api.openweathermap.org/data/2.5/weather?q=" +
        city +
        "&units=metric&appid=" +
        this.apiKey
    )
      .then((response) => {
        if (!response.ok) {
          alert("No weather found.");
          throw new Error("No weather found.");
        }
        return response.json();
      })
      .then((data) => this.displayWeather(data));
  }
  ,sendCityToBackend: function(city) {
    console.log("Sending city to backend:", city);

    fetch("backend.php", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "city=" + city
    })
    .then((response) => response.text())
    .then((data) => console.log("Response from backend:", data));
},
  displayWeather: function (data) {
    this.sendCityToBackend(city);
    const { name } = data;
    const { icon, description } = data.weather[0];
    const { temp, humidity } = data.main;
    const { speed } = data.wind;
    document.querySelector(".city").innerText = "Weather in " + name;
    document.querySelector(".icon").src =
      "https://openweathermap.org/img/wn/" + icon + ".png";
    document.querySelector(".description").innerText = description;
    document.querySelector(".temp").innerText = temp + "°C";
    document.querySelector(".humidity").innerText =
      "Humidity: " + humidity + "%";
    document.querySelector(".wind").innerText =
      "Wind speed: " + speed + " km/h";
    document.querySelector(".weather").classList.remove("loading");
    if (description.includes("clear")) {
      document.body.style.backgroundImage = "url('clear_sky.jpg')";
    } else if (description.includes("rain")) {
      document.body.style.backgroundImage = "url('rainy.jpg')";
    } else if (description.includes("cloud")) {
      document.body.style.backgroundImage = "url('cloudy.jpeg')";
    } else if (description.includes("light snow")) {
      document.body.style.backgroundImage = "url('snow.jpg')";
    } else {
      document.body.style.backgroundImage = "url('default_weather.jpg')";
    }
    
  },
  search: function () {
    this.fetchWeather(document.querySelector(".search-bar").value);
  },

  

};

document.querySelector(".search button").addEventListener("click", function () {
  weather.search();
});

document
  .querySelector(".search-bar")
  .addEventListener("keyup", function (event) {
    if (event.key == "Enter") {
      weather.search();
    }
  });

weather.fetchWeather("jamshoro");
