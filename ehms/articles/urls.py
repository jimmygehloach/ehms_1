from django.urls import path

from .views import ArticleCountryCreateView, ArticleCountryListView, ArticleCountryUpdateView

app_name = 'articles'
urlpatterns = [
    path(route='country/list/', view=ArticleCountryListView.as_view(), name='country-list'),
    path(route='country/new/', view=ArticleCountryCreateView.as_view(), name='country-new'),
    path(route='country/<int:pk>/edit', view=ArticleCountryUpdateView.as_view(), name='country-edit'),
]
