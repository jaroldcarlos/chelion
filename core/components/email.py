SERVER_EMAIL = f'noreply@{SERVER_DOMAIN}'
INFO_EMAIL = f'info@{SERVER_DOMAIN}'

ADMINS = [
    ('Developer', 'django@ecdesign.es')
]

MANAGERS = ADMINS

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = SERVER_DOMAIN
    DEFAULT_FROM_EMAIL = f'noreply@{SERVER_DOMAIN}'
    EMAIL_HOST_USER = f'noreply@{SERVER_DOMAIN}'
    EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD', default='not_set')

    EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
    EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
