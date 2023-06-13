from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {  # Добавили выбор валюты
    'rub': '₽',
    'usd': '$',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
# @register.filter(name='currency_rub')  # название можем менять самостоятельно
@register.filter()
def currency(value, code='rub'):  # Будем указывать значение в фильтре, по-умолчанию Рубли
    """
    value: значение, к которому нужно применить фильтр
    code: код валюты
    """
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'
