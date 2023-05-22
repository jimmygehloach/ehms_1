from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Article, ArticleCategory


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'published', 'published_at', 'status', 'created')
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('created', 'status', 'published', 'category')
    ordering = ('-created', '-status',)
    search_fields = ['title', 'excerpt', ]
    list_display_links = ['title', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    save_on_top = True
    readonly_fields = ['id', 'created', 'modified', 'creator_user']
    list_filter = ('status', )
    ordering = ('-created', '-status',)
    search_fields = ['name', ]
    list_display_links = ['name', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)


# admin model registrations
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
