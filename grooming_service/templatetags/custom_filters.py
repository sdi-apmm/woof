from django import template
from datetime import timedelta
from django.utils import timezone

register = template.Library()


@register.filter
def add_hours(value, arg):
    result = timezone.now() + timedelta(hours=arg)
    return result


@register.filter(name='get_current_time')
def get_current_time(args):
    return timezone.now()