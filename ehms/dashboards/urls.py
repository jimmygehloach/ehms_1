from . import views
from django.urls import path

app_name = "dashboards"
urlpatterns = [
    path("country-level/", view=views.country_level_dashboard, name="country-level"),
    path("region-level/", view=views.region_level_dashboard, name="region-level"),
    path("state-level/", view=views.state_level_dashboard, name="state-level"),
    path("district-level/", view=views.district_level_dashboard, name="district-level"),
    path("hospital-level/", view=views.hospital_level_dashboard, name="hospital-level"),
    path("practitioner-level/", view=views.practitioner_level_dashboard, name="practitioner-level"),
    path("nurse-level/", view=views.nurse_level_dashboard, name="nurse-level"),
    path("reception-level/", view=views.reception_level_dashboard, name="reception-level")
    # path("logout/", view=views.logout_user, name="logout"),
]
