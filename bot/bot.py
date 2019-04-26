#!/usr/bin/env python

import requests

r = requests.get('https://google.com/')
print(r.status_code)
