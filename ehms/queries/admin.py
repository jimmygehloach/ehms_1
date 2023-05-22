from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ehms.queries.models import HospitalQuery, PractitionerQuery


@admin.register(PractitionerQuery)
class PractitionerQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'response_status', 'status', 'created')
    readonly_fields = ['id', 'created', 'modified', ]
    list_filter = ('status',)
    search_fields = ['subject', 'body']
    ordering = ('-created', '-status', )

    list_display_links = ['id', ]
    fieldsets = [
        (None, {'fields': ('id', 'practitioner', 'hospital', )}),
        (_('Query info'), {'fields': (
            'subject', 'body', 'attachment', 'response_status', 'response', )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]


@admin.register(HospitalQuery)
class HospitalQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'response_status', 'status', 'created')
    readonly_fields = ['id', 'created', 'modified', ]
    list_filter = ('status',)
    search_fields = ['subject', 'body']
    ordering = ('-created', '-status',)

    list_display_links = ['id', ]
    fieldsets = [
        (None, {'fields': ('id', 'hospital',)}),
        (_('Query info'), {'fields': (
            'subject', 'body', 'attachment', 'response_status', 'response',)},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]
