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

def generar_csv_salida(archivo, totalizador_inicial):
    df = pd.read_csv(
        archivo,
        sep=";",
        header=0,
        thousands=",",
        skiprows=6
    )

    df.columns = ['Time', 'Flow', 'Pressure', 'Temperature', 'Totalizer']

    # Convertir columnas a numéricas
    df['Flow'] = pd.to_numeric(df['Flow'], errors='coerce')
    df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
    df['Totalizer'] = pd.to_numeric(df['Totalizer'], errors='coerce')



    # Convertir de GPa a psi
    df['Pressure'] = round(df['Pressure']/1000000000*145.037737, 2)  # Convertir de GPa a psi


    # Constantes para corrección de flujo
    constante_presion_psi_abs = 14.69597535
    constante_temp_r = 491.67
    # Convertir Flow de Ln/min a L/min (flujo actual)
    df['Pressure_abs'] = df['Pressure'] + 14.5
    # Temperatura en Rankine
    df['Temperature_R'] = (df['Temperature'] * 1.8)+ constante_temp_r
    # Convertir de Ln/min a L/min y redondear a 2 decimales
    df['Flow'] = round(df['Flow']*df['Temperature_R']*constante_presion_psi_abs/(df['Pressure_abs']*constante_temp_r), 2)  

    # Calcular Totalizer corregido
    df['Totalizer'] = round((df['Totalizer'] - totalizador_inicial)*1000*df['Temperature_R']*constante_presion_psi_abs/(df['Pressure_abs']*constante_temp_r), 2)  # Convertir a litros y corregir por temperatura y presión   



    # Eliminar columnas temporales
    df.drop(['Pressure_abs', 'Temperature_R'], axis=1, inplace=True)

    df.columns = ['Timestamp', 'Flow (L/min)', 'Pressure (Psi)', 'Temperature (°C)', 'Totalizer (L)']
    df.to_csv('outputs/datos_preprocesados.csv', index=False)
    print("Csv de salida generado exitosamente")
    print(df.head())
    return None
