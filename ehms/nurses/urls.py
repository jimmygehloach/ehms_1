from . import views
from django.urls import path

app_name = "nurses"
urlpatterns = [
    path(route="", view=views.nurses_in_hospital_list, name="list"),
    path(route="token", view=views.nurse_token_request_page, name="token"),
    path(route="dashboard/", view=views.nurse_dashboard, name="nurse-dashboard"),
    path(route="vital-sign-record/<int:pk>/", view=views.nurse_vital_sign_record, name="vital-sign-record"),
    path(route="vital-sign-record/detail/<int:pk>/", view=views.nurse_vital_sign_record_detail,
         name="vital-sign-record-detail"),
    path(route="intake-output-chart/<int:pk>/", view=views.nurse_intake_output_chart, name="intake-output-chart"),
    path(route="intake-output-chart/detail/<int:pk>/", view=views.nurse_intake_output_chart_detail,
         name="intake-output-chart-detail"),
    path(route="session-notes/<int:pk>/", view=views.nurses_notes, name="session-notes"),
    path(route="session-notes/detail/<int:pk>/", view=views.nurse_notes_detail, name="session-notes-detail"),
    path(route="<int:pk>/", view=views.nurse_profile_page, name="detail"),
]
