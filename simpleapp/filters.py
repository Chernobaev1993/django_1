from django_filters import FilterSet, ModelChoiceFilter
from .models import Product, Category


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ProductFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='category__name',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Любая'
    )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Product
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = {
            'name': ['icontains'],  # поиск по названию
            'quantity': ['gt'],     # количество товаров должно быть больше или равно
            'price': [
                'lt',  # цена должна быть меньше или равна указанной
                'gt',  # цена должна быть больше или равна указанной
            ],
        }
