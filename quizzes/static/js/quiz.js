/* jshint esversion: 11, jquery: true */

const quizStartBtn = document.getElementById("quiz-start-btn");
const quizSubmitBtn = document.getElementById("quiz-submit-btn");
const quizForm = document.getElementById("quiz-form");
const duration = document.getElementById("duration");
let progressBar = document.getElementById("progress-bar-first");
let qPercent, durationInterval, timeTakenInterval;
let durationTime = 0;
let timeTaken = 0;
let qIndex = progressBar.dataset.questionindex;
let qCount = progressBar.dataset.questioncounter;


// update the progress bar value and width
window.addEventListener("load", updateProgress);
function updateProgress() {
    qPercent = Math.ceil((qIndex / qCount) * 100) + "%";
    progressBar.style.width = qPercent;
    progressBar.innerText = `${qIndex} of ${qCount}`;
}


function ajaxQuizStart(quizID) {
    url = "/submissions/ajax_quiz_start/";
    csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
        url: url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": csrfToken,
            "quizID": quizID,
        },
        success: function(data) {console.log(data);},
        error: function(data) {
            let errText = data.responseText;
            // specific error is between `<pre></pre>` elements
            let errMsg = errText.match(/<pre>[\s\S]*?<\/pre>/g)[0];
            // remove `<pre></pre>` tags and trim excess whitespace
            console.log(errMsg.replace("<pre>", "").replace("</pre>", "").trim());
        }
    });
}


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
    let quizID = window.location.pathname.split("/")[2];
    // attempt to parse quizID to integer, and confirm it is indeed an integer
    if (!isNaN(parseInt(quizID))) {
        ajaxQuizStart(quizID);
    }
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
            // update progress bar
            qIndex++;
            progressBar = document.getElementById(`progress-bar-${qIndex}`);
            updateProgress();
        }
    });
});


// validate the final question of the quiz using the submit-btn dataset
quizSubmitBtn.addEventListener("click", function (e) {
    e.preventDefault();
    let btnNum = this.dataset.submit;
    // only proceed if validated properly
    if (validateQuestion(btnNum)) {
        // disable the submit button in case a user takes longer than 30mins to do the quiz,
        // due to Heroku's dynos timing out, this can cause the app to spin-up slowly
        // and users to submit multiple quiz results.
        quizSubmitBtn.disabled = true;
        quizForm.submit();
    }
});


function validateQuestion(btnNum) {
    // check if user input an answer in order to proceed
    let dataValidator = document.querySelector(`[data-validator="${btnNum}"]`);

    if (dataValidator.checkValidity()) {
        return true;
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
