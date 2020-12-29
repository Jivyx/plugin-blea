# coding: utf-8
from bluepy import btle
import time
import logging
import globals
from multiconnect import Connector
import struct
import utils

class YeelightCandela():
	def __init__(self):
		self.name = 'yeelight_candela'
		self.ignoreRepeat = True
		self.key = 'eff6e316dcf300000000000000000000'

	def isvalid(self,name,manuf='',data='',mac=''):
		if 'yeelight_ms' in [name.lower()] or name.lower()==self.name:
			return True

	def parse(self,data,mac,name,manuf):
		action={}
		action['present'] = 1
		return action
	
	def action(self,message):
		logging.debug('action for yeelight_candela received')
		type =''
		mac = message['device']['id']
		handle = message['command']['handle']
		value = message['command']['value']
		if 'type' in message['command']:
			type = message['command']['type']
		if mac in globals.KEEPED_CONNECTION:
			logging.debug('Already a connection for ' + mac + ' use it')
			conn = globals.KEEPED_CONNECTION[mac]
		else:
			logging.debug('Creating a new connection for ' + mac)
			conn = Connector(mac)
			globals.KEEPED_CONNECTION[mac]=conn
			conn.connect()
		if not conn.isconnected:
			conn.connect()
			if not conn.isconnected:
				return
		if type == 'pair':
			conn.writeCharacteristic('0x001f','4367'+self.key)
			time.sleep(5)
		if type == 'switch':
			conn.writeCharacteristic('0x001f','4340'+value)
		if type == 'brightness':
			conn.writeCharacteristic('0x001f','4342'+str(int(value)))
		conn.disconnect()
		return
	
	def read(self,mac,connection=''):
		# TODO
		result={}
		result['id'] = mac
		return result

globals.COMPATIBILITY.append(YeelightCandela)