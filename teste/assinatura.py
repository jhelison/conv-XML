from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.utils.flags import NAMESPACE_NFE
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from lxml import etree

certificado = r'.\ORIZA VIEIRA LIMA03867404000175 (8).pfx'
senha = '81979780'
uf = 'ma'
homologacao = False

nfe = open(r'./cplus_not_assigned.xml')

xml_a = etree.parse(nfe)

# a1 = AssinaturaA1(certificado, senha)
# xml_a = a1.assinar(xml)

xml_text = etree.tostring(xml_a, encoding='unicode')
xml_text = xml_text.replace("""<NFe xmlns="http://www.portalfiscal.inf.br/nfe" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.portalfiscal.inf.br/nfe enviNFe.xsd">""",
    """<NFe xmlns="http://www.portalfiscal.inf.br/nfe">""")
xml_text = xml_text.replace("\n","")

xml_text = etree.fromstring(xml_text)

a1 = AssinaturaA1(certificado, senha)
xml_a = a1.assinar(xml_text)

xml_text = str(etree.tostring(xml_a, encoding='utf-8'))

output = open("output.xml", 'w', encoding="utf-8")
output.write(xml_text)   
output.close()

print(xml_text)