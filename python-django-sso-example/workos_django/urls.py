"""
WorkOS Django SSO Application - URL Configuration

Routes URLs to views for SSO authentication flow.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.static import serve as static_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("sso.urls")),
]

# Serve static files when DEBUG=False (requires --insecure flag)
if not settings.DEBUG:
    urlpatterns += [
        path('static/<path:path>', static_serve, {'document_root': settings.STATIC_ROOT}),
    ]
