from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/imgs/favicon.png', permanent=True)

urlpatterns = [
    path('ad/', admin.site.urls),
    path('favicon.ico', favicon_view),
    path('', include('parchment.urls')),
    path('thoughts/', include('thought.urls')),
    path('admin/', include('admin_honeypot.urls'), name='admin_honeypot'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
