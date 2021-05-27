from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Quiz(models.Model):
    title = models.CharField(max_length=200)

    def get_questions(self):
        return self.question_set.all()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("a description of the quiz")
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def get_answers(self):
        return self.answer_set.all()

    def get_correct_answer(self):
        return self.answer_set.filter(is_correct=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)


class UserAnswer(models.Model):
    quiz_session_id = models.UUIDField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
