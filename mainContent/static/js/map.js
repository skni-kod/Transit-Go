
var vectorSource = new ol.source.Vector();
var myLocationLon = null;
var myLocationLat = null;

var vectorLayer = new ol.layer.Vector({
  source: vectorSource,
  style: new ol.style.Style({
    image: new ol.style.Circle({
      radius: 8,
      fill: new ol.style.Fill({
        color: '#466199'
      }),
      stroke: new ol.style.Stroke({
        color: 'white',
        width: 2
      })
    })
  })
});

var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
    vectorLayer
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([21.9333, 50.0413]), // Centrum Rzeszowa
    zoom: 13
  })
});

var displayedBusStops = 12; // Liczba początkowo wyświetlanych przystanków
var busStopList = document.getElementById('bus-stops');
var start = 0; // Indeks pierwszego przystanku do wyświetlenia

var apiBusStopUrl = apiUrl + 'BusStop/';

fetch(apiBusStopUrl)
  .then(response => response.json())
  .then(data => {
    // Wylicz odległość dla każdego przystanku
    var promises = data.map(busStop => calculateDistance(busStop.gps_n, busStop.gps_e));
    Promise.all(promises)
      .then(distances => {
        // Połącz odległości z danymi przystanków
        data.forEach((busStop, index) => {
          busStop.distance = distances[index];
        });

        // Sortuj przystanki od najbliższego do najdalszego
        data.sort(function(a, b) {
          return a.distance - b.distance;
        });

        // Dodaj markery przystanków na mapę
        data.forEach(busStop => {
          var marker = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([busStop.gps_e, busStop.gps_n])),
            name: busStop.name
          });

          var iconStyle = new ol.style.Style({
            image: new ol.style.Circle({
              radius: 5,
              fill: new ol.style.Fill({
                color: 'white'
              }),
              stroke: new ol.style.Stroke({
                color: '#5264AE',
                width: 4
              })
            })
          });

          marker.setStyle(iconStyle);
          vectorSource.addFeature(marker);
        });

        // Wyświetl listę przystanków
        updateBusStopList();

function updateBusStopList() {
  busStopList.innerHTML = ''; // Wyczyść listę przystanków

  // Wybierz fragment przystanków do wyświetlenia
  var selectedBusStops = data.slice(start, start + displayedBusStops);

  selectedBusStops.forEach(busStop => {
    var busStopName = busStop.name;
    var busStopDistance = busStop.distance.toFixed(2); // Zaokrąglenie do dwóch miejsc po przecinku

    // Tworzenie elementów HTML dla przystanku
    var listItem = document.createElement("div");
    var busStopInfo = document.createElement("div");
    var busStopNameContainer = document.createElement("span");
    var busStopDistanceContainer = document.createElement("span");
    var busStopButton = document.createElement("button");

    listItem.classList.add("bus-stop-item");
    busStopInfo.classList.add("bus-stop-info");
    busStopNameContainer.classList.add("bus-stop-name");
    busStopDistanceContainer.classList.add("bus-stop-distance");
    busStopButton.classList.add("bus-stop-button");

    // Ustawienie treści i stylizacji dla elementów HTML
    busStopNameContainer.textContent = busStopName;
    busStopDistanceContainer.textContent = '(Odległość: ' + busStopDistance + ' km)';
    busStopButton.textContent = 'Wyznacz trasę';
    busStopButton.setAttribute("data-busstop", JSON.stringify(busStop));
    busStopButton.addEventListener("click", function() {
      calculateRouteToBusStop(this);
    });

    // Dodanie elementów do przystanku
    busStopInfo.appendChild(busStopNameContainer);
    busStopInfo.appendChild(busStopDistanceContainer);
    listItem.appendChild(busStopInfo);
    listItem.appendChild(busStopButton);

    // Dodanie przystanku do listy
    busStopList.appendChild(listItem);
  });
}


      })
      .catch(function(error) {
        console.log('Błąd podczas obliczania odległości: ' + error.message);
      });
});

// Monitoruj lokalizację użytkownika
let myLocationPoint; // Przeniesiona deklaracja na początek skryptu

navigator.geolocation.watchPosition(function(position) {
  myLocationLon = position.coords.longitude;
  myLocationLat = position.coords.latitude;
  updateMyLocationPoint();
});

function updateMyLocationPoint() {
  if (myLocationLon && myLocationLat) {
    var lon = myLocationLon;
    var lat = myLocationLat;

    if (myLocationPoint) {
      vectorSource.removeFeature(myLocationPoint); // Usuń poprzedni myLocationPoint
      myLocationPoint.getGeometry().setCoordinates(ol.proj.fromLonLat([lon, lat]));
    } else {
      myLocationPoint = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
      });
    }

    vectorSource.addFeature(myLocationPoint); // Dodaj nowy myLocationPoint
  }
}


// Funkcja do obliczania trasy
function calculateRouteToBusStop(button) {
  var busStop = JSON.parse(decodeURIComponent(button.getAttribute('data-busstop')));
  console.log('Funkcja calculateRouteToBusStop() została wywołana.');

  if (myLocationLon && myLocationLat) {
    var lon = myLocationLon;
    var lat = myLocationLat;

    var busStopLon = busStop.gps_e;
    var busStopLat = busStop.gps_n;

    var url = `https://api.openrouteservice.org/v2/directions/foot-walking?api_key=5b3ce3597851110001cf6248de4d1c6590404065ae8661b1571f13ff&start=${lon},${lat}&end=${busStopLon},${busStopLat}`;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        var routeCoordinates = data.features[0].geometry.coordinates;
        var routePoints = routeCoordinates.map(coord => ol.proj.transform(coord, 'EPSG:4326', 'EPSG:3857'));

        var routeFeature = new ol.Feature({
          geometry: new ol.geom.LineString(routePoints),
          name: 'route'
        });

        //Styl trasy ciągły
/*        var routeStyle = new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: '#13a0f1',
            width: 4
          })
        });*/

        var routeStyle = new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: '#369400',
            width: 4,
            lineDash: [6, 6] // Definiuje przerywany wzór [długość-segmentu, długość-przerwy]
          })
        });

        routeFeature.setStyle(routeStyle);
        vectorSource.addFeature(routeFeature);

        var routeExtent = routeFeature.getGeometry().getExtent();
        map.getView().fit(routeExtent, { padding: [50, 50, 50, 50] });
      });
  }
}

// Tworzenie pustego cache
var distanceCache = new Map();

// Funkcja do obliczania odległości między dwoma punktami
function calculateDistance(lat, lon) {
  return new Promise(function(resolve, reject) {
    // Sprawdź, czy odległość jest już w cache
    var cacheKey = lat + ',' + lon;
    if (distanceCache.has(cacheKey)) {
      resolve(distanceCache.get(cacheKey));
    } else {
      navigator.geolocation.getCurrentPosition(function(position) {
        var lat1 = position.coords.latitude;
        var lon1 = position.coords.longitude;

        // Konwersja na radiany
        var latRad1 = degToRad(lat1);
        var lonRad1 = degToRad(lon1);
        var latRad2 = degToRad(lat);
        var lonRad2 = degToRad(lon);

        // Różnice pomiędzy współrzędnymi
        var latDiff = latRad2 - latRad1;
        var lonDiff = lonRad2 - lonRad1;

        // Promień Ziemi w kilometrach
        var earthRadius = 6371;

        // Obliczanie odległości przy użyciu wzoru Haversine
        var a =
          Math.sin(latDiff / 2) * Math.sin(latDiff / 2) +
          Math.cos(latRad1) * Math.cos(latRad2) *
          Math.sin(lonDiff / 2) * Math.sin(lonDiff / 2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        var distance = earthRadius * c;

        // Zapisz odległość w cache
        distanceCache.set(cacheKey, distance);

        resolve(distance);
      }, function(error) {
        reject(error);
      });
    }
  });
}

function degToRad(degrees) {
  return degrees * (Math.PI / 180);
}

function clearRoute() {
  // Usuń trasę samochodową
  var featuresToRemove = [];
  vectorSource.forEachFeature(function(feature) {
    var featureName = feature.get('name');
    if (featureName && featureName === 'route') {
      featuresToRemove.push(feature);
    }
  });

  featuresToRemove.forEach(function(feature) {
    vectorSource.removeFeature(feature);
  });

  // Przywróć widok mapy do pierwotnego stanu
  var initialView = map.getView();
  map.setView(initialView);
}


