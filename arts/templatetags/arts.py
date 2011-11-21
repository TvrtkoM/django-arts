from django import template

from ..models import Artist, Art

register = template.Library()

@register.filter
def arts(user_):
    '''
    get all arts for specified user
    '''
    return Art.objects.filter(artist=Artist.objects.get(user=user_))

@register.filter
def art_count(user_):
    '''
    number of arts for specified user
    '''
    return len(arts(user_))
