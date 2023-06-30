from django.urls import path
# Импортируем созданные нами представления
from .views import ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом, а Django ожидает функцию,
    # нам надо представить этот класс в виде view. Для этого вызываем метод as_view.
    path('', ProductsList.as_view(), name='product_list'),

    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
    # path('<int:id>', ProductDetail.as_view()),  # можем изменить с помощью pk_url_kwarg

    # Путь для представления создания объекта
    path('create/', ProductCreate.as_view(), name='product_create'),

    # Изменять товар будем по такому адресу, дописывая в конце update/
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),

    # Указываем путь для удаления объекта
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
]
