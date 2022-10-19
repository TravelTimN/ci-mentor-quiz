/* jshint esversion: 8 */

const takeQuizBtn = document.getElementById("btn-take-quiz");

takeQuizBtn?.addEventListener("click", function() {
    // take the user to the appropriate quiz page
    let quiz = this.dataset.quiz;
    window.location.assign(`/quizzes/${quiz}`);
});
