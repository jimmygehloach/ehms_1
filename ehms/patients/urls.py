from . import views
from django.urls import path

from .views import PatientListView, PatientReceptionListView

app_name = "patients"
urlpatterns = [
    path("", view=PatientListView.as_view(), name="list"),
    path("reception/list/", view=PatientReceptionListView.as_view(), name="reception-list"),
    path("create/", view=views.patient_create, name="create"),
    path("search/", view=views.patient_search_list, name="search"),
    path("<int:pk>/", view=views.patient_detail, name="detail"),
    path("search/keyword/", view=views.patient_search_by_keyword, name="keyword"),
    path("search/advanced/", view=views.patient_advanced_search_list, name="advanced"),
    path("death-record/<int:pk>", view=views.patient_death_record, name="death-record"),
    path("<int:pk>/address/<int:pa>/edit/", view=views.edit_patient_address, name="edit-address"),
]
