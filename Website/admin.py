from django.contrib import admin
from .models import Announcement, Complaints, Room, Team, Student, Session, Attendence, Review, Teacher, TimeTable,Rubrics
from import_export.admin import ImportExportModelAdmin

admin.site.site_header = 'KL CSE-H Learnathon/Hackathon Administration (1)'
admin.site.site_title = 'KL CSE-H Learnathon/Hackathon Administration (1)'
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_no']
    # list_editable=['room_no']
    pass

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ['team_name', 'room']
    list_filter=['team_name','room']
    search_fields=['team_name']
    pass

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'attendance','score']
    list_filter=['team']
    search_fields=['id']
    pass

@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    list_display = ['session_no', 'Attendence', 'Review']
    list_filter=['session_no','Review']
    list_editable=['Attendence','Review']
    pass
    
@admin.register(Attendence)
class AttendanceAdmin(ImportExportModelAdmin):
    list_display = ['student', 'session', 'status']
    list_filter=['session','status','student']
    search_fields=['student__id']
    list_editable=['status']
    pass

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ['review_no', 'session', 'review_marks', 'student', 'remarks']
    list_filter =['review_no','session','room']
    search_fields=['student__id']
    pass

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name','room']
    list_filter=['room']
    search_fields=['id']
    pass


@admin.register(Rubrics)
class Rubrics(ImportExportModelAdmin):
    list_display=['review_no','review_rubrics']
# Register your models here.
admin.site.register(Announcement)
admin.site.register(Complaints)
admin.site.register(TimeTable)

