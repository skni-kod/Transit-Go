function showTravel() {
  var apiUrl = "http://127.0.0.1:8000/api/user/4/traveler/50/";

  // Wywołaj żądanie HTTP dla pobrania danych JSON
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      // Pobierz id_bus_stop_start i id_bus_stop_end z danych JSON
      var idStart = data.id_bus_stop_start;
      var idEnd = data.id_bus_stop_end;

      // Pobierz start_time z danych JSON
      var startTime = data.start_time;

      // Porównaj start_time z aktualnym czasem
      var currentTime = new Date();
      var startTimeDiff = new Date(startTime) - currentTime;

      if (startTimeDiff > 0) {
        console.log("Autobus przyjedzie za:", startTimeDiff / 1000, "sekund");
      } else {
        console.log("Autobus jest już w drodze");
      }

      // Zbuduj URL dla pobrania danych pierwszego przystanku
      var busStopUrl1 = "http://127.0.0.1:8000/api/BusStop/" + idStart + "/";

      // Zbuduj URL dla pobrania danych drugiego przystanku
      var busStopUrl2 = "http://127.0.0.1:8000/api/BusStop/" + idEnd + "/";

      // Wywołaj żądania HTTP dla pobrania danych przystanków
      Promise.all([fetch(busStopUrl1), fetch(busStopUrl2)])
        .then(responses => Promise.all(responses.map(response => response.json())))
        .then(busStopData => {
          // Pobierz gps_n i gps_e dla pierwszego przystanku
          var gpsN1 = busStopData[0].gps_n.toString();
          var gpsE1 = busStopData[0].gps_e.toString();

          // Pobierz gps_n i gps_e dla drugiego przystanku
          var gpsN2 = busStopData[1].gps_n.toString();
          var gpsE2 = busStopData[1].gps_e.toString();

          // Wyświetl wyniki w konsoli
          console.log("Lokalizacja pierwszego przystanku:");
          console.log("gps_n:", gpsN1);
          console.log("gps_e:", gpsE1);

          console.log("Lokalizacja drugiego przystanku:");
          console.log("gps_n:", gpsN2);
          console.log("gps_e:", gpsE2);

          // Wywołaj funkcję do obliczania trasy
          calculateRouteForBusStops(gpsN1, gpsE1, gpsN2, gpsE2);
        })
        .catch(error => {
          console.error("Wystąpił błąd:", error);
        });
    })
    .catch(error => {
      console.error("Wystąpił błąd:", error);
    });
}

// Pozostała część kodu bez zmian
function calculateRouteForBusStops(gpsN1, gpsE1, gpsN2, gpsE2) {
  var url = `https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248de4d1c6590404065ae8661b1571f13ff&start=${gpsE1},${gpsN1}&end=${gpsE2},${gpsN2}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      var routeCoordinates = data.features[0].geometry.coordinates;
      var routePoints = routeCoordinates.map(coord => ol.proj.transform(coord, 'EPSG:4326', 'EPSG:3857'));

      var routeFeature = new ol.Feature({
        geometry: new ol.geom.LineString(routePoints),
        name: 'route'
      });

        var routeStyle = new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: '#ef0505',
            width: 4
          })
        });

      routeFeature.setStyle(routeStyle);
      vectorSource.addFeature(routeFeature);

      var routeExtent = routeFeature.getGeometry().getExtent();
      map.getView().fit(routeExtent, { padding: [50, 50, 50, 50] });
    })
    .catch(error => {
      console.error("Wystąpił błąd:", error);
    });
}