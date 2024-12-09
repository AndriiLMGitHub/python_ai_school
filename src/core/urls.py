from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve


handler404 = views.my_handler404

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Root media route
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),

    # Start page route
    path('', views.start_view, name="index"),

    # Account routes
    path('account/', include('account.urls')),
    path('account/', include('social_django.urls', namespace='social')),

    # Apps routes
    path('', include('app.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
