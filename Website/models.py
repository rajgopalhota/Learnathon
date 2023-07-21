from xmlrpc.client import DateTime
from django.db import models
import datetime
from django.contrib.auth.models import User,AbstractBaseUser
from django.utils.timezone import now
from datetime import date

# Create your models here.


class Announcement(models.Model):
    sno = models.AutoField(primary_key=True)
    notice = models.TextField(default="")
    rev1 = models.TextField(default="")
    rev2 = models.TextField(default="")
    rev3 = models.TextField(default="")
    rev4 = models.TextField(default="")
    source = models.TextField(null=True)
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.notice+" at:"+str(self.timestamp))


class Complaints(models.Model):
    sno = models.AutoField(primary_key=True)
    teamno = models.TextField()
    idno = models.TextField()
    roomno = models.TextField()
    query = models.TextField()
    msg = models.TextField()
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return 'By: '+self.idno+' Room: '+self.roomno+' Issue: '+self.query

class Room(models.Model):
    
    room_no=models.CharField(max_length=20,unique=True,default=None)
    def __str__(self):
        return str(self.room_no)
# Create your models here.

class Team(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    team_name=models.CharField(max_length=20)
    submitted=models.BooleanField(default=False)
    def __str__(self):
        return str(self.team_name)
    def room_no(self):
        return self.room
    
class Student(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    id=models.BigIntegerField(primary_key=True)
    name=models.CharField(max_length=20,default="")
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    # team = models.ForeignKey(Team,on_delete=models.CASCADE)
   
    @property
    def attendance(self):
        sras=Attendence.objects.filter(student=self)
        att=sras.filter(status=False).count()
        total=sras.count()
        if total == 0:
            return "0%"
        return str((att / total)*100)+'%'
    
    @property
    def score(self):
        scrs=Review.objects.filter(student=self)
        score=0
        for s in scrs:
            score+=int(s.review_marks)
        return score
    
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        self.room=self.team.room
        super(Student, self).save(*args, **kwargs)
    
class Session(models.Model):
    session_no=models.IntegerField(primary_key=True,default=None)
    Attendence=models.BooleanField(null=True)
    Review=models.BooleanField(null=True)
    # rubrics=models.CharField(max_length=500,null=False,default=" ")
    
    def __str__(self):
        return str(self.session_no)

class Attendence(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE,default=None)
    
    @property
    def stu_id(self):
        return str(self.student.id)
    
    def __str__(self):
        return str(self.student.id)
    
    
class Review(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE,default=None)
    review_no=models.IntegerField(default=0)
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    review_marks = models.IntegerField(default=0)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    remarks=models.CharField(max_length=500,default="")
    # attendence= models.ForeignKey(Attendence,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.review_no)

class Teacher(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="")
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=20,default="")
    room=models.ForeignKey(Room,on_delete=models.CASCADE,default="")
    def __str__(self):
        return str(self.id)


# Timetable
class TimeTable(models.Model):
    text = models.CharField(max_length=30, unique=False)
    pdf = models.FileField(upload_to='timetables')
    
class Rubrics(models.Model):
    review_no=models.IntegerField(primary_key=True,default=0)
    review_rubrics=models.CharField(max_length=500)