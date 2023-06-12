from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):  # Сущность "товар" для нашей витрины
    name = models.CharField(max_length=50, unique=True,)  # названия товаров не должны повторяться
    description = models.TextField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)])  # Минимальное значение = 0

    # поле категории будет ссылаться на модель категории
    # все продукты в категории будут доступны через поле products
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):  # Как печатать объект
        return f'{self.name.title()}: {self.description[:40]} ({self.price})'


class Category(models.Model):  # Категория, к которой будет привязываться товар
    name = models.CharField(max_length=100, unique=True)  # названия категорий тоже не должны повторяться

    def __str__(self):
        return self.name.title()
