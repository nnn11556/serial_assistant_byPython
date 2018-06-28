# encoding: utf-8
"""
@author: nnn11556
@software: PyCharm
@file: myGUI.py
@time: 2018/5/23 21:19
"""

# import sys
import serial
import serial.tools.list_ports as ser_list
import threading
import time
# import binascii

from serialUI import Ui_MainWindow
from PyQt5 import QtGui

class Myui(Ui_MainWindow):
    ser = serial.Serial()
    def setupUi(self, Form):
        super().setupUi(Form)
        self.rec_num = 0
        self.send_num = 0
        Form.setFixedSize(745,495)
        self.cheak_Btn.clicked.connect(self.cheak_port)
        self.clear_send_Btn.clicked.connect(self.clear_send_text)
        self.clear_receive_Btn.clicked.connect(self.clear_receive_text)
        self.open_device_Btn.clicked.connect(self.open_device)
        self.send_Btn.clicked.connect(self.send_data)

    def cheak_port(self):
        port_list = list(ser_list.comports())
        self.com_comboBox.clear()
        if len(port_list) > 0:
            self.com_comboBox.addItems([com[0] for com in port_list])
        else:
            self.com_comboBox.addItem("None")

    def clear_send_text(self):
        self.send_tE.setText("")
        self.send_num = 0
        self.ser.flushOutput()

    def clear_receive_text(self):
        self.rec_num = 0
        self.rec_label.setText(str(self.rec_num))
        self.receive_tB.setText("")
        self.ser.flushInput()

    def cheak_parity(self):
        str = self.parity_comboBox.currentText()
        if str == '无':
            return 'N'
        elif str == '奇校验':
            return 'E'
        else:
            return 'O'

    def open_device(self):
        self.ser.port = self.com_comboBox.currentText()
        self.ser.baudrate = int(self.baud_comboBox.currentText())
        self.ser.bytesize = int(self.data_comboBox.currentText())
        self.ser.stopbits = int(self.stop_comboBox.currentText())
        self.ser.parity = self.cheak_parity()
        try:
            self.ser.open()
            if(self.ser.isOpen()):
                # self.open_device_Btn.setEnabled(False)
                self.open_device_Btn.setText("关闭串口")
                self.rthread = threading.Thread(target=self.receive_data)
                self.rthread.setDaemon(True)
                self.rthread.start()
                self.open_device_Btn.clicked.connect(self.close_device)
        except:
            pass

    def close_device(self):
        Flag = True
        while(Flag):
            try:
                if(self.ser.isOpen()):
                    self.ser.close()
                    Flag = False
                    if(self.ser.isOpen()):
                        Flag = True
            except:
                pass
        self.open_device_Btn.setText("打开串口")
        self.open_device_Btn.clicked.connect(self.open_device)

    def receive_data(self):
        rec_buffer = ''
        self.rec_num = 0
        while(self.ser.isOpen()):
            # wait 10ms
            try:
                time.sleep(0.02)
                size = self.ser.inWaiting()
                #receive data end with '\r\n'
                if size > 0:
                    rec_buffer1 = self.ser.read_all()
                    self.receive_tB.insertPlainText(rec_buffer1.decode())
                    self.receive_tB.moveCursor(QtGui.QTextCursor.End)
                    # self.ser.flushInput()
                    self.rec_num += len(rec_buffer1)
                    self.rec_label.setText('R:'+str(self.rec_num))
            except:
                pass

    def send_data(self):
        if(self.ser.isOpen()):
            send_buffer = self.send_tE.toPlainText()+'\r\n'
            self.ser.write(send_buffer.encode('utf-8'))
            self.send_num += len(send_buffer)
            self.send_label.setText('S:'+str(self.send_num))


