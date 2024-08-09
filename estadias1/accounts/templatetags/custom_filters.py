from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def currency_format(value):
    try:
        # Asegúrate de que el valor sea un número
        value = Decimal(value)
    except (ValueError, TypeError):
        return value  # O un valor predeterminado o mensaje de error

    # Formatea el valor como una cadena en formato de moneda
    return f"${value:,.2f}"



'''from django import template

register = template.Library()

@register.filter
def currency_format(value):
    return "{:,.2f}".format(value)'''