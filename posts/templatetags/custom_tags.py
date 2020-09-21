from django import template

register = template.Library()

@register.filter(name='match')
def match(value, arg):
    
    x = len(value.filter(liked_by__username=arg))>0
    return str(x)