from django import template
from users.models import Profile

register = template.Library()

@register.simple_tag
def moderators():
    return Profile.objects.filter(role="moderator")