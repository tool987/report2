
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from usermngt.models import User,Role,Employee,Departement,Attendance,Leave,Recruitment
from .forms import usercreationform,AttendanceForm,LeaveForm,RecruitmentForm
from django.views.generic import FormView,ListView,TemplateView,CreateView,DetailView,UpdateView,DeleteView
from django.views.generic.base import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .email import send_message_toemail
from django.urls import reverse_lazy
import time
from django.utils import timezone
from django.db.models import Q

# Create your views here.

class customuserloginview(LoginView):
    template_name = 'usermngt/login.html'
    fields = '__all__'

    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('userprofile')
    
class homeview(TemplateView):
   
    template_name = 'usermngt/home.html'
    # def get(self, request,*args,**kwargs):
    #     admin= User.objects.get(username=request.POST.username)
    #     return admin


class userprofile(LoginRequiredMixin,ListView):
    model = User
    context_object_name = 'userprofile'
    template_name ='usermngt/user_profile.html'
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['adminstrator'] = User.objects.all().count()
        context['employee'] = Employee.objects.all()
        context['departement'] = Departement.objects.all().count()

        return context



def logout_view(request):
    logout(request)
    return redirect('home')



class addemployee(CreateView):
    model = Employee
    fields = '__all__'
    template_name = 'usermngt/addemployee.html'
   
    success_url = "../userprofile"
    
    
class eachview(DetailView):
    model = Employee
    template_name = 'usermngt/edit.html'
    context_object_name = 'each'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        each= Employee.objects.filter(id=self.kwargs.get('pk'))
        return context

class updateeachview(UpdateView):
    model = Employee
    template_name= 'usermngt/update.html'
    fields = '__all__'
    context_object_name='man'
    success_url ="../../userprofile"


class delateview(DeleteView):
    model= Employee
    template_name= 'usermngt/delete.html'
    success_url ='../../userprofile'


class registerviews(LoginRequiredMixin,FormView):
    template_name = 'usermngt/login.html'
    form_class = usercreationform
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
         user = form.save()
         if user is not None:
              login(self.request,user)
              return super(registerviews,self).form_valid(form)
                       
    
def change(request,token):
    userobject = User.objects.filter(forgetten_password_token = token).first()

    try:
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

        if user_id is None:
            return redirect('changepassword/{token}/')
        
        if new_password != confirm_password:
            
            return redirect('changepassword/{token}/')

        userobj = User.objects.get(id =user_id)
        userobj.set_password(new_password)
        userobj.save()
        return redirect('login')
    except Exception as e:
        print(e)
    context ={'user_id':userobject.id}

    return render(request,'usermngt/change_password.html',context)

import uuid
def forgetpassword(request):
    try:
        if request.method =='POST':
            email = request.POST.get('email')

            if not User.objects.filter(email=email):
                messages.success(request,'dose not exist')
                return redirect('forget-password')
            userobjects= User.objects.get(email=email)
            token = str(uuid.uuid4())
            userobjects.forgetten_password_token = token
            userobjects.save()
            
            send_message_toemail(userobjects.email,token,userobjects.username)
            
    except Exception as e:
        print(e)        
        
    return render(request,'usermngt/forget_password.html',{})              

# def EmployeAttendence(request):
#     model = Atttendance
#     form = attendenceform()
#     if request.method == 'POST':
#         form = attendenceform(request.POST)
#         if form.is_valid():
#            form.save()
#         return form
#     context ={"form":form}
#     return render(request,'usermngt/attendence.html',context)


class EmployeAttendence(LoginRequiredMixin,CreateView):
    model = Attendance
    form_class = AttendanceForm
    login_url = 'login'
    template_name = 'usermngt/attendence.html'
    success_url = '/attendence'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.localdate()
        pstaff = Attendance.objects.filter(Q(status='PRESENT') & Q (date=timezone.localdate())) 
        context['present_staffers'] = pstaff
        return context
    
class Attendance_Out(LoginRequiredMixin,View):
    login_url = 'login'

    def get(self, request,*args, **kwargs):
      
       user=Attendance.objects.get(Q(staff__id=self.kwargs['pk']) & Q(status='PRESENT')& Q(date=timezone.localdate()))
       user.last_out=timezone.localtime()
       user.save()
       return redirect('/attendence')   


class Employeeview(ListView):
    model = Employee
    context_object_name = 'employee'
    template_name ='usermngt/Employee.html'


class leavview(CreateView):
    model = Leave
    form_class=LeaveForm
    template_name = 'usermngt/leave.html'
    success_url = '/leaveout'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['start'] = timezone.localdate()
        context['leave'] = Leave.objects.filter(Q(status='unapproved'))
        context['employee']= Employee.objects.all()
class leave_out(View):

    def get(self,request,*args,**kwargs):
        user = Employee.objects.get


class applicantview(ListView):
    model = Recruitment
    context_object_name = 'applicant'
    template_name='usermngt/applicant_list.html'
    



class applicantrequestview(CreateView):
    model = Recruitment
    form_class = RecruitmentForm
    template_name = 'usermngt/applicant_request.html'
    success_url = '/recuriment'

class successview(View):
    # template_name='usermngt/success.html'
    success_url = '/recuriment'

    

        