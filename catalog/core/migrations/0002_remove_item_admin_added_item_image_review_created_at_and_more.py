# Generated by Django 5.1.6 on 2025-02-07 12:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='admin_added',
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='items/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('game', 'Игра'), ('movie', 'Фильм'), ('book', 'Книга')], max_length=10, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='release_date',
            field=models.DateField(verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
