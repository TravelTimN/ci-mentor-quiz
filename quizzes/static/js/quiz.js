/* jshint esversion: 8 */

const dataUrl = window.location.href;
const quizStartBtn = document.getElementById("quiz-start-btn");
const quizSubmitBtn = document.getElementById("quiz-submit-btn");
const quizForm = document.getElementById("quiz-form");
const csrfToken = document.getElementsByName("csrfmiddlewaretoken");
let quizContainer = document.getElementById("quiz-container");
let time = 0;
let timeInterval;


quizStartBtn.addEventListener("click", function() {
    this.classList.add("hide", "full");
    quizForm.classList.remove("hide");
    
    timeInterval = setInterval(setTime, 1000);
});


function setTime() {
  ++time;
  console.log(time);
}


fetch(`${dataUrl}data/`)
    .then(response => response.json())
    .then(data => {
        // console.log(data);

        Object.entries(data).forEach(entry => {
            const [, value] = entry;
            Object.entries(value).forEach(item => {
                const [, val] = item;
                // display the "Question"
                quizContainer.innerHTML += `
                    <hr>
                    <p>${val.question}</p>
                `;
                // TODO: possibly shuffle the various choices? how will this affect comparing answers from DB choices?
                // loop through the question "Choices"
                val.choices.forEach((choice, i) => {
                    i++;
                    switch (val.type) {
                        case "radio":
                            quizContainer.innerHTML += `
                                <p>
                                <input type="radio" id="q${val.id}-${i}" name="q${val.id}" class="choice" value="${choice}" required>
                                <label for="q${val.id}-${i}" class="">${choice}</label>
                                </p>
                            `;
                            break;
                        case "checkbox":
                            quizContainer.innerHTML += `
                                <p>
                                <input type="checkbox" id="q${val.id}-${i}" name="q${val.id}" class="choice" value="${choice}">
                                <label for="q${val.id}-${i}" class=""> - ${choice}</label>
                                </p>
                            `;
                            break;
                        case "textarea":
                            quizContainer.innerHTML += `
                                <p>
                                <textarea id="q${val.id}-${i}" name="q${val.id}" class="choice" required></textarea>
                                </p>
                            `;
                            break;
                        case "number":
                            quizContainer.innerHTML += `
                                <p>
                                <input type="number" id="q${val.id}-${i}" name="q${val.id}" class="choice" required>
                                </p>
                            `;
                            break;
                        case "url":
                            quizContainer.innerHTML += `
                                <p>
                                <input type="url" id="q${val.id}-${i}" name="q${val.id}" class="choice" required>
                                </p>
                            `;
                            break;
                        default:
                            quizContainer.innerHTML += `
                                <p>
                                <input type="text" id="q${val.id}-${i}" name="q${val.id}" class="choice" required>
                                </p>
                            `;
                            break;
                    }
                });
            });
        });
    })
    .catch(error => {
        console.log(error);
    });


function saveQuizResults() {
    const userAnswers = {};
    const choices = document.querySelectorAll(".choice");
    // userAnswers["csrfmiddlewaretoken"] = csrfToken[0].value; // TODO: remove this - no longer needed???
    choices.forEach(choice => {
        // storing "choice.name" value to userAnswers dict
        // must cast as Array() for the fetch data to match on DB
        switch (choice.type) {
            case "radio":
                if (choice.checked) {
                    // if radio is checked
                    userAnswers[choice.name] = Array(choice.value);
                } else {
                    if (!userAnswers[choice.name]) {
                        // field not checked, user left if blank
                        userAnswers[choice.name] = null;
                    }
                }
                break;
            case "checkbox":
            // checkbox needs to be an array, to handle multiple values
                if (choice.checked) {
                    // if checkbox is checked
                    if (!userAnswers[choice.name]) {
                        // if no existing options are checked
                        userAnswers[choice.name] = Array(choice.value);
                    } else {
                        // additional options are also checked
                        userAnswers[choice.name].push(choice.value);
                    }
                } else {
                    if (!userAnswers[choice.name]) {
                        // field not checked, user left if blank
                        userAnswers[choice.name] = null;
                    }
                }
                break;
            case "textarea":
            case "number":
            case "url":
            case "text":
                if (choice.value) {
                    // grab the user's value
                    userAnswers[choice.name] = Array(choice.value);
                } else {
                    if (!userAnswers[choice.name]) {
                        // field not checked, user left if blank
                        userAnswers[choice.name] = null;
                    }
                }
                break;
            default:
                // TODO: what needs to be the default here?
                break;
        }
    });
    // add the total duration of 'time'
    userAnswers["duration"] = time;

    // https://docs.djangoproject.com/en/3.2/ref/csrf/#setting-the-token-on-the-ajax-request
    const request = new Request(
        `${dataUrl}save/`,
        {headers: {"X-CSRFToken": csrfToken[0].value}}
    );

    fetch(request, {
        method: "POST",
        body: JSON.stringify(userAnswers),
        mode: "same-origin",
        })
        .then(response => response.json())
        .then(data => {
            // console.log(data); // JsonResponse({}) from views.py
            const results = data.results;
            console.log(results);
        })
        .catch(error => {
            console.log(error);
        });
}

quizForm.addEventListener("submit", function(e) {
    e.preventDefault();
    clearInterval(timeInterval);
    quizForm.classList.add("hide", "full");
    document.getElementById("thank-you").classList.remove("hide", "full");
    saveQuizResults();
});
