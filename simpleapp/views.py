# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
# List выводит список объектов модели, Detail - подробно об одном, Create - создание
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from datetime import datetime  # Для получения текущей даты/времени
from .filters import ProductFilter
from .forms import ProductForm


class ProductsList(ListView):
    model = Product  # Указываем модель, объекты которой мы будем выводить

    ordering = '-name'  # Поле, которое будет использоваться для сортировки объектов
    # ordering = '-name'  # Обратная сортировка

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'

    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
    paginate_by = 1  # вот так мы можем указать количество записей на странице

    # Вот так мы можем использовать дженерик ListView для вывода списка товаров:
    #
    # 1. Создаем свой класс, который наследуется от ListView.
    # 2. Указываем модель, из которой будем выводить данные.
    # 3. Указываем поле сортировки данных модели (необязательно).
    # 4. Записываем название шаблона.
    # 5. Объявляем, как хотим назвать переменную в шаблоне.

    # Если поступит задача отфильтровать по цене, то в текущем виде мы не сможем этого сделать
    # Для этого мы будем использовать queryset и там делаем фильтр и можно даже сортировку туда же:
    # queryset = Product.objects.filter(
    #     price__lt=56000  # Выведем только те продукты, у которых цена меньше 56000
    # ).order_by('-name')

    # Метод get_context_data позволяет нам изменить словарь данных, который будет передан в шаблон.
    # Изначально за нас это делает само представление, но мы можем изменить этот словарь (добавить что-то)
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)

        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()

        # Добавим ещё одну пустую переменную, чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['next_sale'] = None
        context['next_sale'] = 'Распродажа в среду!'

        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        return context

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем обычный запрос
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs  # Возвращаем из функции отфильтрованный список товаров


class ProductDetail(DetailView):
    model = Product  # Модель всё та же, но мы хотим получать информацию по отдельному товару
    template_name = 'product.html'  # Используем другой шаблон — product.html
    context_object_name = 'product'  # Название объекта, в котором будет выбранный пользователем продукт
    # Будет выводить товар как, как мы описали его в методе __str__
    # Мы также можем указать Django как называть идентификатор в urlpatterns (по-умолчанию стоит pk)
    # pk_url_kwarg = 'id'


# Добавляем новое представление для создания товаров.
class ProductCreate(CreateView):
    form_class = ProductForm  # Указываем нашу разработанную форму
    model = Product  # модель товаров
    template_name = 'product_edit.html'  # и новый шаблон, в котором используется форма.


# Добавляем представление для изменения товара. Обрати внимание, что мы используем тот же шаблон! И ту же форму
class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


# Представление удаляющее товар.
class ProductDelete(DeleteView):
    # Обрати внимание, мы не используем форму для удаления товара
    model = Product
    template_name = 'product_delete.html'
    # Однако добавляем перенаправление после удаления, то же самое, что и reverse
    success_url = reverse_lazy('product_list')
