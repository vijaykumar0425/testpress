from django import forms
from . import models


class BaseModelFolrm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class StudentAnswerForm(forms.ModelForm):
    class Meta:
        model = models.UserAnswer
        fields = "__all__"


class QuizForm(BaseModelFolrm):
    class Meta:
        model = models.Quiz
        fields = '__all__'


class QuizQuestionForm(BaseModelFolrm):
    class Meta:
        model = models.Question
        fields = "__all__"


AnswerFormSet = forms.inlineformset_factory(models.Question, models.Answer, fields=('text', 'is_correct',),
                                            exclude=('id',), min_num=4,
                                            max_num=4, can_delete=False)
