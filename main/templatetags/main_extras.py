from django import template
register = template.Library()


@register.filter('is_string')
def is_string(val):
    return isinstance(val, basestring)
