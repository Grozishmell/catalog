# Generated by Django 5.1.6 on 2025-02-22 11:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_list_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_items',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.review'),
        ),
    ]
