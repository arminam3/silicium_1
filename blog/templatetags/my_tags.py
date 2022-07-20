from django import template
from django.utils.safestring import SafeString

from blog.models import Category

register = template.Library()

@register.simple_tag
def ME():
    return 'ME'


@register.inclusion_tag("blog/partial/category_nav.html")
def category_nav():
    return {
    'categories': Category.objects.filter(status=True),
    }



