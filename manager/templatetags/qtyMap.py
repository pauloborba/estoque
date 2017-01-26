from django import template

register = template.Library()

@register.filter
def qtyMap(val):
    if val == 0:
        qtyMapped = 'Suficiente'
    elif val == 1:
        qtyMapped = 'Pouco'
    else:
        qtyMapped = 'Acabou'
    return qtyMapped
