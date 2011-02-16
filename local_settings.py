#!/usr/bin/env python
# encoding=utf-8

import os
import settings

file_dir = os.path.dirname(__file__)

settings.SCANNED_ROOT = file_dir + '/scans/'
settings.SCANNED_URL = '/scans/'
settings.STATIC_URL = '/static/'
settings.TEMPLATE_DIRS = (file_dir + '/scan/templates',)

