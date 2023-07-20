
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib import messages
from .models import Announcement, Complaints, Attendence,Student,Session,Review,Room,Team, TimeTable
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import AttendanceForm

from django.urls import reverse

# from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'components/home.html')

def reviews(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            teamno = request.POST.get('teamno')
            idno = request.POST.get('idno')
            roomno = request.POST.get('roomno')
            query = request.POST.get('query')
            msg = request.POST.get('msg')
            complaint = Complaints(teamno=teamno, idno=idno, roomno = roomno, query = query, msg = msg)
            complaint.save()
            messages.success(request, "Your Complaint has been posted successfully")
            return render(request, 'components/reviews.html')
        return render(request, 'components/reviews.html')
        
    messages.warning(request,"please login first and add the complaint then")
    return render(request, 'components/home.html')

def announcements(request):
    announced = Announcement.objects.all().order_by('sno').reverse()
    context = {'announce': announced, 'user': request.user}
    return render(request, 'components/announcements.html', context)

def timetable(request):
    tt = TimeTable.objects.all()
    context = {'timetable': tt}
    return render(request, 'components/timetable.html', context)


def marksheets(request):
    # print(request.user)
    # print(Student.objects.get(user=request.user))
    if request.user.is_authenticated:
        a=Student.objects.filter(user=User.objects.get(username=request.user))
        x=0
        for i in a:
            x=i
            break
        print(x.name)
        context={}
        context['student']=x
        context['marks']=Review.objects.filter(student=x).order_by('review_no')
        
        return render(request, 'components/marksheets.html',context)
    else:
        messages.warning(request,"login first to see the marksheets")
        return redirect('login')

def leaderboard(request):
    a=Student.objects.all()
    context={}
    f=[]
    for i in a:
        c=[]
        r=Review.objects.filter(student=i)
        s=0
        for p in r:
            s+=p.review_marks
        c.append(i.id)
        c.append(i.name)
        c.append(s)
        f.append(c)
    
    f=sorted(f,key=lambda f:f[2],reverse=True)
    context["marks"]=f
    return render(request, 'components/leaderboard.html',context)


# Main typo..............
def signin(request):
    # lg = login.objects.all().values()
    if request.method == 'POST' :
        username = request.POST.get('uname')
        pass1 = request.POST.get('pass')
        user = authenticate(username=username, password=pass1)
        print(user)
        if user is not None:
            if user.is_staff == True:
                login(request, user)
                return redirect('/admin')
            login(request, user)
            msg = "Welcome " + username
            messages.success(request, msg)
            return redirect('home')
        else:
            messages.error(request, "wrong credentials")
            return redirect('home')
    return render(request, "components/home.html", {})

def signout(request):
    logout(request)
    return redirect('home')

# Faculty

def room_display(request):
    # if request.user.is_authenticated and request.user.is_staff:
    context={}
    context["rooms"]=Room.objects.all()
    context["sessions"]=Session.objects.all()
    return render(request,"components/rooms.html",context)
    # else:
        # messages.error(request,"you does not have acess to use this")
        # logout(request)
        # return redirect('home')

def handleroom(request):
    if request.user.is_staff and request.user.is_authenticated:
        a=Room.objects.get(room_no=(request.POST["room"]))
        b=Student.objects.filter(room=a)
        context={}
        context["room"]=a
        context["students"]=b
        session=Session.objects.get(session_no=int(request.POST['session']))
    
        if session.Attendence == True:
            context["session"]=session
            return redirect('postattendance',room_no=str(a),session_no=request.POST['session'])
        else:
            messages.info(request,"Attendence not yet opened!")
            return redirect('home')
    else:
        messages.error(request,"you don't have acess to use this")
        logout(request)
        return redirect("home")
    


def postattendance(request, room_no, session_no):
    if request.user.is_staff and request.user.is_authenticated:
        room = Room.objects.get(room_no=room_no)
        session = Session.objects.get(session_no=session_no, Attendence=True)

        if request.method == 'POST' and request.user.is_staff:
            form = AttendanceForm(request.POST, session_id=session_no, room_no=room_no)
            if form.is_valid():
                form.save_attendance(session)
                messages.success(request,"Attendance saved successfully!")
                return redirect('home')  # Redirect to a success page
        elif not request.user.is_staff:
            messages.error(request,"You don't have access to it!")
            return redirect('home')  # Redirect to a success page
        else:
            form = AttendanceForm(session_id=session.session_no, room_no=room_no)
    
        return render(request, 'components/postattendance.html', {'students': form})
    else:
        messages.error(request,"you don't have acess to use this")
        logout(request)
        return redirect("home")
    



def room_display_review(request):
    if request.user.is_staff and request.user.is_authenticated:
        context={}
        context["rooms"]=Room.objects.all()
        context["sessions"]=Session.objects.all()
        return render(request,"components/rooms_review.html",context)
    else:
        messages.error(request,"you did not have access to use this")
        logout(request)
        return redirect("home")
    

def handle_review_room(request):
    if request.user.is_staff and request.user.is_authenticated:
        a=Room.objects.get(room_no=(request.POST["room"]))
        b=Student.objects.filter(room=a)
        context={}
        context["room"]=a
        context["students"]=b
        context["teams"]=Team.objects.filter(room=a)
        session=Session.objects.get(session_no=int(request.POST['session']))
    
        if session.Attendence == True:
            context["session"]=session
            return render(request,'components/teams.html',context)
        else:
            messages.info(request,"Session not activated!")
            return redirect('home')  # Redirect to a success page

    else:
        messages.error(request,"you does not have the permissions to use this")
        logout(request)
        return redirect("home")


def handle(request,room,session):
    if request.user.is_staff and request.user.is_authenticated:
        a=Room.objects.get(room_no=room)
        b=Student.objects.filter(room=a)
        context={}
        context["room"]=a
        context["students"]=b
        context["teams"]=Team.objects.filter(room=a)
        sessio=Session.objects.get(session_no=session)
    
        if sessio.Attendence == True:
            context["session"]=sessio
            return render(request,'components/teams.html',context)
        else:
            messages.info(request,"Session not activated!")
            return redirect('home')  # Redirect to a success page
    else:
        messages.error(request,"you does not have the permissions to use this")
        logout(request)
        return redirect("home")


def handle_team(request, session_no, room_no):
    if request.user.is_authenticated and request.user.is_staff:
        team_id = request.POST.get('team')
        redirect_url = reverse('postmarks', args=(session_no, room_no, team_id))
        return redirect(redirect_url)
    else:
        messages.error(request,"you don't have the acess to use this")
        logout(request)
        return redirect("home")

def postmarks(request, session_no, room_no, team_name):
    if request.user.is_staff and request.user.is_authenticated:
        r = Room.objects.get(room_no=room_no)
        session = Session.objects.get(session_no=session_no, Attendence=True)
        team = Team.objects.get(team_name=team_name)
        a = Student.objects.filter(team=team)
        context = {}
        context["students"] = a

        if request.method == 'POST':
            for i in a:
                review_marks = request.POST[str(i.id)]
                if Review.objects.filter(student=i, session=session, review_no=session_no, room=r).exists():
                    messages.error(request,"updation of the marks is not possible")
                    return redirect('handle',room=room_no,session=session_no)
                
                Review.objects.update_or_create(
                    student=i,
                    session=session,
                    review_no=session.session_no,
                    room=r,
                    defaults={'review_marks': review_marks}
                )
        # team.submitted = True
        # team.save()
            return redirect('handle',room=room_no,session=session_no)

        return render(request, 'components/postmarks.html', context=context)
    else:
        messages.error(request,"you don't have acess to use this")
        return redirect('home')

def errorPage(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'components/error.html')
def error500Page(request, exception=None, *_, **_k):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'components/error.html')

def viewattendance(request):
    if request.user.is_authenticated :
        a=Student.objects.filter(user=User.objects.get(username=request.user))
        x=0
        for i in a:
            x=i
            break
        print(x.name)
        context={}
        context['student']=x
        context['att']=Attendence.objects.filter(student=x).order_by('session')
        return render(request,'components/viewattendance.html',context)
    else:
        messages.error(request,"login first to view this")
        return redirect("login")