#!/usr/bin/python
import os, thread, time
from clint.textui import colored
from datetime import datetime
# import API functions
from api.signatum import *
from api.suprnova import *
from api.cryptopia import *
from api.coinsph import *

# Variable declarations
IS_ACTIVE = True

sigt_bal = 0.0
last_trade_price = 0.0
btc_value = 0.0
php_value = 0.0
php_rate = 0.0
sigt_difficulty = 0.0
block_height = 0

#########################
# Function declarations #
#########################

# Get current datetime and format
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Thread for getting SIGT balance
def t_getbalance(timeout):
    # Shared variables with other threads
    global sigt_bal

    while True:
        sigt_bal = sigt.getbalance()
        time.sleep(timeout)

# Thread for getting block height
def t_getblockcount(timeout):
    # Shared variables with other threads
    global block_height
    global sigt_difficulty

    current_block = 0

    while True:
        block_height = sigt.getblockcount()
        sigt_difficulty = sigt.getdifficulty()
        if (block_height * sigt_difficulty > 0) and (current_block != block_height):
            print colored.cyan("[%s] skunk block %d, diff %0.3f" % (get_timestamp(), block_height, sigt_difficulty))
            current_block = block_height
        time.sleep(timeout)

# Threaf for getting PHP_BTC price
def t_get_bidprice(timeout):
    global php_rate

    last_value = 0.0
    show_prompt = True

    while IS_ACTIVE:
        try:
            php_rate = cph.get_bidprice()
            last_value = php_rate
            show_prompt = True
        except:
            php_rate = last_value
            if show_prompt:
                print "Unable to get last trade data, using last known price"
            show_prompt = False
        time.sleep(timeout)

# Thread for getting SIGT_BTC price
def t_getlastprice(timeout):
    # Shared variables with other threads
    global last_trade_price

    last_value = 0.0
    show_prompt = True

    while IS_ACTIVE:
        try:
            last_trade_price = cex.getlastprice()
            last_value = last_trade_price
            show_prompt = True
        except:
            last_trade_price = last_value
            if show_prompt:
                print "Unable to get last trade data, using last known price"
            show_prompt = False
        time.sleep(timeout)

# Thread for displaying BTC stats
def t_displaystats_btc(timeout):
    # Shared variables with other threads
    global btc_value
    global last_trade_price

    current_value = 0.0
    while IS_ACTIVE:
        btc_value = sigt_bal * last_trade_price
        if (btc_value > 0) and (btc_value != current_value):
            text = "[%s] Value[BTC]: %0.8f\tRate: %0.8f\tBTC/SIGT\t" % (get_timestamp(), btc_value, last_trade_price)
            if (btc_value >= current_value):
                print colored.green("%s%s" % (text, "(+)"))
            else:
                print colored.red("%s%s" % (text, "(-)"))
            current_value = btc_value
        else:
            pass
        time.sleep(timeout)

# Thread for displaying PHP stats
def t_displaystats_php(timeout):
    # Shared variables with other threads
    # global php_value
    global btc_value
    global last_trade_price
    global php_rate

    current_value = 0.0

    while IS_ACTIVE:
        php_value = btc_value * php_rate
        php_sigt = php_rate * last_trade_price

        if (php_value > 0) and (php_value != current_value):
            text = "[%s] Value[PHP]: %0.2f\tRate: %0.2f\t\tPHP/SIGT\t" % (get_timestamp(), php_value, php_sigt)

            if (php_value >= current_value):
                print colored.green("%s%s" % (text, "(+)"))

            else:
                print colored.red("%s%s" % (text, "(-)"))
            current_value = php_value

        else:
            pass
        time.sleep(timeout)


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

# Try to run threads
try:
    # Call thread for getting Signatum balance
    tmon = 0
    thread.start_new_thread(t_getbalance, (60.0,))

    # Call thread for getting last trade price
    tmon = 1
    thread.start_new_thread(t_getlastprice, (1.0,))

    # Call thread for getting current block height and difficulty
    tmon = 2
    thread.start_new_thread(t_getblockcount, (0.5,))

    # Call thread for getting current PHP bid price, 9-second price validity
    tmon = 3
    thread.start_new_thread(t_get_bidprice, (9.0,))

    # Call thread for displaying BTC stats, t=1.0s
    tmon = 4
    thread.start_new_thread(t_displaystats_btc, (1.0,))

    # Call thred for displaying PHP stats, t=1.01s to avoid overlapping with BTC stats
    tmon = 5
    thread.start_new_thread(t_displaystats_php, (1.01,))

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
