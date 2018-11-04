from django.db import models
from .fields import HTMLField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username_proxy = models.TextField(max_length=50, blank=True)
    def __str__(self):
        return self.user.first_name +" " + self.user.last_name

@receiver(post_save, sender=User)
def create_applicant_profile(sender, instance, created, **kwargs):
    if created:
        Applicant.objects.create(user=instance, username_proxy=instance.username)

@receiver(post_save, sender=User)
def save_applicant_profile(sender, instance, **kwargs):
    instance.applicant.username_proxy = instance.username
    instance.applicant.save()


class Task(models.Model):
    name = models.CharField(max_length=100, default= 'default')
    url = models.URLField(default="")
    status = models.BooleanField(default=False)
    applicant = models.ForeignKey(Applicant, default= "" , on_delete=models.CASCADE)
    html = HTMLField(default="")
    def __str__(self):
        return self.name + ": " + self.applicant.user.username
    def __eq__(self, other):
        return self.id == other.id
