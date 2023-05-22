from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import DatabaseError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from ehms.activities.views import create_activity, cam
from . import forms
from ehms.queries.models import HospitalQuery, PractitionerQuery

from ehms.core.decorators import logged_in_user, fetch_user_details
from .forms import NewHospitalQueryForm
from ..core.utils import check_activity_level
from ..utils.helpers import UTL


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class HospitalQueryInboxListView(FormMixin, ListView):
    model = HospitalQuery
    form_class = NewHospitalQueryForm
    template_name = 'queries/hospital_query_inbox.html'
    paginate_by = 30

    def get_queryset(self):
        queryset = HospitalQuery.objects.filter(status='active',
                                                hospital_id=self.request.hospital.pk).select_related('hospital')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                with transaction.atomic():
                    query = form.save(commit=False)
                    query.hospital = request.hospital
                    query.creator_user = request.user
                    query.save()
                    create_activity(request, 'INSERT', cam().get('hospital_query_inbox'), check_activity_level(request))
                messages.success(request, UTL.success_message('INBOX_QUERY_SUBMIT'))
                return redirect(reverse('queries:hospital-inbox'))
            except Exception as e:
                messages.error(request, 'Something went wrong.')
        else:
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            context['form'] = form
            messages.error(request, 'Something went wrong.')
            return self.render_to_response(context)


@login_required
@logged_in_user(['practitioner level'])
@fetch_user_details
def practitioner_query_inbox(request, pk):
    if str(request.practitioner.pk) != str(pk):
        return redirect('/patients/')

    _count = 0
    _queries = []
    _sort_by = ''
    context = {
        'title': 'Practitioner Inbox',
        'hospital_user': True,
    }
    # TODO convert this into _()
    message = 'Practitioner with uid: ' + request.practitioner.uid + \
              ' fetched the query inbox. Check other columns for more detail.'
    create_activity(request, 'GET', message, check_activity_level(request))

    practitioner_query_form = forms.NewPractitionerQueryForm(request.POST or None, request.FILES or None)

    context['practitioner_query_form'] = practitioner_query_form

    _count = PractitionerQuery.objects.filter(
        practitioner=request.practitioner.pk,
        status='active',
        hospital_id=request.hospital.pk
    ).count()

    context['queries_count'] = _count

    _sort_by = request.GET.get('sort')

    if _sort_by not in ['asc', 'desc']:
        _sort_by = 'desc'

    if _sort_by == 'asc':
        _queries = PractitionerQuery.objects.filter(
            practitioner=request.practitioner.pk,
            status='active',
            hospital_id=request.hospital.pk
        ).order_by('created')

    elif _sort_by == 'desc':
        _queries = PractitionerQuery.objects.filter(
            practitioner=request.practitioner.pk,
            status='active',
            hospital_id=request.hospital.pk
        ).order_by('-created')

    paginator = Paginator(_queries, 30)
    page_number = request.GET.get('page', 1)
    context['page_obj'] = paginator.get_page(page_number)
    if _count > 30:
        context['is_paginated'] = True
    else:
        context['is_paginated'] = False

    if 'new_practitioner_query' in request.POST:
        if practitioner_query_form.is_valid():
            try:
                query = practitioner_query_form.save(commit=False)
                query.hospital = request.hospital
                query.creator_user = request.user
                query.practitioner = request.practitioner
                query.save()
                messages.success(request, 'Query submitted.')
                # TODO convert this into _()
                message = 'Practitioner with uid: ' + request.practitioner.uid + \
                          ' created the query. Check other columns for more detail.'
                create_activity(request, 'INSERT', message, check_activity_level(request))
                return redirect(reverse('queries:practitioner-inbox', args=(pk,)))
            except DatabaseError:
                messages.error(request, 'Something went wrong.')
                context['practitioner_query_form'] = forms.NewPractitionerQueryForm(
                    request.POST or None, request.FILES or None
                )
        else:
            context['practitioner_query_form'] = forms.NewPractitionerQueryForm(
                request.POST or None, request.FILES or None
            )
            messages.error(request, 'Something went wrong.')

    return render(request, 'queries/practitioner_query_inbox.html', context)
