#!/usr/bin/python
# cryptopia api
import requests
import json

class Cryptopia(object):
    base_url = 'https://www.cryptopia.co.nz/api/GetMarket/'

    def __init__(self, coin_pair='SIGT_BTC'):
        self.coin_pair = coin_pair

    def getlastprice(self):
        
        url = '%s%s' % (self.base_url, self.coin_pair)
        try:
            reply = requests.get(url)
            reply = reply.text
        except:
            reply = "{}"

        json_str = json.loads(reply)

        AskPrice = 0.0
        LastPrice = 0.0
        TempPrice = 0.0

        if json_str['Success']:
            AskPrice = json_str['Data']['AskPrice']
            LastPrice = json_str['Data']['LastPrice']

        return LastPrice
