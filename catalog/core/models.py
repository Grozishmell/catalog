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


class List_Items(models.Model):
    status_choices = [
        ('not_watched', 'Не смотрю'),
        ('will_watch', 'Буду смотреть'),
        ('watching', 'Смотрю'),
        ('dropped', 'Заброшен'),
        ('watched', 'Просмотрено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Контент")
    review = models.ForeignKey('Review', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Отзыв",
                               related_name="list_items")
    status = models.CharField(max_length=20, choices=status_choices, default='not_watched')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.user} - {self.item}"


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Сохраняем отзыв
        super().save(*args, **kwargs)

        # Получаем или создаем запись List_Items для данного пользователя и предмета
        list_item, created = List_Items.objects.get_or_create(
            user=self.user,
            item=self.item
        )

        # Привязываем отзыв к записи List_Items
        list_item.review = self  # Здесь мы связываем отзыв с записью в List_Items

        # Логика изменения статуса в List_Items на основе рейтинга отзыва
        if self.rating >= 7:  # Пример: если рейтинг 7 или выше, статус меняем на "Просмотрено"
            list_item.status = 'watched'
        elif self.rating <= 3:  # Пример: если рейтинг ниже 3, ставим "Заброшено"
            list_item.status = 'dropped'
        else:
            list_item.status = 'watching'  # В других случаях статус будет "Смотрю"

        # Сохраняем изменения статуса и привязанный отзыв
        list_item.save()

    def __str__(self):
        return f'{self.user} - {self.item}'

