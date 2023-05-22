from django.contrib import admin

from ehms.mortuaries.models import Mortuary, MortuaryPatient


@admin.register(Mortuary)
class MortuaryAdmin(admin.ModelAdmin):
    pass


@admin.register(MortuaryPatient)
class MortuaryPatientAdmin(admin.ModelAdmin):
    pass
