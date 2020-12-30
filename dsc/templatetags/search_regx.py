import re

from django import template

register = template.Library()

@register.filter
def find_match(text, regx):
    """Return True if regx found in text else returns False"""
    match = re.search(regx, text,  re.I)
    if match is None:
        return False
    return True
