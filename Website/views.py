
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib import messages
from .models import Announcement, Complaints, Attendence,Student,Session,Review,Room,Team, TimeTable,Teacher,Rubrics
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import AttendanceForm
from django.urls import reverse
import csv
# from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.utils import timezone
# from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login, logout
from . import utils
# Create your views here.
def home(request):
    context={}
    
    a=Session.objects.filter(Attendence=True)
    context['session_att']=a
    b=Session.objects.filter(Review=True)
    context['session_rev']=b
    return render(request, 'components/home.html',context)

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
    announced = Announcement.objects.all().order_by('sno')
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
            # if user.is_staff == True:
            #     login(request, user)
            #     return redirect('/admin')
            login(request, user)
            msg = "Welcome " + user.username
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
    #     messages.error(request,"you does not have acess to use this")
    #     logout(request)
    #     return redirect('home')

def handleroom(request):
    # if request.user.is_staff and request.user.is_authenticated:
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
  
def postattendance(request, room_no, session_no):
    
    a=Teacher.objects.get(user=User.objects.get(username=request.user))
    r=Room.objects.get(room_no=room_no)
    print(a.room)
    if r !=a.room :
        messages.error(request,"please select the room number what you have been allocated")
        return redirect("room_display")
    # if request.user.is_staff and request.user.is_authenticated:
    room = Room.objects.get(room_no=room_no)
    session = Session.objects.get(session_no=session_no, Attendence=True)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, session_id=session_no, room_no=room_no)
        if form.is_valid():
            form.save_attendance(session)
            messages.success(request,"Attendance saved successfully!")
            return redirect('home')  # Redirect to a success page
    else:
        form = AttendanceForm(session_id=session.session_no, room_no=room_no)
    return render(request, 'components/postattendance.html', {'students': form})
    # else:
    #     messages.error(request,"you don't have acess to use this")
    #     logout(request)
    #     return redirect("home")
    



def room_display_review(request):
    # if request.user.is_staff and request.user.is_authenticated:
    context={}
    context["rooms"]=Room.objects.all()
    context["sessions"]=Session.objects.all()
    return render(request,"components/rooms_review.html",context)
    # else:
    #     messages.error(request,"you did not have access to use this")
    #     logout(request)
    #     return redirect("home")
    

def handle_review_room(request):
    # if request.user.is_staff and request.user.is_authenticated:
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

    # else:
    #     messages.error(request,"you does not have the permissions to use this")
    #     logout(request)
    #     return redirect("home")


def handle(request,room,session):
    # if request.user.is_staff and request.user.is_authenticated:
    a=Room.objects.get(room_no=room)
    b=Student.objects.filter(room=a)
    context={}
    context["room"]=a
    context["students"]=b
    
    f=Team.objects.filter(room=a,submitted=False)
    if len(f)==0:
        messages.success(request,"no teams left to post the marks")
        messages.success(request,"You have sucess fully posted the marks for all the teams")
        return redirect('home')
    
    context["teams"]=f
    sessio=Session.objects.get(session_no=session)
    
    if sessio.Attendence == True:
        context["session"]=sessio
        return render(request,'components/teams.html',context)
    else:
        messages.info(request,"Session not activated!")
        return redirect('home')  # Redirect to a success page
    
    # else:
    #     messages.error(request,"you does not have the permissions to use this")
    #     logout(request)
    #     return redirect("home")

 
def handle_team(request, session_no, room_no):
    # if request.user.is_authenticated and request.user.is_staff:
    team_id = request.POST.get('team')
    redirect_url = reverse('postmarks', args=(session_no, room_no, team_id))
    return redirect(redirect_url)
    # else:
    #     messages.error(request,"you don't have the acess to use this")
    #     logout(request)
    #     return redirect("home")


def postmarks(request, session_no, room_no, team_name):
       
    a=Teacher.objects.get(user=User.objects.get(username=request.user))
    if room_no != a.room.room_no:
        messages.error(request,"please choose alocated section")
        redirect('room_display_review')
    
    r = Room.objects.get(room_no=room_no)
    session = Session.objects.get(session_no=session_no, Attendence=True)
    if session == None:
        messages.error(request,"please post the attendence first")
        redirect('home')
        
    team = Team.objects.get(team_name=team_name)
    b=True
    a = Student.objects.filter(team=team)
    absent=[]
    for i in a:
        qw=Attendence.objects.get(room=r,student=i,session=session) 
        
        if qw.status == False or not qw:
            absent.append(i)
    rbs=Rubrics.objects.get(review_no=session_no)
    context = {}
    context['rubrics']=rbs.review_rubrics
    context["students"] = a
    # c=Attendence.objects.filter(room=r,status=True)
    if request.method == 'POST':
        for i in a:
            if i in absent:
                b=True
            else:
                b=False

            review_marks = request.POST["id_"+str(i.id)] if b ==True else 0
            review_remarks=request.POST["remarks_"+str(i.id)] if b==True else "You are absent to session"+session_no
            if Review.objects.filter(student=i, session=session, review_no=session_no, room=r).exists():
                messages.error(request,"updation of the marks is not possible")
                return redirect('handle',room=room_no,session=session_no)
                
            Review.objects.update_or_create(
                student=i,
                session=session,
                review_no=session.session_no,
                room=r,
                defaults={'review_marks': review_marks,'remarks':review_remarks}
            )
        team.submitted = True
        team.save()
        return redirect('handle',room=room_no,session=session_no)

    return render(request, 'components/postmarks.html', context=context)
    # else:
    #     messages.error(request,"you don't have acess to use this")
    #     return redirect('home')

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


def openSession(request):
    if request.user.is_superuser:
        Team.objects.update(submitted=False)
        return HttpResponse("Done")

def generate_report_Attendence(request,session):
    s=Session.objects.get(session_no=int(session))
    if s.Attendence !=True:
        messages.error(request,"Attendence not yet opened check after opened")
    context={}
    
    r=Room.objects.all()
    
    f=[]
    for i in r:
        c=[]
        Tcstu=len(Student.objects.filter(room=i))
        Present=len(Attendence.objects.filter(room=i,status=True,session=Session.objects.get(session_no=session)))
        Absent=Tcstu-Present
        c.append(i.room_no)
        c.append(Present)
        c.append(Absent)
        c.append("%.2f"%((Present/Tcstu)*100) if Tcstu > 0 else 0)
        f.append(c)
    context["rooms"]=f
    return render(request,'components/attendancereport.html',context)


def genmarks(request,session):
    s=Session.objects.get(session_no=int(session))
    if s.Review != True:
        messages.error(request,"Review not yet opened check after opened")
    context={}
    r=Room.objects.all()
    
    f=[]
    for i in r:
        c=[]
        Tcstu=len(Student.objects.filter(room=i))
        Present=len(Review.objects.filter(room=i,session=Session.objects.get(session_no=session)))
        Absent=Tcstu-Present 
        Abs_reviewmarks=len(Review.objects.filter(room=i,session=Session.objects.get(session_no=session),remarks="You are absent to session"+session))
        # the people whose form didn't get filled ignored
        c.append(i.room_no)
        c.append(Present)
        c.append(Absent)
        c.append(Abs_reviewmarks)
        # c.append("%.2f"%((Present/Tcstu)*100) if Tcstu > 0 else 0)
        f.append(c)
    context["rooms"]=f
    return render(request,'components/Marksreport.html',context)


def add_users(request):
    try:
        if request.user.is_superuser:
            utils.add_students()
            messages.success(request,"Users added")
            return redirect('home')
        messages.error(request,"you does  not have the acess to do this")
        return redirect('home')
    except:
        messages.error(request,"csv not found")
        return redirect('home')
    
def add_faculty(request):
    try:
        if request.user.is_superuser:
            utils.add_faculty()
            messages.success(request,"Users added")
            return redirect('home')
        messages.error(request,"you does  not have the acess to do this")
        return redirect('home')
    except:
        messages.error(request,"csv not found")
        return redirect('home')

def add_rooms(request):
    try:
        if request.user.is_superuser:
            utils.add_rooms()
            messages.success(request,"Users added")
            return redirect('home')
        messages.error(request,"you does  not have the acess to do this")
        return redirect('home')
    except:
        messages.error(request,"csv not found")
        return redirect('home')


# # data entry
# def add_stu(request):
#     try:
#         if request.user.is_superuser:
#             with open('static/csvs/smap.csv', 'r') as csv_file:
#                 csv_reader = csv.reader(csv_file)
#                 for row in csv_reader:
#                     print(row)
#                     team_name = str(row[2]) + "-" + str(row[0])
#                     print(team_name)
                    
#                     room = Room.objects.get(room_no=str(row[1]))
#                     print(room)
                    
#                     a = Team.objects.create(room=room, team_name=team_name)
#                     print(a)
                    
#                     s1 = User.objects.filter(username=row[2]).first()
#                     print(s1)
                    
#                     s2 = User.objects.filter(username=row[3]).first()
#                     print(s2)
                    
#                     s3 = None
#                     if row[4]!='\xa0':
#                         s3 = User.objects.filter(username=row[4]).first()
#                         print(s3)
                    
#                     if s1:
#                         Student.objects.create(user=s1, id=int(row[2]), name=str(row[2]), team=a, room=room).save()
#                     if s2:
#                         Student.objects.create(user=s2, id=int(row[3]), name=str(row[3]), team=a, room=room).save()
#                     if s3:
#                         Student.objects.create(user=s3, id=int(row[4]), name=str(row[4]), team=a, room=room).save()

#     except Exception as e:
#         print("An error occurred:", str(e))


#     return HttpResponse("hurray")