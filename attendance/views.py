from django.shortcuts import render
from .models import Attend, Event
from accounts.models import CustomUser
import json
import time
from django.middleware.csrf import get_token
from django.template import loader
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.shortcuts import redirect
import pytz

# Create your views here.
def attends(request):
    user = request.user
    userlog = CustomUser.objects.get(username=user)
    owner_flag = userlog.owner_flag
    if not owner_flag:
        return redirect('check')
    else:
        attend_data = Attend.objects.all()
        params = {
        'attend_data':attend_data
        }
        return render(request, 'attendance/attends.html', params)

# def checks(request):
#     flag=True
#     if request.method == 'POST':
#         ontime = Attend.get_ontime()
#         user = request.user
#         if 'sample' in request.POST:
#             if Attend.objects.filter(user=user, end_time != None,).exists():
#                 print(Attend.objects.filter(user=user, date=ontime))
#             else:
#                 print('そのレコードはありませんの')
#                 flag = False
#     params = {
#     'flag':flag,
#     }
#     return render(request, 'attendance/check.html', params)

def check(request):
    start_flag = True
    end_flag = True
    ontime = Attend.get_ontime()
    user = request.user
    if Attend.objects.filter(user=user, date=ontime).exists():
        start_flag = False
        if Attend.objects.get(user=user, date=ontime).end_time != None:
            end_flag = False
    print(start_flag)
    print(end_flag)

    if request.method == 'POST':
        ontime = Attend.get_ontime()
        user = request.user
        if 'start' in request.POST:
            #startボタンが押された時の処理
            start = ontime
            start = naive.astimezone(pytz.timezone('Asia/Tokyo'))
            Attend.objects.create(start_time=start, date=ontime, user=user)
            start_flag = False
            print('startを通りました')
        if 'end' in request.POST:
            end_flag = False
            attend_today = Attend.objects.get(user=user, date=ontime, end_time=None)
            end_time = ontime
            end_time = naive.astimezone(pytz.timezone('Asia/Tokyo'))
            attend_today.end_time = end_time
            start = attend_today.start_time
            start = start.replace(tzinfo=None)
            start = timedelta(days = start.day, minutes = start.minute, seconds = start.second).seconds - start.second
            end = ontime
            end = end.replace(tzinfo=None)
            end = timedelta(days = end.day, minutes = end.minute, seconds = end.second).seconds - end.second

            #勤務時間の計算処理
            total_time = Attend.get_totaltime(start, end)
            attend_today.total_time = total_time

            #給料の計算処理
            user_log = CustomUser.objects.get(username=user)
            pay_per_hour = user_log.pay_per_hour
            salary = Attend.get_salary(total_time, pay_per_hour)
            attend_today.salary = salary

            attend_today.save()
    params = {
    'start_flag':start_flag,
    'end_flag':end_flag,
    }
    return render(request, 'attendance/check.html', params)

def payments(request):
    user = request.user
    userlog = CustomUser.objects.get(username=user)
    owner_flag = userlog.owner_flag
    if not owner_flag:
        return redirect('check')
    else:
        payments_logs = dict()
        salary_logs = dict()
        for user_data in CustomUser.objects.all():
            attends = Attend.objects.filter(user=user_data.id)
            payments_logs[user_data.username] = attends
            total_salary = 0
            for attend in attends:
                total_salary += attend.salary
            salary_logs[user_data.username] = total_salary
        params = {
        'payments_logs':payments_logs,
        'salary_logs':salary_logs
        }
        return render(request, 'attendance/payments.html', params)

def add_event(request):

    datas = json.loads(request.body)
    start_date = datas['start_date']
    end_date = datas['end_date']
    event_name = datas['event_name']

    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    event = Event(
        event_name=str(event_name),
        start_date=formatted_start_date,
        end_date=formatted_end_date,
    )
    event.save()


    return render(request, 'attendance/schedule.html')

def get_event(request):
    datas = json.loads(request.body)

    start_date = datas['start_date']
    end_date = datas['end_date']

    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    events = Event.objects.filter(
        start_date__lt=formatted_end_date, end_date__gt=formatted_start_date
    )

    list = []
    for event in events:
        print(event)
        print('--------------------------')
        list.append(
            {
                "title": event.event_name,
                "start": event.start_date,
                "end": event.end_date,
            }
        )
        return JsonResponse(list, safe=False)

def schedule(request):
    get_token(request)

    return render(request, 'attendance/schedule.html')

def employees(request):
    user = request.user
    userlog = CustomUser.objects.get(username=user)
    owner_flag = userlog.owner_flag
    if not owner_flag:
        return redirect('check')
    else:
        users_logs = CustomUser.objects.all()
        params = {
        'users_logs':users_logs,
        }
        if request.method == 'POST':
            name = ""
            if 'on' in request.POST:
                name = request.POST.get('on')
                user_log = CustomUser.objects.get(username=name)
                user_log.owner_flag = True
                user_log.save()
            elif 'off' in request.POST:
                name = request.POST.get('off')
                user_log = CustomUser.objects.get(username=name)
                user_log.owner_flag = False
                user_log.save()
            elif 'delete' in request.POST:
                name = request.POST.get('delete')
                CustomUser.objects.get(username=name).delete()
        return render(request, 'attendance/employees.html', params)
