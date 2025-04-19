from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def comma_wrap(value):
    """
    Replace commas with a comma followed by a <wbr> tag,
    so that browsers can break lines after commas.
    """
    if not isinstance(value, str):
        value = str(value)
    return mark_safe(value.replace(',', ',<wbr>'))