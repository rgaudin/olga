#!/usr/bin/env python
# encoding=utf-8

import subprocess
import tempfile


class ScanInterface(object):

    def __init__(self):

        pass

    @classmethod
    def devices(cls):
        raw_list = subprocess.Popen(['scanimage','-f','%d|%v|%m|%t|%i%n'], \
                                    stdout=subprocess.PIPE)\
                             .communicate()[0].split('\n')
        devices = []
        for device in raw_list:
            dev = device.split('|')
            if dev.__len__() >= 3:
                devices.append((dev[0], dev[1], dev[2]))
        return devices

    @classmethod
    def class_name(cls, device_id):
        class_name = ScanDevice

        scan_map = {'plustek': PlustekDevice}

        for slug, scan_class in scan_map.items():
            if slug in device_id.lower():
                class_name = scan_class
                break

        return class_name

    @classmethod
    def create_device(cls, device_id):
        class_name = cls.class_name(device_id)
        return class_name(device_id=device_id)


class ScanDevice(object):

    def __init__(self, device_id):
        self.device_id = device_id
        self._options = {}

    def set_option(self, option, value):
        self._options[option] = '%s' % value

    def unset_option(self, option):
        pass

    def set_options(self, dic):
        pass

    def list_options(self):
        pass

    def forge_options(self):
        options = []
        for name, value in self._options.items():
            prefix = '-' if name.__len__() == 1 else '--'
            options.append('%(pref)s%(opt)s' % {'pref': prefix, 'opt': name})
            options.append(value)
        return options

    def scan(self, filename=None):
        fd = tempfile.NamedTemporaryFile()

        print self.forge_options()
        retcode = subprocess.call(["scanimage", '-d', self.device_id] + \
                                                      self.forge_options(), \
                                  stdout=fd)
        print "RET: %s" % retcode

        if filename:
            retcode = subprocess.call(['convert', '-quality', '100', fd.name, filename])
        
        fd.close()
        return filename

class PlustekDevice(ScanDevice):

    @classmethod
    def list_options(cls):
        return ['l','t','x','y','resolution']
