/* jshint esversion: 8 */

const dataUrl = window.location.href;
const quizSubmitBtn = document.getElementById("quiz-submit-btn");
let quizContainer = document.getElementById("quiz-container");

fetch(`${dataUrl}data`)
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        let counter = 1;

        Object.entries(data).forEach(entry => {
            const [, value] = entry;
            Object.entries(value).forEach(item => {
                const [, val] = item;
                quizContainer.innerHTML += `
                    <hr>
                    <p>${val.question}</p>
                `;
                val.choices.forEach(choice => {
                    quizContainer.innerHTML += `<p>`;
                    switch (val.type) {
                        case "radio":
                            quizContainer.innerHTML += `
                                <input type="radio" id="${counter}-${val.type}" name="${val.question.replace(/[^a-zA-Z]/g, '')}" class="" value="${choice}">
                                <label for="${counter}-${val.type}" class="">${choice}</label>
                            `;
                            break;
                        case "checkbox":
                            quizContainer.innerHTML += `
                                <input type="checkbox" id="${counter}-${val.type}" name="${val.question.replace(/[^a-zA-Z]/g, '')}" class="" value="${choice}">
                                <label for="${counter}-${val.type}" class=""> - ${choice}</label>
                            `;
                            break;
                        case "textarea":
                            quizContainer.innerHTML += `<textarea id="${counter}-${val.type}" name="${val.question.replace(/[^a-zA-Z]/g, '')}" class=""></textarea>`;
                            break;
                        case "number":
                            quizContainer.innerHTML += `<input type="number" id="${counter}-${val.type}" name="${val.question.replace(/[^a-zA-Z]/g, '')}" class="">`;
                            break;
                        case "url":
                            quizContainer.innerHTML += `<input type="url" id="${counter}-${val.type}" name="${val.question.replace(/[^a-zA-Z]/g, '')}" class="">`;
                            break;
                        default:
                            quizContainer.innerHTML += `<input type="text" id="${counter}-${val.type}" name="${val.question.replace(/[^a-zA-Z]/g, '')}" class="">`;
                            break;
                    }
                    quizContainer.innerHTML += `</p>`;
                    counter++;
                });
            });
        });
    })
    .catch(function (error) {
        console.log(error);
    });