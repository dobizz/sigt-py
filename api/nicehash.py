#!/usr/bin/python
# nicehashapi
import requests
import json

EMPTY_JSON = '{}'

class Nicehash(object):
    # Current API version is: 1.2.6

    # General Syntax
    # https://api.nicehash.com/api?method=methodname&parameter1=parameter1value&parameter2=parameter2value...

    # Returned data is in JSON format

    # Location
    # 0 - Europe (NiceHash)
    # 1 - USA (WestHash)

    # Algorithms are marked with following numbers:
    # 0 = Scrypt
    # 1 = SHA256
    # 2 = ScryptNf
    # 3 = X11
    # 4 = X13
    # 5 = Keccak
    # 6 = X15
    # 7 = Nist5
    # 8 = NeoScrypt
    # 9 = Lyra2RE
    # 10 = WhirlpoolX
    # 11 = Qubit
    # 12 = Quark
    # 13 = Axiom
    # 14 = Lyra2REv2
    # 15 = ScryptJaneNf16
    # 16 = Blake256r8
    # 17 = Blake256r14
    # 18 = Blake256r8vnl
    # 19 = Hodl
    # 20 = DaggerHashimoto
    # 21 = Decred
    # 22 = CryptoNight
    # 23 = Lbry
    # 24 = Equihash
    # 25 = Pascal
    # 26 = X11Gost
    # 27 = Sia
    # 28 = Blake2s
    # 29 = Skunk

    api_version = '1.2.6'
    api_base_url = 'https://api.nicehash.com/api'

    # Class methods
    def __fetch_json__(self, api_url, method_url):
        url = '%s%s' % (api_url, method_url)
        try:
            reply = requests.get(url)
            reply = reply.text
            json_str = json.loads(reply)
            stats = json_str['result']
            return stats
        except:
            return EMPTY_JSON

    def __init__ (self):
        # try to get current API version
        try:
            self.api_version = self.__fetch_json__(self.api_base_url)['api_version']
        except:
            pass

    ##################
    # Public methods #
    ##################
    # Provides global statistics
    def get_stats_global_current(self, algo=None):
        method = '?method=stats.global.current'
        data = EMPTY_JSON

        try:
            if algo != None:
                data = self.__fetch_json__(self.api_base_url, method)['stats'][algo]
            else:
                data = self.__fetch_json__(self.api_base_url, method)['stats']
        except:
            pass
        return data
        # sample output
        '''
        {u'price': u'0.0154', u'profitability_above_ltc': u'-100.00', u'speed': u'311.77360574', u'algo': 29, u'profitability_ltc': u'0.0129'}
        '''
    # Provides global statistics for the past 24 hours
    def get_stats_global_24h(self, algo=None):
        method = '?method=stats.global.24h'
        data = EMPTY_JSON

        try:
            if algo != None:
                data = self.__fetch_json__(self.api_base_url, method)['stats'][algo]
            else:
                data = self.__fetch_json__(self.api_base_url, method)['stats']
        except:
            pass
        return data
        # sample output
        '''
        {u'price': u'0.0159', u'speed': u'146.57585508', u'algo': 29}
        '''
    # Provides current statistics for a given provider address
    def get_stats_provider(self, btc_address):
        method = '?method=stats.provider&addr=%s' % btc_address
        data = EMPTY_JSON

        try:
            data = self.__fetch_json__(self.api_base_url, method)['stats']
        except:
            pass
        return data
        # sample output
        '''
        {"balance":"0.00130560","rejected_speed":"0.00000000","algo":20,"accepted_speed":"0.17199000"},{"balance":"0.00000000","rejected_speed":"0.00000000","algo":22,"accepted_speed":"0.00000000"},{"balance":"0.00000312","rejected_speed":"0.00000000","algo":23,"accepted_speed":"0.00000000"},{"balance":"0.00033024","rejected_speed":"0.00000000","algo":24,"accepted_speed":"0.00000000"},{"balance":"0.00010157","rejected_speed":"0.02863310","algo":25,"accepted_speed":"1.14532000"},{"balance":"0.00000000","rejected_speed":"0.00000000","algo":27,"accepted_speed":"0.00000000"},{"balance":"0.00000000","rejected_speed":"0.00000000","algo":29,"accepted_speed":"0.00000000"}],"payments":[{"amount":"0.00146802","fee":"0.00002996","TXID":"","time":"2017-08-22 10:00:46"},{"amount":"0.00124608","fee":"0.00002543","TXID":"","time":"2017-08-17 10:00:19"},{"amount":"0.00232538","fee":"0.00004746","TXID":"","time":"2017-08-15 09:59:35"},{"amount":"0.00256390","fee":"0.00005232","TXID":"","time":"2017-08-13 09:59:24"},{"amount":"0.00112523","fee":"0.00002296","TXID":"","time":"2017-08-09 09:58:24"}],"addr":"3L5Uetx1GfLQufY3mjBRPYb7mCY7BhDPPG"}
        '''

    # Provides detailed statistics for a given provider address
    # Warning! This method returns a long JSON formated data, please consider before printing on screen
    def get_stats_provider_ex(self, btc_address):
        method = '?method=stats.provider.ex&addr=%s' % btc_address
        data = EMPTY_JSON

        try:
            data = self.__fetch_json__(self.api_base_url, method)
        except:
            pass
        return data

    # Provides detailed worker statistics for a given provider address
    def get_stats_provider_workers(self, btc_address, algo=None):
        method = '?method=stats.provider.workers&addr=%s' % btc_address
        data = EMPTY_JSON

        try:
            if algo != None:
                method = '%s&algo=%d' % (method, algo)
            data = self.__fetch_json__(self.api_base_url, method)['workers']
        except:
            pass
        return data
        # Return data format
        '''
        "workers":[[
                "rigname",                      // name of the worker
                {"a":"11.02","rs":"0.54"},      // speed object
                15,                             // time connected (minutes)
                1,                              // 1 = xnsub enabled, 0 = xnsub disabled
                "0.1",                          // difficulty
                0,                              // connected to location (0 for EU, 1 for US, 2 for HK and 3 for JP)
            ],
            ... // other workers here
        '''

    # Provides all order information on a certain algorithm, data is refreshed every 30 seconds
    # Warning! This method returns a long JSON formated data, please consider before printing on screen
    def get_orders(self, location=0, algo=0):
        method = '?method=orders.get&location=%d&algo=%d' % (location, algo)
        data = EMPTY_JSON

        try:
            data = self.__fetch_json__(self.api_base_url, method)
        except:
            pass
        return data

    # Provides information about Mult-Algorithm Mining
    # Warning! This method returns a long JSON formated data, please consider before printing on screen
    def get_multialgo_info(self):
        method = '?method=multialgo.info'
        data = EMPTY_JSON

        try:
            data = self.__fetch_json__(self.api_base_url, method)['multialgo']
        except:
            pass
        return data

    # Provides information about Simple Multi-Algorithm Mining
    def get_simple_multialgo_info(self):
        method = '?method=simplemultialgo.info'
        data = EMPTY_JSON

        try:
            data = self.__fetch_json__(self.api_base_url, method)['simplemultialgo']
        except:
            pass
        return data

    # Get needed information for buying hashing power using NiceHashBot
    def get_buy_info(self):
        method = '?method=buy.info'
        data = EMPTY_JSON

        try:
            data = self.__fetch_json__(self.api_base_url, method)
        except:
            pass
        return data

    ###################
    # Private methods #
    ###################

# For debugging
if __name__ == '__main__':
    nh = Nicehash()
    BTC_addr = '3L5Uetx1GfLQufY3mjBRPYb7mCY7BhDPPG'

    try:
        # print nh.get_stats_global_current()
        # print nh.get_stats_global_current(29)['price']
        # print nh.get_stats_global_24h(29)['price']
        # print nh.get_stats_provider(BTC_addr)
        # print nh.get_stats_provider_ex(BTC_addr)
        # print nh.get_stats_provider_workers(BTC_addr, 24)
        # print nh.get_orders(0,0)
        # print nh.get_buy_info()

        # data = nh.get_multialgo_info()
        # for item in data:
        #     print "%d,%s,%d" % (item['algo'], item['name'], item['port'])

        # data = nh.get_simple_multialgo_info()
        # for item in data:
        #     print "%d,%s,%d,%s" % (item['algo'], item['name'], item['port'], item['paying'])
        pass
        
    except:
        print 'Exception occurred'
