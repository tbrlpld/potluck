from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def inject_class(value, attr):
    return mark_safe(value[:-1] + f' class="{attr}">')
