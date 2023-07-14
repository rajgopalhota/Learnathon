from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path("login", views.signin, name="login"),
    path("logout", views.signout, name="logout"),
    path('marksheets', views.marksheets, name='marksheets'),
    path('timetable', views.timetable, name='timetable'),
    path('announcements', views.announcements, name='announcements'),
    path('reviews', views.reviews, name='reviews'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path("room/<room_no>",views.handleroom,name="room"),
    path("room_display",views.room_display,name="room_display"),
    path("handle_room",views.handleroom,name="handle_room"),
    path('postattendance/<room_no>/<session_no>', views.postattendance, name='postattendence'),
    path('room_display_review',views.room_display_review,name='room_display_review'),
    path("handle_review_room",views.handle_review_room,name="handle_review_room"),
    path("handle_team/<session_no>/<room_no>",views.handle_team,name="handle_team"),
    path("postmarks/<session_no>/<room_no>/<team_name>",views.postmarks,name="postmarks")
    
]
