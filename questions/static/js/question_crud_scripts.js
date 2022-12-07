/* jshint esversion: 11, jquery: true */

// disable first option of each <select> element
$("select").each(function() {
    $(this).children("option:first").prop("disabled", true);
});

// force-require first Choice, since this cannot be set in FormSet due to 'empty_form'
// https://docs.djangoproject.com/en/3.2/topics/forms/formsets/#empty-form-1
$("tbody input[type=text]").each(function() {
    $(this).prop("required", true);
});

// this is for new questions, and "extras", so placeholder should NOT be "Original Choice"
$("input[type='text'][id$='-choice']:not([value])").each(function() {
    $(this).prop("placeholder", "New Choice");
});

// unhide the formset Choices once quiz-type is selected, or if editing an existing Question
$("#id_type").on("change", function() {
    $("#card-body").removeClass("hide full");
    validateCorrectAnswerCheckboxes();
});
if ($("#id_question").val()) {
    $("#card-body").removeClass("hide full");
    $("#submit-btn").removeClass("hide");
}

// get absolute MAX_NUM_FORMS
let absoluteMaxFormCount = $("[name=form-MAX_NUM_FORMS]").val();

// hide any formset checkboxes ending with "-DELETE"
$("input[type='checkbox'][id$='-DELETE']").closest("td").addClass("hide full");

// click event for add_choice button
$("#add_choice").on("click", function() {
    // remove any instance of "remove_choice" button to avoid duplicates
    $("#remove_choice").remove();
    // increment formset total count and add new instance of row
    addChoice();
    validateCorrectAnswerCheckboxes();
});

// add new row to the formset Choice model
function addChoice() {
    // https://stackoverflow.com/a/5479472
    // increment formset total Choices for DB-submission
    let formCount = $("[name=form-TOTAL_FORMS]").val();
    let formCountNext = parseInt(formCount) + 1;
    $("[name=form-TOTAL_FORMS]").val(formCountNext);

    // add new row to table with next formset incremented number
    // cloning doesn't work when formset is in table/tr; must create manually
    let newRow = `
        <tr id="tr-${formCount}">
            <td>
                <span class="text-danger">*</span>
                <input type="text" name="form-${formCount}-choice" maxlength="100" id="id_form-${formCount}-choice" placeholder="New Choice" required>
            </td>
            <td>
                <input type="checkbox" name="form-${formCount}-correct_answer" id="id_form-${formCount}-correct_answer">
            </td>
            <td class="hide full">
                <input type="checkbox" name="form-${formCount}-DELETE" id="id_form-${formCount}-DELETE">
            </td>
            <td id="td-${formCount}">
                <span id="remove_choice" class="btn btn-small btn-danger lh-1">
                    <i class="fas fa-trash-alt fs-6"></i>
                </span>
            </td>
        </tr>
    `;
    $("#tbody").append(newRow);
    // disable add_choice button if maximum formset choices reached
    let maxFormCount = $("[name=form-MAX_NUM_FORMS]").val();
    let totalRows = $("#tbody").children("tr:not(.hide)").length;
    if (totalRows >= absoluteMaxFormCount) {
        disableAddBtn();
    }
}

// clicking the remove_choice button triggers a few events
$("body").on("click", "#remove_choice", function(e) {
    removeChoice(e);
    validateCorrectAnswerCheckboxes();
});

// remove_choice button clicked
function removeChoice(e) {
    // remove any instance of "remove_choice" button to avoid duplicates
    $("#remove_choice").remove();

    // decrement formset total Choices for DB-submission
    let formCount = $("[name=form-TOTAL_FORMS]").val();
    let maxFormCount = $("[name=form-MAX_NUM_FORMS]").val();

    let parentTR = $("#tbody").children("tr:not(.hide):last");
    let deleteTD = $(parentTR).children("td.hide.full");
    let getChoiceID = $(parentTR).find("input[name^='form-'][name$='-id']");
    let checkPlaceholder = $(parentTR).find("input[id$='-choice']");
    let checkName = $(checkPlaceholder).prop("name");
    let checkChoiceNumber = checkName.split("-")[1];

    // handle functionality to hide/remove depending on whether it's original or not
    if ($(checkPlaceholder).prop("placeholder") == "Original Choice") {
        // original choice found - must use 'form-#-DELETE'
        // https://docs.djangoproject.com/en/3.2/topics/forms/formsets/#understanding-the-managementform
        $(deleteTD).children("input[id$='-DELETE']").prop("checked", true);
        $(parentTR).addClass("hide full");
        // increment max formset total Choices for DB-submission, but retain total-form count
        $("[name=form-MAX_NUM_FORMS]").val(parseInt(maxFormCount) + 1);
    } else {
        // not from original choices - can simply just remove
        $(parentTR).remove();
        // decrement formset total Choices for DB-submission
        $("[name=form-TOTAL_FORMS]").val(parseInt(formCount) - 1);
    }

    // count total <tr> rows, except hidden ones for deletion
    let totalRows = $("#tbody").children("tr:not(.hide)").length;
    if (totalRows > 1) {
        // add another "remove_choice" button to last row, unless only 1 row remains
        $("#tbody").children("tr:not(.hide):last").children("td:last").html(
            `<span id="remove_choice" class="btn btn-small btn-danger lh-1">
                <i class="fas fa-trash-alt fs-6"></i>
            </span>`
        );
    }
    // re-enable "add" btn if max choices not hit
    if (totalRows < maxFormCount) {
        enableAddBtn();
    }
}

// disable add_choice if greater than permitted formset Choices
function disableAddBtn() {
    $("#add_choice").addClass("hide");
}

// enable add_choice if fewer than permitted formset Choices
function enableAddBtn() {
    $("#add_choice").removeClass("hide");
}

// enable "Submit" button if the first formset Choice has data/value, or updating existing question
let getFirstTR = $("#tbody").children("tr:not(.hide)").first();
if ($(getFirstTR).next("input[id$='-choice']").val() != "" && $(getFirstTR).next("input[id$='-choice']").val() != undefined) {
    $("#question-submit-btn").removeClass("hide full");
}
$("body").on("input", "input[id$='-choice']", function() {
    if ($(this).val() != "") {
        $("#question-submit-btn").removeClass("hide full");
    } else {
        $("#question-submit-btn").addClass("hide full");
    }
    validateCorrectAnswerCheckboxes();
});

// check if at least one correct_answer is toggled on
$("body").on("change", "input[id$='-correct_answer'][type=checkbox]", function() {
    validateCorrectAnswerCheckboxes();
});

// ensure at least one checkbox is always checked (unless it's "non-mentor quiz")
function validateCorrectAnswerCheckboxes() {
    let validChoices = $("#tbody").children("tr:not(.hide)").children("td:not(.hide)").children("input[id$='-correct_answer'][type=checkbox]:checked");
    if (validChoices.length == 0 && $("#id_quiz option:selected").text() != "Non-Mentor Quiz") {
        $("#question-submit-btn").addClass("hide full");
    } else {
        $("#question-submit-btn").removeClass("hide full");
    }
}

// enable "Submit" button if the quiz_type is "Not Mentor"
$("#id_quiz").on("change", function() {
    if ($("#id_quiz option:selected").text() == "Non-Mentor Quiz") {
        $("#question-submit-btn").removeClass("hide full");
    } else {
        $("#question-submit-btn").addClass("hide full");
    }
});
