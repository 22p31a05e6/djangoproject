from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),

    # Dashboards
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('unknown/', views.unknown_role_view, name='unknown_role'),

    # Logout
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
