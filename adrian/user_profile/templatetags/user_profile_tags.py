from django import template

from user_profile import models as user_profile_models

register = template.Library()

@register.inclusion_tag('users/show_main_contacts.html')
def show_main_contacts():
    main_contacts_user = user_profile_models.UserProfile.objects.filter(use_contacts_as_main=True)
    if main_contacts_user:
        return {'user': main_contacts_user[0]}
    else:
        return {'user': None}
