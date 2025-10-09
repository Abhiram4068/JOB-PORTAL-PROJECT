from django.db import models

# Create your models here.
class user_login(models.Model):
    login_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=225)
    password=models.CharField(max_length=225)

class user_registered(models.Model):
    user_registered_id=models.AutoField(primary_key=True)
    fullname=models.CharField(max_length=225)
    phno=models.CharField(max_length=10)
    email=models.CharField(max_length=225)
    place=models.CharField(max_length=225)
    district=models.CharField(max_length=225)
    country=models.CharField(max_length=225)
    pincode=models.CharField(max_length=225)
    login=models.ForeignKey(user_login,on_delete=models.CASCADE)
    
class saved_jobs(models.Model):
    saved_jobs_id=models.AutoField(primary_key=True)
    job_role=models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    job_location=models.CharField(max_length=255)
    job_salary=models.CharField(max_length=255)
    job_experience=models.CharField(max_length=255)
    login=models.ForeignKey(user_login,on_delete=models.CASCADE)

    
    
