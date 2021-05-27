from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('quiz-list/', views.QuizListView.as_view(), name='quiz-list'),
    path('quiz/<pk>/', views.QuizQuestionsListView.as_view(), name='quiz-view'),
    path('student-answer/', views.student_answer, name='student-answer'),
    path('quiz/add', views.QuizCreateView.as_view(), name='quiz-add'),
    path('question/add', views.QuizQuestionCreateView.as_view(), name='question-add'),
]
