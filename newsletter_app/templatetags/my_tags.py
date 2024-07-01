from django import template

register = template.Library()


@register.filter()
def only_60(some_text):
    el_list = list(some_text)
    return f'{''.join(el_list)[:60]}...'


@register.filter()
def only_100(some_text):
    el_list = list(some_text)
    return f'{''.join(el_list)[:100]}...'


@register.filter()
def media_filter(path):
    if path:
        return f'/media/{path}'
    return '#'
