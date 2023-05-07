from django import template

register = template.Library()

@register.filter
def bro(value):
    return value.replace("h","h ")



@register.filter
def timeReverse(value):
    list = value.split('-')
    list.reverse()
    new_value = list[0] + "-" + list[1] + "-" + list[2]
    return new_value 