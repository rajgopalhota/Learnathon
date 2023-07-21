from django.contrib import admin
from .models import Announcement, Complaints, Room, Team, Student, Session, Attendence, Review, Teacher, TimeTable
from import_export.admin import ImportExportModelAdmin

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_no']

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ['team_name', 'room']

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'team']

@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    list_display = ['session_no', 'Attendence', 'Review']

@admin.register(Attendence)
class AttendanceAdmin(ImportExportModelAdmin):
    list_display = ['student', 'session', 'status']

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ['review_no', 'session', 'review_marks', 'student', 'remarks']

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name']

# Register your models here.
admin.site.register(Announcement)
admin.site.register(Complaints)
admin.site.register(TimeTable)
