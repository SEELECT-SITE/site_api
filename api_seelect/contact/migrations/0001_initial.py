# Generated by Django 4.2.3 on 2023-10-20 14:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=256)),
                ('phone', models.CharField(max_length=16)),
                ('message', models.CharField(max_length=1024)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
