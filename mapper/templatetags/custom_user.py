from django import template

register = template.Library()

@register.simple_tag
def user_display(user):
    """
    Show first_name + last_name, falling back to username
    """
    full = user.get_full_name()
    return full if full.strip() else user.get_username()