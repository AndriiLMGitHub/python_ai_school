# Generated by Django 5.1.3 on 2024-12-01 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_testforuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testforuser',
            name='user',
        ),
        migrations.AlterField(
            model_name='testforuser',
            name='test_response',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tests_for_user', to='app.testworkresponse'),
        ),
    ]
