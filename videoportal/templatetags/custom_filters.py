from django import template
import datetime

register = template.Library()

@register.filter(name='secondstohms')
def secondstohms(value):
    if (value):
        return str(datetime.timedelta(seconds=int(value)))
