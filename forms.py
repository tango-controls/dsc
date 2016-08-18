# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.utils.html import format_html
from dsc.models import DeviceServer
from tango.forms import BaseForm

class DeviceServerFilterForm(BaseForm):
    def filter(self, model, queryset=None):
        if not queryset:
            queryset = model.objects.all()
        return queryset
    #TODO filter form for DS list if needed

