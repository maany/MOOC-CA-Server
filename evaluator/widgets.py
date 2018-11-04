from django import forms
from django.db.transaction import commit
from django.template.loader import render_to_string
from django.utils.safestring import  mark_safe

from .models import Applicant, Task


class ApplicantForm(forms.ModelForm):

    tasks = forms.ModelMultipleChoiceField(queryset=Task.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['tasks'].initial = self.instance.task_set.all()
            self.fields['tasks'].widget = ApplicantTaskSetWidget()

    def save(self, *args, **kwargs):
        instance = super(ApplicantForm, self).save(commit=commit)
        #self.fields['tasks'].initial.update(applicant=None)
        self.cleaned_data['tasks'].update(applicant=instance)
        return instance

    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantTaskSetWidget(forms.Widget):
    template_name = 'evaluator/applicant_task_set.html'

    def render(self, name, value, attrs=None):
        tasks = []
        if value == None:
            context = {
                'tasks' : None
            }
            return mark_safe(render_to_string(self.template_name, context))
        for task_id in value:
            tasks.append(Task.objects.get(pk=task_id))
        context = {
            'tasks': tasks
        }
        return mark_safe(render_to_string(self.template_name, context))


class HTMLRenderWidget(forms.Widget):
    template_name = 'evaluator/task_admin.html'

    def render(self, name, value, attrs=None):
        context = {
            'html': value
        }
        return mark_safe(render_to_string(self.template_name, context))




