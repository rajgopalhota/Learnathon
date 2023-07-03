from xmlrpc.client import DateTime
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Announcement(models.Model):
    sno = models.AutoField(primary_key=True)
    notice = models.TextField(default="Example notice....")
    source = models.TextField(null=True)
    timestamp = models.DateTimeField(default=now)


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

