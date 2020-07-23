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

        self.pushButton_local_certificado.clicked.connect(self.button_open_certify)
        self.pushButton_input_xml.clicked.connect(self.button_xml_input_folder)
        self.pushButton_output_xml.clicked.connect(self.button_xml_output_folder)
        self.pushButton_process.clicked.connect(self.button_processar)
        
        self.lineEdit_senha_certificado.textChanged.connect(self.on_password_edit)
        
        self.initialize_elements()

        self.show()
        
    def initialize_elements(self):
        if not os.path.isdir('./config'):
            os.makedirs('./config')

        self.config = shelve.open('./config/conf')
        keys = list(self.config.keys())
        
        if 'cert_path' in keys:
            self.lineEdit__local_certificado.setText(self.config['cert_path'])
            self.lineEdit_senha_certificado.setEnabled(True)
        else:
            self.config['cert_path'] = os.getcwd()
        if 'input_folder' in keys:
            self.lineEdit_input_xml.setText(self.config['input_folder'])
        else:
            self.config['input_folder'] = os.getcwd()
        if 'output_folder' in keys:
            self.lineEdit_output_xml.setText(self.config['output_folder'])
        else:
            self.config['output_folder'] = os.getcwd()
        if 'cert_password' in keys:
            self.lineEdit_senha_certificado.setText(self.config['cert_password'])
        else:
            self.config['cert_password'] = ''
            
        self.enable_process_button()
            

    def button_open_certify(self):      
        self.config['cert_path'] = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                         'Abrir Certificado',
                                                                         self.config['cert_path'],
                                                                         "Arquivo de Certificado (*.pfx *.cer)")[0]
        
        self.lineEdit__local_certificado.setText(self.config['cert_path'])
        self.lineEdit_senha_certificado.setEnabled(True)
        self.enable_process_button()
        
    def button_xml_input_folder(self):            
        self.config['input_folder'] = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                                 'Pasta de entrada de XML',
                                                                                 self.config['input_folder'])
        
        self.lineEdit_input_xml.setText(self.config['input_folder'])
        self.enable_process_button()

    def button_xml_output_folder(self):
        self.config['output_folder'] = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                                 'Pasta de saída de XML',
                                                                                 self.config['output_folder'])
        
        self.lineEdit_output_xml.setText(self.config['output_folder'])
        self.enable_process_button()

    def enable_process_button(self):
        keys = list(self.config.keys())
        if 'cert_path' in keys and 'input_folder' in keys and 'output_folder' in keys:
            self.pushButton_process.setEnabled(True)
            
    def on_password_edit(self):
        self.config['cert_password'] = self.lineEdit_senha_certificado.text()
        
    def button_processar(self):
        cert = self.config['cert_path']
        password = self.config['cert_password']
        input_folder = self.config['input_folder']
        output_folder = self.config['output_folder']
        
        self.show_error('teste')
        
    def show_error(self, text):
        msg = QtWidgets.QErrorMessage()
        msg.showMessage(text)
        msg.exec_()





app = QtWidgets.QApplication(sys.argv)
window = Main()
sys.exit(app.exec_())

