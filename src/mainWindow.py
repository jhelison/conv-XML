import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

from src.components import mainWindowComponent
from src.XMLSigner import XMLSigner
from src.Config import Config

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
        self.cf = Config()
        
        self.lineEdit__local_certificado.setText(self.cf.get('cert_path'))
        if self.cf.get('cert_path'):
            self.lineEdit_senha_certificado.setEnabled(True)
            self.lineEdit_senha_certificado.setText(self.cf.get('cert_password'))
        
        self.lineEdit_input_xml.setText(self.cf.get('input_folder'))

        self.lineEdit_output_xml.setText(self.cf.get('output_folder'))
        
        self.enable_process_button()
    
            
    def button_open_certify(self): 
        path = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                     'Abrir Certificado', 
                                                     self.cf.get('cert_path'), 
                                                     "Arquivo de Certificado (*.pfx *.cer)")[0]
        
        self.cf.save('cert_path', path)
        
        self.lineEdit__local_certificado.setText(path)
        if path:
            self.lineEdit_senha_certificado.setEnabled(True)
        self.enable_process_button()
        
    def button_xml_input_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                          'Pasta de entrada de XML',
                                                          self.cf.get('input_folder'))
        
        self.cf.save('input_folder', path)
        
        self.lineEdit_input_xml.setText(path)
        self.enable_process_button()

    def button_xml_output_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                          'Pasta de saída de XML',
                                                          self.cf.get('output_folder'))
        
        self.cf.save('output_folder', path)
        
        self.lineEdit_output_xml.setText(path)
        self.enable_process_button()

    def enable_process_button(self):
        if self.cf.get('cert_path') and self.cf.get('input_folder') and self.cf.get('output_folder'):
            self.pushButton_process.setEnabled(True)
            
    def on_password_edit(self):
        self.cf.save('cert_password', self.lineEdit_senha_certificado.text())
        
    def button_processar(self):
        cert = self.cf.get('cert_path')
        password = self.cf.get('cert_password')
        input_folder = self.cf.get('input_folder')
        output_folder = self.cf.get('output_folder')
        
        XMLSigneri = XMLSigner()
        
        try:
            XMLSigneri.certify_credential(cert, password)
            
            self.plainTextEdit_log.appendPlainText("Certificado Validado!")
            self.plainTextEdit_log.appendPlainText("")
            QtWidgets.QApplication.processEvents()
            
        except Exception as exception:
            self.show_error(str(exception))
            return
        
        xmls = [file for file in os.listdir(input_folder) if file.endswith('.xml')]
        
        for index, file in enumerate(xmls):
                full_path = input_folder + '/' + file
                
                self.plainTextEdit_log.appendPlainText(f"Processando: {file}")
                QtWidgets.QApplication.processEvents()
                self.progressBar.setValue(((index+1)/len(xmls)) * 100)
                
                signed_xml = XMLSigneri.process_nfe(full_path)
                XMLSigneri.save_xml(signed_xml, output_folder, file)
                
    def show_error(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()


app = QtWidgets.QApplication(sys.argv)
app.setStyle("Fusion")
window = Main()
sys.exit(app.exec_())

