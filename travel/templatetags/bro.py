from django import template
from datetime import datetime

register = template.Library()


@register.filter
def bro(value):
    return value.replace("h", "h ")


@register.filter
def timeReverse(value):
    list = value.split('-')
    list.reverse()
    new_value = list[0] + "." + list[1] + "." + list[2]
    return new_value


def format_date(date_string):
    # Parse the date string to a datetime object using strptime
    date_obj = datetime.strptime(date_string, '%d.%m.%Y %H:%M')

    # Format the datetime object to the specified format using strftime
    formatted_date = date_obj.strftime('%B %d, %Y, %I:%M %p')

    # Replace 'AM' with 'a.m.' and 'PM' with 'p.m.'

    # Strip leading zero from the hour part if it exists
    formatted_date = formatted_date.replace(' 0', ' ')

    return formatted_date


@register.filter
def timeReverseBookings(value):
    list = value.split('T')
    # list.reverse()
    dateNew = list[0]
    dateNewList = dateNew.split('-')
    dateNewList.reverse()

    timeNew = list[1]
    timeNew = timeNew[:-3]

    new_value = dateNewList[0] + "." + dateNewList[1] + \
        "." + dateNewList[2] + " " + timeNew

    new_value = format_date(new_value)

    return new_value
