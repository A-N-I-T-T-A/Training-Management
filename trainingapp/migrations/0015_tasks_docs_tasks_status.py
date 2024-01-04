# Generated by Django 4.2.7 on 2023-12-26 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0014_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='docs',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
