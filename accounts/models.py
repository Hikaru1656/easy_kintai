from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = 'CustomUser'

    pay_per_hour = models.IntegerField(default=1000)
    owner_flag = models.BooleanField(default=False)
