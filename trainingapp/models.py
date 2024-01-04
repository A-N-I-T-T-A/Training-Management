from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.
class CustomUser(AbstractUser):
    user_type=models.CharField(default=1, max_length=10)

class department(models.Model):
    Dept=models.CharField(max_length=255)

class alldetails(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    dep=models.ForeignKey(department,on_delete=models.CASCADE,null=True)
    gender=models.CharField(max_length=255)
    Join_Date=models.DateField()
    phone=models.CharField(max_length=255)
    Image=models.ImageField(blank=True,upload_to="image/",null=True)
    Docs=models.FileField(blank=True,upload_to="documents/",null=True)
    status = models.CharField(max_length=20)

class trainers(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    details=models.ForeignKey(alldetails,on_delete=models.CASCADE,null=True)
class trainees(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    details=models.ForeignKey(alldetails,on_delete=models.CASCADE,null=True)
    trainer=models.ForeignKey(trainers,on_delete=models.CASCADE,null=True)
class trainerAttendence(models.Model):
    trainer=models.ForeignKey(trainers,on_delete=models.CASCADE,null=True)
    date=models.DateField()
    status=models.CharField(max_length=20,null=True)
class traineeAttendence(models.Model):
    trainee=models.ForeignKey(trainees,on_delete=models.CASCADE,null=True)
    date=models.DateField()
    status=models.CharField(max_length=20,null=True)
class trainerLeave(models.Model):
    trainer=models.ForeignKey(trainers,on_delete=models.CASCADE,null=True)
    reason=models.CharField(max_length=255)
    from_date=models.DateField()
    to_date=models.DateField()
    status=models.CharField(max_length=20,null=True)
class traineeLeave(models.Model):
    trainee=models.ForeignKey(trainees,on_delete=models.CASCADE,null=True)
    reason=models.CharField(max_length=255)
    from_date=models.DateField()
    to_date=models.DateField()
    status=models.CharField(max_length=20,null=True)

class schedule(models.Model):
    trainer=models.ForeignKey(trainers,on_delete=models.CASCADE,null=True)
    topic=models.CharField(max_length=255)
    from_date=models.DateField()
    time=models.TimeField()
    

class tasks(models.Model):
    trainer=models.ForeignKey(trainers,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=255)
    from_date=models.DateField()
    to_date=models.DateField()
class submittedTask(models.Model):
    task=models.ForeignKey(tasks,on_delete=models.CASCADE,null=True)
    trainee=models.ForeignKey(trainees,on_delete=models.CASCADE,null=True)
    desc=models.TextField(null=True)
    docs=models.FileField(blank=True,upload_to="documents/",null=True)
    delay=models.CharField(max_length=20,null=True)
    status=models.CharField(max_length=20,null=True,default='Pending')
class TrainerNotifications(models.Model):
    trainer=models.ForeignKey(trainers,on_delete=models.CASCADE,null=True)
    notify=models.CharField(max_length=255,null=True)
    link=models.URLField()
    read_status = models.BooleanField(default=False)
class TraineeNotifications(models.Model):
    trainee=models.ForeignKey(trainees,on_delete=models.CASCADE,null=True)
    notify=models.CharField(max_length=255,null=True)
    link=models.URLField()
    read_status = models.BooleanField(default=False)