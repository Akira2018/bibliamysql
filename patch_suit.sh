#!/bin/bash
sed -i 's/from django.utils.translation import ugettext as _/from django.utils.translation import gettext as _/g' venv/lib/python3.x/site-packages/suit/admin.py
