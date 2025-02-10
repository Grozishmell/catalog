from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('game', 'Игра'),
        ('movie', 'Фильм'),
        ('book', 'Книга'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    release_date = models.DateField(verbose_name="Дата создания")
    image = models.ImageField(upload_to='items/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.title


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.item}'