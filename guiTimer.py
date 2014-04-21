#!/usr/bin/python
#coding=utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_guiTimer import Ui_Form
import sys
import time


class MainWidget( QWidget ):
    def __init__( self ):
	QWidget.__init__( self )
	self.createSystemTray()
	self.createUI()
	self.setWindowTitle( u'小定时器' )
	#then the size policy
	self.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
	self.quitWithoutTray = False
	#then the positon/geometry
	self.setGeometry( 400, 400, self.size().width(), self.size().height() )

    def closeEvent( self, evt ):
	if self.quitWithoutTray:
	    evt.accept()
	else:
	    self.hide()
	    evt.ignore()

    def keyPressEvent( self, evt ):
	if evt.key() == Qt.Key_Escape or (evt.key() == Qt.Key_W\
		and evt.modifiers() & Qt.ControlModifier ):
	    self.hide()
	elif ( evt.key() == Qt.Key_Q and evt.modifiers()&Qt.ControlModifier ):
	    self.noTrayClose()
	#global shortcut to invoke the app, not implemented
	elif ( evt.key() == Qt.Key_T and evt.modifiers()&Qt.AltModifier ):
	    self.show()
	else:
	    QWidget.keyPressEvent( self, evt )

    @pyqtSlot(int)
    def trayActivated( self, reason ):
	if QSystemTrayIcon.DoubleClick == reason:
	    self.show()

    def createUI( self ):
	self.ui = Ui_Form()
	self.ui.setupUi( self )
	self.nowTimeText = time.strftime(u'%H:%M:%S'.encode('utf-8')).decode('utf-8') 
	self.ui.labelStartTime.setText( self.nowTimeText )
	self.ui.labelEndTime.setText( '' )
	self.connect( self.ui.btnSetStartTime, SIGNAL('clicked()'),\
		self.updateStartTime )
	self.connect( self.ui.btnStartTimer, SIGNAL('clicked()'), \
		self.startTimer )
	self.ui.lineEditTimeCount.setFocus()

    def startTimer( self ):
	self.timer = QTimer()
	minute = self.ui.lineEditTimeCount.text()
	try:
	    minute = float( minute )
	except ValueError:
	    return
	self.timer.singleShot( minute*60*1000, self, SLOT('timeOutMsg()'))

    @pyqtSlot()
    def timeOutMsg( self ):
	self.systemTray.showMessage( u'时间到了', u'真的到了', QSystemTrayIcon.Information, \
		2000 )
	self.msgLabel = QLabel( u'<h1>时间到!</h1><img src="./38.gif"/>' )
	self.msgLabel.setWindowFlags( Qt.FramelessWindowHint )
	self.msgLabel.setGeometry( 400, 400, self.size().width(), self.size().height() )
	self.timer.singleShot( 2800, self.msgLabel, SLOT('hide()') )
	self.msgLabel.show()
    @pyqtSlot()
    def noTrayClose( self ):
	self.quitWithoutTray = True
	self.close()

    @pyqtSlot()
    def updateStartTime( self ):
	text = self.ui.lineEditStartTime.text()
	if len(text) < 1:
	    text =  self.nowTimeText
	self.ui.labelStartTime.setText( text )

    def createSystemTray( self ):
	self.systemTray = QSystemTrayIcon( self )
	self.trayIcon = QIcon( 'tray.ico' )
	self.trayMenu = QMenu( self )
	self.exitAction = QAction( u'退出', self )
	self.showAction = QAction( u'显示', self )
	self.connect( self.exitAction, SIGNAL('triggered()'), self.noTrayClose )
	self.connect( self.showAction, SIGNAL('triggered()'), self.show )
	self.trayMenu.addAction( self.exitAction )
	self.trayMenu.addAction( self.showAction )
	self.systemTray.setContextMenu( self.trayMenu )
	self.systemTray.setIcon( self.trayIcon )
	#self.connect( self.systemTray, SIGNAL('activated(int)'), self.trayActivated )
	self.systemTray.activated.connect( self.trayActivated )
	self.systemTray.show()
    pass

a = QApplication( sys.argv )
mywidget = MainWidget()
mywidget.show()
sys.exit( a.exec_() )

