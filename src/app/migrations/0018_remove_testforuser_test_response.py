# Generated by Django 5.1.3 on 2024-12-01 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_testforuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testforuser',
            name='test_response',
        ),
    ]
