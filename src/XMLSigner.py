from pynfe.processamento.assinatura import AssinaturaA1
from lxml import etree
import re

class XMLSigner:
    def __init__(self):
        pass
        
    def certify_credential(self, certify_path, password):
        try:
            self.a1 = AssinaturaA1(certify_path, password)
        except:
            raise Exception("Certifacado ou senha invalidos")

    def process_nfe(self, xml_path):
        try:
            nfe = etree.parse(open(xml_path))
            xml_text = etree.tostring(nfe, encoding='unicode')
        except:
            raise Exception("Não foi possivel abrir o arquivo XML")
        
        try:
            xml_text = re.sub(r'<NFe([\s\S\n]*?)>',
                  """<NFe xmlns="http://www.portalfiscal.inf.br/nfe">""", xml_text)

            xml_text = re.sub(r'</infNFe>([\s\S\n]*?)</NFe>',
                            "</infNFe></NFe>", xml_text)

            xml_text = re.sub(r'<verProc>([\s\S\n]*?)</verProc>',
                            "<verProc>4.01_b029</verProc>", xml_text)

            xml_text = xml_text.replace("\n","")
            
            xml_text = etree.fromstring(xml_text)
            
            sign_xml = self.a1.assinar(xml_text)
            
            return etree.tostring(sign_xml, encoding='utf-8').decode('utf-8')
            
        except Exception as exception:
            raise Exception(f"Não foi possivel processar o XML com erro {exception}")
        
    def save_xml(self, xml_text, save_path, file_name = ""):
        signed_name = save_path + '/' + file_name[:-4] + '-nfe-sign' + '.xml'
        print(save_path)
        output = open(signed_name, 'w', encoding="utf-8")
        output.write(xml_text)
        output.close()