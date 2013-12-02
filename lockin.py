import Gpib,time,string
import random


class Lockin():
	def __init__(self):
		self.device=Gpib.Gpib('lockin')

	def write(self,cmd):
		self.device.write(cmd)
	def read(self,bytes):
		self.device.read(bytes) #return '%f,%f,%f,%f'%(random.random(),random.random(),random.random(),random.random())
	def clear(self):
		self.device.clear()
