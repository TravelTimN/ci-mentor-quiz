/* jshint esversion: 8 */

const dataUrl = window.location.href;
const quizSubmitBtn = document.getElementById("quiz-submit-btn");
let quizContainer = document.getElementById("quiz-container");

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

const quizForm = document.getElementById("quiz-form");
const csrfToken = document.getElementsByName("csrfmiddlewaretoken");

function saveQuizResults() {
    const userAnswers = {};
    const choices = document.querySelectorAll(".choice");
    // userAnswers["csrfmiddlewaretoken"] = csrfToken[0].value; // TODO: remove this - no longer needed???
    choices.forEach(choice => {
        switch (choice.type) {
            case "radio":
            case "checkbox":
                if (choice.checked) {
                    // store 'name' key as the value of the question_type from user
                    userAnswers[choice.name] = choice.value;
                } else {
                    if (!userAnswers[choice.name]) {
                        // if 'name' key not available, this question hasn't been answered
                        userAnswers[choice.name] = null;
                    }
                }
                break;
            case "textarea":
            case "number":
            case "url":
            case "text":
                if (choice.value) {
                    // store 'name' key as the value of the question_type from user
                    userAnswers[choice.name] = choice.value;
                } else {
                    if (!userAnswers[choice.name]) {
                        // if 'name' key not available, this question hasn't been answered
                        userAnswers[choice.name] = null;
                    }
                }
                break;
            default:
                break;
        }
    });

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
            console.log(data);
            console.log(userAnswers);
        })
        .catch(error => {
            console.log(error);
        });
}

quizForm.addEventListener("submit", function(e) {
    e.preventDefault();
    saveQuizResults();
});
