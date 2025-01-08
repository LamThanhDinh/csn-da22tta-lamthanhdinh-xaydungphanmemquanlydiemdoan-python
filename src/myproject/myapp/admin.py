from django.contrib import admin
from .models import User, Advior, Exam

# Đăng ký model
admin.site.register(User)

admin.site.register(Advior)

admin.site.register(Exam)