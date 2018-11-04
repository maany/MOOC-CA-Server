from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from evaluator.models import Task, Applicant

@login_required
def profile(request):
    tasks = Task.objects.filter(applicant=request.user.applicant)
    context = {
        'tasks': tasks,

    }
    return render(request,'registration/profile.html', context)
