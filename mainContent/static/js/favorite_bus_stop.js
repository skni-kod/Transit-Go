
        function dodajPrzystanek() {
            var nazwaPrzystanku = document.getElementById("nazwa_przystanku").value;

            if (nazwaPrzystanku.trim() === "") {
                alert("Wprowadź nazwę przystanku.");
                return;
            }

            var tripContent = document.getElementById("trip_content");

            var div = document.createElement("div");
            div.className = "trip_info";

            var favBusStop = document.createElement("div");
            favBusStop.className = "Fav_BusStop";
            favBusStop.textContent = nazwaPrzystanku;

            var link = document.createElement("a");
            link.href = "";
            link.className = "Idz_pieszo";
            link.textContent = "Idź do przystanku";

            div.appendChild(favBusStop);
            div.appendChild(link);

            tripContent.querySelector("#Bus_container").appendChild(div);

            document.getElementById("nazwa_przystanku").value = "";
        }
