from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter('endswith')
@stringfilter
def endswith(text, ends):
    return text.endswith(ends)
