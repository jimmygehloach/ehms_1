from . import views
from django.urls import path

app_name = "medical_sessions"
urlpatterns = [
    path(route="", view=views.medical_session_list, name="list"),
    path(route="detail/<str:suid>/", view=views.medical_session_detail, name="detail"),
    path(route="new/", view=views.medical_session_create, name="new"),
    path(route="reception/new/", view=views.reception_medical_session_create, name="reception-new"),
]
