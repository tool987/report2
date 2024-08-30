from django.urls import path
from .views import customuserloginview,registerviews,homeview,forgetpassword,change,userprofile,logout_view,addemployee,eachview,updateeachview,delateview,EmployeAttendence,Attendance_Out,Employeeview,applicantview,applicantrequestview,successview,leavview,leave_out



urlpatterns = [
    path('',homeview.as_view(),name = 'home'),
    path('login/',customuserloginview.as_view(),name='login'),
    path('userprofile/',userprofile.as_view(),name='userprofile'),
    path('logout/',logout_view,name='logout'),
    path('forget-password/',forgetpassword,name='forget-password'),
    path('changepassword/<token>/',change,name='changepassword'),
    path('register/',registerviews.as_view(),name='register'),
    path('addemployee/',addemployee.as_view(),name='addemployee'),
    path('view/<int:pk>/',eachview.as_view(),name='eachprofile'),
    path('update/<int:pk>/',updateeachview.as_view(),name='update'),
    path('delete/<int:pk>/',delateview.as_view(),name='delete'),
    path('attendence/', EmployeAttendence.as_view(), name='attendence'),
    path('attendence/<int:pk>', Attendance_Out.as_view(), name='attendence_out'),
    path('employee/',Employeeview.as_view(),name='employee'),
    path('applicant/',applicantview.as_view(),name='applicant'),
    path('recuriment/',applicantrequestview.as_view(),name='recur'),
    #  path('success/',successview.as_view(),name='recu'),
    path('leave/',leavview.as_view(),name='leave'),
    path('leaveout/<int:id>/',leave_out.as_view(),name='leaveout'),

]
