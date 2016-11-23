# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.utils.html import format_html
from dsc.models import DeviceServerAddModel, DeviceServerUpdateModel
from tango.forms import BaseForm
from xmi_parser import TangoXmiParser
import dal.autocomplete
from django.core.urlresolvers import reverse_lazy


class DeviceServerFilterForm(BaseForm):
    def filter(self, model, queryset=None):
        if not queryset:
            queryset = model.objects.all()
        return queryset
    # TODO filter form for DS list if needed


class DeviceServerSearchForm(forms.Form):
    pass
    manufacturer = dal.autocomplete.Select2ListCreateChoiceField(label='Manufacturer', required=False,
                                      widget=dal.autocomplete.ListSelect2(url=reverse_lazy('deviceserver_manufacturers')))

    product = forms.CharField(label='Product', required=False,
                              widget=dal.autocomplete.ListSelect2(url=reverse_lazy('deviceserver_products'),
                                                                  forward=['manufacturer','family']))

    family = forms.CharField(label='Class family', required=False,
                              widget=dal.autocomplete.ListSelect2(url=reverse_lazy('deviceserver_families')))

    bus = forms.CharField(label='Communication bus', required=False,
                             widget=dal.autocomplete.ListSelect2(url=reverse_lazy('deviceserver_buses')))


class DeviceServerAddForm(forms.ModelForm):

    def clean(self):
        """Will check if fields are provided according to checkboxes"""
        cleaned_data = super(DeviceServerAddForm, self).clean()

        if not cleaned_data['use_uploaded_xmi_file'] and not cleaned_data['use_manual_info']:
            raise forms.ValidationError('You must provide either .XMI file or enter information manually.')

        if cleaned_data['use_uploaded_xmi_file']:
            try:
                xmi_file = cleaned_data['xmi_file']

                if xmi_file.size < 10:
                    raise forms.ValidationError('The uploaded .XMI file seems to be empty.')
                if xmi_file.size > 1000000:
                    raise forms.ValidationError('The uploaded file is to large to be a Tango .XMI file.')

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
                    raise forms.ValidationError('You must provide at least name, description and contact information.')

        if cleaned_data.get('repository_url','')=='' and cleaned_data.get('repository_contact','')=='':
            raise forms.ValidationError('You must provide either repostiry URL or contact email to let someone  '
                                        'access your device server.')

        return cleaned_data

    class Meta:
        model = DeviceServerAddModel
        fields = ['use_uploaded_xmi_file', 'xmi_file',
                  'use_manual_info',
                  'name', 'description', 'contact_email', 'platform', 'language', 'license_name',
                  'repository_type', 'repository_url', 'repository_path',
                  'repository_contact',
                  'upload_readme', 'readme_file',
                  'other_documentation1',
                  'documentation1_type', 'documentation1_url',
                  'class_copyright', 'class_family',
                  'manufacturer', 'product_reference', 'bus', 'key_words'
                  ]


class DeviceServerUpdateForm(DeviceServerAddForm):

    class Meta:
        model = DeviceServerUpdateModel
        fields = ['use_uploaded_xmi_file', 'xmi_file',
                  'use_manual_info',
                  'name', 'description', 'contact_email', 'platform', 'language', 'license_name',
                  'repository_type', 'repository_url', 'repository_path', 'repository_contact',
                  'upload_readme', 'readme_file',
                  'other_documentation1',
                  'documentation1_type', 'documentation1_url',
                  'class_copyright', 'class_family',
                  'manufacturer', 'product_reference', 'bus', 'key_words'
                  ]