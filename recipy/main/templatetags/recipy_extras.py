from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter('endswith')
@stringfilter
def endswith(text, ends):
    return text.endswith(ends)


@register.filter(needs_autoescape=True)
@stringfilter
def read_more(text, word_count=100, autoescape=True):
    words = text.split()
    word_count = int(word_count)

    if len(words) > word_count:
        return mark_safe("""
            <span>{initial_text}</span><span class="to-be-hide">...</span>
            <br class="to-be-hide">
            <btn class="btn btn-sm btn-default read-more-button to-be-hide">
                Show more <i class="fas fa-xs fa-chevron-down"></i>
            </btn>
            <span class="more-text" style="display: none;">{remaining_text}</span>
        """.format(
            initial_text=' '.join(words[:word_count]),
            remaining_text=' '.join(words[word_count:])
        ))

    return text
