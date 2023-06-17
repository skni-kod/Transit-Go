/*Pojawianie aside dla przejazdów*/
var asideVisible = false;
function showAside() {
  var aside = document.getElementById("Hidden_content");
  if (asideVisible) {
    aside.style.display = "none";
    asideVisible = false;
  } else {
    aside.style.display = "flex";
    asideVisible = true;
  }
}

/*Pojawianie aside dla powiadomiennajbliższych przystanków*/
function showClosestBusStop() {
  var aside = document.getElementById("Hidden_BusStop");
  if (asideVisible) {
    aside.style.display = "none";
    asideVisible = false;
  } else {
    aside.style.display = "flex";
    asideVisible = true;
  }
}

/*Pojawianie aside dla powiadomien*/
var asideVisibleNot = false;
var blinkAnimation;
var displayedNotifications = [];

function showAsideNotifications() {
  var aside = document.getElementById("Hidden_notifications");
  var icon = document.getElementById("Bell");

  if (asideVisibleNot) {
    aside.style.display = "none";
    asideVisibleNot = false;
    clearInterval(blinkAnimation);
    icon.style.backgroundColor = "";
  } else {
    aside.style.display = "flex";
    asideVisibleNot = true;
    icon.style.animation = "none";
    void icon.offsetWidth;
    icon.style.animation = "blink 1.5s infinite";
    stopBlinking();
  }
}

function startBlinking() {
  blinkAnimation = setInterval(blinkBackground, 500);
}

function stopBlinking() {
  clearInterval(blinkAnimation);
  var icon = document.getElementById("Bell");
  icon.style.backgroundColor = "#fff";
  icon.classList.remove("notification-active");
  icon.style.borderRadius = "50%"; // Dodaj stylowanie okręgu
}

function blinkBackground() {
  var icon = document.getElementById("Bell");
  var backgroundColor = window.getComputedStyle(icon).backgroundColor;

  if (backgroundColor === "rgb(255, 255, 255)") {
    icon.style.backgroundColor = "#f18b8b";
    icon.classList.add("notification-active");
    icon.style.borderRadius = "50%"; // Dodaj stylowanie okręgu
  } else {
    icon.style.backgroundColor = "#fff";
    icon.classList.remove("notification-active");
    icon.style.borderRadius = "50%"; // Dodaj stylowanie okręgu
  }
}

/*Funkcja dodająca powiadomienia*/
function checkTime() {
    console.log("check time wywołane");
    var apiUrl = window.apiUrl + 'user/';  // Użyj wartości apiUrl zdefiniowanej w bloku skryptu
    var userId = getUserID(); // Pobierz identyfikator użytkownika zalogowanego
    var userApiUrl = apiUrl + userId + '/traveler/'; // Utwórz pełny adres URL API

    fetch(userApiUrl)
        .then(response => response.json())
        .then(data => {
            // Przetwarzaj dane przejazdów
            var notificationsContainer = document.createElement("div");
            notificationsContainer.className = "notification-container";

            data.forEach(traveler => {
                var startTime = new Date(traveler.start_time);
                startTime.setHours(startTime.getHours() + 2); // Dodaj dwie godziny do czasu
                var currentTime = new Date(); // Pobierz aktualny czas
                var timeDiff = startTime.getTime() - currentTime.getTime(); // Oblicz różnicę czasu w milisekundach
                var minutesDiff = Math.round(timeDiff / (1000 * 60)); // Konwertuj różnicę na minuty

                if (minutesDiff <= 10 && startTime > currentTime) { // Wyświetl tylko przejazdy, do których pozostało 10 minut lub mniej i czas odjazdu jest późniejszy niż aktualny czas
                    var formattedTime = startTime.toLocaleTimeString('pl-PL', { timeZone: 'Europe/Warsaw', hour: '2-digit', minute: '2-digit' });
                    var hour = startTime.getHours();
                    var minutes = startTime.getMinutes();
                    var notification = document.createElement("div");
                    notification.className = "notification";
                    var link = document.createElement("a");
                    link.href = "#"; // Ustaw odpowiedni link, jeśli jest dostępny
                    link.innerText = "Twój przejazd odbywa się o godzinie " + formattedTime;
                    link.className = "notification-link"; // Dodaj klasę dla linku
                    notification.appendChild(link);
                    notificationsContainer.appendChild(notification);

                      // Sprawdź, czy powiadomienie już zostało wyświetlone
                      if (!displayedNotifications.includes(traveler.id)) {
                        displayedNotifications.push(traveler.id); // Dodaj identyfikator powiadomienia do tablicy displayedNotifications
                        startBlinking(); // Uruchom funkcję startBlinking() tylko dla nowych powiadomień
                      }
                }
            });

            var hiddenNotifications = document.getElementById("Hidden_notifications");
            hiddenNotifications.innerHTML = "";
            hiddenNotifications.appendChild(notificationsContainer);
            hiddenNotifications.classList.add("notification-container"); // Dodaj klasę dla kontenera powiadomień
        })
        .catch(error => console.error(error));
}


// Funkcja do pobrania identyfikatora użytkownika zalogowanego
function getUserID() {
    console.log("getUser wywołane");
    var userDataElement = document.getElementById("user-data");
    var userID = userDataElement.dataset.userId;
    console.log("ID użytkownika: " + userID);

    return userID;
}

  function toggleRadio(id) {
    var radio = document.getElementById(id);
    radio.checked = !radio.checked;
  }
