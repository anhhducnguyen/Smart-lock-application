from modeltranslation.translator import TranslationOptions, register

from authentication.models import UserProfile


@register(UserProfile)
class UserProfileTranslation(TranslationOptions):
    # fields = ('name', 'sex', 'data')
    # fields = ["name"]
    pass