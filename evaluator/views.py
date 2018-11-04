from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator

from .models import Applicant, Task
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required

import json
# Create your views here.
@login_required()
def task(request, id):
    applicant = request.user.applicant
    tasks = Task.objects.filter(applicant=applicant)
    requested_task = Task.objects.get(pk=id)
    if requested_task in tasks:
        context = {
            'task': requested_task
        }
        return render(request,'evaluator/task.html', context)
    else:
     return HttpResponse("You are trying to be a sneaky cheeki. Please do not try to view tasks submitted by other candidates. The incident has been logged", status=401)

# def get_csrf_token(request):
#     template = loader.get_template('evaluator/task.html')
#     render(request, template)

@method_decorator(csrf_exempt, name='dispatch')
class OAuthProtectedEndpoints(ProtectedResourceView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print("Task Submitted!!")
        data = json.loads(request.body)
        url = data['url']
        task_name = data['name']
        html = data['html']
        print(url)
        print(task_name)
        #print(html)
        # create Task
        task = Task(name=task_name, applicant_id=request.user.id, html=html, url=url)
        print("User was : " + str(request.user.id))
        task.save()

        # response is 200
        return HttpResponse("{'status' : True")