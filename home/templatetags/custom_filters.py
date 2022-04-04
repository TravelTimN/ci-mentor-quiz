import random
from django import template
register = template.Library()


@register.filter
def shuffle(arg):
    # https://stackoverflow.com/a/7162816
    shuffled_list = list(arg)[:]
    random.shuffle(shuffled_list)
    return shuffled_list


@register.filter
def replace(string, replace="*|*"):
    # https://stackoverflow.com/a/35477957
    find, replace = replace.split("|")
    return string.replace(find, replace)


@register.filter
def startswith(text, starter):
    # https://simpleisbetterthancomplex.com/snippets/startswith/
    if isinstance(text, str):
        return text.startswith(starter)
    return False
