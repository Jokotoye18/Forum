from django import template

register = template.Library()


@register.filter
def substract_by(value, arg):
        return value - arg
    