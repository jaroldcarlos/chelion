import os
import sys
import locale
# import logging

from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.static import serve


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


@login_required
def protected_serve_full(request, path, document_root=None, show_indexes=False):
    # logger = logging.getLogger(__name__)

    folder = (path.split('/')[0])
    if folder == "invoices":
        if request.user.is_authenticated:
            if request.user.is_staff:
                return serve(request, path, document_root, show_indexes)
            else:
                from apps.voucher.models import Voucher
                reference = (path.split('/')[1].split('_')[1])
                voucher = get_object_or_404(Voucher, reference=reference)

                if voucher.partner().id == request.user.partner.id:
                    return serve(request, path, document_root, show_indexes)

        return HttpResponseNotFound("restricted access")

    return serve(request, path, document_root, show_indexes)


def is_in_group(user, group):
    return user.groups.filter(name=group).exists()


def is_in_group_admin(user):
    return is_in_group(user, 'admin')


def is_in_group_staff(user):
    return is_in_group(user, 'staff')


def is_in_group_user(user):
    return is_in_group(user, 'user')


def print_http_response(f):
    """ Wraps a python function that prints to the console, and
    returns those results as a HttpResponse (HTML)"""

    class WritableObject:

        def __init__(self):
            self.content = []

        def write(self, string):
            self.content.append(string)

    def new_f(*args, **kwargs):
        printed = WritableObject()
        sys.stdout = printed
        f(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return HttpResponse(
            ['<BR>' if c == '\n' else c for c in printed.content]
        )
    return new_f


def humanreadable_timedelta(
        theDateAndTime,
        precise=False,
        complete=False,
        fromDate=None):

    if not theDateAndTime:
        return ""
    if not fromDate:
        fromDate = datetime.now(timezone.utc)
    if theDateAndTime > fromDate:
        return None
    elif theDateAndTime == fromDate:
        return _('now')

    delta = fromDate - theDateAndTime

    '''
    the timedelta structure does not have all units; bigger units are converted
    into smaller ones (hours -> seconds, minutes -> seconds, weeks > days, ...)
    but we need all units:
    '''
    deltaMinutes = delta.seconds // 60
    deltaHours = delta.seconds // 3600
    deltaYears = delta.days // 365
    deltaMonths = delta.days // 30
    deltaMinutes -= deltaHours * 60
    deltaWeeks = delta.days // 7
    deltaSeconds = delta.seconds - deltaMinutes * 60 - deltaHours * 3600
    deltaDays = delta.days - deltaWeeks * 7
    deltaMilliSeconds = delta.microseconds // 1000
    deltaMicroSeconds = delta.microseconds - deltaMilliSeconds * 1000

    valuesAndNames = [
        (deltaYears, _('year')),
        (deltaMonths, _('month')),
        (deltaWeeks, _('week')),
        (deltaDays, _('day')),
        (deltaHours, _('hour')),
        (deltaMinutes, _('minute')),
        (deltaSeconds, _('second'))
    ]
    if precise:
        valuesAndNames.append((deltaMilliSeconds, _('millisecond')))
        valuesAndNames.append((deltaMicroSeconds, _('microsecond')))

    text = ""
    for value, name in valuesAndNames:
        if complete:
            if value > 0:
                text += len(text) and ", " or ""
                text += "%d %s" % (value, name)
                text += (value > 1) and "s" or ""
        else:
            if value > 0:
                text += "%d %s" % (value, name)
                text += (value > 1) and "s" or ""
                break

    # replacing last occurrence of a comma by an 'and'
    if text.find(",") > 0:
        text = " and ".join(text.rsplit(", ", 1))

    return text


def currency(value):
    if not value:
        value = 0
    return locale.currency(value, symbol=False, grouping=True)


def validate_image(fieldfile_obj):
    if not fieldfile_obj:
        return

    filesize = fieldfile_obj.file.size
    megabyte_limit = 10

    if filesize > megabyte_limit*1024*1024:
        raise ValidationError(
            _('Max file size is {}MB').format(str(megabyte_limit))
        )


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.'))


def deg_to_dec(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


def dec_to_deg(deg, min, sec):
    if deg < 0:
        dec = -1.0 * deg + 1.0 * min/60.0 + 1.0 * sec/3600.0
        return -1.0 * dec


def list_of_themes(where='Backend'):
    from django.conf import settings

    list_themes = []
    folder = f'{settings.BASE_DIR}/templates/{where}'
    items = os.listdir(folder)

    for item in items:
        root_item = f'{settings.BASE_DIR}/templates/{where}/{item}'
        if os.path.isdir(root_item):
            list_themes.append([item, item])

    return list_themes
