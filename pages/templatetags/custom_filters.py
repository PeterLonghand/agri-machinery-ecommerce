from django import template

register = template.Library()

@register.filter
def spacify(value):
    """Displays number with spaces for thousand separator"""
    return '{:,}'.format(int(value)).replace(',', ' ')