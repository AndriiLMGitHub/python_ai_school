from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Team(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    image = models.FileField(upload_to="teams/photos/", null=True, blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tasks',
        blank=True,
    )
    name = models.CharField(max_length=128)
    team = models.ForeignKey(
        Team, blank=True, null=True, on_delete=models.SET_NULL, related_name='tasks')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    image = models.FileField(
        upload_to="tasks/images/",
        null=True,
        blank=True,
        help_text="Image to task"
    )
    task_image = models.FileField(
        upload_to="tasks/images/for/solving/",
        null=True,
        blank=True,
        help_text="The image to solve"
    )

    def __str__(self):
        return self.name


# Test models
class TestWorkRequest(models.Model):
    DIFFICULTY = (
        ('легкий', 'Легкий'),
        ('середньої складності', 'Середньої складності'),
        ('тяжкий', 'Тяжкий'),
    )
    FORMS = (
        ('7', '7 клас'),
        ('8', '8 клас'),
        ('9', '9 клас'),
    )
    title = models.CharField(max_length=128)
    topic = models.CharField(max_length=128)
    difficulty = models.CharField(
        max_length=128,
        choices=DIFFICULTY,
        default='легкий'
    )
    form_class = models.CharField(
        max_length=128, null=True, blank=True, choices=FORMS, default='7')
    description = models.TextField(null=True, blank=True)
    quantity_questions = models.PositiveIntegerField(default=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TestWorkResponse(models.Model):
    test_work = models.ForeignKey(TestWorkRequest, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answers = models.TextField(null=True, blank=True)
    count_questions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Test work result for {self.test_work.title}"


class TestForUser(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tests',
        blank=True,
    )
    test_response = models.ForeignKey(
        TestWorkResponse,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        users_list = ', '.join(
            user.email if user.email else "Unknown" for user in self.users.all())
        return f"TestForUser(id={self.id}, users=[{users_list}])"


class AnswerTest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    test = models.ForeignKey(
        TestWorkResponse, on_delete=models.CASCADE)
    answers = models.JSONField(null=True, blank=True)
    score = models.PositiveIntegerField(default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(12),
    ],)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Answer test(user={self.user.email}, score={self.score})"
