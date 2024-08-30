from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime
# Create your models here.
class Role(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title
    

class User(AbstractUser):
    username = models.CharField(unique=True,max_length=200)
    password = models.CharField(max_length=200)
    forgetten_password_token =models.CharField(max_length=255,null=True,blank=True)
    photo = models.ImageField(null=True,blank=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username

class Departement(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class Base(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=16,null=True,blank=True,
        validators= [RegexValidator(r'^\d\d\d\d-\d\d-\d\d\d\d$')])
    email = models.EmailField(unique=True)
    photo = models.ImageField(null=True,blank=True)

    class Meta:
        abstract = True


class Employee(Base):
    class gender(models.TextChoices):
        male='MALE'
        female='FEMALE'
        
    
    gender = models.CharField(max_length=10,choices=gender.choices)
    departement = models.ForeignKey(Departement,on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    month_salary = models.FloatField()
    enrollment_date = models.DateTimeField(auto_now_add=True)
    account_number =models.IntegerField()

    class Meta:
        ordering =['-enrollment_date']
    

    class employemanager(models.Manager):
        pass

    # def get_absolute_url(self,*args,**kwargs):
    #     return reverse('',args[self.id])
        

    def __str__(self):
        return self.first_name

class Application(Base):
    
     
    def __str__(self):
        return self.first_name


class Attendance(models.Model):
    STATUS = (('PRESENT', 'PRESENT'), ('ABSENT', 'ABSENT'),('UNAVAILABLE', 'UNAVAILABLE'))
    date = models.DateField(auto_now_add=True)
    first_in = models.TimeField()
    last_out = models.TimeField(null=True)
    status = models.CharField(choices=STATUS, max_length=15 )
    staff = models.OneToOneField(Employee,on_delete=models.CASCADE,null=True)

    def save(self,*args, **kwargs):
        self.first_in = timezone.localtime()
        super(Attendance,self).save(*args, **kwargs)
    
    # def __str__(self):
    #     return 'Attendance -> '+str(self.date) + ' -> ' + str(self.staff)
    


class Leave (models.Model):
    STATUS = (('approved','APPROVED'),('unapproved','UNAPPROVED'),('decline','DECLINED'))
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    start = models.CharField(blank=False, max_length=15)
    end = models.CharField(blank=False, max_length=15)
    status = models.CharField(choices=STATUS,  default='Not Approved',max_length=15)

    def __str__(self):
        return self.employee + ' ' + self.start

class Recruitment(models.Model):
    first_name = models.CharField(max_length=25)
    last_name= models.CharField(max_length=25)
    position = models.CharField(max_length=15)
    email = models.EmailField(max_length=25)
    phone = models.CharField(max_length=11)

    # def __str__(self):
    #     return self.first_name +' - '+self.position
