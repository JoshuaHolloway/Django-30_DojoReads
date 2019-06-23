# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-23 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DojoApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='DojoApp.Users')),
            ],
        ),
        migrations.RemoveField(
            model_name='messages',
            name='user',
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
    ]