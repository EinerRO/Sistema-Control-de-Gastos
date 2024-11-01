from conexionmongo import conectar_mongodb, leer_documentos
from datetime import *



conexion1, conexion2 = conectar_mongodb()


fecha_actual = datetime.today()
dia_actual = fecha_actual.strftime('%d')
mes_actual = fecha_actual.strftime('%m')
anio_actual = fecha_actual.strftime('%Y')
format_fecha = f'{dia_actual}/{mes_actual}/{anio_actual}'

lista_dias = []
 
def clasificar_monto_transaccion(transaccion):
    monto = 0
    documentos = leer_documentos(conexion2)
    for documento in documentos:
        if documento["fecha"] == format_fecha:
            monto = documento[transaccion]
    return monto

def extraer_monto_ahorro():
    monto_ahorro = 0
    documentos = leer_documentos(conexion1)
    for documento in documentos:
        fecha = datetime.strptime(documento["fecha"], '%d/%m/%Y').date()
        mes = fecha.strftime('%m')
        if mes == mes_actual and documento["concepto"] == "Ahorro":
            monto_ahorro += int(documento["valor"])
    return monto_ahorro


def extraer_saldo_mes_anterior():
    documentos = leer_documentos(conexion2)
    for documento in documentos:
        fecha = datetime.strptime(documento["fecha"], '%d/%m/%Y').date()
        dia = fecha.strftime('%d')
        mes = fecha.strftime('%m')
        anio = fecha.strftime('%Y')
        lista_dias.append(f'{dia}/{mes}/{anio}')

        if  f'31/{int(mes_actual) - 1}/{anio_actual}' in lista_dias:
            for documento in documentos:
                fecha = datetime.strptime(documento["fecha"], '%d/%m/%Y').date()
                if fecha.strftime('%d') == '31':
                    saldo_rindediario = documento["saldorindediario"]

        elif f'31/{int(mes_actual) - 1}/{anio_actual}' not in lista_dias:
            for documento in documentos:
                fecha = datetime.strptime(documento["fecha"], '%d/%m/%Y').date()
                if fecha.strftime('%d') == '30':
                    saldo_rindediario = documento["saldorindediario"]

        elif f'30/{int(mes_actual) - 1}/{anio_actual}' not in lista_dias:
            for documento in documentos:
                fecha = datetime.strptime(documento["fecha"], '%d/%m/%Y').date()
                if fecha.strftime('%d') == '29':
                    saldo_rindediario = documento["saldorindediario"]
    return saldo_rindediario

def definir_nombre_mes(fecha_actual):

    if fecha_actual.strftime('%B') == 'January':
        nombre_mes = 'enero'
    elif fecha_actual.strftime('%B') == 'February':
        nombre_mes = 'febrero'
    elif fecha_actual.strftime('%B') == 'March':
        nombre_mes = 'marzo'
    elif fecha_actual.strftime('%B') == 'April':
        nombre_mes = 'abril'
    elif fecha_actual.strftime('%B') == 'May':
        nombre_mes = 'mayo'
    elif fecha_actual.strftime('%B') == 'June ':
        nombre_mes = 'junio'
    elif fecha_actual.strftime('%B') == 'July':
        nombre_mes = 'julio'
    elif fecha_actual.strftime('%B') == 'August':
        nombre_mes = 'agosto'
    elif fecha_actual.strftime('%B') == 'September':
        nombre_mes = 'septiembre'
    elif fecha_actual.strftime('%B') == 'October':
        nombre_mes = 'octubre'
    elif fecha_actual.strftime('%B') == 'November':
        nombre_mes = 'noviembre'
    elif fecha_actual.strftime('%B') == 'December':
        nombre_mes = 'diciembre'
    return nombre_mes
     