import sys
import pytz

from re import compile

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response


##############################################################################
#     _     ___   ____ ___ _   _   ____  _____ ___  _   _ ___ ____  ____     #
#    | |   / _ \ / ___|_ _| \ | | |  _ \| ____/ _ \| | | |_ _|  _ \| ____|   #
#    | |  | | | | |  _ | ||  \| | | |_) |  _|| | | | | | || || |_) |  _| |   #
#    | |__| |_| | |_| || || |\  | |  _ <| |__| |_| | |_| || ||  _ <| |___|   #
#    |_____\___/ \____|___|_| \_| |_| \_\_____\__\_\\___/|___|_| \_\_____|   #
#                                                                            #
##############################################################################
EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):

        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        if not request.user.is_authenticated or not request.user.is_superuser:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)


##########################################################################
#     ____  _____ ____  _   _  ____      _    ____  __  __ ___ _   _     #
#    |  _ \| ____| __ )| | | |/ ___|    / \  |  _ \|  \/  |_ _| \ | |    #
#    | | | |  _| |  _ \| | | | |  _    / _ \ | | | | |\/| || ||  \| |    #
#    | |_| | |___| |_) | |_| | |_| |  / ___ \| |_| | |  | || || |\  |    #
#    |____/|_____|____/ \___/ \____| /_/   \_\____/|_|  |_|___|_| \_|    #
#                                                                        #
##########################################################################
class UserBasedExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())


###############################################################################
#     _   _ ____  _____ ____ _____ ___ __  __ _____ ________  _   _ _____     #
#    | | | / ___|| ____|  _ \_   _|_ _|  \/  | ____|__  / _ \| \ | | ____|    #
#    | | | \___ \|  _| | |_) || |  | || |\/| |  _|   / / | | |  \| |  _|      #
#    | |_| |___) | |___|  _ < | |  | || |  | | |___ / /| |_| | |\  | |___     #
#     \___/|____/|_____|_| \_\|_| |___|_|  |_|_____/____\___/|_| \_|_____|    #
#                                                                             #
###############################################################################
# make sure you add `TimezoneMiddleware` appropriately in settings.py
class TimezoneMiddleware(object):
    """
    Middleware to properly handle the users timezone
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # make sure they are authenticated so we know we have their tz info.
        if request.user.is_authenticated():
            # we are getting the users timezone that in this case is stored in
            # a user's profile
            tz_str = request.user.profile.timezone
            timezone.activate(pytz.timezone(tz_str))
        # otherwise deactivate and the default time zone will be used anyway
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response
