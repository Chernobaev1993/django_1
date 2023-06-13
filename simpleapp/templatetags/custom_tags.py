from datetime import datetime

from django import template


register = template.Library()


@register.simple_tag()  # Регистрируем собственный тег с датой, в нужном нам формате
def current_time(format_string='%b %d %Y'):
    return datetime.utcnow().strftime(format_string)
