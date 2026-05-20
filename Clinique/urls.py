from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', lambda request: redirect('login')),
    path('accounts/', include('accounts.urls')),
    path('', include('patients.urls')),
    path('', include('staff.urls')),
    path('', include('appointments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
