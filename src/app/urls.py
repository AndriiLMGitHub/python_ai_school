from django.urls import path
from . import views

urlpatterns = [
    # Dashboard urlpattern
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Tasks all urlpattern
    path('dashboard/all/tasks/', views.get_all_tasks_view, name='all-tasks'),
    # Task create urlpattern
    path('dashboard/new-tasks/', views.new_tasks_view, name='new-tasks'),
    # Task detail urlpattern
    path(
        'dashboard/task/detail/<int:task_id>/',
        views.task_detail_view,
        name='task-detail'
    ),
    # Team urlpattern
    path(
        'dashboard/teams/',
        views.teams_view,
        name='teams'
    ),
    # Team detail urlpattern
    path(
        'dashboard/team/detail/<int:team_id>/',
        views.team_detail_view,
        name='team-detail'
    ),
    path('dashboard/team/create/', views.create_team_view, name='create-team'),

    # Test create urlpattern
    path('dashboard/tests/', views.list_test_view, name='list-tests'),
    path('dashboard/tests/detail/<int:test_id>/',
         views.test_detail_view, name='test-detail'),
    # API urlpattern for creating test
    path('tests/create/test/', views.create_test_view, name='create-test'),
    path('dashboard/create/test/',
         views.create_test_page, name='create-test-page'),

    # Assessments urlpattern
    path('dashboard/assessments/', views.assessments_view, name='assessments'),

]
