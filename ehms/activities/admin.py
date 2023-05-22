from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ehms.activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('description', 'user_group', 'action', 'uid', 'activity_level', 'status', 'created')
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', 'activity_level')
    ordering = ('-created', '-status',)
    search_fields = ['uid', 'user_group', 'activity_level', ]
    list_display_links = ['uid', ]
    fieldsets = [
        (None, {'fields': ('id', 'patient', 'hospital', )}),
        (_('Region details'), {'fields': (
            'user_group', 'uid', 'description', 'user_agent', 'ip_address', 'ip_routable', 'activity_level', 'action',
        )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who registered the country'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)
