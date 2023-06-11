from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    # Модель формы, которую реализует данный дженерик
    model = User

    # Форма, которая заполняется пользователем
    form_class = BaseRegisterForm

    # URL, на который нужно направить пользователя после успешного ввода данных в форму.
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')
