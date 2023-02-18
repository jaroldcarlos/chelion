from django.utils.translation import gettext as _

from dynamic_preferences.types import (
    BooleanPreference, LongStringPreference, FilePreference, StringPreference, ChoicePreference
)
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

from core.utils import list_of_themes

general = Section('general')
app = Section('app')


@global_preferences_registry.register
class app_name(StringPreference):
    section = app
    name = 'app_name'
    default = _('Default')
    required = True

@global_preferences_registry.register
class app_theme_backend(ChoicePreference):
    section = app
    name = 'app_theme_backend'
    choices = list_of_themes()
    default='default'

@global_preferences_registry.register
class VerificationEmail(BooleanPreference):
    section = app
    name = 'validated_email'
    default = False

@global_preferences_registry.register
class MaintenanceMode(BooleanPreference):
    section = general
    name = 'maintenance_mode'
    default = False

@global_preferences_registry.register
class MaintenaceModeText(LongStringPreference):
    section = general
    name = 'maintenance_mode_text'
    default = _( 'technical difficulties')
    required = False

@global_preferences_registry.register
class MaintenaceModeTitle(StringPreference):
    section = general
    name = 'maintenance_mode_title'
    default = _('maintenance')
    required = False
