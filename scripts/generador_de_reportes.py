import funciones

def main():
    archivo= "scr/datalogger_rawData.csv"
    totalizador = funciones.revisar_totalizador(archivo)    
    datos_crudos = funciones.leer_csv(archivo)
    datos_procesados = funciones.generar_csv_salida(archivo, totalizador)


if __name__ == "__main__":
    main()