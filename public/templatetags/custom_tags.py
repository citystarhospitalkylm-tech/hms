# public/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except AttributeError:
        return None
@register.filter
def eq(a, b):
    try:
        return str(a).lower() == str(b).lower()
    except Exception:
        return False