# Generated by Django 5.1.3 on 2024-12-03 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_answertest_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='testforuser',
            name='answer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.answertest'),
        ),
    ]
