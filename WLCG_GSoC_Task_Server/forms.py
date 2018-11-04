from registration.forms import RegistrationForm
from registration.signals import user_registered
from django import forms

class RegistrationFormExtension(RegistrationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

def user_created(sender, user, request, **kwargs):
    form = RegistrationFormExtension(request.POST)
    user.first_name = form.data['first_name']
    user.last_name = form.data['last_name']
    user.save()

user_registered.connect(user_created)
