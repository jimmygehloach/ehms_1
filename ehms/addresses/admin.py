from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Country, Region, District, Town, Postcode


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'population', 'status', 'created')
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', )
    ordering = ('-created', '-status',)
    search_fields = ['name']
    list_display_links = ['name', ]
    fieldsets = [
        (None, {'fields': ('id', 'uid')}),
        (_('Country details'), {'fields': ('name', 'population', 'capital', )},),
        (_('Permissions'), {'fields': ('status', )},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed', )},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'population', 'status', 'created')
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', 'country', )
    ordering = ('-created', '-status',)
    search_fields = ['name', ]
    list_display_links = ['name', ]
    fieldsets = [
        (None, {'fields': ('id', 'uid')}),
        (_('Region details'), {'fields': ('name', 'population', 'capital', 'country', )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'population', 'region', 'country', 'status', 'created', )
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', 'country', 'region', )
    ordering = ('-created', '-status',)
    search_fields = ['name']
    list_display_links = ['name', ]
    fieldsets = [
        (None, {'fields': ('id', 'uid')}),
        (_('District details'), {'fields': ('name', 'population', 'country', 'region', )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


class TownAdmin(admin.ModelAdmin):
    list_display = ('name', 'population', 'region', 'district', 'country', 'status', 'created', )
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', 'country', 'region', 'district')
    search_fields = ['name']
    ordering = ('-created', '-status',)
    list_display_links = ['name', ]
    fieldsets = [
        (None, {'fields': ('id', 'uid')}),
        (_('District details'), {'fields': ('name', 'population', 'country', 'region', 'district')},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


class PostcodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'population', 'region', 'district', 'town', 'country', 'status', 'created', )
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', 'country', 'region', 'district', 'town')
    ordering = ('-created', '-status',)
    search_fields = ['name']
    list_display_links = ['name', ]
    fieldsets = [
        (None, {'fields': ('id', 'uid')}),
        (_('District details'), {'fields': ('name', 'population', 'country', 'region', 'district', 'town')},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


# admin model registrations
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Postcode, PostcodeAdmin)

