from django.contrib import admin
from .models import CustomUser, Profile


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser',
                    'is_leader', 'form_pupil')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'form_pupil')}),
        ('Permissions', {'fields': ('is_active',
         'is_staff', 'is_superuser', 'is_leader')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Additional fields', {'fields': ('date_joined',)}),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_filter = ('user',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('user',)
    autocomplete_fields = ('user',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
