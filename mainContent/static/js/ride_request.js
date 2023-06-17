var apiBusStopUrl = apiUrl + 'BusStop/';
var busStopsData = []; // Przechowuje dane wszystkich przystanków
var selectedBusStops = [];
var apiTravelerUrl = apiUrl + 'Traveler/';


// Wyświetlanie listy przystanków po kliknięciu na pole tekstowe
function showBusStops(inputId) {
  var inputElement = document.getElementById(inputId);
  var busStopList = document.getElementById("bus-stop-list");

  if (busStopList) {
    busStopList.remove();
  }

  var busStopListContainer = document.createElement("div");
  busStopListContainer.classList.add("bus-stop-list");
  busStopListContainer.setAttribute("id", "bus-stop-list-container");

  fetch(apiBusStopUrl)
      .then(response => response.json())
      .then(data => {
        busStopsData = data; // Zapisz dane wszystkich przystanków

        data.forEach(busStop => {
          var listItem = document.createElement("div");
          listItem.textContent = busStop.name;
          listItem.classList.add("bus-stop-list-item");

          // Obsługa wyboru przystanku
          listItem.addEventListener("click", function () {
            inputElement.value = busStop.name;
            busStopListContainer.remove();

            // Dodaj wybrany przystanek do zmiennej selectedBusStops
            selectedBusStops.push(busStop);
          });

          busStopListContainer.appendChild(listItem);
        });

        inputElement.parentNode.insertBefore(busStopListContainer, inputElement.nextSibling);
        busStopListContainer.style.display = "block";
      })
      .catch(error => {
        console.error("Błąd pobierania danych przystanków:", error);
      });
}

// Filtrowanie listy przystanków na podstawie wpisanego tekstu
function filterBusStops(inputId) {
  var inputElement = document.getElementById(inputId);
  var busStopListContainer = document.getElementById("bus-stop-list-container");

  if (busStopListContainer) {
    var filterValue = inputElement.value.toLowerCase();
    var filteredBusStops = busStopsData.filter(busStop => busStop.name.toLowerCase().includes(filterValue));

    while (busStopListContainer.firstChild) {
      busStopListContainer.firstChild.remove();
    }

    filteredBusStops.forEach(busStop => {
      var listItem = document.createElement("div");
      listItem.textContent = busStop.name;
      listItem.classList.add("bus-stop-list-item");

      // Obsługa wyboru przystanku
      listItem.addEventListener("click", function () {
        inputElement.value = busStop.name;
        busStopListContainer.remove();
      });

      busStopListContainer.appendChild(listItem);
    });
  }
}

// Obsługa zamykania listy po kliknięciu poza nią
document.addEventListener("click", function (event) {
  var busStopListContainer = document.getElementById("bus-stop-list-container");
  var targetElement = event.target;

  if (busStopListContainer && !busStopListContainer.contains(targetElement)) {
    busStopListContainer.remove();
  }
});

var apiUrlUser = apiUrl + 'user/'; // Użyj wartości apiUrl zdefiniowanej w bloku skryptu

function getMaxTravelerId() {
  var apiUrlTraveler = apiUrl + 'Traveler/'; // Użyj wartości apiUrl zdefiniowanej w bloku skryptu

  return fetch(apiUrlTraveler)
    .then(response => response.json())
    .then(data => {
      var maxId = 0;
      data.forEach(record => {
        var recordId = parseInt(record.id_traveler);
        if (recordId > maxId) {
          maxId = recordId;
        }
      });
      return maxId + 1;
    })
    .catch(error => {
      console.error("Błąd pobierania maksymalnego ID z tabeli 'Traveler':", error);
    });
}


// Obsługa zamówienia przejazdu
function orderRide() {
    event.preventDefault(); // Zapobieganie domyślnej akcji formularza
  var departureTime = document.getElementById('departure_time').value;
  var departureDate = new Date(departureTime);
  var stopDate = new Date(departureDate.getTime() + 10 * 60000);
  var stopTime = stopDate.toISOString();

  var startInput = document.getElementById('start-input');
  var endInput = document.getElementById('end-input');

  // Pobierz wybrane przystanki
  var startBusStop = selectedBusStops.find(busStop => busStop.name === startInput.value);
  var endBusStop = selectedBusStops.find(busStop => busStop.name === endInput.value);

  console.log("startBusStop:", startBusStop.id_bus_stop);
  console.log("endBusStop:", endBusStop.id_bus_stop);

  var userApiUrl = apiUrlUser + getUserID() + '/Client/'; // Utwórz pełny adres URL API

  fetch(userApiUrl)
    .then(response => response.json())
    .then(data => {
      var clientId = data[0].id_client; // Pobierz ID klienta zwrócone przez API
      console.log(data[0].id_client);
      console.log(clientId);

      getMaxTravelerId() // Pobierz maksymalne ID podróżnika
        .then(newTravelerId => {
          var newTravelerRecord = {
            id_traveler: newTravelerId,
            start_time: departureTime,
            stop_time: stopTime,
            client_id_client: clientId, // Użyj pobranego ID klienta
            id_bus_stop_start: startBusStop.id_bus_stop, // Pobierz id przystanku początkowego
            id_bus_stop_end: endBusStop.id_bus_stop // Pobierz id przystanku końcowego
          };

          // Wyślij żądanie API, aby dodać rekord do tabeli "traveler"
          fetch(apiTravelerUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(newTravelerRecord)
          })
            .then(response => response.json())
            .then(data => {
              // Rekord został dodany pomyślnie
              console.log("Rekord został dodany do tabeli 'traveler'.", data);
            })
            .catch(error => {
              console.error("Błąd dodawania rekordu do tabeli 'traveler':", error);
            });
        })
        .catch(error => {
          console.error("Błąd pobierania maksymalnego ID podróżnika:", error);
        });
    })
    .catch(error => {
      console.error("Błąd pobierania danych klienta:", error);
    });
      setTimeout(function() {
      location.reload(); // Odśwież stronę po zakończeniu działań
    }, 2000); // 2000 ms = 2 sekundy (zmień wartość na odpowiednią dla Twoich potrzeb)
}



