import pandas as pd
import requests
from io import StringIO 

url = "https://es.wikipedia.org/wiki/Categor%C3%ADa_Primera_A"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("📡 Conectando con Wikipedia...")

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Leemos el HTML
    tablas = pd.read_html(StringIO(response.text))
    
    # Buscamos la tabla de campeones
    tabla_campeones = None
    for tabla in tablas:
        # Convertimos columnas a texto para buscar palabras clave
        cols_str = str(tabla.columns).lower()
        if "campeón" in cols_str and "subcampeón" in cols_str:
            tabla_campeones = tabla.copy() # Hacemos una copia para no dañar el original
            break
            
    if tabla_campeones is not None:
        print("✅ Tabla encontrada. Procesando encabezados...")

        # --- NUEVO: APLANAR ENCABEZADOS (El truco mágico) ---
        # Si la tabla tiene encabezados múltiples (MultiIndex), los unimos con un espacio
        if isinstance(tabla_campeones.columns, pd.MultiIndex):
            nuevas_columnas = []
            for col in tabla_campeones.columns.values:
                # Une los niveles del encabezado (Ej: "Año" + "Nivel1" -> "Año")
                nombre_col = ' '.join(map(str, col)).strip()
                nuevas_columnas.append(nombre_col)
            tabla_campeones.columns = nuevas_columnas

        print(f"Primera fila histórica: {tabla_campeones.iloc[0, 0]}") # Debería decir 1948

        # Guardamos
        archivo = "historial_fpc.xlsx"
        tabla_campeones.to_excel(archivo, index=False)
        print(f"\n💾 ¡GOLAZO! Archivo guardado: {archivo}")
        
    else:
        print("⚠️ No encontré la tabla exacta.")

except Exception as e:
    print(f"❌ Error: {e}")