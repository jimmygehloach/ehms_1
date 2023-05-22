from . import views
from django.urls import path

app_name = "user_requests"
urlpatterns = [
    path("api/create/", view=views.user_request_create, name="create"),
]
