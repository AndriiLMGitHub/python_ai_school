# Generated by Django 5.1.3 on 2024-12-02 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_testforuser_test_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='testworkresponse',
            name='answers',
            field=models.TextField(blank=True, null=True),
        ),
    ]
