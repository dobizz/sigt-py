#!/usr/bin/python
import os, time, thread, subprocess
from clint.textui import colored
from datetime import datetime
from thread import allocate_lock

# import API functions
from api.signatum import *
from api.suprnova import *
from api.cryptopia import *
from api.coinsph import *
from api.nicehash import *
from api.whattomine import *

# Variable declarations
IS_ACTIVE = True
DEBUG_MODE = False
MINER_PID = None
MINER_ACITVE = False

BLOCK_HEIGHT = 0
SIGT_BAL = 0.0
BTC_VALUE = 0.0
PHP_VALUE = 0.0
PHP_RATE = 0.0
LAST_TRADE_PRICE = 0.0
SIGT_DIFFICULTY = 0.0
NH_PROFITABILITY = 0.0
POOL_PROFITABILITY = 0.0

NH_MINER = 'edit in config.json'
POOL_MINER = 'edit in config.json'

# Get current datetime and format
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

#################################
# Create Objects and Parse JSON #
#################################

# .bat file for mining
NH_MINER = json_str['miner']['nicehash']
POOL_MINER = json_str['miner']['pool']

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

# Nicehash
nh = Nicehash()

# Whattomine
wtm = Whattomine()

# Create thread lock
lock = allocate_lock()

#########################
# Function declarations #
#########################

# Check task
def is_task_active(pid):
    try:
        cmd = 'tasklist /FI "PID eq %d"' % pid
        stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        # pid not found
        if ('No tasks are running which match the specified criteria' in stdout):
            return False
        # pid found
        return True
    except:
        return False

# Kill tasks
def kill_task(pid):
    try:
        # kill task if active
        if is_task_active(pid):
            cmd = 'taskkill /PID %d /f' % pid
            stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return True
        return False
    except:
        return False

# Call miner
def start_miner(miner):
    global MINER_PID
    global MINER_ACITVE
    # miner = 'start-nicehash-sigt-ccminer.bat'
    try:
        p = subprocess.Popen(miner, creationflags=subprocess.CREATE_NEW_CONSOLE)
        # For reading miner output - For future development
        # stdout, stderr = p.communicate()
        MINER_PID = int(p.pid)
        MINER_ACITVE = True
        return True

    except:
        MINER_PID = None
        return False

# Stop miner
def stop_miner():
    global MINER_PID
    global MINER_ACITVE
    if kill_task(MINER_PID):
        MINER_ACITVE = False
        return True
    return False

# Get profitability for Nicehash mining
def get_nh_profitability():
    global NH_PROFITABILITY
    nh_algo = 29 # skunk
    last_value = 0.0
    try:
        NH_PROFITABILITY = float(nh.get_stats_global_current(nh_algo)['price'])
        last_value = NH_PROFITABILITY
    except:
        NH_PROFITABILITY = last_value

    return NH_PROFITABILITY

# Get profitability for Pool Mining
def get_pool_profitability():
    global POOL_PROFITABILITY
    coin_id = 191 # signatum
    last_value = 0.0
    try:
        btc_rev =  float(wtm.get_raw_stats(coin_id)['btc_revenue'])
        last_value = btc_rev
    except:
        btc_rev = last_value
    POOL_PROFITABILITY = btc_rev * 24
    return POOL_PROFITABILITY

# Thread for printing BTC/GH/day profitability
def t_get_btc_profitability(timeout):
    global IS_ACTIVE
    global MINER_ACITVE
    global NH_MINER
    global POOL_MINER

    current_miner = None

    while IS_ACTIVE:
        nh = get_nh_profitability()
        pool = get_pool_profitability()
        ts = get_timestamp()
        lock.acquire()
        print colored.magenta("[%s] %0.4f BTC/GH/day (Nicehash), %0.4f BTC/GH/day (Pool)" % (ts, nh, pool))
        lock.release()

        # If a miner is already active
        if MINER_ACITVE:
            ts = get_timestamp()
            if nh >= pool:
                if current_miner == POOL_MINER:
                    lock.acquire()
                    print '[%s] Stoping Miner on Pool' % (ts)
                    lock.release()
                    stop_miner()
                    ts = get_timestamp()
                    lock.acquire()
                    print '[%s] Starting Miner on Nicehash' % (ts)
                    lock.release()
                    start_miner(NH_MINER)

                    current_miner = NH_MINER

                elif current_miner == NH_MINER:
                    pass

            else:
                if current_miner == NH_MINER:
                    lock.acquire()
                    print '[%s] Stoping Miner on Nicehash' % (ts)
                    lock.release()
                    stop_miner()
                    ts = get_timestamp()
                    lock.acquire()
                    print '[%s] Starting Miner on Pool' % (ts)
                    lock.release()
                    start_miner(POOL_MINER)

                    current_miner = POOL_MINER
                elif current_miner == POOL_MINER:
                    pass

        # If no miners are active
        else:
            if nh >= pool:
                ts = get_timestamp()
                lock.acquire()
                print '[%s] Starting Miner on Nicehash' % (ts)
                lock.release()
                start_miner(NH_MINER)
                current_miner = NH_MINER
            else:
                ts = get_timestamp()
                lock.acquire()
                print '[%s] Starting Miner on Pool' % (ts)
                lock.release()
                start_miner(POOL_MINER)
                current_miner = POOL_MINER

        time.sleep(timeout)

# Thread for getting SIGT balance
def t_getbalance(timeout):
    # Shared variables with other threads
    global IS_ACTIVE
    global SIGT_BAL

    last_value = 0.0

    while IS_ACTIVE:
        SIGT_BAL = sigt.getbalance()
        if SIGT_BAL >= 0:
            last_value = SIGT_BAL
        if SIGT_BAL < 0:
            SIGT_BAL = last_value
        time.sleep(timeout)

# Thread for getting block height
def t_getblockcount(timeout):
    # Shared variables with other threads
    global BLOCK_HEIGHT
    global SIGT_DIFFICULTY
    global IS_ACTIVE

    current_block = 0

    while IS_ACTIVE:
        BLOCK_HEIGHT = sigt.getblockcount()
        SIGT_DIFFICULTY = sigt.getdifficulty()

        if DEBUG_MODE:
            print 'BLOCK_HEIGHT =', BLOCK_HEIGHT
            print 'SIGT_DIFFICULTY =', SIGT_DIFFICULTY

        if (BLOCK_HEIGHT > 0) and (SIGT_DIFFICULTY > 0) and (current_block != BLOCK_HEIGHT):
            ts = get_timestamp()
            lock.acquire()
            print colored.cyan("[%s] skunk block %d, diff %0.3f" % (ts, BLOCK_HEIGHT, SIGT_DIFFICULTY))
            lock.release()
            current_block = BLOCK_HEIGHT
        time.sleep(timeout)

# Threaf for getting PHP_BTC price
def t_get_bidprice(timeout):
    global PHP_RATE
    global IS_ACTIVE

    last_value = 0.0
    expiresin = 0
    show_prompt = True

    while IS_ACTIVE:
        try:
            PHP_RATE, expiresin = cph.get_bidprice()
            last_value = PHP_RATE
            show_prompt = True
            sleep_time = expiresin
            if DEBUG_MODE:
                print 'PHP_RATE =', PHP_RATE
                print 'expiresin =', expiresin
        except:
            PHP_RATE = last_value
            if show_prompt:
                print "Unable to get last trade data, using last known price"
            show_prompt = False
            sleep_time = timeout
        time.sleep(sleep_time)

# Thread for getting SIGT_BTC price
def t_getlastprice(timeout):
    # Shared variables with other threads
    global LAST_TRADE_PRICE
    global IS_ACTIVE

    last_value = 0.0
    show_prompt = True

    while IS_ACTIVE:
        try:
            LAST_TRADE_PRICE = cex.getlastprice()
            last_value = LAST_TRADE_PRICE
            show_prompt = True
            if DEBUG_MODE:
                print 'LAST_TRADE_PRICE =', LAST_TRADE_PRICE
                print 'last_value =', last_value
        except:
            LAST_TRADE_PRICE = last_value
            if show_prompt:
                lock.acquire()
                print "Unable to get last trade data, using last known price"
                lock.release()
            show_prompt = False
        time.sleep(timeout)

# Thread for displaying BTC stats
def t_displaystats_btc(timeout):
    # Shared variables with other threads
    global BTC_VALUE
    global LAST_TRADE_PRICE
    global IS_ACTIVE

    current_value = 0.0

    while IS_ACTIVE:
        BTC_VALUE = SIGT_BAL * LAST_TRADE_PRICE
        if (BTC_VALUE > 0) and (BTC_VALUE != current_value):
            text = "[%s] Value[BTC]: %0.8f\tRate: %0.8f\tBTC/SIGT\t" % (get_timestamp(), BTC_VALUE, LAST_TRADE_PRICE)
            if (BTC_VALUE >= current_value):
                text = colored.green("%s%s" % (text, "(+)"))
            else:
                text = colored.red("%s%s" % (text, "(-)"))

            lock.acquire()
            print text
            lock.release()

            current_value = BTC_VALUE
        else:
            pass
        time.sleep(timeout)

# Thread for displaying PHP stats
def t_displaystats_php(timeout):
    # Shared variables with other threads
    # global PHP_VALUE
    global BTC_VALUE
    global LAST_TRADE_PRICE
    global PHP_RATE
    global IS_ACTIVE

    current_value = 0.0

    while IS_ACTIVE:
        PHP_VALUE = BTC_VALUE * PHP_RATE
        php_sigt = PHP_RATE * LAST_TRADE_PRICE

        if (PHP_VALUE > 0) and (PHP_VALUE != current_value):
            text = "[%s] Value[PHP]: %0.2f\tRate: %0.2f\t\tPHP/SIGT\t" % (get_timestamp(), PHP_VALUE, php_sigt)

            if (PHP_VALUE >= current_value):
                text = colored.green("%s%s" % (text, "(+)"))

            else:
                text = colored.red("%s%s" % (text, "(-)"))

            lock.acquire()
            print text
            lock.release()

            current_value = PHP_VALUE

        else:
            pass
        time.sleep(timeout)

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

    # Call thread for getting current PHP bid price, initial 10-second price validity, timeout will be replaced from JSON data
    tmon = 3
    thread.start_new_thread(t_get_bidprice, (10.0,))

    # Call thread for displaying BTC stats
    tmon = 4
    thread.start_new_thread(t_displaystats_btc, (1.0,))

    # Call thred for displaying PHP stats
    tmon = 5
    thread.start_new_thread(t_displaystats_php, (1.0,))

    # Call thred for displaying NH/Pool BTC profitability
    tmon = 6
    thread.start_new_thread(t_get_btc_profitability, (60.0,))

# Exception handling
except:
    print "A thread exception occurred [%d]" % tmon
    quit()

# Give time for other API calls to fetch data
time.sleep(5)

# Call miner
# miner = 'start-nicehash-sigt-ccminer.bat'
# start_miner(miner)
# print 'is active',is_task_active(MINER_PID)
# time.sleep(5)
# print 'kill miner',kill_task(MINER_PID)
# print 'is active',is_task_active(MINER_PID)

# is_task_active(MINER_PID)
# Loop while active
while IS_ACTIVE:
    # Display SIGT balance every 5 minutes
    if SIGT_BAL:
        lock.acquire()
        print colored.yellow("[%s] Value[SIGT]: %0.2f" % (get_timestamp(), SIGT_BAL))
        lock.release()
    time.sleep(300)
