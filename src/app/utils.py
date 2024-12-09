from django.contrib.auth import get_user_model

User = get_user_model()


def get_team_members(user):
    # Отримати всі команди, в яких знаходиться користувач
    teams = user.team_set.all()

    # Отримати всіх членів цих команд (крім самого користувача)
    members = User.objects.filter(
        team__in=teams).exclude(id=user.id).distinct()

    return members
