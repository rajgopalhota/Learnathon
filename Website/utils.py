from django.contrib.auth.models import User
import csv
from .models import Room,Team,Student
def add_students():
    with open('static/csvs/student.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            username = row[0]
            password = row[1]
            email = f"{username}@kluniversity.in"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password)
            # print(row)

def add_faculty():
    with open('static/csvs/faculty.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            username = row[0]
            password = row[2]
            email = f"{username}@kluniversity.in"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password, is_staff = True)
            # print(row)

def add_rooms():
    with open('static/csvs/rooms.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            room_no = row[0]
            # print(row)
            if not Room.objects.filter(room_no=room_no).exists():
                Room.objects.create(room_no=room_no).save()


def add_Teams():
    with open('static/csvs/teams.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            room = Room.objects.get(room_no=row[0])
            team_name=row[1]
            
            # print(row)
            if not Team.objects.filter(room=room,team_name=team_name).exists():
                Team.objects.create(room=room,team_name=team_name).save()

def add_stu():
    with open('static/csvs/teams.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            stu = User.objects.get(username=str(row[0]))
            id=stu.username
            name=stu.username
            team=Team.objects.get(team_name=str(row[1]))
            room=team.room
            # print(row)
            if not Student.objects.filter(room=room,team=team,user=stu,id=id,name=name).exists():
                Student.objects.create(room=room,team=team,user=stu,id=id,name=name).save()

