from django.urls import path
from .views import IndexView

urlpatterns = [
    # Просто перенаправляемся в представление IndexView в views.py
    path('', IndexView.as_view()),
]