# Generated by Django 4.2 on 2023-11-18 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('identification', models.CharField(max_length=50, unique=True, verbose_name='identification')),
                ('names', models.CharField(help_text="employee's names", max_length=100, verbose_name='employee names')),
                ('last_names', models.CharField(help_text="employee's lastnames", max_length=100, verbose_name='employee last names')),
                ('role', models.CharField(choices=[('management', 'management'), ('hr', 'human resources'), ('quality', 'quality'), ('prod_manager', 'production manager'), ('prod', 'production'), ('accounting', 'accounting')], default='prod', help_text='employee role', max_length=20, verbose_name='role')),
                ('birthday', models.DateField(help_text='birthday of the employee', null=True, verbose_name='birthday')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='Joining date')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last Login')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='OOO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('ooo_type', models.CharField(choices=[('paid_leave', 'paid leave'), ('non_paid_leave', 'non paid leave'), ('work_accident', 'work accident'), ('non_work_accident', 'non_work_accident'), ('paid_permit', 'paid permit'), ('non_paid_permit', 'non paid permit')], help_text='out of office time', max_length=20, verbose_name='out of office')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='employee')),
            ],
            options={
                'verbose_name': 'out of office',
                'verbose_name_plural': 'out of office',
                'db_table': 'ooo',
            },
        ),
    ]