from django import template
from ..models import User
register = template.Library()

@register.filter(name='pop')
def pop(value, id):
    for v in value:
        print(str(v.id) + " == " + str(id))
        if v.id == id:
            return True
    
    return False

register.filter('pop', pop)
