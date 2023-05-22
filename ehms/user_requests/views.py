from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from ehms.core.decorators import logged_in_user


@login_required
@logged_in_user(['hospital level'])
@csrf_protect
@api_view(['POST'])
def region_api_view(request):
    if request.method == 'POST':
        request.POST.get('description', None)
        request.FILES.get('document', None)

        

        # # we will get the country from the ajax call
        # country_id = request.POST.get('country_id', False)
        #
        # if is_valid_uuid(country_id):
        #     # check if country exists or not
        #     try:
        #         # check if exists or not
        #         country = Country.objects.get(status='active', pk=country_id)
        #     except Country.DoesNotExist:
        #         print(traceback.format_exc())
        #         return Response(None, HTTP_400_BAD_REQUEST)
        #
        #     if not data:
        #         return Response(None, HTTP_404_NOT_FOUND)
        #     else:
        return Response({'value': True}, HTTP_200_OK)
    else:
        return Response(None, HTTP_400_BAD_REQUEST)
