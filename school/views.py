from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from . import models
from django.http import Http404, JsonResponse
from . import forms
import uuid
from django.contrib.auth.decorators import login_required
import copy
from django.urls import reverse_lazy


# Create your views here.


class HomePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'


class QuizListView(LoginRequiredMixin, generic.ListView):
    template_name = 'quiz_list.html'
    queryset = models.Quiz.objects.all()


class QuizQuestionsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'quiz.html'
    paginate_by = 1

    def get_object(self):
        queryset = models.Quiz.objects.filter(pk=self.kwargs["pk"])
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_queryset(self):
        return models.Question.objects.filter(quiz=self.object).order_by('id')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        if self.object:
            context['quiz'] = self.object
        return context


@login_required
def student_answer(request):
    if request.session.get(f"quiz_{request.user.id}", None):
        quiz_session_id = request.session[f"quiz_{request.user.id}"]
    else:
        request.session[f"quiz_{request.user.id}"] = str(uuid.uuid4())
        quiz_session_id = request.session[f"quiz_{request.user.id}"]
    context = {"success": False}
    if request.method == 'POST':
        quiz_finish = request.POST.get('is_finish')
        if quiz_finish == "true":
            correct_answers = request.user.quiz_answers.filter(quiz_session_id=quiz_session_id,
                                                               answer__is_correct=True).count()
            quiz = models.Quiz.objects.get(id=request.POST.get('quiz'))
            total_questions = quiz.get_questions().count()
            percentage = round((correct_answers / total_questions) * 100.0, 2)
            if percentage >= 70:
                status = "Pass"
            else:
                status = "Fail"
            del request.session[f"quiz_{request.user.id}"]
            result_msg = f"<p><b>Correct Answer</b>: {correct_answers}" \
                         f"<br><b>Status</b>: {status}"
            return JsonResponse({"result": result_msg})
        data = copy.copy(request.POST)
        data["quiz_session_id"] = request.session[f"quiz_{request.user.id}"]
        form = forms.StudentAnswerForm(data=data)
        if form.is_valid():
            instance = form.save()
            if instance.answer.is_correct:
                context["msg"] = "<div class='alert alert-success' role='alert'>" \
                                 "Correct Answer" \
                                 "</div>"
                context["success"] = True
                return JsonResponse(context)
            else:
                answer = "<br>".join(instance.answer.question.get_correct_answer().values_list('text', flat=True))
                context["msg"] = "<div class='alert alert-danger' role='alert'>" \
                                 "<b>InCorrect</b><p>Correct Answer: {answer}</p>".format(answer=answer)
                return JsonResponse(context)
        else:
            return JsonResponse({"msg": form.errors.as_json(), "success": False})
    else:
        return JsonResponse({"msg": "GET method Not Valid method", "success": False})


class QuizCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'school.add_quiz'
    template_name = 'quiz_form.html'
    form_class = forms.QuizForm
    success_url = reverse_lazy('quiz-list')


class QuizQuestionCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'school.add_question'
    template_name = 'question_form.html'
    form_class = forms.QuizQuestionForm

    success_url = reverse_lazy('quiz-list')

    def form_valid(self, form):
        self.object = form.save()
        formset = forms.AnswerFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = forms.AnswerFormSet()
        return context
