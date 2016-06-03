__author__ = 'Dmitriy<paparome@ya.ru>'

from django.contrib import admin

from user_profile import models as user_profile_models


class UserPhoneNumberInLine(admin.StackedInline):
    model = user_profile_models.PhoneNumber
    extra = 1


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserPhoneNumberInLine]


admin.site.register(user_profile_models.UserProfile, UserProfileAdmin)
