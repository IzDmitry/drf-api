# Generated by Django 4.1 on 2023-09-30 16:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1)])),
                ('worth', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('price', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parcel.category')),
            ],
        ),
    ]
