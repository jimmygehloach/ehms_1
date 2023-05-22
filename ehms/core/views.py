from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.views import APIView

from ehms.core.decorators import home_visit, logged_in_user
from ehms.medical_sessions.models import Ward
from ehms.core.serializers import WardPractitionerSerializer
from ehms.practitioners.models import Practitioner
from ehms.utils.helpers import UTL


@home_visit
def common_home_page(request):
    context = {
        'title': 'Home | EHMS',
    }
    return render(request, 'core/home.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level', 'reception level']), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class WardPractitionerAPIView(APIView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def post(self, request):
        UTL.custom_print('I am here ... .')
        ward_id = request.data.get('ward_id')

        try:
            ward = Ward.objects.get(id=ward_id, status='active')
        except Ward.DoesNotExist:
            return Response({'message': 'Ward not found'}, status=HTTP_404_NOT_FOUND)

        practitioners = Practitioner.objects.filter(ward__id=ward.id, status='active')
        serializer = WardPractitionerSerializer(practitioners, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)
