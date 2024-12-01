from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import role

urlpatterns = [
    # Redirect to role-based dashboard
    path('role_direct/', role.role_redirect, name="role"),

    path('login/', views.login, name='login'),

    path('enrollment/new/student/', views.enroll, name='enrollment'),

    path('contact/', views.contact, name='contact'),

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('approve_student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

    path('teacher/profile/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('student/profile', views.student_profile, name='student_profile'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    path('admin/register/', views.register_teacher, name='register_teacher'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

]