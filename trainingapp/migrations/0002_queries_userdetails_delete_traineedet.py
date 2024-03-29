# Generated by Django 4.2.7 on 2023-12-21 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='queries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('question', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='userdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=255)),
                ('Join_Date', models.DateField()),
                ('phone', models.CharField(max_length=255)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('Docs', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('status', models.CharField(default='pending', max_length=20)),
                ('dep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainingapp.department')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Traineedet',
        ),
    ]
