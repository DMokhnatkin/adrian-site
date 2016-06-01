__author__ = 'Dmitriy'

from user_profile import models as user_profile_models
from django import template
from slideshows import models
from django.template import loader, Context


register = template.Library()

@register.simple_tag()
def render_slideshow(slideshow_name, template_path='slideshows/render.html'):
    t = loader.get_template(template_path)
    slideshow = models.Slideshow.objects.get(name=str(slideshow_name))
    context = Context({'slideshow': slideshow})
    return t.render(context)
