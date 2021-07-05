from django import template

register = template.Library()


@register.filter
def debug_breakpoint(value):
    breakpoint()
