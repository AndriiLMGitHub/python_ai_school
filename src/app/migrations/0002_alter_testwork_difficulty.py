# Generated by Django 5.1.3 on 2024-11-30 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testwork',
            name='difficulty',
            field=models.CharField(choices=[('легкий', 'Легкий'), ('середньої складності', 'Середньої складності'), ('тяжкий', 'Тяжкий')], default='легкий', max_length=128),
        ),
    ]
