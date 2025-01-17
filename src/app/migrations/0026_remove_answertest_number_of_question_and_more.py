# Generated by Django 5.1.3 on 2024-12-02 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_answertest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answertest',
            name='number_of_question',
        ),
        migrations.RemoveField(
            model_name='answertest',
            name='user_choose',
        ),
        migrations.AddField(
            model_name='answertest',
            name='answers',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='answertest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
