from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from ehms.activities.views import create_activity, cam
from ehms.articles.models import Article
from ehms.core.decorators import logged_in_user, fetch_user_details
from ehms.nurses.models import Nurse
from ehms.practitioners.models import Practitioner
from ehms.receptions.models import Reception
from ehms.utils.helpers import UTL


@login_required
@logged_in_user(['country level'])
@fetch_user_details
def country_level_dashboard(request):
    articles_other = Article.objects.filter(published=True, status='active', type='Article Other').select_related(
        'category')
    articles_sticky_aside = Article.objects.filter(published=True, status='active',
                                                   type='Article Sticky Aside').select_related('category')
    article_sticky_big = Article.objects.filter(published=True, status='active',
                                                type="Article Sticky Big").select_related('category').first()

    context = {
        'title': 'Home | Country',
        'articles_other': articles_other,
        'articles_sticky_aside': articles_sticky_aside,
        'article_sticky_big': article_sticky_big,
    }

    return render(request, 'dashboards/country_home.html', context)


@login_required
@logged_in_user(['region level'])
@fetch_user_details
def region_level_dashboard(request):
    articles_other = Article.objects.filter(published=True, status='active', type='Article Other',
                                            region=request.region, country=request.country).select_related(
        'category')
    articles_sticky_aside = Article.objects.filter(published=True, status='active', region=request.region,
                                                   country=request.country, type='Article Sticky Aside').select_related(
        'category')
    article_sticky_big = Article.objects.filter(published=True, status='active', region=request.region,
                                                country=request.country, type="Article Sticky Big").select_related(
        'category').first()

    context = {
        "title": "Home | Region",
        'articles_other': articles_other,
        'articles_sticky_aside': articles_sticky_aside,
        'article_sticky_big': article_sticky_big,
    }
    return render(request, 'dashboards/region_home.html', context)


@login_required
@logged_in_user(['district level'])
@fetch_user_details
def district_level_dashboard(request):
    context = {
        "title": "Home | District",
    }
    return render(request, 'dashboards/district_home.html', context)


@login_required
@logged_in_user(['state level'])
@fetch_user_details
def state_level_dashboard(request):
    context = {
        "title": "Home | State",
    }
    return render(request, 'dashboards/state_home.html', context)


@login_required
@logged_in_user(['hospital level'])
@fetch_user_details
def hospital_level_dashboard(request):
    sticky = False

    create_activity(request, 'GET', _('User visited to hospital level dashboard page'), 'Hospital')

    sticky_article = Article.objects.filter(status="active", published=True, type="Article Sticky Big").select_related(
        'category').first()

    aside_articles = Article.objects.filter(
        status="active", published=True, type="Article Sticky Aside").select_related('article_category')

    other_articles = Article.objects.filter(status="active", published=True, type="Article Other").select_related(
        'category')

    if sticky_article:
        sticky = True

    data_send = {
        "title": "Home | Hospital ",
        "sticky": sticky,
    }

    return render(request, 'dashboards/hospital_home.html', data_send)


@login_required
@logged_in_user(['practitioner level'])
@fetch_user_details
def practitioner_level_dashboard(request):
    context = {
        "title": "Home | Practitioner",
    }

    create_activity(request, 'GET', _('User visited to practitioner level dashboard page'), 'Practitioner')

    if request.method == 'POST':
        if request.POST.get('token') == request.practitioner.token and \
            request.practitioner.token_timestamp > timezone.now():
            Practitioner.objects.filter(
                pk=request.practitioner.pk,
                status='active',
            ).update(verify_token=True)

            messages.success(request, 'Token is verified.')

        else:
            messages.error(request, 'Something went wrong.')

        return redirect(reverse('dashboards:practitioner-level'))

    return render(request, 'dashboards/practitioner_home.html', context)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
def nurse_level_dashboard(request):
    create_activity(request, 'GET', _('User visited to nurse level dashboard page'), 'Nurse')

    if request.method == 'POST':
        if (request.POST.get('token') == request.nurse.token) and (request.nurse.token_timestamp > timezone.now()):
            Nurse.objects.filter(pk=request.nurse.pk, status='active').update(verify_token=True)
            messages.success(request, 'Token is verified.')
        else:
            messages.error(request, 'Something went wrong.')
        return redirect(reverse('dashboards:nurse-level'))

    context = {
        "title": "Home | Nurse",
    }

    return render(request, 'dashboards/nurse_home.html', context)


@login_required
@logged_in_user(['mortuary level'])
@fetch_user_details
def mortuary_level_dashboard(request):
    create_activity(request, 'GET', _('User visited to mortuary level dashboard page'), 'Mortuary')
    context = {
        "title": "Home | Mortuary",
    }
    return render(request, 'dashboards/mortuary_home.html', context)


@login_required
@logged_in_user(['inventory  level'])
@fetch_user_details
def inventory_level_dashboard(request):
    create_activity(request, 'GET', _('User visited to inventory level dashboard page'), 'Inventory')
    context = {
        "title": "Home | Inventory",
    }
    return render(request, 'dashboards/inventory_home.html', context)


@login_required
@logged_in_user(['reception level'])
@fetch_user_details
def reception_level_dashboard(request):
    create_activity(request, 'GET', cam().get('reception_level_dashboard_1'), 'Reception')

    if request.method == 'POST':
        if (request.POST.get('token') == request.reception.token) and (
            request.reception.token_timestamp > timezone.now()
        ):
            try:
                Reception.objects.filter(pk=request.reception.pk, status='active').update(verify_token=True)
                messages.success(request, UTL.success_message('TOKEN_VERIFIED'))
                create_activity(request, 'GET', cam().get('reception_level_dashboard_2'), 'Reception')
            except Exception as e:
                messages.error(request, UTL.error_message('DB_EX_ER'))
        else:
            messages.error(request, UTL.error_message('TOKEN_NOT_VERIFIED'))
        return redirect(reverse('dashboards:reception-level'))

    context = {
        "title": "Home | Reception",
    }
    return render(request, 'dashboards/reception_home.html', context)
