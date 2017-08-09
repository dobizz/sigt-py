#!/usr/bin/bash
# coinsphapi
import requests
import json

class CoinsPH(object):

    market_api_url = 'https://quote.coins.ph/v1/markets/'

    def __init__(self):
        pass

    def get_bidprice(self, coin_pair = 'BTC-PHP'):
        url = '%s%s' % (self.market_api_url, coin_pair)
        try:
            reply = requests.get(url)
        except:
            reply = '{}'

        bidprice = 0.0

        try:    
            reply = reply.text
            json_str = json.loads(reply)
            bidprice = json_str['market']['bid']
            return float(bidprice)

        except:
            return -1

