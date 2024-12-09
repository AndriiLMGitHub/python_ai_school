from .models import CustomUser, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'form_pupil',
            'email',
            'password1',
            'password2'
        )

        def clean_password_confirmation(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get(
                'password2')
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            return password2

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data.get('password'))
            if commit:
                user.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'birth_date',
            'phone_number',
            'address',
            'sex',
            'image',
            'bio',
        )


class CompleteUserSocialForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'form_pupil',
        )
