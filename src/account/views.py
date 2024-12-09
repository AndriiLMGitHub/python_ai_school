from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from .forms import CustomUserSignUpForm, ProfileForm, CompleteUserSocialForm
from .models import CustomUser
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            form = CustomUserSignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False  # Deactivate account until it is confirmed
                user.save()

                # Email confirmation
                current_site = get_current_site(request)
                subject = _("Activate Your Account")
                message = render_to_string("auth/account_activation_email.html", {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                })
                send_mail(subject, message, None, [
                    user.email], fail_silently=False)

                messages.success(request, _(
                    "Registration successful. Check your email to confirm your account."))
                return redirect("signin")
            else:
                messages.error(request, _("Please correct the errors."))
                return redirect('signup')
        else:
            form = CustomUserSignUpForm()
    return render(request, "auth/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _(
            "Your account has been activated. You can now log in."))
        return redirect("signin")
    else:
        messages.error(request, _(
            "Activation link is invalid or has expired."))
        return redirect("signup")


def complete_user(request):
    if request.method == 'POST':
        form = CompleteUserSocialForm(request.POST)
        if form.is_valid():
            user = request.user
            user.form_pupil = form.cleaned_data['form_pupil']
            user.save()
            return redirect('profile')
    else:
        form = CompleteUserSocialForm()
    return render(request, 'auth/complete_user.html', {'form': form})


def signin_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _(
                    "You have successfully logged in."))
                return redirect('profile')
            else:
                messages.error(request, _("Invalid email or password."))
    return render(request, 'auth/login.html')


def signout_view(request):
    logout(request)
    messages.success(request, _("You have successfully logged out."))
    return redirect('signin')


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'auth/password_change.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(
            self.request, "Password has been changed successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error changing your password. Please try again.")
        return super().form_invalid(form)

    def is_social_user(self):
        """
        Проверяет, залогинился ли пользователь через соцсети.
        """
        user = self.request.user
        return UserSocialAuth.objects.filter(user=user).exists() if user.is_authenticated else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_social_user'] = self.is_social_user()
        return context


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        if request.method == 'POST':
            form = ProfileForm(request.POST,
                               request.FILES,
                               instance=request.user.profile
                               )
            if form.is_valid():
                form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, _(
                    "Profile has been updated successfully!"))
                return redirect('dashboard')
            else:
                messages.error(request, _(
                    "There was an error updating your profile. Please try again."))
                print(form.errors)
        else:
            form = ProfileForm(instance=request.user.profile)
    return render(request, 'auth/profile.html', {'form': form})
