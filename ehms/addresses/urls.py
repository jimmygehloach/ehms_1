from django.urls import path
from . import views
from .views import RegionAPIView, DistrictAPIView, TownAPIView, PostcodeAPIView

app_name = 'addresses'
urlpatterns = [
    path(route='country/dashboard', view=views.country_dashboard, name='country-dashboard'),
    path(route='region/dashboard', view=views.region_dashboard, name='region-dashboard'),
    path(route='api/region', view=RegionAPIView.as_view(), name='api-region'),
    path(route='api/district', view=DistrictAPIView.as_view(), name='api-district'),
    path(route='api/town', view=TownAPIView.as_view(), name='api-town'),
    path(route='api/postcode', view=PostcodeAPIView.as_view(), name='api-postcode'),
]
