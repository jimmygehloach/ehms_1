from . import views
from django.urls import path

app_name = "family_tree"
urlpatterns = [
    path("relation", view=views.patient_relation, name="relation"),
    path("relation/<int:pk>/", view=views.relation_fetch, name="fetch"),
]
