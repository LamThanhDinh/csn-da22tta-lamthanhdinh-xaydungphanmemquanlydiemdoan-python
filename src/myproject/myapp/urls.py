from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('home', views.home, name='home'),
    path('user/', views.user_list, name='user_list'),
    path('advior/', views.advior_list, name='advior_list'),
    path('exam/', views.exam_list, name='exam_list'),
    path('edit/<str:ma_so_sinh_vien>/', views.edit_user, name='edit_user'),  # Sửa sinh viên
    path('delete/<str:ma_so_sinh_vien>/', views.delete_user, name='delete_user'),  # Xóa sinh viên
    path('advior/edit/<str:id>/', views.edit_advior, name='edit_advior'),  # Sửa giảng viên
    path('advior/delete/<str:id>/', views.delete_advior, name='delete_advior'),  # Xóa giảng viên
    path('exam/edit/<str:idstudent>/', views.edit_exam, name='edit_exam'),  # Sửa kết quả
    path('exam/delete/<str:idstudent>/', views.delete_exam, name='delete_exam'),  # Sửa kết quả
    path('export_results/', views.export_results, name='export_results'),#thống kê
    path("login/", views.ad_login, name="login"),
    path("logout/", views.ad_logout, name='logout'),
]

