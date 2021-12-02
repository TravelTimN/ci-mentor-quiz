/* jshint esversion: 8 */

document.addEventListener("DOMContentLoaded", function () {
    // on page load, hide the preloader animation
    document.getElementById("preloader").style.opacity = 0;
    setTimeout(() => {
        document.getElementById("preloader").remove();
    }, 1000);
});

// update copyright year
document.getElementById("year").innerText = new Date().getFullYear();

// auto-hide alerts
const alerts = document.querySelectorAll("aside.alert");
if (alerts.length > 0) {
    // only if any alerts found on DOM
    for (let i = 0; i < alerts.length; i++) {
        setTimeout(() => {
            // start after 2500ms
            setTimeout(() => {
                // slight delay between each alert
                alerts[i].classList.add("alert-slide");
                setTimeout(() => {
                    // remove from DOM entirely
                    alerts[i].style.display = "none";
                }, 1000);
            }, i * 100);
        }, 2500);
    }
}
