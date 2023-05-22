from django.urls import path
from . import views
from .views import HospitalQueryInboxListView

app_name = 'queries'
urlpatterns = [
    path(
        route='inbox/hospital',
        view=HospitalQueryInboxListView.as_view(),
        name='hospital-inbox'
    ),
    path(
        route='inbox/<int:pk>/practitioner',
        view=views.practitioner_query_inbox,
        name='practitioner-inbox'
    )
]
