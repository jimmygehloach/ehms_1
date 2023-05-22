from . import views
from django.urls import path

from .views import WardPractitionerAPIView

app_name = "core"
urlpatterns = [
    path("", view=views.common_home_page, name="home"),
    path(route="api/ward/practitioner/list/", view=WardPractitionerAPIView.as_view(), name="ward-practitioners"),
]
