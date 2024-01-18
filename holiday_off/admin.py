from django.contrib import admin

from holiday_off.models import OffDuty,Holiday,Holiday
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


admin.site.register(OffDuty)
admin.site.register(Holiday)
