#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import time
from datetime import datetime

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms
from django.conf import settings

from scanner import *


def make_scan_form(request):
    devices = ScanInterface.devices()
    device_choices = [(dev[0], u'%(brand)s %(model)s' \
                               % {'brand': dev[1], 'model': dev[2]}) \
                      for dev in devices]
    class _ScanForm(forms.Form):
        scanner = forms.ChoiceField(choices=device_choices)
        mode = forms.ChoiceField(choices=[('Lineart', u"Monochrome"), \
                                          ('Gray', u"Gray scale"), \
                                          ('Color', u"Color")])
        resolution = forms.ChoiceField(choices=[('72', u"72"), \
                                          ('96', u"96"), \
                                          ('150', u"150"), \
                                          ('200', u"200"), \
                                          ('300', u"300"), \
                                          ('600', u"600")], \
                                                       initial='300')
    return _ScanForm

def scan(request, success_url=None, \
          template_name='scan/index.html', \
          extra_context={}):

    context = {'SCANNED_URL': settings.SCANNED_URL, \
               'STATIC_URL': settings.STATIC_URL}

    form_cls = make_scan_form(request)

    if request.method == 'POST':
        form = form_cls(request.POST)
        if form.is_valid():
            print form.cleaned_data
            print "OK!"
            scanner = ScanInterface.create_device(form.cleaned_data['scanner'])


            scanner.set_option('l', 0)
            scanner.set_option('t', 0)
            scanner.set_option('x', 215)
            scanner.set_option('y', 297)
            scanner.set_option('mode', form.cleaned_data['mode'])
            scanner.set_option('resolution', form.cleaned_data['resolution'])

            filename = scanner.scan(settings.SCANNED_ROOT + '/%s.jpg' % datetime.now().strftime('%s'))

            # create thumbnail
            path, leaf = filename.rsplit('/', 1)
            retcode = subprocess.call(['convert', filename, '-resize', '430x594', '-quality', '65', path + 'thumb_'+leaf])

            context.update({'scan_path': leaf, 'scan_thumb': 'thumb_'+leaf, 'scan_ok': True})

    else:
        form = form_cls()

    context.update({'form': form})
    context.update(extra_context)
    context.update(csrf(request))
    return render_to_response(template_name, context)

