import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import shelve

from src.components import mainWindowComponent
from src.XMLSigner import XMLSigner

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
        if 'input_folder' in keys:
            self.lineEdit_input_xml.setText(self.config['input_folder'])
        if 'output_folder' in keys:
            self.lineEdit_output_xml.setText(self.config['output_folder'])
        if 'cert_password' in keys:
            self.lineEdit_senha_certificado.setText(self.config['cert_password'])
        else:
            self.config['cert_password'] = ''
            
        self.enable_process_button()
            

    def button_open_certify(self): 
        if 'cert_path' in list(self.config.keys()):
            location = self.config['cert_path']
        else:
            location = ""
        self.config['cert_path'] = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                         'Abrir Certificado',
                                                                         location,
                                                                         "Arquivo de Certificado (*.pfx *.cer)")[0]
        
        self.lineEdit__local_certificado.setText(self.config['cert_path'])
        self.lineEdit_senha_certificado.setEnabled(True)
        self.enable_process_button()
        
    def button_xml_input_folder(self):
        if 'input_folder' in list(self.config.keys()):
            location = self.config['input_folder']
        else:
            location = ""        
        self.config['input_folder'] = QtWidgets.QFileDialog.getExistingDirectory(self, 'Pasta de entrada de XML', location)
        
        self.lineEdit_input_xml.setText(self.config['input_folder'])
        self.enable_process_button()

    def button_xml_output_folder(self):
        if 'output_folder' in list(self.config.keys()):
            location = self.config['output_folder']
        else:
            location = ""  
        self.config['output_folder'] = QtWidgets.QFileDialog.getExistingDirectory(self, 'Pasta de saída de XML', location)
        
        self.lineEdit_output_xml.setText(self.config['output_folder'])
        self.enable_process_button()

    def enable_process_button(self):
        if self.config['cert_path'] and self.config['input_folder'] and self.config['output_folder']:
            self.pushButton_process.setEnabled(True)
            
    def on_password_edit(self):
        self.config['cert_password'] = self.lineEdit_senha_certificado.text()
        
    def button_processar(self):
        cert = self.config['cert_path']
        password = self.config['cert_password']
        input_folder = self.config['input_folder']
        output_folder = self.config['output_folder']
        
        XMLsigner = XMLSigner()
        
        try:
            XMLsigner.certify_credential(cert, password)
        except Exception as exception:
            self.show_error(str(exception))
            return
        
        for file in os.listdir(input_folder):
            if file.endswith('.xml'):
                full_path = input_folder + '/' + file
                signed_xml = XMLsigner.process_nfe(full_path)
                print(output_folder)
                XMLSigner.save_xml(signed_xml, output_folder, file)
                
    def show_error(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()





app = QtWidgets.QApplication(sys.argv)
window = Main()
sys.exit(app.exec_())

