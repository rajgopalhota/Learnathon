from django.contrib.auth.models import User
import csv

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
            