# Generated by Django 4.2.7 on 2023-12-28 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0021_remove_schedule_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='status',
        ),
        migrations.AddField(
            model_name='submittedtask',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
