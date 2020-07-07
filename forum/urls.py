from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from ckeditor_uploader import urls 


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('admin@jokotoye18/', admin.site.urls),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('pages.urls')),
    path('account/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('boards.urls')),
    # path('api/', include('boards.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns