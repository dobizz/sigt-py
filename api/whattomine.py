#!/usr/bin/python
# whattomineapi
import requests
import json

class Whattomine(object):
    api_base_url = 'https://whattomine.com/coins/'
    def __init__(self):
        pass

    def get_raw_stats(self, coin_id=1):
        url = '%s%d.json' % (self.api_base_url, coin_id)
        try:
            reply = requests.get(url)
            reply = reply.text
            json_str = json.loads(reply)
            return json_str

        except:
            return {}

# wtm = Whattomine()
# btc_rev =  wtm.get_raw_stats(191)['btc_revenue']
# print float(btc_rev) * 24
