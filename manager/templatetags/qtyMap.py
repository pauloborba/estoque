from django import template

register = template.Library()

@register.filter
def qtyMap(val):
    return 'Suficiente' if val else 'Comprar'
