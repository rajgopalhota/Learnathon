
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login, logout

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


# def LoginView(request):
#     if request.method == 'POST':
#         username = request.POST['mail']
#         password = request.POST['passwd']
#         user = auth.authenticate(username=username, password=password)
#         print(username, password)
#         if user is not None:
#             if User.is_staff:
#                 login(request, user)
#                 return redirect('/admin')
#             login(request, user)
#             return redirect('/')
#         else:
#             context = {'Error': 'INVALID CREDENTIALS', 'Sign': ' X'}
#             return render(request, 'Rentals/login.html', context)