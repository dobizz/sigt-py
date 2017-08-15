#!/usr/bin/python
# nicehashapi
import requests
import json

class Nicehash(object):
    # Current API version is: 1.2.6

    # General Syntax
    # https://api.nicehash.com/api?method=methodname&parameter1=parameter1value&parameter2=parameter2value...

    # Returned data is in JSON format

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

    api_base_url = 'https://api.nicehash.com/api'

    def __init__ (self):
        pass

    #public methods
    def get_stats_global_current(self, algo=0):
        method = '?method=stats.global.current'
        url = '%s%s' % (self.api_base_url, method)
        try:
            reply = requests.get(url)
            reply = reply.text
            json_str = json.loads(reply)
            stats = json_str['result']['stats'][algo]
            return stats
        except:
            return {}

    #private methods

# nh = Nicehash()
# print nh.get_stats_global_current(29)['price']
