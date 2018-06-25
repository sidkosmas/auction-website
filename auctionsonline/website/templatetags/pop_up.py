from django import template
from ..models import User
from django.utils import timezone

register = template.Library()

@register.filter(name='pop')
def pop(value, id):
    for v in value:
        if v.id == id:
            return True
    
    return False

@register.filter(name="time_left")
def time_left(value):
    t = value - timezone.now()
    days, seconds = t.days, t.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    st = str(minutes) + "m " + str(seconds) + "s"
    return st

@register.filter(name="current_price")
def current_price(value):
    current_cost = 0.20 + (value.number_of_bids * 0.20)
    current_cost = "%0.2f" % current_cost
    return current_cost

register.filter('pop', pop)
register.filter('time_left', time_left)
