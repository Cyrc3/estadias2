from django import template

register = template.Library()

@register.filter
def currency_format(value):
    return "{:,.2f}".format(value)