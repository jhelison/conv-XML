import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import shelve

from src.components import mainWindowComponent

class Main(QtWidgets.QMainWindow, mainWindowComponent.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.config = shelve.open('./config/conf')

        self.pushButton_local_certificado.clicked.connect(self.button_open_certify)

        self.show()

    def button_open_certify(self):
        try:
            self.config['cert_path']
        except:
            self.config['cert_path'] = os.getcwd()
        
        self.config['cert_path'] = QtWidgets.QFileDialog.getOpenFileName(self,
        'Abrir Certificado',
        self.config['cert_path'],
        "Arquivo de Certificado (*.pfx *.cer)")[0]

        





app = QtWidgets.QApplication(sys.argv)
window = Main()
sys.exit(app.exec_())

