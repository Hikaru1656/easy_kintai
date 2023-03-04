from django.shortcuts import render
from .models import Attend
from accounts.models import CustomUser

# Create your views here.
def attends(request):
    attend_data = Attend.objects.all()
    params = {
    'attend_data':attend_data
    }
    return render(request, 'attendance/attends.html', params)

def check(request):
    if request.method == 'POST':
        ontime = Attend.get_ontime()
        user = request.user
        if 'start' in request.POST:
            #startボタンが押された時の処理
            attend = Attend.objects.create(start_time=ontime, date=ontime, user=user)
        if 'end' in request.POST:
            attend_today = Attend.objects.get(user=user, date=ontime, end_time=None)
            attend_today.end_time = ontime
            start = attend_today.start_time
            start = start.replace(tzinfo=None)
            end = ontime
            end = end.replace(tzinfo=None)

            total_time = Attend.get_totaltime(start, end)
            attend_today.total_time = total_time
            print("--------------------------------")
            print(total_time)
            print("--------------------------------")
            attend_today.save()
            #endボタンが押された時の処理
            print('end')
    return render(request, 'attendance/check.html')

def payments(request):
    attend_data = Attend.objects.all()
    username = CustomUser.objects.all().values("username")
    params = {
    'username':username
    }
    return render(request, 'attendance/payments.html', params)
