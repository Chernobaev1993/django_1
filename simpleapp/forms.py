from django import forms
from .models import Product
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):  # Класс для быстрого создания форм на основе конкретных моделей
    description = forms.CharField(min_length=20)  # Можно сделать так, чтобы проверять длину описания и не писать clean

    class Meta:
        model = Product  # Саму модель прописываем в мета классе
        # fields = '__all__'  # Здесь мы указали, что хотим использоваться все поля модели, кроме pk
        fields = [  # Либо можем сами редактировать
            'name',
            'description',
            'quantity',
            'category',
            'price',
        ]

        # Если мы хотим сделать свои собственные проверки, нам нужно переопределить метод clean в форме
    def clean(self):
        # Вызовем в нашем методе clean из родительского класса и сохраним данные формы в cleaned_data.
        cleaned_data = super().clean()

        description = cleaned_data.get("description")
        name = cleaned_data.get("name")
        # Добавляем проверку длины описания, смотри выше вариант получше
        # if description is not None and len(description) < 20:
        #     raise ValidationError({
        #         "description": "Описание не может быть менее 20 символов."
        #     })

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


# python manage.py shell
# from simpleapp.forms import ProductForm
# f = ProductForm({'name': 'test', 'category': 1, 'price': 42, 'description': '', 'quantiry': 1})
# f.is_valid()
# False Django говорит, что форма невалидна. То есть мы допустили какие-то ошибки. Чтобы узнать, какие именно,
# обратимся к полю errors формы.

# f.errors
# {'description': ['This field is required.'], 'quantity': ['This field is required.']}
# Получается, мы не заполнили описание и количество товара

# f = ProductForm({'name': 'test', 'category': 1, 'price': 42, 'description': 'test', 'quantity': 1})
# f.is_valid()
# True
# f.errors
# {} В этот раз форма валидна, ошибок нет

# Для доступа к обработанным данным формы существует поле cleaned_data.
# f.cleaned_data
# {'name': 'test', 'description': 'test', 'quantity': 1, 'category': <Category: Видеокарты>, 'price': 42.0}
# И теперь мы видим, что вместо id категории подставился объект модели, а цена теперь имеет тип float.

# Если нам передадут в форму лишние данные, то при обработке они будут пропущены и не возникнет никаких ошибок.
# Попробуем добавить в форму лишний ключ 'extra'.
# f = ProductForm({'name': 'test', 'category': 1, 'price': 42, 'description': 'test', 'quantity': 1, 'extra': 123})
# f.is_valid() True
# f.errors {}
# f.cleaned_data
# {'name': 'test', 'description': 'test', 'quantity': 1, 'category': <Category: Видеокарты>, 'price': 42.0}

# Теперь самое интересное. Если мы напечатаем объект формы, то увидим сгенерированный html.
# Именно этот html код и будет добавляться в шаблон, когда мы будем использовать в нем формы.
# f = ProductForm({'name': 'test', 'category': 1, 'price': 42, 'description': 'test', 'quantity': 1})
# print(f)
# Обратите внимание, что в полях html-формы уже проставлены значения из нашей: input с name="name" имеет value="test",
# select name="category" в теге с option value="1" имеет selected и так далее.



