from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.views import APIView

from ehms.activities.views import create_activity
from ehms.addresses.models import Country, Region, District, Town, Postcode
from ehms.addresses.serializers import RegionSerializer, DistrictSerializer, TownSerializer, PostcodeSerializer
from ehms.core.decorators import logged_in_user, fetch_user_details
from ehms.core.utils import check_activity_level
from ehms.hospitals.models import Hospital
from ehms.nurses.models import Nurse
from ehms.patients.models import Patient
from ehms.practitioners.models import Practitioner


@login_required
@logged_in_user(['country level'])
@fetch_user_details
def country_dashboard(request):  # TODO: convert this later on to some class Based View
    create_activity(request, 'GET', _('Country dashboard is fetched.'), check_activity_level(request))
    total_patients = Patient.objects.filter(patient_belong_to_address__country=request.country).count()
    total_nurses = Nurse.objects.filter(country=request.country).count()
    total_practitioners = Practitioner.objects.filter(country=request.country).count()
    total_hospitals = Hospital.objects.filter(country=request.country).count()

    data_send = {
        'title': 'Dashboard | Country',
        'total_hospitals': total_hospitals,
        'total_practitioners': total_practitioners,
        'total_nurses': total_nurses,
        'total_patients': total_patients,
    }
    return render(request, "addresses/country-dashboard.html", data_send)


@login_required
@logged_in_user(['region level'])
@fetch_user_details
def region_dashboard(request):  # TODO: convert this later on to some class Based View
    create_activity(request, 'GET', _('Region dashboard is fetched.'), check_activity_level(request))
    total_patients = Patient.objects.filter(patient_belong_to_address__region=request.region,
                                            patient_belong_to_address__country=request.country).count()
    total_nurses = Nurse.objects.filter(region=request.region, country=request.country).count()
    total_practitioners = Practitioner.objects.filter(region=request.region, country=request.country).count()
    total_hospitals = Hospital.objects.filter(region=request.region, country=request.country).count()

    data_send = {
        'title': 'Dashboard | Country',
        'total_hospitals': total_hospitals,
        'total_practitioners': total_practitioners,
        'total_nurses': total_nurses,
        'total_patients': total_patients,
    }
    return render(request, "addresses/region-dashboard.html", data_send)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class RegionAPIView(APIView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def post(self, request):
        country_id = request.data.get('country_id')

        try:
            country = Country.objects.get(id=country_id, status='active')
        except Country.DoesNotExist:
            return Response({'message': 'Country not found'}, status=HTTP_404_NOT_FOUND)

        regions = Region.objects.filter(country=country, status='active')
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class DistrictAPIView(APIView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def post(self, request):
        country_id = request.data.get('country_id')
        region_id = request.data.get('region_id')

        try:
            country = Country.objects.get(id=country_id, status='active')
            region = Region.objects.get(id=region_id, country=country, status='active')
        except Country.DoesNotExist:
            return Response({'message': 'Country not found'}, status=HTTP_404_NOT_FOUND)
        except Region.DoesNotExist:
            return Response({'message': 'Region not found'}, status=HTTP_404_NOT_FOUND)

        districts = District.objects.filter(country=country, region=region, status='active')
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class TownAPIView(APIView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def post(self, request):
        country_id = request.data.get('country_id')
        region_id = request.data.get('region_id')
        district_id = request.data.get('district_id')

        try:
            country = Country.objects.get(id=country_id, status='active')
            region = Region.objects.get(id=region_id, country=country, status='active')
            district = District.objects.get(id=district_id, country=country, region=region, status='active')
        except Country.DoesNotExist:
            return Response({'message': 'Country not found'}, status=HTTP_404_NOT_FOUND)
        except Region.DoesNotExist:
            return Response({'message': 'Region not found'}, status=HTTP_404_NOT_FOUND)
        except District.DoesNotExist:
            return Response({'message': 'District not found'}, status=HTTP_404_NOT_FOUND)

        towns = Town.objects.filter(country=country, region=region, district=district, status='active')
        serializer = TownSerializer(towns, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class PostcodeAPIView(APIView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def post(self, request):
        country_id = request.data.get('country_id')
        region_id = request.data.get('region_id')
        district_id = request.data.get('district_id')
        town_id = request.data.get('town_id')

        try:
            country = Country.objects.get(id=country_id, status='active')
            region = Region.objects.get(id=region_id, country=country, status='active')
            district = District.objects.get(id=district_id, country=country, region=region, status='active')
            town = Town.objects.get(
                id=town_id, country=country, region=region, district=district, status='active')
        except Country.DoesNotExist:
            return Response({'message': 'Country not found'}, status=HTTP_404_NOT_FOUND)
        except Region.DoesNotExist:
            return Response({'message': 'Region not found'}, status=HTTP_404_NOT_FOUND)
        except District.DoesNotExist:
            return Response({'message': 'District not found'}, status=HTTP_404_NOT_FOUND)
        except Town.DoesNotExist:
            return Response({'message': 'Town not found'}, status=HTTP_404_NOT_FOUND)

        postcodes = Postcode.objects.filter(
            country=country, region=region, district=district, town=town, status='active')
        serializer = PostcodeSerializer(postcodes, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)
