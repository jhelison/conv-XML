from OpenSSL import crypto
import tempfile
import os

caminho_arquivo = "./ORIZA VIEIRA LIMA03867404000175 (8).pfx"
senha = "81979780"

pkcs12 = crypto.load_pkcs12(open(caminho_arquivo, "rb").read(), senha)

print(pkcs12)

cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
chave = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())

print(cert, chave)
