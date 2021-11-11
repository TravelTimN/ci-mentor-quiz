/* jshint esversion: 8 */

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("preloader").style.opacity = 0;
    setTimeout(() => {
        document.getElementById("preloader").remove();
    }, 1000);
});

// update copyright year
document.getElementById("year").innerText = new Date().getFullYear();
