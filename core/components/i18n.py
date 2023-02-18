from django.utils.translation import gettext_lazy

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('es', gettext_lazy('Español')),
    ('en', gettext_lazy('English')),
)
LOCALE_PATHS = (BASE_DIR / 'locale', )
