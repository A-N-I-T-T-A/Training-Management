# Generated by Django 4.2.7 on 2023-12-26 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0010_trainees_trainer_delete_assigntrainee'),
    ]

    operations = [
        migrations.CreateModel(
            name='traineeAttendence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=20, null=True)),
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainingapp.trainees')),
            ],
        ),
    ]
