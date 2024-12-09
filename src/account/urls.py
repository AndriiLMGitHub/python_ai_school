from django.urls import path
from django.conf import settings
from social_core.utils import setting_name
from django.contrib.auth import views as auth_views
from .social_views import complete, disconnect
from . import views

extra = getattr(settings, setting_name("TRAILING_SLASH"), True) and "/" or ""


urlpatterns = [
    # Add a new URL for the signin view
    path('signup/', views.signup_view, name='signup'),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.signout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Social authentication
    path(f"complete/<str:backend>{extra}", complete, name="complete"),
    path(f"disconnect/<str:backend>{extra}",
         disconnect, name="disconnect"),
    path(
        f"disconnect/<str:backend>/<int:association_id>{extra}",
        disconnect,
        name="disconnect_individual",
    ),

    # Adding user detail after social login
    path('add/user/details/', views.complete_user, name='complete_user'),

    # Paswords
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="auth/password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"),
         name='password_reset_complete'),

    # Password change
    path('password_change/', views.CustomPasswordChangeView.as_view(),
         name='password_change'),


]
