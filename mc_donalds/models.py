from django.db import models
from datetime import datetime, timezone  # для получения текущего времени


class Order(models.Model):  # Сущность заказы
    time_in = models.DateTimeField(auto_now_add=True)  # auto_now_add - автоматическая запись при создании
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)  # False - доставка, True - самовывоз
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)  # Вторичный ключ в таблице Staff
    # Указываем промежуточную таблицу для связи многие-ко-многим
    products = models.ManyToManyField('Product', through='ProductOrder')

    def finish_order(self):  # Метод для завершения заказа
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60


class Product(models.Model):  # Сущность продукты
    name = models.CharField(max_length=255)
    # price = models.DecimalField(max_digits=7, decimal_places=2)
    price = models.FloatField(default=0)
    composition = models.TextField(default="Состав не указан")


class Staff(models.Model):  # Сущность персонал
    director, admin, cook, cashier, cleaner = 'DI', 'AD', 'CO', 'CA', 'CL'
    # Выбор профессий ограничен, поэтому сделаем кортеж
    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.CharField(max_length=255)
    # Так как список профессий ограничен, мы можем указать полю выборку
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class ProductOrder(models.Model):  # Промежуточная таблица продукт-заказ
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1)

    @property
    def amount(self):  # геттер для amount
        return self._amount

    @amount.setter
    def amount(self, value):  # сеттер дял amount с проверкой на отрицательное значение
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):  # Подсчет стоимости товаров
        product_price = self.product.price
        return product_price * self.amount


# Don't forget to make migrations
