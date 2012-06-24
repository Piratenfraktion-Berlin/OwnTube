from django import template
import datetime

register = template.Library()

@register.filter(name='secondstohms')
def secondstohms(value):
    ''' This is used to have a nicer format for the video duration in the template'''
    if (value):
        return str(datetime.timedelta(seconds=int(value)))
