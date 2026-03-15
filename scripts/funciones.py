import csv
import pandas as pd




def revisar_totalizador(archivo):
    with open(archivo, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)
        if len(rows) > 2:
            totalizador_inicial = float(rows[2][1])
            print("Totalizador inicial: " + str(totalizador_inicial))
            return totalizador_inicial  # Convertir a float si es necesario
        else:
            return None



def leer_csv(archivo):
    df = pd.read_csv(
        archivo,
        sep=";",
        header=0,
        thousands=",",
        skiprows=6
    )

    print("Csv leído exitosamente")
    print(df.head())
    return df

def generar_csv_salida(archivo):
    contante_presion_psi_abs = 14.69657535
    constante_temp_r = 491.67


    df = pd.read_csv(
        archivo,
        sep=";",
        header=0,
        thousands=",",
        skiprows=6
    )

    df.columns = ['Time', 'Flow', 'Pressure', 'Temperature', 'Totalizer']

# Multiplicar Temperature por 2
    temperatura_R = df['Temperature'] * 1.8 + constante_temp_r
    presion_psi_abosulta = df['Pressure'] + contante_presion_psi_abs



    # Asegurarse de que Flow sea numérico, permitiendo tanto cadenas con comas como números flotantes
    flow = df['Flow']
    if flow.dtype == object:
        flow = flow.str.replace(',', '', regex=False)
    df['Flow'] = pd.to_numeric(flow, errors='coerce')

    df['Flow'] = df['Flow'] * temperatura_R * contante_presion_psi_abs / presion_psi_abosulta *constante_temp_r


    

    # Cambia el nombre de las columnas a algo más amigable
    df.columns = ['Timestamp', 'Flow (L/min)', 'Pressure (Psi)', 'Temperature (°C)', 'Totalizer (L)']
    df.to_csv('outputs/datos_preprocesados.csv', index=False)

    print("Csv de salida generado exitosamente")
    print(df.head())
    return None
