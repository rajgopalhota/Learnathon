from django import forms
from .models import Student, Attendence,Room,Session

class AttendanceForm(forms.Form):
    def __init__(self, *args, session_id=None, room_no=None, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        a=Room.objects.get(room_no=room_no)
        b=Session.objects.get(session_no=session_id)
        self.session=b
        students = Student.objects.filter(room=a)
        for student in students:
            self.fields[str(student.id)] = forms.BooleanField(label=student.name,required=False)

        # Retrieve the room object
        self.room = a

    def save_attendance(self, session):
        for field_name, field_value in self.cleaned_data.items():
            student_id = int(field_name)
            student = Student.objects.get(id=student_id)
            status = field_value if field_value else False

            Attendence.objects.update_or_create(
                student=student,
                session=self.session,
                room=self.room,
                defaults={'status': status}
            )

        # Handle unchecked checkboxes (mark attendance as absent)
        student_ids = [int(field_name) for field_name in self.fields.keys() if field_name != 'status']
        unchecked_students = Student.objects.filter(id__in=student_ids).exclude(id__in=self.cleaned_data.keys())
        for student in unchecked_students:
            Attendence.objects.get_or_create(
                student=student,
                session=self.session,
                room=self.room,
                defaults={'status': False}
            )
