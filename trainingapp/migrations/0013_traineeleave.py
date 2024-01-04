# Generated by Django 4.2.7 on 2023-12-26 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0012_trainerleave'),
    ]

    operations = [
        migrations.CreateModel(
            name='traineeLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('status', models.CharField(max_length=20, null=True)),
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainingapp.trainees')),
            ],
        ),
    ]