from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ehms.medical_sessions.models import MedicalSession, Department, Keyword, Ward


@admin.register(MedicalSession)
class MedicalSessionAdmin(admin.ModelAdmin):
    list_display = ('uid', 'status', 'created')
    save_on_top = True
    readonly_fields = ['id', 'uid', 'created', 'modified', 'creator_user']
    list_filter = ('status', )
    ordering = ('-created', '-status', )
    search_fields = ['uid', ]
    list_display_links = ['uid', ]
    fieldsets = [
        (None, {'fields': ('id', 'uid', 'patient', 'practitioner', 'hospital', )}),
        (_('Medical session'), {'fields': (
            'diagnosis', 'medication', 'procedure', 'hard_file', 'supporting_documents', 'emergency_session')},),
        (_('Other Information'), {'fields': ('keywords', 'department', 'ward', 'ipd_status')},),
        (_('Permissions'), {'fields': ('status', )},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed', )},),
        (_('User who registered the practitioner'), {'fields': ('creator_user', )},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Department detail'), {'fields': ('name', 'description', 'hospital', )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Ward detail'), {'fields': ('name', 'description', 'hospital', 'practitioners')},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'created',)
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    search_fields = ['name']
    ordering = ('-created',)
    fieldsets = [
        (None, {'fields': ('id',)}),
        (_('Keyword detail'), {'fields': ('name', )},),
        (_('Permissions'), {'fields': ('status',)},),
        (_('Important dates'), {'fields': ('created', 'modified', 'status_changed',)},),
        (_('User who created this record'), {'fields': ('creator_user',)},),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)
