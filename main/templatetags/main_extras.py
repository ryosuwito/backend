from django import template
register = template.Library()

from main import templatedata


@register.filter('is_string')
def is_string(val):
    return isinstance(val, basestring)


@register.inclusion_tag('main_snippet/career_menu.html')
def career_menu():
    return {'menu_items': templatedata.get_sidebar_menu_items()}
