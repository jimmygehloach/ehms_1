from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view

from ehms.activities.views import create_activity
from ehms.core.decorators import logged_in_user, fetch_user_details
from ehms.inventory.forms import NewReceivedDetailForm, NewIssuedDetailForm
from ehms.inventory.models import Item, ReceivedDetail, IssuedDetail, Inventory


def check_activity_tag(request):
    activity_tag = 'Inventory'
    if request.group_name == 'hospital level':
        activity_tag = 'Hospital'

    return activity_tag


@csrf_protect
@api_view(['POST'])
def item_list(request):
    if request.method == 'POST':
        category_id = request.data['categoryId']
        items = Item.objects.filter(item_category=category_id)
        item = {i.item_name: i.id for i in items}
        return JsonResponse(data=item, safe=False)


@login_required
@logged_in_user(['hospital level', 'inventory level'])
@fetch_user_details
def received_detail(request):
    activity_tag = check_activity_tag(request)
    create_activity(request, 'GET', _('Inventory received page is visited.'), activity_tag)

    inventory_formset = inlineformset_factory(
        ReceivedDetail,
        Inventory,
        fields=('item_category', 'item', 'received_quantity', 'price', 'vat', 'discount', 'total_price', 'remarks')
    )

    if request.method == 'POST':
        form = NewReceivedDetailForm(request.POST or None)
        formset = inventory_formset(request.POST or None)

        if all([form.is_valid(), formset.is_valid()]):
            try:
                with transaction.atomic():
                    __received = form.save(commit=False)
                    __received.creator_user = request.user
                    __received.hospital = request.hospital
                    __received.total_items = len(formset)
                    __received.save()

                    for inline_form in formset:

                        if inline_form.cleaned_data:
                            __inventory = inline_form.save(commit=False)
                            __inventory.received_detail = __received
                            __inventory.creator_user = request.user
                            __inventory.hospital = request.hospital
                            __inventory.save()
                    create_activity(request, 'UPDATE', _('Items are received from inventory.'), activity_tag)
                    messages.success(request, _('Detail stored successfully.'))
                    return redirect(reverse('inventory:received'))

            except DatabaseError:
                messages.error(request, _('Something went wrong.'))
        else:
            messages.error(request, _('Something went wrong. Please check the errors.'))
    else:
        form = NewReceivedDetailForm()
        formset = inventory_formset()

    data_send = {
        'title': 'Received | Inventory',
        'form': form,
        'formset': formset,
        'inline_form_min': 3,
    }

    return render(request, "inventory/new_received_detail.html", data_send)


@login_required
@logged_in_user(['hospital level', 'inventory level'])
@fetch_user_details
def issued_detail(request):
    activity_tag = check_activity_tag(request)
    create_activity(request, 'GET', _('Inventory issued page is visited.'), activity_tag)

    inventory_formset = inlineformset_factory(
        IssuedDetail,
        Inventory,
        fields=('item_category', 'item', 'issued_quantity', 'price', 'vat', 'discount', 'total_price', 'remarks')
    )
    if request.method == 'POST':
        form = NewIssuedDetailForm(request.POST or None)
        formset = inventory_formset(request.POST or None)

        if all([form.is_valid(), formset.is_valid()]):
            try:
                with transaction.atomic():
                    __issued = form.save(commit=False)
                    __issued.creator_user = request.user
                    __issued.hospital = request.hospital
                    __issued.total_items = len(formset)
                    __issued.save()

                    for inline_form in formset:

                        if inline_form.cleaned_data:
                            __inventory = inline_form.save(commit=False)
                            __inventory.issued_detail = __issued
                            __inventory.creator_user = request.user
                            __inventory.hospital = request.hospital
                            __inventory.save()
                    create_activity(request, 'UPDATE', _('Items are issued from inventory.'), activity_tag)
                    messages.success(request, _('Detail stored successfully.'))
                    return redirect(reverse('inventory:issued'))

            except DatabaseError:
                messages.error(request, _('Something went wrong.'))
        else:
            messages.error(request, _('Something went wrong. Please check the errors.'))

    else:
        form = NewIssuedDetailForm()
        formset = inventory_formset()

    data_send = {
        'title': 'Issued | Inventory',
        'form': form,
        'formset': formset,
        'inline_form_min': 3,
    }

    return render(request, "inventory/new_issued_detail.html", data_send)


@login_required
@logged_in_user(['hospital level', 'inventory level'])
@fetch_user_details
def inventory_detail(request):
    activity_tag = check_activity_tag(request)
    create_activity(request, 'GET', _('Inventory detail page is visited.'), activity_tag)

    received_items_detail = ReceivedDetail.objects.filter(status='active').select_related('supplier').order_by('-created')
    issued_items_detail = IssuedDetail.objects.filter(status='active').select_related('department').order_by('-created')

    inventory = Inventory.objects.values(
            'item',
            'item__item_name',
            'item_category__name',
            'item__sku',
            'item__minimum_stock_value',
        ).annotate(
            total_received=Sum('received_quantity'),
            total_issued=Sum('issued_quantity'),
        ).order_by('item')

    data_send = {
        'title': 'Detail | Inventory',
        'received_items_detail': received_items_detail,
        'issued_items_detail': issued_items_detail,
        'inventory': inventory,
    }

    return render(request, "inventory/inventory_detail.html", data_send)


@login_required
@logged_in_user(['hospital level', 'inventory level'])
@fetch_user_details
def inventory_received_bill_detail(request, pk):
    activity_tag = check_activity_tag(request)
    create_activity(request, 'GET', _('Inventory received bill page is visited.'), activity_tag)

    bill = get_object_or_404(ReceivedDetail, pk=pk, status='active')

    items_detail = Inventory.objects.filter(
        received_detail=bill,
        status='active'
    )

    data_send = {
        'title': 'Received Bill | Inventory',
        'bill': bill,
        'items_detail': items_detail
    }

    return render(request, "inventory/inventory_received_bill_detail.html", data_send)


@login_required
@logged_in_user(['hospital level', 'inventory level'])
@fetch_user_details
def inventory_issued_bill_detail(request, pk):
    activity_tag = check_activity_tag(request)
    create_activity(request, 'GET', _('Inventory issued bill page is visited.'), activity_tag)

    bill = get_object_or_404(IssuedDetail,  pk=pk, status='active')

    items_detail = Inventory.objects.filter(
        issued_detail=bill,
        status='active'
    )

    data_send = {
        'title': 'Issued Bill | Inventory',
        'bill': bill,
        'items_detail': items_detail
    }

    return render(request, "inventory/inventory_issued_bill_detail.html", data_send)
