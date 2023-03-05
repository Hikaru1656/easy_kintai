from django.db import models
from datetime import datetime, timedelta
from accounts.models import CustomUser

# Create your models here.
class Attend(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    total_time = models.IntegerField(null=True, default=0)
    date = models.DateField()
    salary = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "user_attends")

    def __str__(self):
        return self.user.username + str(self.id)

    def get_ontime():
        ontime = datetime.today()
        return ontime

    def get_totaltime(start, end):
        total = end-start
        total = total.seconds//60  #分に変換
        return total

    def get_salary(time, pay_per_hour):
        salary = int(time * (pay_per_hour/60))
        return salary

class Event(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event_name = models.CharField(max_length = 50)
