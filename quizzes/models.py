import random
from django.db import models


class Quiz(models.Model):
    # quiz types available
    QUIZ_TYPE = [
        ("is_mentor", "Quiz for Mentors"),
        ("is_not_mentor", "Quiz for Potential Mentors"),
    ]
    name = models.CharField(max_length=50, null=False, blank=False)
    quiz_type = models.CharField(
        choices=QUIZ_TYPE, max_length=20, null=False, blank=False)
    max_count = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_questions(self):
        if self.quiz_type != "is_not_mentor":
            # shuffle quiz unless it's is_not_mentor quiz
            questions = list(self.question_set.all())
            random.shuffle(questions)
            return questions[:self.max_count]
        else:
            return self.question_set.all()[:self.max_count]

    class Meta:
        verbose_name_plural = "Quizzes"
