from django import template


register = template.Library()

@register.filter
def model_type(instance):
    return type(instance).__name__

@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'You'
    return user.username

@register.filter
def format_date(time):
    return time.strftime("%I:%M%p, %-d %B %y")

@register.simple_tag
def get_rating(rate):
    return '★' * rate + '☆' * (5-rate)
