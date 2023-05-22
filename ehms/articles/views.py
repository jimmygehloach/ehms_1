from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ehms.articles.forms import ArticleCountryForm, ArticleRegionForm
from ehms.articles.models import Article
from ehms.core.decorators import logged_in_user, fetch_user_details


def article_type_check_before_save(request, form):
    if form.instance.published:
        form.instance.published_at = timezone.now()

    if form.instance.type == "Article Sticky Aside":
        articles_count = Article.objects.filter(type="Article Sticky Aside").count()
        if articles_count == 3:
            form.instance.type = "Article Other"
            messages.info(request, _("Cannot change article type. 3 sticky aside articles already exist."))

    if form.instance.type == "Article Sticky Big":
        article_id = (Article.objects.filter(type="Article Sticky Big").values_list('id', flat=True).first())
        if article_id:
            messages.info(request,
                          _("Existing Sticky Big article removed. Attached to current article. Only 1 Sticky "
                            "Big allowed."))
            Article.objects.filter(pk=article_id).update(type="Article Other")


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['country level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ArticleCountryCreateView(SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleCountryForm
    template_name = 'articles/create_country_article.html'
    success_url = reverse_lazy('articles:country-list')
    success_message = "Article is created successfully."

    def form_valid(self, form):
        form.instance.country = self.request.country
        form.instance.creator_user = self.request.user
        article_type_check_before_save(self.request, form)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['country level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ArticleCountryListView(ListView):
    model = Article
    template_name = 'articles/article_country_list.html'
    paginate_by = 30

    def get_queryset(self):
        return Article.objects.select_related('category').prefetch_related('region').all()


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['country level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ArticleCountryUpdateView(SuccessMessageMixin, UpdateView):
    model = Article
    template_name = 'articles/article_country_update.html'
    success_message = "Article is updated successfully."
    form_class = ArticleCountryForm

    def form_valid(self, form):
        article_type_check_before_save(self.request, form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('articles:country-edit', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['region level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ArticleRegionCreateView(SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleRegionForm
    template_name = 'articles/create_region_article.html'
    success_url = reverse_lazy('articles:region-list')
    success_message = "Article is created successfully."

    def form_valid(self, form):
        form.instance.country = self.request.country
        form.instance.region = self.request.region
        form.instance.creator_user = self.request.user
        article_type_check_before_save(self.request, form)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['region level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ArticleRegionListView(ListView):
    model = Article
    template_name = 'articles/article_region_list.html'
    paginate_by = 30

    def get_queryset(self):
        return Article.objects.select_related('category').prefetch_related('region').all()


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['region level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ArticleRegionUpdateView(SuccessMessageMixin, UpdateView):
    model = Article
    template_name = 'articles/article_region_update.html'
    success_message = "Article is updated successfully."
    form_class = ArticleRegionForm

    def form_valid(self, form):
        article_type_check_before_save(self.request, form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('articles:region-edit', kwargs={'pk': self.object.pk})
