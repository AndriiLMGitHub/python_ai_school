from django import forms
from .models import Task, Team, TestWorkRequest, TestWorkResponse, AnswerTest
from account.models import CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('is_completed', 'image')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'image']


class TestWorkForm(forms.ModelForm):
    class Meta:
        model = TestWorkRequest
        fields = (
            'title',
            'topic',
            'description',
            'form_class',
            'difficulty',
            'quantity_questions',
        )


class TestWorkResultForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Виберить користувачів"
    )

    class Meta:
        model = TestWorkResponse
        fields = (
            'test_work',
            'content',
        )


class AnswerTestForm(forms.ModelForm):
    class Meta:
        model = AnswerTest
        fields = ('answers',)
