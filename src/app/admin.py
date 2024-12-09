from django.contrib import admin
from account.models import CustomUser
from .models import Task, Team, TestWorkRequest, TestWorkResponse, TestForUser, AnswerTest
from .forms import TestWorkResultForm

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'is_completed', 'team')
    list_filter = ('users', 'created_at', 'updated_at', 'is_completed', 'team')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    filter_horizontal = (
        'users',
    )

    # Додатковий метод для автоматичного призначення
    def assign_users_to_all_tasks(self, request, queryset):
        # Наприклад, всі активні користувачі
        users = CustomUser.objects.filter(is_active=True)
        for task in queryset:
            task.users.add(*users)
        self.message_user(
            request, "Користувачі призначені вибраним завданням.")

    actions = [assign_users_to_all_tasks]


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    list_filter = ('name', 'created_at',)
    search_fields = ('name',)
    filter_horizontal = (
        'members',
    )


class TestWorkRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(TestForUser)
class TestForUserAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'users',
    )


@admin.register(TestWorkResponse)
class TestWorkResultAdmin(admin.ModelAdmin):
    # form = TestWorkResultForm

    # def save_model(self, request, obj, form, change):
    #     # Создаем отдельный пост для каждого выбранного пользователя
    #     users = form.cleaned_data.pop('users', [])
    #     for user in users:
    #         TestWorkResult.objects.create(
    #             user=user,
    #             team=obj.team,
    #             team_member=obj.team_member,
    #             test_work=obj.test_work,
    #             is_active=obj.is_active,
    #             thumbnail=obj.thumbnail,
    #         )
    pass


@admin.register(AnswerTest)
class AnswerTestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TestWorkRequest, TestWorkRequestAdmin)
