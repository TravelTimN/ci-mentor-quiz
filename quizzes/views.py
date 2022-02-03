import json
from types import SimpleNamespace
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Quiz
from questions.models import Question, Choice
from submissions.models import Submission, Response


@login_required
def quiz_info(request):
    user = get_object_or_404(User, username=request.user)
    get_quiz = Quiz.objects.filter(
        name=user.profile.mentor_type).values_list("id", flat=True)[:1]
    for quiz_id in get_quiz:
        quiz_id = quiz_id

    template = "quizzes/info.html"
    context = {
        "user": user,
        "quiz_id": quiz_id,
    }

    return render(request, template, context)


@login_required
def take_quiz(request, pk):
    user = get_object_or_404(User, username=request.user)
    get_quiz = Quiz.objects.filter(
        name=user.profile.mentor_type).values_list("id", flat=True)[:1]
    for quiz_id in get_quiz:
        if quiz_id != pk:
            # user trying to brute-force to another quiz URL
            return redirect(take_quiz, quiz_id)
        else:
            # user accessing correct quiz URL
            quiz = Quiz.objects.get(pk=pk)

    template = "quizzes/quiz.html"
    context = {
        "quiz": quiz,
    }

    return render(request, template, context)


@login_required
def quiz_data(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for question in quiz.get_questions():
        choices = []
        for choice in question.get_choices():
            choices.append(choice.choice)
        questions.append({
            "id": question.pk,
            "question": str(question),
            "choices": choices,
            "type": question.type,
        })
    return JsonResponse({"data": questions, })


@login_required
def save_quiz_results(request, pk):

    quiz = Quiz.objects.get(pk=pk)
    user = request.user
    results = []
    correct_answer = None
    is_correct = "False"

    # load the fetched POST from JavaScript (.body not .POST)
    data = json.loads(request.body.decode("utf-8"))
    questions = []
    duration = 0

    for key, value in data.items():
        # ignore "duration" for obtaining each question
        if key == "duration":
            duration = value
        else:
            # build questions list with user's responses
            key = key.replace("q", "")
            current_question = Question.objects.get(id=key)
            questions.append({
                "id": key,
                "question": current_question,
                "user_answer": value,
            })

    for question in questions:
        # https://docs.python.org/3/library/types.html#types.SimpleNamespace
        # SimpleNamespace allows the use of dot-notation
        q = SimpleNamespace(**question)
        if q.user_answer != "":  # only if user's value is not empty
            question_choices = Choice.objects.filter(question=q.question)
            choices = []  # resets with each loop intentionally
            # loop through the DB question's possible choices
            for choice in question_choices:
                # if the choice is marked 'correct_answer', append to choices
                if choice.correct_answer:
                    choices.append(choice.choice)
            correct_answer = choices  # set the correct_answer
            # check if the user's answer is equal to the correct choices
            if q.user_answer == choices:
                is_correct = "True"
            else:
                # correct_answer = choices
                is_correct = "False"
            # build a dict with the user's answers + the correct answers
            results.append({
                str(q.question): {
                    "id": q.id,
                    "is_correct": is_correct,
                    "correct_answer": correct_answer,
                    "user_answers": q.user_answer,
                }
            })
        else:
            # user's answer was blank/null/empty
            results.append({
                str(question): "User did not submit an answer"
            })

    # create new instance of Submission
    submission = Submission.objects.create(
        user=user,
        quiz=quiz,
        duration=duration,
        original_response=results
    )

    # create individual instances of Response for the Submission
    for result in results:
        Response.objects.create(submission=submission, answer=result)

    # update the user's profile to show they've taken the quiz
    user_profile = get_object_or_404(User, username=request.user)
    user_profile.profile.taken_quiz = True
    user_profile.save()

    return JsonResponse({"results": results})
