import csv
import xml.etree.ElementTree as ET
import datetime
from pathlib import Path
import os
from conexionmongo import conectar_mongodb, leer_documentos, insertar_totales, insetar_transaccion
from procedimientos import extraer_saldo_mes_anterior, definir_nombre_mes, calcular_totales

#Función para clasificar las transacciones según su tipo
def clasificar_transaccion_tipo(tipo_transaccion, lista, contenido):
    if tipo_transaccion in sms.get('body'):
        lista.append(contenido)

#Función para extrarer el valor de la transacción del cuerpo del mensaje (pagos, retiros y compras)
def extraer_valores(lista_transacciones, lista_rindediario, lista_cupo, lista_valores, indice_valor, indice_cuenta):

    for transaccion in lista_transacciones:
        cuenta_transaccion = transaccion.split()[indice_cuenta]
        transaccion = transaccion.split()[indice_valor]
        if len(transaccion) == 10:
            valor = transaccion[1] + transaccion[2] + transaccion[4] + transaccion[5] + transaccion[6]
            lista_valores.append(int(valor))
        elif len(transaccion) == 11:
            valor = transaccion[1] + transaccion[2] + transaccion[3] + transaccion[5] + transaccion[6] + transaccion[7]
            lista_valores.append(int(valor))
        elif len(transaccion) == 13:
            valor = transaccion[1] + transaccion[3] + transaccion[4] + transaccion[5] + transaccion[7] + transaccion[8] + transaccion[9]
            lista_valores.append(int(valor))
        clasificar_transaccion_cuenta(cuenta_transaccion, lista_rindediario, lista_cupo, valor)


#Función para clasificar la transacción según la cuenta
def clasificar_transaccion_cuenta(cuenta_transaccion, lista_rindediario, lista_cupo, valor):
    if '1385' in cuenta_transaccion:
        lista_rindediario.append(valor)
    elif '3778' in cuenta_transaccion:
        lista_cupo.append(valor)
    
#Función para extraer transacciones de la base de datos Mongodb
def extraer_otras_transacciones(consignaciones, retiros, pagos, transferencias, mes_actual, conexion1):
    transacciones = leer_documentos(conexion1)
    for transaccion in transacciones:
        fecha = datetime.datetime.strptime(transaccion['fecha'], "%d/%m/%Y")
        if transaccion['transaccion'] == 'Consignación' and fecha.strftime('%m') == mes_actual:
            consignaciones.append(transaccion['valor'])
        elif transaccion['transaccion'] == 'Retiro' and fecha.strftime('%m') == mes_actual:
            retiros.append(transaccion['valor'])
        elif transaccion['transaccion'] == 'Pago' and fecha.strftime('%m') == mes_actual:
            pagos.append(transaccion['valor'])
        elif transaccion['transaccion'] == 'Transferencia' and fecha.strftime('%m') == mes_actual:
            transferencias.append(transaccion['valor'])



#Conexion a la base de datos
conexion1, conexion2 = conectar_mongodb()


# Fecha hora actual
fecha_actual = datetime.datetime.now()
mes_actual = fecha_actual.strftime('%m')
dia_actual = fecha_actual.strftime('%d')
anio_actual = fecha_actual.strftime('%Y')
format_fecha = f'{dia_actual}/{mes_actual}/{anio_actual}'
hora = fecha_actual.hour
minutos = fecha_actual.minute
segundos = fecha_actual.second


#Lista de archivos de la rura donde se encuentra el archivo xml
archivos = os.listdir("C:/Users/Power/Dropbox/Aplicaciones/SMSBackupRestore")

#Recorre la lista para obtener el archivo correcto
for archivo in archivos:
    if f'{anio_actual}-{mes_actual}-{dia_actual}' in archivo:
        datos = archivo

#Listas para almacenar las diferentes transacciones segun su tipo con la estructura completa del cuerpo del mensaje
pago_productos_pse = []
retiros = []
retiros_sin_tarjeta = []
transferencias = []
compras = []
consignaciones = []

#Listas para almacenar los valores de cada tipo de transacción
valores_pagos_pse = []
valores_retiros = []
valores_retiro_sin_tarjeta = []
valores_transferencias = []
valores_compras = []
valores_consignaciones = []

#Listas para almacenar las transacciones según la cuenta
rindediario_pago = []
cupo_credito_pago = []
rindediario_retiro = []
cupo_credito_retiro = []
rindediario_transferencia = []
cupo_transferencia = []
rindediario_compra = []
cupo_compra = []

#Acumuladores para obtener los valores totales
total_pagos_pse = 0
total_retiros = 0
total_transferencias = 0
total_compras = 0


archivo_xml = Path(f"C:/Users/Power/Dropbox/Aplicaciones/SMSBackupRestore/{datos}")
archivo_csv = "sms_xml.csv"

arbol = ET.parse(archivo_xml)
raiz = arbol.getroot()

# Consignar el Saldo del mes anterior
if dia_actual == "01":
    saldo_mes_anterior = extraer_saldo_mes_anterior()
    insetar_transaccion("Consignación", "Saldo mes anterior", saldo_mes_anterior, format_fecha,conexion1)

# Extarer otras transacciones que se han ingresado de forma manual
extraer_otras_transacciones(valores_consignaciones, valores_retiros, valores_pagos_pse, valores_transferencias,mes_actual,conexion1)

with open(archivo_csv, 'w', newline='') as csvfile:
    csvwrite = csv.writer(csvfile)
    csvwrite.writerow(['Dirección', 'Cuerpo', 'Fecha'])
    for sms in raiz.findall('sms'):
        # fecha_actual.strftime('%B')
        if definir_nombre_mes(fecha_actual) in sms.get('readable_date') or fecha_actual.strftime('%B') in sms.get('readable_date'):
            direccion = sms.get('address')
            cuerpo = sms.get('body')
            fecha = sms.get('readable_date')
            csvwrite.writerow([direccion, cuerpo, fecha])
            clasificar_transaccion_tipo('Pago productos', pago_productos_pse, cuerpo)
            clasificar_transaccion_tipo('Retiro', retiros, cuerpo)
            clasificar_transaccion_tipo('Retiro - Sin tarjeta', retiros_sin_tarjeta, cuerpo)
            clasificar_transaccion_tipo('realizo una transferencia', transferencias, cuerpo)
            clasificar_transaccion_tipo('realizo Compra', compras, cuerpo)
            clasificar_transaccion_tipo('consignacion', consignaciones, cuerpo)

# PAGO DE PRODUCTOS PSE
print("PAGOS PSE")
extraer_valores(pago_productos_pse,rindediario_pago,cupo_credito_pago,valores_pagos_pse,7,8)
print(valores_pagos_pse)
print(f'Total pagos pse: {calcular_totales(valores_pagos_pse)} ')
print(f'Pagos de Rindediario: {rindediario_pago}')
print(f'Total pagos Rindediario: {calcular_totales(rindediario_pago)}')
print(f'Pagos cupo de crédito: {cupo_credito_pago}')
print(f'Total pagos cupo de crédito: {calcular_totales(cupo_credito_pago)}\n')

# RETIRO POR CAJERO ELECTRÓNICO
print('RETIROS')
extraer_valores(retiros,rindediario_retiro, cupo_credito_retiro,valores_retiros,4,5)
extraer_valores(retiros_sin_tarjeta,rindediario_retiro, cupo_credito_retiro,valores_retiro_sin_tarjeta,7,8)
print(valores_retiros)
print(valores_retiro_sin_tarjeta)
print(f'Total retiros: {calcular_totales(valores_retiros) + calcular_totales(valores_retiro_sin_tarjeta)}')
print(f'Retiros de Rindediario: {rindediario_retiro}')
print(f'Total retiros Rindediario: {calcular_totales(rindediario_retiro)}')
print(f'Retiros cupo de crédito: {cupo_credito_retiro}')
print(f'Total retiros cupo de crédito: {calcular_totales(cupo_credito_retiro)}\n')

# TRANSFERENCIAS
print("TRANSFERENCIAS")
#extraer_valores(transferencias,rindediario_transferencia, cupo_transferencia, valores_transferencias, 7, 0)
for transferencia in transferencias:
    if len(transferencia) == 150:
        valor = transferencia[46] + transferencia[48] + transferencia[49] + transferencia[50]
        valores_transferencias.append(int(valor))
    elif len(transferencia) == 151:
        valor = transferencia[46] + transferencia[47] + transferencia[49] + transferencia[50] + transferencia[51]
        valores_transferencias.append(int(valor))
    elif len(transferencia) == 152:
        valor = transferencia[46] + transferencia[47] + transferencia[48] + transferencia[50] + transferencia[51] + transferencia[52]
        valores_transferencias.append(int(valor))
    elif len(transferencia) == 154:
        valor = transferencia[46] + transferencia[48] + transferencia[49] + transferencia[50] + transferencia[52] + transferencia[53] + transferencia[54]
        valores_transferencias.append(int(valor))
    

print(f'Total transferencias: {calcular_totales(valores_transferencias)}')
print(valores_transferencias)
print(f'transferencias de Rindediario: {rindediario_transferencia}')
print(f'Total transferencias Rindediario: {calcular_totales(rindediario_transferencia)}')
print(f'transferencias cupo de crédito: {cupo_transferencia}')
print(f'Total transferencias cupo de crédito: {calcular_totales(cupo_transferencia)}\n')
    
# COMPRAS
print("COMPRAS")
extraer_valores(compras,rindediario_compra,cupo_compra,valores_compras,4,5)
print(f'Total compras: {calcular_totales(valores_compras) - calcular_totales(cupo_compra)}')
print(f'compras de Rindediario: {rindediario_compra}')
print(f'Total compras Rindediario: {calcular_totales(rindediario_compra)}')
print(f'compras cupo de crédito: {cupo_compra}')
print(f'Total compras cupo de crédito: {calcular_totales(cupo_compra)}\n')
    
# CONSIGNACIONES
print("CONSIGNACIONES")
# extraer_valores(consignaciones, rindediario_consignacion, cupo_consignacion, valores_consignaciones, 9, 0)
for consignacion in consignaciones:
    if len(consignacion) == 67:
        valor = consignacion[61] + consignacion[63] + consignacion[64] + consignacion[65]
    elif len(consignacion) == 68:
        valor = consignacion[61] + consignacion[62] + consignacion[64] + consignacion[65] + consignacion[66]
    elif len(consignacion) == 69:
        valor = consignacion[61] + consignacion[62] + consignacion[63] + consignacion[65] + consignacion[66] + consignacion[67]
    elif len(consignacion) == 71:
        valor = consignacion[61] + consignacion[63] + consignacion[64] + consignacion[65] + consignacion[67] + consignacion[68] + consignacion[69]
    valores_consignaciones.append(valor) 

print(f'Total consignaciones: {calcular_totales(valores_consignaciones)}')
print(valores_consignaciones)

# Totales por tipo de transacción sin disriminar la cuenta origen
total_pagos_pse = calcular_totales(valores_pagos_pse)
total_retiros = calcular_totales(valores_retiros) + calcular_totales(valores_retiro_sin_tarjeta) 
total_transferencias = calcular_totales(valores_transferencias)
total_compras = calcular_totales(valores_compras)
total_consignaciones = calcular_totales(valores_consignaciones)

# Totales por tipo transacción de acuerdo a la cuenta origen
cupo_pse = calcular_totales(cupo_credito_pago)
cupo_retiro = calcular_totales(cupo_credito_retiro)
cupo_compras = calcular_totales(cupo_compra)
usos_cupo = cupo_pse + cupo_retiro + cupo_compras

# Total general de gastos
total_gastos = total_pagos_pse + total_retiros + total_transferencias + total_compras

# Total gastos cuenta principal
total_gastos_rindediario = (total_pagos_pse - cupo_pse) + (total_retiros - cupo_retiro) + (total_compras - cupo_compras) + total_transferencias

saldo_general = total_consignaciones - total_gastos
saldo_rindediario = total_consignaciones - total_gastos_rindediario
insertar_totales(total_pagos_pse,total_transferencias,total_retiros,total_compras,total_consignaciones,saldo_rindediario,saldo_general,usos_cupo,total_gastos_rindediario, format_fecha,conexion2)
print(saldo_general)
print(saldo_rindediario)
print(usos_cupo)




