# encoding: utf-8
"""
@author: nnn11556
@software: PyCharm
@file: main.py
@time: 2018/5/23 21:19
"""
import sys
from myGUI import Myui
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()  # 创建QT对象
ui = Myui()
ui.setupUi(window)
window.show()  # QT对象显示
sys.exit(app.exec_())