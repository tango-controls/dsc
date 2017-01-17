from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=False)
def safe_for_robots(text, autoescape=False):
    """ Divides the text into pieces these are then connected by javascript. This way one can hide emials from robots"""
    text += '  '
    safe_text = '\n<script language="JavaScript">\n'
    safe_text += 'var unchunked="";\n'
    chunks = [text[i:i+3] for i in range(0, len(text), 3)]
    for j in range(0, len(chunks)):
        safe_text +='unchunked=unchunked.concat("%s"); ' % chunks[j].replace('"','\\"')
        if len(safe_text)%78 == 0:
            safe_text += '\n'

    safe_text += 'document.write(unchunked);'
    safe_text += '</script>'
    return mark_safe(safe_text)