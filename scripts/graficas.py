import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

def generar_grafica_tendencia(df):
    # ==============================
    # Procesar dataframe
    # ==============================
    df.columns = df.columns.str.strip()

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        format="%Y-%m-%d %H:%M:%S"
    )

    df = df.sort_values("Timestamp")
    df = df.set_index("Timestamp")

    # ==============================
    # Convertir numéricos
    # ==============================
    cols = ["Flow (L/min)", "Pressure (Psi)", "Temperature (°C)", "Totalizer (L)"]

    for col in cols:
        if col == "Totalizer [L]":
            df[col] = df[col].astype(str).str.replace(",", "")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Flow (L/min)", "Pressure (Psi)", "Temperature (°C)"])

    # ==============================
    # Resample inteligente
    # ==============================
    df_resampled = df.resample('5min').agg({
        "Flow (L/min)": "mean",
        "Pressure (Psi)": "mean",
        "Temperature (°C)": "mean",
        "Totalizer (L)": "last"  # 🔥 importante
    })

    df_resampled = df_resampled.dropna()
    df_plot = df_resampled

    print(f"Muestras originales: {len(df)}")
    print(f"Muestras remuestreadas: {len(df_plot)}")

    # ==============================
    # Crear figura
    # ==============================
    fig, (ax1, ax4) = plt.subplots(2, 1, figsize=(14, 10))

    # ===== GRÁFICA 1 =====
    color1 = "tab:blue"
    color2 = "tab:red"
    color3 = "tab:green"

    l1, = ax1.plot(df_plot.index, df_plot["Flow (L/min)"],
                   color=color1, linewidth=2, label="Flow (L/min)")
    ax1.set_ylabel("Flow (L/min)", color=color1, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # Segundo eje
    ax2 = ax1.twinx()
    l2, = ax2.plot(df_plot.index, df_plot["Pressure (Psi)"],
                   color=color2, linewidth=2, label="Pressure (Psi)")
    ax2.set_ylabel("Pressure (Psi)", color=color2, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Tercer eje
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 70))
    l3, = ax3.plot(df_plot.index, df_plot["Temperature (°C)"],
                   color=color3, linewidth=2, label="Temperature (°C)")
    ax3.set_ylabel("Temperature (°C)", color=color3, fontweight='bold')
    ax3.tick_params(axis='y', labelcolor=color3)

    # Leyenda combinada
    lines = [l1, l2, l3]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left")

    # Formato de fecha automático
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))

    ax1.set_title("Flow, Pressure and Temperature vs Time",
                  fontsize=13, fontweight='bold', pad=15)

    # ===== GRÁFICA 2 =====
    color4 = "tab:purple"
    ax4.plot(df_plot.index, df_plot["Totalizer (L)"],
             color=color4, linewidth=2)

    ax4.set_xlabel("Time", fontweight='bold')
    ax4.set_ylabel("Totalizer (L)", color=color4, fontweight='bold')
    ax4.tick_params(axis='y', labelcolor=color4)
    ax4.grid(True, alpha=0.3)
    ax4.set_title("Totalizer vs Time",
                  fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    fig.savefig('outputs/grafica.png', dpi=300, bbox_inches='tight')
    print("Gráfica de tendencia generada exitosamente")

    return fig

def generar_histogramas(df):
    # ==============================
    # Procesar dataframe para histogramas
    # ==============================
    df.columns = df.columns.str.strip()

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        format="%Y-%m-%d %H:%M:%S"
    )

    df = df.sort_values("Timestamp")
    df = df.set_index("Timestamp")

    # ==============================
    # Convertir numéricos (ya deberían estarlo)
    # ==============================
    cols = ["Flow (L/min)", "Pressure (Psi)", "Temperature (°C)", "Totalizer (L)"]

    for col in cols:
        if col == "Totalizer (L)":
            df[col] = df[col].astype(str).str.replace(",", "")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Flow (L/min)", "Pressure (Psi)", "Temperature (°C)"])

    # ==============================
    # Resample inteligente para histogramas
    # ==============================
    df_resampled = df.resample('5min').agg({
        "Flow (L/min)": "mean",
        "Pressure (Psi)": "mean",
        "Temperature (°C)": "mean",
        "Totalizer (L)": "last"
    })

    df_resampled = df_resampled.dropna()
    df_plot = df_resampled

    # ==============================
    # Histograma de Flow
    # ==============================
    flow_mean = df_plot["Flow (L/min)"].mean()
    flow_std = df_plot["Flow (L/min)"].std()

    hist_color = 'tab:blue'

    fig_flow = plt.figure(figsize=(10, 6))
    plt.hist(df_plot["Flow (L/min)"], bins=50, color=hist_color, alpha=0.7, edgecolor='black')
    plt.xlabel("Flow (L/min)", fontweight='bold')
    plt.ylabel("Frecuencia", fontweight='bold')
    plt.title("Histograma de Flow", fontsize=13, fontweight='bold', pad=15)
    plt.grid(True, alpha=0.3)

    stats_text = f"Media = {flow_mean:.2f}\nStd = {flow_std:.2f}"
    plt.text(0.98, 0.95, stats_text, transform=plt.gca().transAxes,
             ha='right', va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    fig_flow.savefig('outputs/histograma_flow.png', dpi=300, bbox_inches='tight')
    print("Histograma de Flow generado exitosamente")
    plt.close(fig_flow)

    # ==============================
    # Histograma de Pressure
    # ==============================
    pressure_mean = df_plot["Pressure (Psi)"].mean()
    pressure_std = df_plot["Pressure (Psi)"].std()

    fig_pressure = plt.figure(figsize=(10, 6))
    plt.hist(df_plot["Pressure (Psi)"], bins=50, color=hist_color, alpha=0.7, edgecolor='black')
    plt.xlabel("Pressure (Psi)", fontweight='bold')
    plt.ylabel("Frecuencia", fontweight='bold')
    plt.title("Histograma de Pressure", fontsize=13, fontweight='bold', pad=15)
    plt.grid(True, alpha=0.3)

    stats_text = f"Media = {pressure_mean:.2f}\nStd = {pressure_std:.2f}"
    plt.text(0.98, 0.95, stats_text, transform=plt.gca().transAxes,
             ha='right', va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    fig_pressure.savefig('outputs/histograma_pressure.png', dpi=300, bbox_inches='tight')
    print("Histograma de Pressure generado exitosamente")
    plt.close(fig_pressure)

def generar_mapas_de_calor(df):
    import numpy as np

    # ==============================
    # Procesar dataframe para mapas de calor
    # ==============================
    df.columns = df.columns.str.strip()

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        format="%Y-%m-%d %H:%M:%S"
    )

    df = df.sort_values("Timestamp")
    df = df.set_index("Timestamp")

    # ==============================
    # Convertir numéricos (ya deberían estarlo)
    # ==============================
    cols = ["Flow (L/min)", "Pressure (Psi)", "Temperature (°C)", "Totalizer (L)"]

    for col in cols:
        if col == "Totalizer (L)":
            df[col] = df[col].astype(str).str.replace(",", "")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Flow (L/min)", "Pressure (Psi)", "Temperature (°C)"])

    # ==============================
    # Resample inteligente para mapas de calor
    # ==============================
    df_resampled = df.resample('5min').agg({
        "Flow (L/min)": "mean",
        "Pressure (Psi)": "mean",
        "Temperature (°C)": "mean",
        "Totalizer (L)": "last"
    })

    df_resampled = df_resampled.dropna()
    df_plot = df_resampled

    # ==============================
    # Mapa de calor de Flow
    # ==============================
    # Convertir tiempo a horas desde el inicio
    time_hours = (df_plot.index - df_plot.index[0]).total_seconds() / 3600
    flow_values = df_plot["Flow (L/min)"].values

    # Crear bins
    flow_bins = np.linspace(flow_values.min(), flow_values.max(), 50)
    time_bins = np.linspace(time_hours.min(), time_hours.max(), 50)

    # Histograma 2D con pesos para promedio
    hist_flow, xedges_flow, yedges_flow = np.histogram2d(flow_values, time_hours, bins=[flow_bins, time_bins], weights=flow_values)
    hist_count_flow, _, _ = np.histogram2d(flow_values, time_hours, bins=[flow_bins, time_bins])
    hist_avg_flow = np.divide(hist_flow, hist_count_flow, out=np.zeros_like(hist_flow), where=hist_count_flow != 0)

    fig_heat_flow = plt.figure(figsize=(10, 6))
    plt.imshow(hist_avg_flow.T, origin='lower', aspect='auto', extent=[xedges_flow[0], xedges_flow[-1], yedges_flow[0], yedges_flow[-1]], cmap='viridis')
    plt.colorbar(label='Valor promedio de Flow (L/min)')
    plt.xlabel("Flow (L/min)", fontweight='bold')
    plt.ylabel("Tiempo (horas desde inicio)", fontweight='bold')
    plt.title("Mapa de Calor de Flow", fontsize=13, fontweight='bold', pad=15)
    fig_heat_flow.savefig('outputs/mapa_calor_flow.png', dpi=300, bbox_inches='tight')
    print("Mapa de calor de Flow generado exitosamente")
    plt.close(fig_heat_flow)

    # ==============================
    # Mapa de calor de Pressure
    # ==============================
    pressure_values = df_plot["Pressure (Psi)"].values

    pressure_bins = np.linspace(pressure_values.min(), pressure_values.max(), 50)

    hist_pressure, xedges_pressure, yedges_pressure = np.histogram2d(pressure_values, time_hours, bins=[pressure_bins, time_bins], weights=pressure_values)
    hist_count_pressure, _, _ = np.histogram2d(pressure_values, time_hours, bins=[pressure_bins, time_bins])
    hist_avg_pressure = np.divide(hist_pressure, hist_count_pressure, out=np.zeros_like(hist_pressure), where=hist_count_pressure != 0)

    fig_heat_pressure = plt.figure(figsize=(10, 6))
    plt.imshow(hist_avg_pressure.T, origin='lower', aspect='auto', extent=[xedges_pressure[0], xedges_pressure[-1], yedges_pressure[0], yedges_pressure[-1]], cmap='plasma')
    plt.colorbar(label='Valor promedio de Pressure (Psi)')
    plt.xlabel("Pressure (Psi)", fontweight='bold')
    plt.ylabel("Tiempo (horas desde inicio)", fontweight='bold')
    plt.title("Mapa de Calor de Pressure", fontsize=13, fontweight='bold', pad=15)
    fig_heat_pressure.savefig('outputs/mapa_calor_pressure.png', dpi=300, bbox_inches='tight')
    print("Mapa de calor de Pressure generado exitosamente")
    plt.close(fig_heat_pressure)


def generar_mapas_calor_pivot(df, time_col="Timestamp", flow_col="Flow (L/min)", pressure_col="Pressure (Psi)"):
    # ==============================
    # Leer/limpiar columnas y convertir timestamps
    # ==============================
    df = df.copy()
    df.columns = df.columns.str.strip()

    df[time_col] = pd.to_datetime(df[time_col])
    df["hour"] = df[time_col].dt.hour
    df["date"] = df[time_col].dt.date

    # ==============================
    # Mapa de calor del flujo
    # ==============================
    heatmap_flow = df.pivot_table(
        values=flow_col,
        index="hour",
        columns="date",
        aggfunc="mean"
    )

    cmap = "viridis"

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_flow, cmap=cmap)
    plt.title("Mapa de calor del flujo de aire")
    plt.xlabel("Día")
    plt.ylabel("Hora del día")
    plt.tight_layout()
    plt.savefig("outputs/mapa_calor_flow.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Mapa de calor de Flow generado exitosamente")

    # ==============================
    # Mapa de calor de presión
    # ==============================
    heatmap_pressure = df.pivot_table(
        values=pressure_col,
        index="hour",
        columns="date",
        aggfunc="mean"
    )

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_pressure, cmap=cmap)
    plt.title("Mapa de calor de presión del sistema")
    plt.xlabel("Día")
    plt.ylabel("Hora del día")
    plt.tight_layout()
    plt.savefig("outputs/mapa_calor_pressure.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Mapa de calor de Pressure generado exitosamente")

    # ==============================
    # Mapas de calor 3D (superficies)
    # ==============================
    # Flow 3D
    dates_num = mdates.date2num(heatmap_flow.columns.to_list())
    hours = heatmap_flow.index.to_numpy()

    X, Y = np.meshgrid(dates_num, hours)
    Z_flow = np.nan_to_num(heatmap_flow.values, nan=0.0)

    fig_flow_3d = plt.figure(figsize=(14, 8))
    ax3d_flow = fig_flow_3d.add_subplot(111, projection='3d')
    surf_flow = ax3d_flow.plot_surface(X, Y, Z_flow, cmap=cmap, edgecolor='none')
    ax3d_flow.set_xlabel('Día')
    ax3d_flow.set_ylabel('Hora del día')
    ax3d_flow.set_zlabel(flow_col)
    ax3d_flow.set_title('Mapa de calor 3D - Flow')
    fig_flow_3d.colorbar(surf_flow, shrink=0.5, aspect=10, label=flow_col)
    fig_flow_3d.savefig('outputs/mapa_calor_flow_3d.png', dpi=300, bbox_inches='tight')
    plt.close(fig_flow_3d)
    print("Mapa de calor 3D de Flow generado exitosamente")

    # Pressure 3D
    Z_pressure = np.nan_to_num(heatmap_pressure.values, nan=0.0)

    fig_pressure_3d = plt.figure(figsize=(14, 8))
    ax3d_pressure = fig_pressure_3d.add_subplot(111, projection='3d')
    surf_pressure = ax3d_pressure.plot_surface(X, Y, Z_pressure, cmap=cmap, edgecolor='none')
    ax3d_pressure.set_xlabel('Día')
    ax3d_pressure.set_ylabel('Hora del día')
    ax3d_pressure.set_zlabel(pressure_col)
    ax3d_pressure.set_title('Mapa de calor 3D - Pressure')
    fig_pressure_3d.colorbar(surf_pressure, shrink=0.5, aspect=10, label=pressure_col)
    fig_pressure_3d.savefig('outputs/mapa_calor_pressure_3d.png', dpi=300, bbox_inches='tight')
    plt.close(fig_pressure_3d)
    print("Mapa de calor 3D de Pressure generado exitosamente")


def generar_curva_de_carga(df, flow_col="Flow (L/min)"):
    """Genera la curva de duración de carga (load duration curve) para flujo.

    El gráfico muestra el flujo ordenado de mayor a menor versus el porcentaje de tiempo.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()

    df[flow_col] = pd.to_numeric(df[flow_col], errors="coerce")
    df = df.dropna(subset=[flow_col])

    # Ordenar datos de mayor a menor
    sorted_flow = np.sort(df[flow_col].values)[::-1]
    percent_time = np.linspace(0, 100, len(sorted_flow))

    # Estadísticas
    mean_flow = df[flow_col].mean()
    p95_flow = np.percentile(df[flow_col].values, 95)
    base_flow = np.percentile(df[flow_col].values, 5)

    plt.figure(figsize=(10, 6))
    plt.plot(percent_time, sorted_flow, linewidth=2)

    # líneas de referencia
    plt.axhline(mean_flow, linestyle="--", label="Demanda promedio")
    plt.axhline(p95_flow, linestyle=":", label="Percentil 95")
    plt.axhline(base_flow, linestyle="-.", label="Carga base estimada")

    # Zonas sombreadas
    plt.fill_between(percent_time, p95_flow, sorted_flow, where=(sorted_flow >= p95_flow),
                     color="#fdd0a2", alpha=0.6, label="Picos anormales de demanda")
    plt.fill_between(percent_time, mean_flow, sorted_flow, where=(sorted_flow >= mean_flow) & (sorted_flow < p95_flow),
                     color="#a6bddb", alpha=0.5, label="Picos operativos")
    plt.fill_between(percent_time, base_flow, sorted_flow, where=(sorted_flow >= base_flow) & (sorted_flow < mean_flow),
                     color="#c7e9c0", alpha=0.4, label="Demanda regular")
    plt.fill_between(percent_time, sorted_flow, base_flow, where=(sorted_flow < base_flow),
                     color="#fdd0a2", alpha=0.6, label="Consumo constante")

    plt.xlabel("Porcentaje del tiempo (%)")
    plt.ylabel("Flujo (L/min)")
    plt.title("Curva de duración de carga del sistema")
    plt.legend(loc="upper right")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("outputs/curva_de_carga.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Curva de carga generada exitosamente")

