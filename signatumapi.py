#!/usr/bin/python
# signatumapi
import requests
import json

#############
# API CALLS #
#############
class Signatum(object):
  apiurl='http://explorer.signatum.io/api/'
  exturl='http://explorer.signatum.io/ext/'
  def __init__(self, address=''):
      self.address = address



  #################
  # getdifficulty #
  #################
  # Returns the current difficulty. 
  def getdifficulty(self,pos=False):
    
    try:
      url='getdifficulty'
      reply=requests.get('%s%s' % (self.apiurl,url))
      difficulty=json.loads(reply.text)
      if pos:
        return difficulty['proof-of-stake']
      return difficulty['proof-of-work']
    
    except:
      return -1



  # getconnectioncount
  # Returns the number of connections the block explorer has to other nodes. 
  # sample response
  def getconnectioncount(self):

    try:
      url='getconnectioncount'
      reply=requests.get('%s%s' % (self.apiurl,url))
      connectioncount=int(reply.text)
      return connectioncount

    except:
      return -1



  #################
  # getblockcount #
  #################
  # Returns the current block index. 
  # sample response
  def getblockcount(self):
    
    try:
      url='getblockcount'
      reply=requests.get('%s%s' % (self.apiurl,url))
      blockcount=int(reply.text)
      return blockcount

    except:
      return -1



  #######################
  # getblockhash[index] #
  #######################
  # Returns the hash of the block at ; index 0 is the genesis block. 
  def getblockhash(self,block=0):
    
    try:
      url='getblockhash?index=%s' % str(block)
      reply=requests.get('%s%s' % (self.apiurl,url))
      blockhash=reply.text
      return blockhash

    except:
      return None



  ##################
  # getblock[hash] #
  ##################
  # Returns information about the block with the given hash. 
  def getblock(self, hash):
    
    try:
      url='getblock?hash=%s' % hash
      reply=requests.get('%s%s' % (self.apiurl,url))
      blockinfo = reply.text
      return blockinfo

    except:
      return None



  ####################################
  # getrawtransaction[txid][decrypt] #
  ####################################
  # Returns raw transaction representation for given transaction id. decrypt can be set to 0(false) or 1(true). 
  def getrawtransaction(self,txid,decrypt=1):
    try:
      url='getrawtransaction?txid=%s&decrypt=%d' % (txid,decrypt)
      reply=requests.get('%s%s' % (self.apiurl,url))
      rawtransaction = reply.text
      return rawtransaction

    except:
      return None



  # getnetworkhashps 
  # Returns the current network hashrate. (hash/s) 
  # sample response
  '''
  '''
  # url='getnetworkhashps'

  ################
  # EXTENDED API #
  ################

  #######################
  # getbalance[address] #
  #######################
  # Returns current balance of given address
  def getbalance(self):
    
    try:
      url='getbalance/%s' % (self.address)
      reply=requests.get('%s%s' % (self.exturl,url))
      balance = float(reply.text)
      return balance

    except:
      return -1

# sigt_wallet_address = 'B5GWoN3jmFXkAQRWBUjrEQnE6ApQJgpyba'
# sigt = Signatum(sigt_wallet_address)
# print sigt.getbalance()