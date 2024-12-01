from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from user.urls import urlpatterns

urlpatterns = [
    path('', views.college_portal, name='home'),

    path('about/us/', views.about, name='about'),

    path('privacy/', views.privacy, name='privacy'),
    path('termandcondition/', views.terms, name='terms'),

    path('soon/#/', views.soon, name='soon'),


    # Default denied access page if no role is found
    path('denied/', views.denied, name="denied"),

    path('success/', views.success, name="success"),

    path('teacher/student_list', views.student_list, name='student_list'),
    path('export_students/', views.export_students_to_excel, name='export_students'),  # Export to Excel
    
]
