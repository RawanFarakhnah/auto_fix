# Generated by Django 4.2.20 on 2025-04-05 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('description', models.TextField(blank=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.address')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='workshops.workshop')),
            ],
        ),
    ]
