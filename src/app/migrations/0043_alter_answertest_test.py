# Generated by Django 5.1.3 on 2025-01-03 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_testworkrequest_form_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answertest',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testworkresponse'),
        ),
    ]
