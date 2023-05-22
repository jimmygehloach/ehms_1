from . import views
from django.urls import path

from .views import (
    ReceptionListView, ReceptionDashboardTemplateView, ReceptionProfileTemplateView, ReceptionNewMSDetailTemplateView
)

app_name = "receptions"
urlpatterns = [
    path(route="list/", view=ReceptionListView.as_view(), name="list"),
    path(route="token/", view=views.reception_token_request_page, name="token"),
    path(route="dashboard/", view=ReceptionDashboardTemplateView.as_view(), name="dashboard"),
    path(route="profile/", view=ReceptionProfileTemplateView.as_view(), name="profile"),
    path(route="patient/<int:p_id>/medical_session/<int:ms_id>", view=ReceptionNewMSDetailTemplateView.as_view(),
         name="ms-detail")
]
