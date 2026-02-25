import pandas as pd
import matplotlib.pyplot as plt

# 1. CARGAR DATOS
archivo = "historial_fpc.xlsx"
print(f"📂 Cargando datos de: {archivo}...")

try:
    df = pd.read_excel(archivo)
    
    # Buscamos la columna "Campeón"
    columna_campeon = None
    for col in df.columns:
        if "Campeón" in str(col):
            columna_campeon = col
            break
            
    if columna_campeon:
        # --- LIMPIEZA DE DATOS ---
        df[columna_campeon] = df[columna_campeon].astype(str)
        
        # 1. Quitar paréntesis y basura: "Millonarios (1)" -> "Millonarios"
        df[columna_campeon] = df[columna_campeon].str.split('(').str[0].str.strip()
        df[columna_campeon] = df[columna_campeon].str.split('[').str[0].str.strip()
        
        # 2. CORRECCIÓN HISTÓRICA (Fusión de Equipos)
        # Aquí unimos el nombre antiguo con el nuevo
        print("🔧 Unificando Deportes Caldas con Once Caldas...")
        df[columna_campeon] = df[columna_campeon].replace('Deportes Caldas', 'Once Caldas')
        
        # TIP: Si quisieras unir otros (ej: 'Atl. Nacional' -> 'Atlético Nacional'), lo harías aquí igual.

        # --- CONTAR TÍTULOS ---
        conteo = df[columna_campeon].value_counts()
        print("\n🏆 TABLA OFICIAL DE TÍTULOS:")
        print(conteo.head(10))

        # --- CONFIGURACIÓN DE COLORES ---
        # Diccionario de colores oficiales
        mapa_colores = {
            'Atlético Nacional': '#009900',  # Verde
            'Millonarios': '#0000FF',        # Azul
            'América de Cali': '#FF0000',    # Rojo
            'Junior': '#D92121',             # Rojo Junior
            'Santa Fe': '#C8102E',           # Rojo Cardenal
            'Deportivo Cali': '#00703C',     # Verde Cali
            'Independiente Medellín': '#CC0000', # Rojo DIM
            'Once Caldas': '#FFFFFF',        # Blanco (Ojo: Le pondremos borde negro)
            'Deportes Tolima': '#6C1D45',    # Vinotinto
            'Deportivo Pereira': '#FFD700'   # Amarillo
        }

        # Asignar colores a las barras (si no tiene color, se pone gris)
        colores_barras = [mapa_colores.get(equipo, 'grey') for equipo in conteo.head(10).index]

        # --- GRAFICAR ---
        plt.figure(figsize=(12, 6))
        barras = conteo.head(10).plot(kind='bar', color=colores_barras, edgecolor='black', linewidth=1)

        plt.title('Historial de Campeones FPC', fontsize=16, fontweight='bold')
        plt.xlabel('Equipo')
        plt.ylabel('Estrellas')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        # Etiquetas encima de las barras
        barras.bar_label(barras.containers[0], padding=3)

        plt.tight_layout()
        
        # Guardar
        ruta = 'visualizaciones/campeones_colombia_final.png'
        plt.savefig(ruta)
        print(f"\n🖼️ Gráfica guardada en: {ruta}")
        plt.show()

    else:
        print("❌ No encontré la columna Campeón.")

except Exception as e:
    print(f"❌ Error: {e}")