#!/usr/bin/python
# suprnovaapi
import requests
import json

#############
# API CALLS #
#############

class Suprnova(object):
    base_url = '.suprnova.cc/index.php?page=api&action=getuserstatus&api_key='

    def __init__(self, api_key='0x00', uid=0, pool='sigt'):
        self.api_key = api_key
        self.uid = uid
        self.pool = pool

    def getstats(self):
        try:
            url = 'https://%s%s%s&id=%d' % (self.pool, self.base_url, self.api_key, self.uid)
            reply = requests.get(url)
            return reply.text
        except:
            return None
'''
# Parse JSON
# version = json_str['getuserstatus']['version']
# runtime = json_str['getuserstatus']['runtime']
# username = json_str['getuserstatus']['data']['username']
# shares_valid = json_str['getuserstatus']['data']['shares']['valid']
# shares_invalid = json_str['getuserstatus']['data']['shares']['invalid']
# donate_percent = json_str['getuserstatus']['data']['shares']['donate_percent']
# is_anonymous = json_str['getuserstatus']['data']['shares']['is_anonymous']
# hashrate = json_str['getuserstatus']['data']['hashrate']
# sharerate = json_str['getuserstatus']['data']['sharerate']
'''
