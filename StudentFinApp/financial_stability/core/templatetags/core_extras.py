from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return value - arg
    except (ValueError, TypeError):
        try:
            return Decimal(value) - Decimal(arg)
        except (ValueError, TypeError, InvalidOperation):
            return 0
            
@register.filter
def absolute(value):
    """Return the absolute value."""
    try:
        return abs(value)
    except (ValueError, TypeError):
        return 0 