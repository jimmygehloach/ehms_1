from django.conf import settings
# from django.contrib.gis import admin
from django import forms
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from ehms.hospitals.models import Hospital, HospitalRepresentative

'''
LATITUDE_DEFINITION = _(
    "Latitude (Lat.) is the angle between any point and the "
    "equator (north pole is at 90°; south pole is at -90°)."
)
LONGITUDE_DEFINITION = _(
    "Longitude (Long.) is the angle east or west of a point "
    "on Earth at Greenwich (UK), which is the international "
    "zero-longitude point (longitude = 0°). The anti-meridian "
    "of Greenwich (the opposite side of the planet) is both "
    "180° (to the east) and -180° (to the west)."
)


class HospitalModelForm(forms.ModelForm):
    latitude = forms.FloatField(
        label=_("Latitude"), required=False,
        help_text=LATITUDE_DEFINITION
    )
    longitude = forms.FloatField(
        label=_("Longitude"), required=False,
        help_text=LONGITUDE_DEFINITION
    )

    class Meta:
        model = Hospital
        exclude = ['geo_position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            geo_position = self.instance.get_geo_position()
            if geo_position:
                self.fields["latitude"].initial = geo_position.latitude
                self.fields["longitude"].initial = geo_position.longitude

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        instance = super().save(commit=False)
        instance.set_geo_position(
            longitude=cleaned_data["longitude"],
            latitude=cleaned_data["latitude"],
        )
        if commit:
            instance.save()
            self.save_m2m()
        return instance
'''


@admin.register(Hospital)
# class HospitalAdmin(admin.OSMGeoAdmin):
class HospitalAdmin(admin.ModelAdmin):
    # form = HospitalModelForm
    list_display = ('name', 'uid', 'email', 'phone', 'status', 'created', )
    save_on_top = True
    readonly_fields = ['id', 'uid', 'created', 'modified', 'creator_user']
    list_filter = ('status', )
    ordering = ('-created', '-status', )
    search_fields = ['name', 'email', 'phone', 'uid', ]
    list_display_links = ['name', ]

    def get_fieldsets(self, request, obj=None):
        '''
        map_html = render_to_string(
            "admin/hospitals/includes/map.html",
            {"MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY},
        )
        '''
        fieldsets = [
            (None, {'fields': ('id', )}),
            (_('Hospital basic info'), {'fields': ('uid', 'name', 'image', 'beds')},),
            (_('Hospital address info'), {'fields': ('address_line_1', 'address_line_2', 'country', 'region',
                                                     'district', 'town', 'postcode', "latitude", "longitude", )},),
            # (_("Hospital Map"), {"description": map_html, "fields": []}),
            (_('Hospital contact info'), {'fields': ('email', 'phone', 'alternate_phone', )},),
            (_('Hospital miscellaneous info'), {'fields': ('remarks', )},),
            (_('Permissions'), {'fields': ('status',)},),
            (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
            (_('User who registered the country'), {'fields': ('creator_user',)},),
        ]
        return fieldsets

    def save_model(self, request, obj, form, change):
        if not change:
            obj.current_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(HospitalRepresentative)
# class HospitalRepresentativeAdmin(admin.OSMGeoAdmin):
class HospitalRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'gender', 'email', 'phone', 'status', 'created',)
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', 'hospital')
    ordering = ('-created', '-status', '-gender', )
    search_fields = ['first_name', 'last_name', 'email', 'phone', ]
    list_display_links = ['get_full_name', ]
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Representative basic info'), {'fields': ('first_name', 'last_name', 'gender', 'image',
                                                     'date_of_birth', 'hospital', 'designation', )},),
        (_('Representative contact info'), {'fields': ('email', 'phone', 'alternate_phone',)},),
        (_('Hospital miscellaneous info'), {'fields': ('remarks',)},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.current_user = request.user
        super().save_model(request, obj, form, change)
