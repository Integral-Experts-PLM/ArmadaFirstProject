from django import template

register = template.Library()

@register.filter
def format_datetime(value):
    try:
        date_part = value.split('T')[0]
        return date_part
    except (ValueError, AttributeError):
        return ''

@register.filter
def extract_after_colon(value):
    try:
        if value is not None:
            if ":" in value:
                return value.split(":")[1].strip()
        return value
    except (ValueError, AttributeError):
        return ''
    
