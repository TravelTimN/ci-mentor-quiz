import random
from django import template
register = template.Library()


@register.filter
def shuffle(arg):
    # https://stackoverflow.com/questions/7162629/django-shuffle-in-templates/7162816  # noqa
    shuffled_list = list(arg)[:]
    random.shuffle(shuffled_list)
    return shuffled_list
