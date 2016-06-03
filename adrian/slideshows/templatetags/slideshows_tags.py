__author__ = 'Dmitriy'

from django import template
from django.template import Context, loader

from slideshows import models
from user_profile import models as user_profile_models

register = template.Library()

@register.simple_tag()
def render_slideshow(slideshow_name, template_path='slideshows/render.html'):
    t = loader.get_template(template_path)
    slideshow = models.Slideshow.objects.get(name=str(slideshow_name))
    context = Context({'slideshow': slideshow})
    return t.render(context)
