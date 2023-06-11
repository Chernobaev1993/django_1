from django.urls import path
# Из встроенного приложения auth импортируем представления для аутентификации
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me

urlpatterns = [
    # Указываем имя шаблона для вывода формы и установим им имена
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),

    # Представления для кнопки logout
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),

    # Представление для регистрации
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),

    path('upgrade/', upgrade_me, name='upgrade')
]
