from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ehms.patients.models import (
    Addiction, Allergy, AgeGroup, HealthStatus,
    MedicalIllness, Patient, PatientDocument,
    PatientAddress, PatientDeathRecord, PatientImage
)


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'range_from', 'range_to', 'description', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Age group detail'), {'fields': ('name', 'range_from', 'range_to', 'description')},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(HealthStatus)
class HealthStatusAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Health Status detail'), {'fields': ('name', 'css_class', 'description',)},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(MedicalIllness)
class MedicalIllnessAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Medical Illness detail'), {'fields': ('name', 'description',)},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Allergy detail'), {'fields': ('name', 'description',)},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Addiction)
class AddictionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Addiction detail'), {'fields': ('name', 'description',)},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'uid', 'gender', 'religion', 'vital_status', 'created', 'modified')
    save_on_top = True
    readonly_fields = ['id', 'uid', 'created', 'modified', 'age_group', 'creator_user', ]
    list_filter = ('vital_status', 'gender', 'religion', 'status')
    ordering = ('-created', '-vital_status', '-modified')
    search_fields = ['first_name', 'middle_name', 'last_name', 'uid', 'voter_card_number',
                     'date_of_birth', 'blood_group', ]
    list_display_links = ['get_full_name', ]
    fieldsets = [
        (None, {'fields': ('id', 'uid', 'voter_card_number')}),
        (_('Patient basic details'), {'fields': (
            'first_name', 'middle_name', 'last_name', 'date_of_birth', 'birth_time', 'religion', 'gender', 'marital_status',
            'pregnancy', 'children', 'email', 'blood_group', 'height', 'weight', 'disability',
            'vital_status', 'health_status', 'age_group', 'hospital', )},),
        (_('Patient immunization detail'), {'fields': (
            'bcg', 'pentavalent', 'pneumo', 'polio', 'rotarix', 'measles_rubella_1', 'measles_rubella_2', 'dpt',
            'yellow_fever', 'vitamin_a', 'tetanus', 'tt_one_pregnant', 'tt_two_pregnant', 'tt_booster',
        )},),
        (_('Patient medical history'), {'fields': (
            'patient_allergies', 'patient_addictions', 'patient_medical_illness', 'patient_kin_medical_illness',
        )},),
        (_('Patient extra information'), {'fields': ('temporary_family_info', 'other_information', 'remarks', )},),
        (_('Permissions'), {'fields': ('status', )},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed', )},),
        (_('User who created this record'), {'fields': ('creator_user', )},),
    ]

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = _("Full name")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(PatientImage)
class PatientImageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('pk', 'patient', 'created', 'modified')
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'created', 'modified',)
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    list_filter = ('status', )
    ordering = ('-created', '-status', '-modified')
    search_fields = ['name', 'type', ]
    list_display_links = ['name', ]
    fieldsets = [
        (None, {'fields': ('id', 'patient', 'hospital', )}),
        (_('Patient document details'), {'fields': (
            'name', 'type', 'document', )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(PatientAddress)
class PatientAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_address', 'status', 'created', 'modified', )
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    list_filter = ('status', )
    ordering = ('-created', '-status', '-modified')
    fieldsets = [
        (None, {'fields': ('id', 'patient', 'hospital', )}),
        (_('Patient contact'), {'fields': ('email', 'phone', 'alternate_phone', )},),
        (_('Patient address'), {'fields': (
            'type', 'current_address', 'address_line_1', 'address_line_2',
            'country', 'region', 'district', 'town', 'postcode',
            )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed', )},),
        (_('User who created this record'), {'fields': ('creator_user', )},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(PatientDeathRecord)
class PatientDeathRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'died_on', 'created', 'modified', )
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user', ]
    list_filter = ('status', )
    ordering = ('-created', '-modified')
    fieldsets = [
        (None, {'fields': ('id', 'patient', 'hospital', 'practitioner', )}),
        (_('Patient death record'), {'fields': ('died_on', 'reason', 'place', )},),
        (_('Extra information'), {'fields': ('notes', )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed', )},),
        (_('User who created this record'), {'fields': ('creator_user', )},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)
