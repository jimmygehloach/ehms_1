from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ehms.nurses.models import Nurse, NurseHospital, VitalSignRecord, IntakeOutputChart, NurseNotes


@admin.register(VitalSignRecord)
class VitalSignRecordAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(IntakeOutputChart)
class IntakeOutputChartAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(NurseNotes)
class NurseNotesAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


# @admin.register(NurseHospital)
class NurseHospitalAdmin(admin.TabularInline):
    model = NurseHospital
    extra = 1
    readonly_fields = ['id', 'created', 'modified', 'creator_user']


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    inlines = (NurseHospitalAdmin,)
    save_on_top = True
    list_display = [
        'get_full_name',
        'uid',
        'status',
        'created',
    ]
    list_filter = ('status', 'created',)
    ordering = ('-created',)
    search_fields = ['uid', 'first_name', ' last_name', ]
    readonly_fields = ['id', 'created', 'modified', 'creator_user']

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    get_full_name.short_description = _("Full name")

    def save_formset(self, request, obj, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.creator_user = request.user
            instance.save()
            formset.save()
