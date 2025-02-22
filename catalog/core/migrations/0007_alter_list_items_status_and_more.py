# Generated by Django 5.1.6 on 2025-02-22 19:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_list_items_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_items',
            name='status',
            field=models.CharField(choices=[('watching', 'Смотрю'), ('completed', 'Просмотрено'), ('planned', 'Хочу посмотреть'), ('dropped', 'Брошено')], default='planned', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterUniqueTogether(
            name='list_items',
            unique_together={('user', 'item')},
        ),
    ]
