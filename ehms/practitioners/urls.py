from . import views
from django.urls import path

from .views import PractitionerHospitalListView

app_name = "practitioners"
urlpatterns = [
    path(route="", view=PractitionerHospitalListView.as_view(), name="list"),
    path(route="token", view=views.practitioner_token_request_page, name="token"),
    path(route="dashboard/", view=views.practitioner_dashboard, name="practitioner-dashboard"),
    path(route="<int:pk>/medical-sessions/", view=views.practitioner_medical_session_list,
         name="practitioner-medical-sessions"),
    path(route="<int:pk>/", view=views.practitioner_profile_page, name="detail"),
]
