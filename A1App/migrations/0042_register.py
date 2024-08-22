# Generated by Django 3.2.23 on 2024-07-15 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('A1App', '0041_delete_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25)),
                ('age', models.CharField(max_length=2)),
                ('member_gender', models.CharField(max_length=10)),
                ('contactno', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('register_date', models.DateField()),
                ('password', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
