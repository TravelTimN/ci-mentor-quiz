from django.db import models


class Quiz(models.Model):
    # quiz types available
    QUIZ_TYPE = [
        ("current_mentor", "Quiz for Mentors"),
        ("potential_mentor", "Quiz for Potential Mentors"),
    ]
    name = models.CharField(choices=QUIZ_TYPE, max_length=20)
    max_count = models.IntegerField(null=True)

    def __str__(self):
        return str(self.name)

    def get_questions(self):
        return self.question_set.all()[:self.max_count]

    class Meta:
        verbose_name_plural = "Quizzes"
