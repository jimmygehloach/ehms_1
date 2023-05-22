from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ehms.family_tree.models import FamilyTree
from ehms.patients.models import Patient


@admin.register(FamilyTree)
class FamilyTreeAdmin(admin.ModelAdmin):
    list_display = ('first_patient', 'relation', 'second_patient', 'status', 'created')
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status',)
    ordering = ('-created', '-status',)
    list_display_links = ['first_patient']
    # fieldsets = [
    #     (None, {'fields': ('id',)}),
    #     (_('Query info'), {'fields': ('patient', 'relation', 'family_member',)},),
    #     (_('Permissions'), {'fields': ('status',)},),
    #     (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
    #     (_('User who entered the record'), {'fields': ('creator_user',)},),
    # ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)



