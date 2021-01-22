# Generated by Django 2.0.2 on 2020-12-03 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('city', models.CharField(max_length=50, verbose_name='Ciudad')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50, verbose_name='Nombre')),
                ('lastName', models.CharField(max_length=50, verbose_name='Apellido')),
                ('date', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('photo', models.ImageField(upload_to='photos/', verbose_name='Foto')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Business', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
            },
        ),
    ]
