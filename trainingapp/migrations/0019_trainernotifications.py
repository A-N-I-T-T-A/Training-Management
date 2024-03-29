# Generated by Django 4.2.7 on 2023-12-26 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0018_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerNotifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify', models.CharField(max_length=255, null=True)),
                ('link', models.URLField()),
                ('read_status', models.BooleanField(default=False)),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainingapp.trainers')),
            ],
        ),
    ]
