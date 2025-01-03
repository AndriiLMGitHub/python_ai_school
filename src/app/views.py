from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from .models import Task, Team, TestWorkResponse, TestForUser, AnswerTest
from asgiref.sync import sync_to_async
from .forms import TaskForm, TeamForm, TestWorkForm, AnswerTestForm
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.db.models import Q
from .utils import get_team_members
from .g4f import get_g4f_answer, get_g4f_formula, get_g4f_stucture
from g4f.client import Client

# Create your views here.


@login_required(login_url="/account/signin/")
def dashboard_view(request):
    user = request.user
    is_social = UserSocialAuth.objects.filter(
        user=user).exists() if user.is_authenticated else False

    # Get team members for current user
    members = get_team_members(user)[:3]

    # Список всіх команд
    teams = Team.objects.all()

    # Завдання, безпосередньо призначені користувачу
    tasks = Task.objects.filter(users=user)
    # Завдання, пов'язані через команди користувача
    team_tasks = Task.objects.filter(team__members=user)
    # Об'єднання обох наборів завдань
    all_tasks = Task.objects.filter(
        Q(users=user) | Q(team__members=user)).distinct()

    return render(
        request,
        'app/dashboard/dashboard.html',
        {
            'is_social_user': is_social,
            'tasks': all_tasks,
            'teams': teams,
            'members': members,
        }
    )


def get_all_tasks_view(request):
    # Get today's date
    today = timezone.now().date()

    all_tasks = Task.objects.filter(
        Q(team__members=request.user) | Q(users=request.user))

    # Get filter criteria from request (default to "today")
    filter_option = request.GET.get('filter', 'all')

    # Filter tasks based on the selected filter option (today, week, month)
    if filter_option == 'today':
        tasks = Task.objects.filter(
            Q(created_at__date=today) | Q(team__members=request.user) | Q(users=request.user))
        messages.success(request, 'Показано завдання, створені сьогодні.')
    elif filter_option == 'week':
        start_of_week = today - timezone.timedelta(days=today.weekday())
        tasks = Task.objects.filter(
            Q(created_at__date__gte=start_of_week) | Q(team__members=request.user) | Q(users=request.user))
        messages.success(
            request, 'Показано завдання, створені за останній тиждень.')
    elif filter_option == 'month':
        tasks = Task.objects.filter(
            Q(created_at__year=today.year) | Q(created_at__month=today.month) | Q(team__members=request.user) | Q(users=request.user))
        messages.info(
            request, 'Показано завдання, створені за останній місяць.')
    elif filter_option == 'all':
        tasks = Task.objects.filter(
            Q(users=request.user) | Q(team__members=request.user))
        messages.info(request, 'Показані всі завдання.')
    else:
        tasks = Task.objects.none()
        messages.warning(request, 'Недійсний параметр фільтра.')

    return render(request, 'app/dashboard/all_tasks.html', {
        'tasks': tasks,
        'filter_option': filter_option,
        'all_tasks': all_tasks
    })


def new_tasks_view(request):
    tasks = Task.objects.filter(
        Q(users=request.user) | Q(team__members=request.user))
    tasks_undone = tasks.filter(is_completed=False)
    return render(request, 'app/dashboard/new_tasks.html', {'tasks': tasks, 'tasks_undone': tasks_undone})


def task_detail_view(request, task_id):
    form = TaskForm()
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.is_completed = True
            form.save()
            messages.success(request, 'Завдання позначено як виконане.')
            return redirect('new-tasks')
        else:
            messages.error(request, 'Помилка оновлення завдання.')

    return render(request, 'app/dashboard/task_detail.html', {'task': task, 'form': form})


# @never_cache
# @sync_to_async
def get_help_formula_view(request, task_id):
    task = Task.objects.get(pk=task_id)
    result = get_g4f_formula(task.description)
    return render(request, 'app/dashboard/get_help.html', {'response': result, 'task': task})


# @never_cache
# @sync_to_async
def get_help_answer_view(request, task_id):
    task = Task.objects.get(pk=task_id)
    result = get_g4f_answer(task.description)
    return render(request, 'app/dashboard/get_help.html', {'response': result, 'task': task})

# @never_cache
# @sync_to_async


def get_help_structure_view(request, task_id):
    task = Task.objects.get(pk=task_id)
    result = get_g4f_stucture(task.description)
    return render(request, 'app/dashboard/get_help.html', {'response': result, 'task': task})


# Team with Mememrs for team Views
def teams_view(request):
    teams_all = []
    teams = Team.objects.prefetch_related('members')
    for team in teams:
        teams_all.append(team)
    return render(request, 'app/dashboard/teams.html', {'teams': teams_all})


def team_detail_view(request, team_id):
    team = Team.objects.get(pk=team_id)
    team_members = team.members.all()
    # team_members = TeamMember.objects.filter(team=team)
    if request.method == 'POST':
        user = request.user
        if (user in team_members):
            messages.error(request, 'Ви вже є членом цієї команди.')
            return redirect('team-detail', team_id=team_id)
        else:
            team.members.add(user)
            messages.success(request, 'Ви успішно приєдналися до команди.')
            return redirect('team-detail', team_id=team_id)
    return render(request, 'app/dashboard/team_detail.html', {'team': team, 'team_members': team_members})


def create_team_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Команда створена успішно.')
            return redirect('teams')
        else:
            messages.error(request, 'Помилка створення команди.')
    else:
        form = TeamForm()
    return render(request, 'app/dashboard/create_team.html', {'form': form})


# @never_cache
# @sync_to_async
def create_test_view(request):
    result = ""
    form = TestWorkForm()
    if request.method == 'POST':
        form = TestWorkForm(request.POST)
        if form.is_valid():
            topic = request.POST.get('topic')
            description = request.POST.get('description')
            quantity = request.POST.get('quantity')
            form_class = request.POST.get('form_class')
            difficulty = request.POST.get('difficulty')
            result = g4f_create_test(
                topic=topic, difficulty=difficulty, form_class=form_class, description=description, quantity=str(
                    quantity)
            )
            form.save()
            TestWorkResponse.objects.create(
                test_work=form.instance,
                content=result,
            )
            messages.success(request, 'Тест успішно створено.')
            return render(request, 'app/tests/create_test.html', {'result': result})
        else:
            messages.error(request, 'Помилка створення тесту.')
    else:
        form = TestWorkForm()
    return render(request, 'app/tests/create_test.html', {'form': form, 'result': result})


def g4f_create_test(topic, difficulty, form_class, description, quantity):
    client = Client()

    # Add necessary parameters to the prompt
    promt = "Склади " + difficulty + " тест для " + form_class + "-го класу на тему " + \
        topic + description + "на " + quantity + "питань"

    # Make the API request and get the response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": promt
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content


def list_test_view(request):
    # Get today's date
    today = timezone.now().date()

    # Get filter criteria from request (default to "today")
    filter_option = request.GET.get('filter', 'all')

    # Filter tasks based on the selected filter option (today, week, month)
    if filter_option == 'today':
        tests = TestForUser.objects.filter(
            created_at__date=today, users=request.user)
        messages.success(request, 'Показано тести, створені сьогодні.')
    elif filter_option == 'week':
        start_of_week = today - \
            timezone.timedelta(days=today.weekday())
        tests = TestForUser.objects.filter(
            created_at__date__gte=start_of_week, users=request.user)
        messages.success(
            request, 'Показано тести, створені за останній тиждень.')
    elif filter_option == 'month':
        tests = TestForUser.objects.filter(
            created_at__year=today.year, created_at__month=today.month, users=request.user)
        messages.info(request, 'Показано тести, створені за останній місяць.')
    elif filter_option == 'all':
        tests = TestForUser.objects.all().filter(users=request.user)
        messages.info(request, 'Показані всі тести.')
    else:
        tests = TestForUser.objects.none()
        messages.warning(request, 'Недійсний параметр фільтра.')

    # Render the test list template with the filtered tasks

    return render(request, 'app/tests/test_list.html', {'tests': tests})


def test_detail_view(request, test_id):
    form = AnswerTestForm()
    test = TestForUser.objects.get(pk=test_id)
    if request.method == 'POST':
        answers = {}
        # Делим на 2, так как есть два поля на строку
        for i in range(1, len(request.POST) // 2 + 1):
            number_of_question = request.POST.get(f'number_of_question_{i}')
            user_choose = request.POST.get(f'user_choose_{i}')
            if number_of_question and user_choose:
                # Сохраняем как "вопрос: ответ"
                answers[number_of_question] = user_choose
            else:
                messages.error(request, 'Помилка відповіді на запитання.')
                break
        AnswerTest.objects.create(
            user=request.user,
            test=test.test_response,
            answers=answers,
            is_done=True,
        )
        messages.success(request, 'Відповіли на запитання успішно.')
        return redirect('test-detail', test.id)
    return render(request, 'app/tests/test_detail.html', {
        'test': test,
        'static_range': range(test.test_response.count_questions),
        'form': form,
    })


def assessments_view(request):
    context = {}
    return render(request, 'app/dashboard/assessments.html', context)
