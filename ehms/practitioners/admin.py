from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ehms.practitioners.models import Practitioner, PractitionerHospital


class PractitionerHospitalAdmin(admin.TabularInline):
    model = PractitionerHospital
    extra = 1
    list_display = ('current_hospital', )
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Practitioner Hospital details'), {'fields': ('hospital', 'current_hospital')},),
        (_('Practitioner dates related to the hospital'), {'fields': ('joined_on', 'relieved_on',)},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]


@admin.register(Practitioner)
class PractitionerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'uid', 'gender', 'email', 'phone', 'status', 'created')
    save_on_top = True
    readonly_fields = ['id', 'uid', 'created', 'modified', 'creator_user', ]
    list_filter = ('status', 'gender', 'hospital', )
    ordering = ('-created', '-status', '-modified')
    search_fields = ['first_name', 'middle_name', 'last_name', 'uid', 'email', 'phone']
    list_display_links = ['get_full_name', ]
    inlines = (PractitionerHospitalAdmin,)
    fieldsets = [
        (None, {'fields': ('id', 'uid',)}),
        (_('Practitioner details'), {'fields': ('first_name', 'middle_name', 'last_name', 'date_of_birth',
                                                'vital_status', 'blood_group', 'religion', 'gender', 'image', )},),
        (_('Contact details'), {'fields': ('email', 'phone', 'alternate_phone',)},),
        (_('Practitioner Address'), {'fields': ('address_line_1', 'address_line_2', 'country',
                                                'region', 'district', 'town', 'postcode',)},),
        (_('Permissions'), {'fields': ('status', 'token', 'token_timestamp', 'verify_token')},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the practitioner'), {'fields': ('creator_user',)},),
    ]

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = _("Full name")

    def save_formset(self, request, obj, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.creator_user = request.user
            instance.save()
            formset.save()
