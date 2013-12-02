import sys,os,thread

from PySide import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl


import numpy as np
# import pyuic generated user interface file
import template

from lockin import *

lockin=Lockin()
lockin.clear()

app = QtGui.QApplication(sys.argv)

def update():
		lockin.write("SNAP?1,2,3,4") #get values of x,y,amplitude and phase (recorded simultaneously) as an array
		myapp.time.append(time.time()-myapp.start_time)
		data=lockin.read(50)
		lockin.clear()
		x=float(data.split(',')[0])
		y=float(data.split(',')[1])
		amp=float(data.split(',')[2])
		phase=float(data.split(',')[3])
		myapp.x.append(x)
		myapp.y.append(y)
		myapp.amp.append(amp)
		myapp.phase.append(phase)
		

		myapp.c1.setData(myapp.time,myapp.x)
		myapp.c2.setData(myapp.time,myapp.y)
		myapp.c3.setData(myapp.time,myapp.amp)
		myapp.c4.setData(myapp.time,myapp.phase)

def zoomx():
	minX, maxX = myapp.xregion.getRegion()
	myapp.c5.setPen(myapp.c1col)
	myapp.c5.setData(myapp.time,myapp.x)
	myapp.zoomgraph.setXRange(minX, maxX, padding=0)
def zoomy():
	minX, maxX = myapp.yregion.getRegion()
	myapp.c5.setPen(myapp.c2col)
	myapp.c5.setData(myapp.time,myapp.y)
	myapp.zoomgraph.setXRange(minX, maxX, padding=0)
def zoomamp():
	minX, maxX = myapp.ampregion.getRegion()
	myapp.c5.setPen(myapp.c3col)
	myapp.c5.setData(myapp.time,myapp.amp)
	myapp.zoomgraph.setXRange(minX, maxX, padding=0)
def zoomph():
	minX, maxX = myapp.phregion.getRegion()
	myapp.c5.setPen(myapp.c4col)
	myapp.c5.setData(myapp.time,myapp.phase)
	myapp.zoomgraph.setXRange(minX, maxX, padding=0)


class MyMainWindow(QtGui.QMainWindow, template.Ui_MainWindow):
	def __init__(self, parent=None):
		super(MyMainWindow, self).__init__(parent)
		self.setupUi(self)
		self.running  = False
		self.x=[]
		self.y=[]
		self.amp=[]
		self.phase=[]
		self.time=[]
		self.c1col=(250,200,50)
		self.c2col=(10,250,250)
		self.c3col=(250,10,250)
		self.c4col=(50,10,255)
		
		self.timer = QtCore.QTimer()
		
		self.xgraph.setLabel('left', 'X', units='V')
		self.xgraph.setLabel('bottom', 'time', units='S')
		self.xregion = pg.LinearRegionItem()
		self.xgraph.addItem(self.xregion)
		self.xregion.sigRegionChanged.connect(zoomx)



		self.ygraph.setLabel('left', 'Y', units='V')
		self.ygraph.setLabel('bottom', 'time', units='S')
		self.yregion = pg.LinearRegionItem()
		self.ygraph.addItem(self.yregion)
		self.yregion.sigRegionChanged.connect(zoomy)

		self.ampgraph.setLabel('left', 'amplitude', units='V')
		self.ampgraph.setLabel('bottom', 'time', units='S')
		self.ampregion = pg.LinearRegionItem()
		self.ampgraph.addItem(self.ampregion)
		self.ampregion.sigRegionChanged.connect(zoomamp)

		self.phasegraph.setLabel('left', 'Phase', units='Degrees')
		self.phasegraph.setLabel('bottom', 'time', units='S')
		self.phregion = pg.LinearRegionItem()
		self.phasegraph.addItem(self.phregion)
		self.phregion.sigRegionChanged.connect(zoomph)


		self.c1 = self.xgraph.plot()
		self.c1.setPen(self.c1col)

		self.c2 = self.ygraph.plot()
		self.c2.setPen(self.c2col)

		self.c3 = self.ampgraph.plot()
		self.c3.setPen(self.c3col)

		self.c4 = self.phasegraph.plot()
		self.c4.setPen(self.c4col)


		self.c5 = self.zoomgraph.plot()
		self.c5.setPen((200,200,100))

		self.start_time=time.time()
		self.timer.timeout.connect(update) 


	
	def saveall(self,name='',directory='plots'):
		if not name == 'auto': name = self.filename.text()
		np.savetxt('%s/%s_x_%s.txt'%(directory,name,time.ctime()),np.column_stack([self.time,self.x]))
		np.savetxt('%s/%s_y_%s.txt'%(directory,name,time.ctime()),np.column_stack([self.time,self.y]))
		np.savetxt('%s/%s_amp_%s.txt'%(directory,name,time.ctime()),np.column_stack([self.time,self.amp]))
		np.savetxt('%s/%s_phase_%s.txt'%(directory,name,time.ctime()),np.column_stack([self.time,self.phase]))

	def __del__(self):
		self.saveall('auto','autosaves')
		print 'BYE BYE'
			
	def start_measuring(self):
		if not self.running :
			self.timer.start(200)
			self.init_button.setText('Stop measurements')
			self.running  = True
		else:
			self.timer.stop()
			self.init_button.setText('Start measurements')
			self.running  = False

		print 'Measuring....'

	def autophase(self):
		if self.running : self.timer.stop()
		lockin.write("APHS") #Autophase
		if self.running : self.timer.start(200)

	def set_frequency(self):
		if self.running : self.timer.stop()
		lockin.write("FREQ %s"%(int(self.freq.value()*1000)) )
		print "FREQ %s"%(int(self.freq.value()*1000))
		if self.running : self.timer.start(200)
		
	def set_amp(self):
		if self.running : self.timer.stop()
		lockin.write("SLVL %s"%(self.amplitude.value()) )
		print "SLVL %s"%(self.amplitude.value())
		if self.running : self.timer.start(200)

	def cleartraces(self):
		self.start_time=time.time()
		self.time = []
		self.x = []
		self.y= []
		self.amp = []
		self.phase = []

		
		print 'saved to file %s'%(self.filename.text())

		
myapp = MyMainWindow()

#thread.start_new_thread(update_buffer,())

myapp.show()
app.exec_()


