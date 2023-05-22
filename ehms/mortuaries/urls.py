from django.urls import path
from . import views

app_name = 'mortuaries'
urlpatterns = [
    path(route='', view=views.mortuaries_list, name='home'),
    path(route='add/<int:pk>', view=views.add_patient_to_mortuary, name='add'),
    path(route='list/<int:pk>', view=views.patients_in_mortuary, name='list'),
    path(route='list/<int:pk>/<int:pt>', view=views.patients_detail_in_mortuary, name='patient-detail'),
    path(route='release/<int:pk>/<int:pt>', view=views.patient_release_from_mortuary, name='release'),
    path(route='detail/<int:pk>', view=views.mortuary_detail, name='detail'),

]
