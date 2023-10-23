from django import template

register = template.Library()

@register.filter
def format_datetime(value):
    try:
        # Split the value at 'T' to separate the date part
        date_part = value.split('T')[0]
        return date_part
    except (ValueError, AttributeError):
        # Handle invalid or empty values gracefully
        return ''

@register.filter
def extract_after_colon(value):
    try:
        if value is not None:
            # Check if the value contains a colon
            if ":" in value:
                # Split the value at the colon and return the second part
                return value.split(":")[1].strip()
        # Handle cases where value is None or doesn't contain a colon
        return value
    except (ValueError, AttributeError):
        # Handle other exceptions gracefully
        return ''
    
