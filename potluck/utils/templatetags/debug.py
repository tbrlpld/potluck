from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def debug_breakpoint(context):
    breakpoint()
