from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """Return True if value starts with arg."""
    return str(value).startswith(str(arg))
