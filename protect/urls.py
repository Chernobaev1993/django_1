from django.urls import path
from .views import IndexView

urlpatterns = [
    # Просто перенаправляемся в представление IndexView
    path('', IndexView.as_view()),
]