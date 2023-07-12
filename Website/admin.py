from django.contrib import admin
from .models import Announcement, Complaints, Room, Team, Student, Session, Attendence, Review, Teacher

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_no']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'room']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'room', 'team']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_no', 'Attendence', 'Review']


@admin.register(Attendence)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_no', 'session', 'review_marks', 'student']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']



# Register your models here.


admin.site.register(Announcement)
admin.site.register(Complaints)

