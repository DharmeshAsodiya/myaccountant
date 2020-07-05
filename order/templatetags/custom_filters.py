from django import template
register = template.Library()


@register.filter
def total_quantity(arg):
    return sum(d.get('qty') for d in arg)
