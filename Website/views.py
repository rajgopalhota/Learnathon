from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'components/home.html')

def reviews(request):
    return render(request, 'components/reviews.html')

def announcements(request):
    return render(request, 'components/announcements.html')

def timetable(request):
    return render(request, 'components/timetable.html')

def marksheets(request):
    return render(request, 'components/marksheets.html')

def postmarks(req):
    return render(req, 'components/postmarks.html')

def postattendance(req):
    return render(req, 'components/postattendance.html')
