/* ==========================================
   RAPIDCARE JAVASCRIPT
   ========================================== */


/* ==========================================
   MOBILE MENU
   ========================================== */

function toggleMenu() {

    var nav = document.querySelector(".nav-links");

    if (nav) {

        nav.classList.toggle("mobile-open");

    }

}


/* ==========================================
   GPS LOCATION
   ========================================== */

function getLocation() {

    var status =
        document.getElementById("location-status");

    var latitude =
        document.getElementById("latitude");

    var longitude =
        document.getElementById("longitude");


    if (!navigator.geolocation) {

        status.textContent =
            "GPS is not supported by this browser.";

        return;

    }


    status.textContent =
        "Detecting your location...";


    navigator.geolocation.getCurrentPosition(

        function(position) {

            var lat =
                position.coords.latitude;

            var lon =
                position.coords.longitude;


            latitude.value = lat;

            longitude.value = lon;


            status.textContent =
                "Location detected successfully.";


            status.classList.add("location-success");

        },


        function(error) {

            if (error.code === 1) {

                status.textContent =
                    "Location permission was denied.";

            }

            else {

                status.textContent =
                    "Unable to detect location.";

            }

        }

    );

}


/* ==========================================
   SCORE PROGRESS BARS
   ========================================== */

document.addEventListener(
    "DOMContentLoaded",
    function() {


        var bars =
            document.querySelectorAll(
                ".progress-fill"
            );


        bars.forEach(

            function(bar) {

                var score =
                    bar.getAttribute(
                        "data-score"
                    );


                if (score) {

                    setTimeout(

                        function() {

                            bar.style.width =
                                score + "%";

                        },

                        200

                    );

                }

            }

        );


        /* ======================================
           SCROLL ANIMATION
           ====================================== */

        var animatedElements =
            document.querySelectorAll(
                ".feature-card, .hospital-card, .analysis-card, .kpi-card"
            );


        var observer =
            new IntersectionObserver(

                function(entries) {

                    entries.forEach(

                        function(entry) {

                            if (entry.isIntersecting) {

                                entry.target.classList.add(
                                    "visible"
                                );

                            }

                        }

                    );

                },

                {
                    threshold: 0.1
                }

            );


        animatedElements.forEach(

            function(element) {

                observer.observe(element);

            }

        );


    }
);