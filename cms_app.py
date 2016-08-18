# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class DSCApphook(CMSApp):
    name = _("Device Servers Catalogue")
    urls = ["dsc.urls_dsc"]

apphook_pool.register(DSCApphook)
