/* jshint esversion: 11 */

document.addEventListener("DOMContentLoaded", function () {
    // on page load, hide the preloader animation
    document.getElementById("preloader").style.opacity = 0;
    setTimeout(() => {
        document.getElementById("preloader").remove();
    }, 1000);
});

// update copyright year
document.getElementById("year").innerText = new Date().getFullYear();

// show navbar menu on hover instead of default "click" events
let navDropdown = document.querySelector(".dropdown");
let navDropdownToggle = document.querySelector(".dropdown-toggle");
let navDropdownMenu = document.querySelector(".dropdown-menu");
navDropdown.addEventListener("mouseenter", function() {
    navDropdownToggle.classList.add("show");
    navDropdownMenu.classList.add("show");
    // required for bootstrap styles to function 100%
    navDropdownToggle.setAttribute("aria-expanded", "true");
    navDropdownMenu.setAttribute("data-bs-popper", "none");
});
navDropdown.addEventListener("mouseleave", function() {
    navDropdownToggle.classList.remove("show");
    navDropdownMenu.classList.remove("show");
    // must be removed for bootstrap to fully function
    navDropdownToggle.setAttribute("aria-expanded", "false");
    navDropdownMenu.removeAttribute("data-bs-popper");
});

// auto-hide alerts
const alerts = document.querySelectorAll("aside.alert");
let overlay = document.getElementById("overlay");
if (alerts.length > 0) {
    // only if any alerts found on DOM
    overlay?.classList.remove("hide");
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
            // remove the overlay background
            setTimeout(() => {
                overlay?.classList.add("hide");
            }, 500);
        }, 2500);
    }
}

// tooltips
let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// disable first item from all <select> elements
$("select").each(function() {
    $(this).children("option:first").prop("disabled", true);
});
