from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)  # Регистрируем модели, чтобы видеть их в админ панели
admin.site.register(Product)
