from django import template

register = template.Library()

@register.filter
def extract_discount_amount(message):
    return message.split(' ')[1]