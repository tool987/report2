from django.contrib import admin
from .models import User,Role,Employee,Departement,Attendance,Leave,Recruitment

# Register your models here.
admin.site.register(User),
admin.site.register(Role),
admin.site.register(Employee),
admin.site.register(Departement),
admin.site.register(Attendance),
admin.site.register(Leave),
admin.site.register(Recruitment),

