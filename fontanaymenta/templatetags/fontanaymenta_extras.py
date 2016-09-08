from django import template
from django.utils.html import mark_safe
import unicodedata

register = template.Library()

import re
@register.filter(name='highlight')
def highlight(text, filter):
    pattern = re.compile(r"(?P<filter>%s)" % filter, re.IGNORECASE)
    return mark_safe(re.sub(pattern, r"<span class='highlight'>\g<filter></span>", text))

@register.filter(name='stripaccents')
def stripaccents(value, arg=""):
    if type(value) == str:
        return value
    return ''.join((c for c in unicodedata.normalize('NFD', value) if unicodedata.category(c) != 'Mn'))

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})