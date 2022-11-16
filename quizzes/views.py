from types import SimpleNamespace
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Quiz
from .forms import QuizForm
from questions.models import Question, Choice
from submissions.models import Submission, Response


@login_required
def quiz(request):
    """ Redirect user from /quiz/ to their profile """
    return redirect(reverse("profile"))


@login_required
def quizzes(request):
    """ Grab all quizzes for Admin management """
    if not request.user.is_superuser:
        # user is not superuser; take them to their profile
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("profile"))
    # is superuser
    quizzes = Quiz.objects.all()
    template = "quizzes/quizzes.html"
    context = {
        "quizzes": quizzes,
    }
    return render(request, template, context)


@login_required
def add_quiz(request):
    """ Allow admins to create new Quizzes on the DB """
    if not request.user.is_superuser:
        # user is not superuser; take them to their profile
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("profile"))
    # is superuser
    quiz_form = QuizForm(request.POST or None)

    if request.method == "POST":
        if quiz_form.is_valid:
            # save the Quiz model
            quiz_form.save()
            messages.success(request, "Quiz successfully added!")
            return redirect(quizzes)
        else:
            messages.error(request, "An error has occurred. Please try again.")

    template = "quizzes/add_quiz.html"
    context = {
        "quiz_form": quiz_form,
    }
    return render(request, template, context)


@login_required
def update_quiz(request, pk):
    """ Allow admins to update existing Quizzes on the DB """
    if not request.user.is_superuser:
        # user is not superuser; take them to their profile
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("profile"))
    # is superuser
    quiz = get_object_or_404(Quiz, id=pk)
    quiz_form = QuizForm(request.POST or None, instance=quiz)

    if request.method == "POST":
        if quiz_form.is_valid:
            # save the Quiz model
            quiz_form.save()
            messages.success(request, "Quiz successfully updated!")
            return redirect(quizzes)
        else:
            messages.error(request, "An error has occurred. Please try again.")

    template = "quizzes/update_quiz.html"
    context = {
        "quiz": quiz,
        "quiz_form": quiz_form,
    }
    return render(request, template, context)


@login_required
def delete_quiz(request, pk):
    """ Allow admins to delete existing Quizzes from the DB """
    if not request.user.is_superuser:
        # user is not superuser; take them to their profile
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("profile"))
    # is superuser
    quiz = get_object_or_404(Quiz, id=pk)
    quiz.delete()
    messages.success(request, "Quiz successfully deleted!")
    return redirect(quizzes)


@login_required
def take_quiz(request, pk):
    user = get_object_or_404(User, username=request.user)
    # check if non-mentor trying to take quiz again, and redirect if so
    if user.profile.mentor_type == "is_not_mentor" and user.profile.taken_quiz and not user.is_superuser:  # noqa
        messages.info(request, "You have already submitted your responses.")
        return redirect(reverse("profile"))

    if user.is_superuser:
        # superuser can take any test type
        quiz = get_object_or_404(Quiz, id=pk)
    elif user.profile.mentor_type == "is_not_mentor":
        # new mentor (hasn't taken quiz yet)
        quiz = get_object_or_404(Quiz, quiz_type=user.profile.mentor_type)
        if quiz.id != pk:
            # force back to correct quiz, if trying to brute-force
            return redirect(take_quiz, quiz.id)
    else:
        # is mentor (unlimited quizzes)
        quiz = get_object_or_404(Quiz, id=pk)
        # mentors can only access 'active' quizzes meant for mentors
        if quiz.quiz_type != user.profile.mentor_type or not quiz.is_active:  # noqa
            messages.error(request, "Invalid Quiz Selected")
            return redirect(reverse("profile"))

    # user accessing correct quiz URL
    questions = []
    for question in quiz.get_questions():
        choices = []
        for choice in question.get_choices():
            choices.append(choice.choice)
        questions.append({
            "id": question.pk,
            "type": question.type,
            "question": str(question),
            "choices": choices,
            "text": question.optional_text
        })

    template = "quizzes/quiz.html"
    context = {
        "quiz": quiz,
        "questions": questions,
    }

    return render(request, template, context)


@login_required
def submit_quiz_results(request, pk):
    if request.method == "POST":

        quiz = Quiz.objects.get(pk=pk)
        user = request.user
        results = []
        correct_answer = None
        is_correct = "False"
        total_correct = 0

        # convert POST results into dictionary of lists
        data = dict(request.POST.lists())
        # remove CSRF token
        data.pop("csrfmiddlewaretoken")
        questions = []
        duration = 0
        time_taken = 0

        for key, value in data.items():
            # ignore "duration" for obtaining each question
            if key == "duration":
                duration = "".join(value)
            elif key.startswith("time_taken-"):
                time_taken = "".join(value)
            elif key.startswith("q"):
                # build questions list with user's responses
                key = key.replace("q", "")
                current_question = Question.objects.get(pk=key)
                questions.append({
                    "id": key,
                    "question": current_question,
                    "user_answer": value,
                    "time_taken": time_taken
                })

        for question in questions:
            # https://docs.python.org/3/library/types.html#types.SimpleNamespace
            # SimpleNamespace allows the use of dot-notation
            q = SimpleNamespace(**question)
            question_choices = Choice.objects.filter(question=q.question)
            choices = []  # resets with each loop intentionally
            # loop through the DB question's possible choices
            for choice in question_choices:
                # if the choice is marked 'correct_answer', append to choices
                if choice.correct_answer:
                    choices.append(choice.choice)
            correct_answer = sorted(choices)  # set the correct_answer
            # check if the user's answer is equal to the correct choices
            if sorted(q.user_answer) == sorted(choices):
                is_correct = "True"
                total_correct += 1
            elif quiz.quiz_type == "is_not_mentor":
                # handle 'is_not_mentor' as always True
                is_correct = "True"
                total_correct += 1
            else:
                is_correct = "False"
            # build a dict with the user's answers + the correct answers
            results.append({
                "id": q.id,
                "question": q.question.question,
                "is_correct": is_correct,
                "correct_answer": correct_answer,
                "user_answers": q.user_answer,
                "time_taken": q.time_taken,
            })

        # calculate percentage of questions answered correctly
        questions_answered = len(questions)
        percent_correct = round((total_correct / questions_answered) * 100)

        # create new instance of Submission
        submission = Submission.objects.create(
            user=user,
            quiz=quiz,
            duration=duration,
            original_response=results,
            percent_correct=percent_correct
        )

        # create individual instances of Response for the Submission
        for result in results:
            Response.objects.create(
                submission=submission,
                question=Question.objects.get(pk=result["id"]),
                is_correct=result["is_correct"],
                correct_answer=result["correct_answer"],
                user_answer=result["user_answers"],
                time_taken=result["time_taken"],
            )

        # update the user's profile to show they've taken the quiz
        user_profile = get_object_or_404(User, username=request.user)
        user_profile.profile.taken_quiz = True
        user_profile.save()

        messages.success(request, "Your responses have been submitted!")
        return redirect(reverse("profile"))

    else:
        return redirect(take_quiz, pk)
