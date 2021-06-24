from PyQt5 import QtWidgets, uic
import sys
app = QtWidgets.QApplication([])
win = uic.loadUi("ejemplo.ui") #especifique su archivo .ui
win.show()
sys.exit(app.exec())
