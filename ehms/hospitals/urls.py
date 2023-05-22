from django.urls import path
from . import views
from .views import ActivityListView, HospitalMedicalSessionListView, HospitalProfileTemplateView

app_name = 'hospitals'
urlpatterns = [
    path(route='dashboard/', view=views.hospital_dashboard, name='hospital-dashboard'),
    path(route='profile/', view=HospitalProfileTemplateView.as_view(), name='profile'),
    path(route='activities/', view=ActivityListView.as_view(), name='activities'),
    path(route='medical_sessions/', view=HospitalMedicalSessionListView.as_view(), name='hospital-medical-sessions')
]
