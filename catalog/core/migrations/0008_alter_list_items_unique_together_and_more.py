# Generated by Django 5.1.6 on 2025-02-22 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_list_items_status_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='list_items',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='list_items',
            name='status',
            field=models.CharField(choices=[('not_watched', 'Не смотрю'), ('will_watch', 'Буду смотреть'), ('watching', 'Смотрю'), ('dropped', 'Заброшен')], default='not_watched', max_length=20),
        ),
    ]
