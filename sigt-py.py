#!/usr/bin/python
import os, thread, time
from clint.textui import colored
from datetime import datetime
# import API's
from signatumapi import *
from suprnovaapi import *
from cryptopiaapi import *
from coinsphapi import *

# Variable declarations
IS_ACTIVE = True

sigt_bal = 0.0
last_trade_price = 0.0
btc_value = 0.0
php_value = 0.0
block_height = 0
sigt_difficulty = 0.0

# Function declarations
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Open config.json
file_name = 'config.json'
try:
    file_handle = open(file_name)
except:
    print "Unable to open %s" % file_name
    quit()
else:
    file_data = file_handle.read()

# Parse contents of config.json
try:
    json_str = json.loads(file_data)
except:
    print "Unable to load config, please check JSON"
    quit()

print colored.white("[%s] Config files successfully loaded from %s" % (get_timestamp(), file_name))
file_handle.close()



# Create Objects

# .bat file for mining
batfile= json_str['miner']['bat_file']

# Suprnova API-key and User ID
api_key = json_str['suprnova']['api_key']
uid = json_str['suprnova']['uid']
snova = Suprnova(api_key, uid)

# Signatum Wallet Address
sigt_wallet_address = json_str['signatum']['wallet_address']
sigt = Signatum(sigt_wallet_address)

# Cryptopia coin pair
cex_coin_pair = json_str['cryptopia']['coin_pair']
cex = Cryptopia(cex_coin_pair)

# Coins.ph
cph_coin_pair = json_str['coinsph']['coin_pair']
cph = CoinsPH()



# Thread for getting SIGT balance
def t_getbalance(t):  
    global sigt_bal
    while True:
        sigt_bal = sigt.getbalance()
        time.sleep(t)

# Thread for getting block height
def t_getblockcount(t):  
    global block_height
    global sigt_difficulty
    current_block = 0
    while True:
        block_height = sigt.getblockcount()
        sigt_difficulty = sigt.getdifficulty()
        if (block_height * sigt_difficulty > 0) and (current_block != block_height):
            print colored.cyan("[%s] skunk block %d, diff %0.3f" % (get_timestamp(), block_height, sigt_difficulty))
            current_block = block_height
        time.sleep(t)

# Thread for getting SIGT_BTC price
def t_getlastprice(t):
    global last_trade_price
    last_value = last_trade_price
    show_prompt = True
    while True:
        try:
            last_trade_price = cex.getlastprice()
            show_prompt = True
        except:
            last_trade_price = last_value
            if show_prompt:
                print "Unable to get last trade data, using last known price"
            show_prompt = False
        time.sleep(t)

# Thread for displaying BTC stats
def t_displaystats_btc(t):
    global btc_value
    current_value = 0.0
    while True:
        btc_value = sigt_bal * last_trade_price
        if (btc_value > 0) and (btc_value != current_value):
            if (btc_value >= current_value):
                print colored.green("[%s] Value[BTC]: %0.8f" % (get_timestamp(), btc_value))
            else:
                print colored.red("[%s] Value[BTC]: %0.8f" % (get_timestamp(), btc_value))
            current_value = btc_value
        else:
            pass
        time.sleep(t)

# Thread for displaying PHP stats
def t_displaystats_php(t):
    global php_value
    global btc_value
    current_value = 0.0
    while True:
        php_value = btc_value * cph.get_bidprice()
        if (php_value > 0) and (php_value != current_value):
            if (php_value >= current_value):
                print colored.green("[%s] Value[PHP]: %0.2f" % (get_timestamp(), php_value))
            else:
                print colored.red("[%s] Value[PHP]: %0.2f" % (get_timestamp(), php_value))
            current_value = php_value
        else:
            pass
        time.sleep(t)

# Try to run threads
try:
    tmon = 0
    thread.start_new_thread(t_getbalance, (1.0,))
    tmon = 1
    thread.start_new_thread(t_getlastprice, (1.0,))
    tmon = 2
    thread.start_new_thread(t_getblockcount, (0.5,))
    tmon = 3
    thread.start_new_thread(t_displaystats_btc, (1.0,))
    tmon = 4
    thread.start_new_thread(t_displaystats_php, (1.0,))

# Exception handling
except:
    print "A thread exception occurred [%d]" % tmon
    quit()

# Give time for other API calls to fetch data
time.sleep(5)

# Loop while active
while IS_ACTIVE:
    # Display SIGT balance every 5 minutes
    if sigt_bal:
        print colored.yellow("[%s] Value[SIGT]: %0.2f" % (get_timestamp(), sigt_bal))
    time.sleep(300)