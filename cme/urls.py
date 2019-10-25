from django.urls import path,re_path

from . import views

app_name = 'cme'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:urlshortOrganization>/events/', views.events, name='events'),
    path('events/<slug:urlshortEvents>', views.event_sessions, name='event_sessions'),
    path('event_Evaluation/<slug:urlshortEvents>', views.event_evaluation, name='event_evaluation'),
    path('speaker_evaluations_all/<slug:urlshortEvents>', views.speaker_evaluations_all, name='speaker_evaluations_all'),
    path('session_evaluation/<int:pk>', views.session_evaluation, name='session_evaluation'),
    path('SAMQuestion/<int:pk>/0', views.samQuestionSubmission, name='samQuestion'),
    re_path('SAMQuestion/(?P<pk>(\d+))/(?P<questionnum>(\d+))/$', views.samQuestionSubmission, name='samQuestion'),
    # path('SAMQuestion/(?P<pk>(\d+))/0$', views.samQuestionSubmission, name='samQuestion'),


]