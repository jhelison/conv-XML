from pynfe.processamento.assinatura import AssinaturaA1
from lxml import etree

certificado = r'.\ORIZA VIEIRA LIMA03867404000175 (8).pfx'
senha = '81979780'
uf = 'ma'
homologacao = False

nfe_file = open(r'./cplus_not_assigned.xml', encoding='utf-8')
nfe_file = nfe_file.read().replace('\n', '')

root = etree.fromstring(nfe_file)

children = root.getchildren()[0]


print(children.keys())