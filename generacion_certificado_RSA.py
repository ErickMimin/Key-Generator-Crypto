# importacion de libreria para la generacion de llaves RSA
from Crypto.PublicKey import RSA

#libreria sobre protocolo SMTP 
# protocolo para transferencia simple de correo es un protocolo de red utilizado para 
# el intercambio de mensajes de correo electrónico entre computadoras u otros dispositivos. 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# libreria decouple para el uso de variables de entorno
from decouple import config

#libreria json para el manejos de archivos .json
import json

#libreria os para añadir variables a la ruta de los archivos
import os

#librerias para la generacion del certfidicado digital x.509 y las llaves RSA 
from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join


def genera_envia_claves_RSA(nombre, correo, cert_dir):

    print('\nSe estan generando el par de llaves y el certificado digital del abogado ' + nombre +' , por favor espera un momento')

    CERT_FILE = nombre + " certificado.pem"
    KEY_FILE = nombre + " private.pem"

    
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    # if not exists(join(cert_dir, CERT_FILE)) \
    #         or not exists(join(cert_dir, KEY_FILE)):

    # creamos el par de llaves RSA
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "MX"
    cert.get_subject().ST = "CDMX"
    cert.get_subject().L = "GAM"
    cert.get_subject().O = "Smith&Jones"
    cert.get_subject().OU = "IPN"
    cert.get_subject().CN = nombre
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    print ('\nEl certificado del abogado ' + nombre + ' se guardo en el archivo ' + nombre + ' certificado.pem')

    open(join(cert_dir, CERT_FILE), "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    print ('\nLa clave privada del abogado ' + nombre + ' se guardo en el archivo ' + nombre + ' private.pem')

    open(join(cert_dir, KEY_FILE), "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    # # generamos las llaves RSA
    # key = RSA.generate(2048)

    # private_key = key.export_key() # llave privada
    # file_out = open(nombre + " private.pem", "wb")
    # file_out.write(private_key)
    # file_out.close()
    # print ('\nLa clave publica se guardo en el archivo ' + nombre + ' private.pem')

    # public_key = key.publickey().export_key() # llave publica
    # file_out = open(nombre + " receiver.pem", "wb")
    # file_out.write(public_key)
    # file_out.close()
    # print ('\nLa clave privada se guardo en el archivo ' + nombre + ' receiver.pem')

    # vamos a generar un JSON en el que se guarde el nombre de los abogados junto
    # a sus respectivas llaves



    # claves_abogado = dict()
    # claves_abogado['nombre'] = nombre
    # claves_abogado['publica'] = public_key.decode("utf-8") 
    # claves_abogado['privada'] = private_key.decode("utf-8") 

    # print(claves_abogado)
    


    # # pedimos el correo del destinatario
    # destinatario_1 = input('\nEscribe el destinario por favor: ')

    # Parte del correo

    # Iniciamos los parámetros del script
    remitente = 'smithjones20201@gmail.com'
    destinatarios = [correo]
    asunto = 'Envio de certificado digital y llave privada. Abogado ' + nombre
    cuerpo = 'Por este medio, le hacemos llegar su certificado digital y su clave privada de RSA abogado ' + nombre

    ruta_adjunto_certificado= os.path.join(r'E:\ESCOM\OCTAVO SEMESTRE\Cripto\Proyecto Cripto (pruebas, etc)\generacion de llave privada y publica RSA', nombre + " certificado.pem")
    nombre_adjunto_certificado = nombre + " certificado.pem"

    ruta_adjunto_llave_privada= os.path.join(r'E:\ESCOM\OCTAVO SEMESTRE\Cripto\Proyecto Cripto (pruebas, etc)\generacion de llave privada y publica RSA', nombre + ' private.pem')
    nombre_adjunto_llave_privada = nombre + ' private.pem'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()

    # atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto


    # se grega el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))


    ### LAS LINEAS DE ABAJO SON PARA LA CARGA DEL ARCHIVO DEL CERTIFICADO

    # Abrimos el archivo de certificado que vamos a adjuntar
    archivo_adjunto_certificado = open(ruta_adjunto_certificado, 'rb')

    # Creamos un objeto MIME base
    adjunto_MIME_certificado = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto del certificado
    adjunto_MIME_certificado.set_payload((archivo_adjunto_certificado).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME_certificado)
    # Agregamos una cabecera al objeto
    adjunto_MIME_certificado.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto_certificado)
    # Y finalmente agregamos el archivo del certificado al mensaje
    mensaje.attach(adjunto_MIME_certificado)


    ### LAS LINEAS DE ABAJO SON PARA LA CARGA DEL ARCHIVO DE LLAVE PRIVADA

    # Abrimos el archivo de llave privada que vamos a adjuntar
    archivo_adjunto_llave_privada = open(ruta_adjunto_llave_privada, 'rb')

    # Creamos un objeto MIME base
    adjunto_MIME_llave_privada = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto de la llave privada
    adjunto_MIME_llave_privada.set_payload((archivo_adjunto_llave_privada).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME_llave_privada)
    # Agregamos una cabecera al objeto
    adjunto_MIME_llave_privada.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto_llave_privada)
    # Y finalmente agregamos el archivo de la llave privada al mensaje
    mensaje.attach(adjunto_MIME_llave_privada)



    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login('smithjones20201@gmail.com', config('MAIL_PASSWORD'))

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()

    print('\nSe le notifica que el certificado digital y llave privada del abogado ' + nombre + ' han sido enviados, favor de verificar su correo')

    # input('\nPresiona ENTER para terminar')

    # return claves_abogado




###################### MAIN

# Opening JSON file 
f = open('datos.json', "r") 

# returns JSON object as  
# a dictionary 
data = json.load(f) 

print()

j = 0

for i in data['datos_abogados']: 
    j += 1



dic = [{}]*j

j = 0
# Iterating through the json 
# list 
for i in data['datos_abogados']: 
    
    # print('Nombre del abogado:', i['nombre'], '  Correo: ', i['correo'])
    # dic[j] = genera_envia_claves_RSA(i['nombre'], i['correo'])

    genera_envia_claves_RSA(i['nombre'], i['correo'], ".")

    # print (dic)

    # j += 1
    # print ('\nnnValor j: ', j)
    


    # with open("data_file.json", "w") as json_file:
    #     json.dump(dic, json_file)

    # print(datos_abogado_RSA)

    
# Closing file 
f.close() 

