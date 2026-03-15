import funciones
import graficas

def main():
    archivo= "scr/datalogger_rawData.csv"
    totalizador = funciones.revisar_totalizador(archivo)    
    datos_crudos = funciones.leer_csv(archivo)
    datos_procesados = funciones.generar_csv_salida(archivo, totalizador)
    graficas.generar_grafica_tendencia(datos_procesados)
    graficas.generar_histogramas(datos_procesados)
    graficas.generar_mapas_calor_pivot(datos_procesados)
    graficas.generar_curva_de_carga(datos_procesados)
    print("Todas las gráficas generadas exitosamente")


if __name__ == "__main__":
    main()