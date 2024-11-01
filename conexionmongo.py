from pymongo import *


def conectar_mongodb():
    try:
        client = MongoClient("localhost", 27017)
        base_de_datos = client['tipotransaccion']
        coleccion_transacciones = base_de_datos['transacciones']
        coleccion_totales = base_de_datos['totales']
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        print("Conexión finalizada")
    return coleccion_transacciones, coleccion_totales

def leer_documentos(coleccion):
    documentos = coleccion.find()
    return documentos
    
def insetar_transaccion(transaccion, concepto, valor, fecha, coleccion1):
    documento_datos = {"transaccion":transaccion, "concepto":concepto, "valor":valor, "fecha": fecha}
    coleccion1.insert_one(documento_datos)
    
def insertar_totales(pagos, transferencias, retiros, compras, consignaciones, saldo_rindediario, saldo_general, uso_cupo, gasto_rindediario, fecha, coleccion2):
    documento_datos = {
        "pagos":pagos, 
        "transferencias":transferencias, 
        "retiros":retiros, 
        "compras":compras, 
        "consignaciones":consignaciones, 
        "saldorindediario":saldo_rindediario, 
        "saldogeneral":saldo_general,
        "usocupo":uso_cupo,
        "gastorindediario":gasto_rindediario,
        "fecha":fecha
    }
    coleccion2.insert_one(documento_datos)


