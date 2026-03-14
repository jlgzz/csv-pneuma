import pandas as pd

def totalizador_inicial(archivo):
    df = pd.read_csv(archivo, sep=";", header=None)
    return float(df.iloc[2,1])


def generar_csv_salida(archivo):
    # Crear un DataFrame de ejemplo
    data = {
        'Nombre': ['Ana', 'Luis', 'María', 'Carlos'],
        'Edad': [25, 30, 28, 35],
        'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla']
    }
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('outputs/datos_preprocesados.csv', index=False)

    print("CSV generado exitosamente en outputs/datos_preprocesados.csv")
