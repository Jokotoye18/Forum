from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('admin@jokotoye18/', admin.site.urls),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('martor/', include('martor.urls')),
    path('', include('pages.urls')),
    path('account/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('boards.urls')),
    # path('api/', include('boards.api.urls')),
]

# urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

admin.site.site_header = "Forum Admin"
admin.site.site_title = "Forum Admin Portal"
admin.site.index_title = "Welcome to Forum Portal"