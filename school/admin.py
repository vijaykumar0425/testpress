from django.contrib import admin
from . import models


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = models.Answer
    min_num = 4
    max_num = 4


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id',)
