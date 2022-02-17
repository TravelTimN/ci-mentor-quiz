/* jshint esversion: 8 */

// const dataUrl = window.location.href;
const quizStartBtn = document.getElementById("quiz-start-btn");
const quizSubmitBtn = document.getElementById("quiz-submit-btn");
const quizForm = document.getElementById("quiz-form");
// const csrfToken = document.getElementsByName("csrfmiddlewaretoken");
const duration = document.getElementById("duration");
// let quizContainer = document.getElementById("quiz-container");
let durationTime = 0;
let durationInterval;
let timeTaken = 0;
let timeTakenInterval;


function setDurationTime() {
    // increment the quiz duration timer
    ++durationTime;
    duration.value = durationTime;
}


function setTimeTaken(qID) {
    // increment the specific question time taken
    ++timeTaken;
    let currentQuestionTimeTaken = document.querySelector(`[id^='time_taken-${qID}']`);
    currentQuestionTimeTaken.value = timeTaken;
}


// start the quiz and the timers
quizStartBtn.addEventListener("click", function() {
    document.getElementById("quiz-start-row").classList.add("hide", "full");
    quizForm.classList.remove("hide", "full");

    // start the duration interval (total length of quiz)
    durationInterval = setInterval(setDurationTime, 1000);
    // grab first question's ID, and start individual question timer
    let firstQuestionId = document.querySelector("[id^='card-set-1'] input").name.replace("time_taken-", "");
    timeTakenInterval = setInterval(function() {setTimeTaken(firstQuestionId)}, 1000);
});


// (fixes GitHub Issue #4) - prevent the "Enter" key from submitting the form
let lastQuestion = document.querySelector("[id^='card-set-'][id$='-last'] .choice");
quizForm.addEventListener("keypress", (e) => {
    // https://stackoverflow.com/a/47266106
    if (document.activeElement == lastQuestion && e.key == "Enter") {
        e.preventDefault();
    }
});


// confirm if any 'clicked' checkbox is :checked, then remove sibling 'required' attributes
let checkboxes = document.querySelectorAll(".checkbox-validation input[type=checkbox]");
checkboxes.forEach(checkbox => {
    // click event listener
    checkbox.addEventListener("click", function() {
        let checkboxQnum = this.dataset.validator;
        // grab only 'this' sibling's checkboxes
        let checkboxSiblings = document.querySelectorAll(`[data-validator="${checkboxQnum}"]`);
        let checkboxChoices = [];
        // loop each sibling - push true/false to array if :checked or not
        checkboxSiblings.forEach(sibling => {
            checkboxChoices.push(sibling.checked);
        });
        if (checkboxChoices.includes(true)) {
            // does array contain 'true' at all?
            checkboxSiblings.forEach(sibling => {
                // remove all sibling's 'required' attributes
                sibling.required = false;
            });
        } else {
            // array does not contain any instance of 'true'
            checkboxSiblings.forEach(sibling => {
                // loop sibling and add 'required' attributes to all
                sibling.required = true;
            });
        }
    });
});


// grab the next question in sequence
const nextBtns = document.querySelectorAll("[id^='next-btn-']");
nextBtns.forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault();
        let btnNum = this.id.replace("next-btn-", "");
        // only proceed if validated properly
        if (validateQuestion(btnNum)) {
            getNextBtn(btnNum);
        }
    });
});


// validate the final question of the quiz using the submit-btn dataset
quizSubmitBtn.addEventListener("click", function (e) {
    e.preventDefault();
    let btnNum = this.dataset.submit;
    // only proceed if validated properly
    if (validateQuestion(btnNum)) {
        quizForm.submit();
    }
});


function validateQuestion(btnNum) {
    // check if user input an answer in order to proceed
    let dataValidator = document.querySelector(`[data-validator="${btnNum}"]`);

    if (dataValidator.checkValidity()) {
        return true
    } else {
        dataValidator?.focus(); // set autofocus back onto the element
        document.getElementById(`error-handler-${btnNum}`).innerHTML = "* this question is required";
    }
}


function getNextBtn(btnNum) {
    // clear previous question time_taken interval and reset back to 0
    clearInterval(timeTakenInterval);
    timeTaken = 0;

    // hide the current question's card-set and next-btn
    let getCard = document.getElementById(`card-set-${btnNum}`);
    getCard?.classList.add("hide", "full");
    document.getElementById(`card-next-btn-${btnNum}`).classList.add("hide", "full");

    // un-hide the next question's card-set and next-btn
    let nextNum = parseInt(btnNum) + 1;
    let getNextCard = document.querySelector(`[id^='card-set-${nextNum}'`);
    getNextCard?.classList.remove("hide", "full");
    let cardNextBtn = document.getElementById(`card-next-btn-${nextNum}`);
    cardNextBtn?.classList.remove("hide", "full");

    // start the time_taken interval counter
    let getQuestionId = document.querySelector(`[id^='card-set-${nextNum}'] input`).name.replace("time_taken-", "");
    timeTakenInterval = setInterval(function() {setTimeTaken(getQuestionId)}, 1000);

    // autofocus the next textarea if applicable
    let getNextInput = getNextCard.querySelector("textarea");
    getNextInput?.focus();
}


// fetch(`${dataUrl}data/`)
//     .then(response => response.json())
//     .then(data => {
//         // console.log(data);

//         Object.entries(data).forEach(entry => {
//             const [, value] = entry;
//             Object.entries(value).forEach(item => {
//                 const [, val] = item;
//                 // display the "Question"
//                 quizContainer.innerHTML += `
//                     <hr>
//                     <p>${val.question}</p>
//                 `;
//                 // TODO: possibly shuffle the various choices? how will this affect comparing answers from DB choices?
//                 // loop through the question "Choices"
//                 val.choices.forEach((choice, i) => {
//                     i++;
//                     switch (val.type) {
//                         case "radio":
//                             quizContainer.innerHTML += `
//                                 <p>
//                                 <input type="radio" id="q${val.id}-${i}" name="q${val.id}" class="choice" value="${choice}" required>
//                                 <label for="q${val.id}-${i}" class="">${choice}</label>
//                                 </p>
//                             `;
//                             break;
//                         case "checkbox":
//                             quizContainer.innerHTML += `
//                                 <p>
//                                 <input type="checkbox" id="q${val.id}-${i}" name="q${val.id}" class="choice" value="${choice}">
//                                 <label for="q${val.id}-${i}" class=""> - ${choice}</label>
//                                 </p>
//                             `;
//                             break;
//                         case "textarea":
//                             quizContainer.innerHTML += `
//                                 <p>
//                                 <textarea id="q${val.id}-${i}" name="q${val.id}" class="choice" required></textarea>
//                                 </p>
//                             `;
//                             break;
//                         case "number":
//                             quizContainer.innerHTML += `
//                                 <p>
//                                 <input type="number" id="q${val.id}-${i}" name="q${val.id}" class="choice" required>
//                                 </p>
//                             `;
//                             break;
//                         case "url":
//                             quizContainer.innerHTML += `
//                                 <p>
//                                 <input type="url" id="q${val.id}-${i}" name="q${val.id}" class="choice" required>
//                                 </p>
//                             `;
//                             break;
//                         default:
//                             quizContainer.innerHTML += `
//                                 <p>
//                                 <input type="text" id="q${val.id}-${i}" name="q${val.id}" class="choice" required>
//                                 </p>
//                             `;
//                             break;
//                     }
//                 });
//             });
//         });
//     })
//     .catch(error => {
//         console.log(error);
//     });


// function saveQuizResults() {
//     const userAnswers = {};
//     const choices = document.querySelectorAll(".choice");
//     // userAnswers["csrfmiddlewaretoken"] = csrfToken[0].value; // TODO: remove this - no longer needed???
//     choices.forEach(choice => {
//         // storing "choice.name" value to userAnswers dict
//         // must cast as Array() for the fetch data to match on DB
//         switch (choice.type) {
//             case "radio":
//                 if (choice.checked) {
//                     // if radio is checked
//                     userAnswers[choice.name] = Array(choice.value);
//                 } else {
//                     if (!userAnswers[choice.name]) {
//                         // field not checked, user left if blank
//                         userAnswers[choice.name] = null;
//                     }
//                 }
//                 break;
//             case "checkbox":
//             // checkbox needs to be an array, to handle multiple values
//                 if (choice.checked) {
//                     // if checkbox is checked
//                     if (!userAnswers[choice.name]) {
//                         // if no existing options are checked
//                         userAnswers[choice.name] = Array(choice.value);
//                     } else {
//                         // additional options are also checked
//                         userAnswers[choice.name].push(choice.value);
//                     }
//                 } else {
//                     if (!userAnswers[choice.name]) {
//                         // field not checked, user left if blank
//                         userAnswers[choice.name] = null;
//                     }
//                 }
//                 break;
//             case "textarea":
//             case "number":
//             case "url":
//             case "text":
//                 if (choice.value) {
//                     // grab the user's value
//                     userAnswers[choice.name] = Array(choice.value);
//                 } else {
//                     if (!userAnswers[choice.name]) {
//                         // field not checked, user left if blank
//                         userAnswers[choice.name] = null;
//                     }
//                 }
//                 break;
//             default:
//                 // TODO: what needs to be the default here?
//                 break;
//         }
//     });
//     // add the total duration of 'time'
//     userAnswers["duration"] = time;

//     // https://docs.djangoproject.com/en/3.2/ref/csrf/#setting-the-token-on-the-ajax-request
//     const request = new Request(
//         `${dataUrl}save/`,
//         {headers: {"X-CSRFToken": csrfToken[0].value}}
//     );

//     fetch(request, {
//         method: "POST",
//         body: JSON.stringify(userAnswers),
//         mode: "same-origin",
//         })
//         .then(response => response.json())
//         .then(data => {
//             // console.log(data); // JsonResponse({}) from views.py
//             const results = data.results;
//             console.log(results);
//         })
//         .catch(error => {
//             console.log(error);
//         });
// }

// quizForm.addEventListener("submit", function(e) {
//     e.preventDefault();
//     clearInterval(timeInterval);
//     duration.value = time;
//     quizForm.classList.add("hide", "full");
//     document.getElementById("thank-you").classList.remove("hide", "full");
//     // saveQuizResults();
//     // window.location.href += "submit/"
//     quizForm.submit();
// });