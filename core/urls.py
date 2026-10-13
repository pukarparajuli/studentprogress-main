from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/<str:role>/', views.role_login, name='role_login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-grade/', views.add_grade, name='add_grade'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('student-report/<int:student_id>/', views.student_report, name='student_report'),
    path('export-pdf/<int:student_id>/', views.export_report_pdf, name='export_pdf'),
    path('about/', views.about_view, name='about'),
    path('features/', views.features_view, name='features'),
    path('contact/', views.contact_view, name='contact'),
    path('support/', views.support_view, name='support'),
    path('teacher-reports/', views.teacher_reports, name='teacher_reports'),
    path('ai-insights/', views.ai_insights, name='ai_insights'),
    path('student-ai-analysis/<int:student_id>/', views.student_ai_analysis, name='student_ai_analysis'),
]