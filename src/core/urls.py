from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


handler404 = views.my_handler404

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Start page route
    path('', views.start_view, name="index"),

    # Account routes
    path('account/', include('account.urls')),
    path('account/', include('social_django.urls', namespace='social')),

    # Apps routes
    path('', include('app.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
