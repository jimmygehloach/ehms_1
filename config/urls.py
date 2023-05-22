from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from two_factor.urls import urlpatterns as tf_urls
from two_factor.views import SetupView, LoginView, SetupCompleteView

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="open-home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url "admin:index" %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("account/login/", LoginView.as_view(), name="login"),
    path("account/logout/", LogoutView.as_view(), name="logout"),
    path("", include('ehms.core.urls', namespace='ehms-core')),

    # TODO Remove this after make sure that from admin side OTP required is working
    # path("account/two_factor/setup/", SetupView.as_view(), name="setup"),
    # path("account/two_factor/setup/complete/", SetupCompleteView.as_view(), name="setup_complete"),

    path("", include("user_sessions.urls", "user_sessions")),

    # Django Admin, use {% url "admin:index" %}
    path("captcha/", include("captcha.urls")),
    # User management
    # path("accounts/", include("django.contrib.auth.urls")),
    # Your stuff: custom urls includes go here
    path("", include("ehms.core.urls", namespace="core")),
    path("dashboards/", include("ehms.dashboards.urls", namespace="dashboards")),
    path("receptions/", include("ehms.receptions.urls", namespace="receptions")),
    path("patients/", include("ehms.patients.urls", namespace="patients")),
    path("practitioners/", include("ehms.practitioners.urls", namespace="practitioners")),
    path("patients/<int:pk>/medical_sessions/", include("ehms.medical_sessions.urls", namespace="medical_sessions")),
    path("hospitals/", include("ehms.hospitals.urls", namespace="hospitals")),
    path("inventory/", include("ehms.inventory.urls", namespace="inventory")),
    path("queries/", include("ehms.queries.urls", namespace="queries")),
    path("mortuaries/", include("ehms.mortuaries.urls", namespace="mortuaries")),
    path("addresses/", include("ehms.addresses.urls", namespace="addresses")),
    path("family_tree/", include("ehms.family_tree.urls", namespace="family_tree")),
    path("nurses/", include("ehms.nurses.urls", namespace="nurses")),
    path("articles/", include("ehms.articles.urls", namespace="articles")),

    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
