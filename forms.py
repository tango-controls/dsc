# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.utils.html import format_html
from dsc.models import DeviceServer, DeviceServerAddModel
from tango.forms import BaseForm
from xmi_parser import TangoXmiParser

class DeviceServerFilterForm(BaseForm):
    def filter(self, model, queryset=None):
        if not queryset:
            queryset = model.objects.all()
        return queryset
    # TODO filter form for DS list if needed


class DeviceServerAddForm(forms.ModelForm):

    def clean(self):
        """Will check if fields are provided according to checkboxes"""
        cleaned_data = super(DeviceServerAddForm, self).clean()
        if cleaned_data['use_uploaded_xmi_file']:
            try:
                xmi_file = cleaned_data['xmi_file']

                if xmi_file.size < 10:
                    raise forms.ValidationError('The uploaded .XMI file seems to be empty!')
                if xmi_file.size > 1000000:
                    raise forms.ValidationError('The uploaded files is to large to be Tango .XMI file!')

                xmi_string = xmi_file.read()
                cleaned_data['xmi_string'] = xmi_string
                parser = TangoXmiParser(xml_string=xmi_string)

                is_valid, message = parser.is_valid()

                if not is_valid:
                    raise forms.ValidationError(message)

            except Exception as e:
                raise forms.ValidationError('Error during .xmi file validation. %s' % e.message)

        if cleaned_data['use_manual_info']:
            if not cleaned_data['use_uploaded_xmi_file']:
                if len(cleaned_data['name']) == 0 or len(cleaned_data['description']) == '' \
                        or len(cleaned_data['contact_email']) == 0:
                    raise forms.ValidationError('You must provide at leas name, description and contact information.')

        return cleaned_data

    class Meta:
        model = DeviceServerAddModel
        fields = ['use_uploaded_xmi_file', 'xmi_file',
                  'available_in_repository', 'repository_type', 'repository_url', 'repository_path',
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
