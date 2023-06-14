from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag()  # Регистрируем собственный тег с датой, в нужном нам формате
def current_time(format_string='%b %d %Y'):
    return datetime.utcnow().strftime(format_string)


# Тег для того, чтобы работала фильтрация и пагинация вместе
@register.simple_tag(takes_context=True)  # Для работы тега требуется передать контекст
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()  # Позволяет скопировать все параметры текущего запроса.
    for k, v in kwargs.items():  # Устанавливаем новые значения, которые нам передали при использовании тега.
        d[k] = v
    return d.urlencode()  # Кодируем параметры в формат, который может быть указан в строке браузера
