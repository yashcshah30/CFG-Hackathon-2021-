from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from . import views
urlpatterns = [
    #path('verify',views.sms,name="verification"),
    path('register_students',register_student,name='register_students'),
    path('register_mentors',register_mentor,name='register_mentors'),
    path('', user_login,name = 'login'),
    path('logout/', user_logout,name = 'Logout'),
    path('homepage/', homepage, name='homepage'),
    path('phase/',phase,name='phase'),
    path('phase/change-phase',change_phase,name='change-phase'),
    path('confirm_team/<int:pk>/', confirm_team, name='confirm-team'),
    path('phase/upload-images',uploadimage, name='upload-images'),
    path('comment/', post_comment, name='comment'),
    path('homepage_judge/', homepage_judge, name='homepage-judge'),
    path('phase/final-submission',final_submission,name='final-submission'),
    path('phase/final',final,name='final'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('display_reps/', views.graphs, name='display'),
    path('update_team_profile',update_team_profile,name="update_team_profile")
    #path('mentorList',mentorList, name='mentorList')
]

    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)