from django.contrib import admin
from django import forms
from .fields import HTMLField
from .models import Applicant, Task
from .widgets import HTMLRenderWidget, ApplicantForm, ApplicantTaskSetWidget

# Register your models here.


class ApplicantAdmin(admin.ModelAdmin):
    form = ApplicantForm

    formfield_overrides = {
        forms.EmailField: {'widget': ApplicantTaskSetWidget}
    }


admin.site.register(Applicant, ApplicantAdmin)


class TaskAdmin(admin.ModelAdmin):
    formfield_overrides = {
        HTMLField: {'widget': HTMLRenderWidget}
    }


admin.site.register(Task, TaskAdmin)