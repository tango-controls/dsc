# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.utils.html import format_html
from dsc.models import DeviceServer, DeviceServerAddModel
from tango.forms import BaseForm

class DeviceServerFilterForm(BaseForm):
    def filter(self, model, queryset=None):
        if not queryset:
            queryset = model.objects.all()
        return queryset
    #TODO filter form for DS list if needed


class DeviceServerAddForm(forms.ModelForm):

    def clean(self):
        """Will check if fields are provided according to checkbox"""
        cleaned_data = super(DeviceServerAddForm, self).clean()


    class Meta:
        model = DeviceServerAddModel
        fields = ['use_uploaded_xmi_file', 'xmi_file',
                  'repository_type', 'repository_url', 'repository_path',
                  'readme_file',
                  'documentation1_type', 'documentation1_url',
                  'documentation2_type', 'documentation2_url',
                  'use_manual_info',
                  'name', 'description',
                  'class_name', 'contact_email', 'class_copyright',
                  'platform', 'language',
                  'class_family', 'manufacturer', 'product_reference', 'bus',
                  'key_words'
                  ]
