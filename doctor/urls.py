from django.urls import path
# Импортируем созданные нами представления
from .views import AppointmentView

urlpatterns = [
    # Путь для представления создания объекта
    path('create/', AppointmentView.as_view(), name='appointments'),
]