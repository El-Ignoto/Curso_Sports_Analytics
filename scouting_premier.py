import pandas as pd
import os

def buscar_joyas():
    archivo = "premier_shooting.html"
    print(f"🕵️‍♂️ Iniciando Scouting en: {archivo}...")
    
    if not os.path.exists(archivo):
        print("❌ Error: No encuentro el archivo HTML.")
        return

    try:
        # 1. CARGAR DATOS
        tablas = pd.read_html(archivo, encoding='utf-8', header=1)
        
        # Buscamos la tabla de jugadores
        df = tablas[0]
        for t in tablas:
            if 'Player' in str(t.columns) or 'Jugador' in str(t.columns):
                df = t
                break
        
        # 2. LIMPIEZA
        if 'Rk' in df.columns:
            df = df[df['Rk'] != 'Rk'].copy()
            
        # Convertir números
        cols_num = ['Age', 'Gls', 'Sh', 'G/Sh'] # Agregamos Edad ('Age') para ver si son jóvenes
        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 3. EL FILTRO DE CALIDAD (La clave del analista)
        # Queremos jugadores que hayan metido al menos 5 goles
        filtro_goles = df['Gls'] >= 5
        
        df_filtrado = df[filtro_goles].copy()
        
        # 4. ORDENAR POR EFECTIVIDAD (De mayor a menor)
        # ascending=False significa "descendente" (del más alto al más bajo)
        ranking = df_filtrado.sort_values(by='G/Sh', ascending=False)
        
        # Seleccionamos solo columnas interesantes
        cols_ver = ['Player', 'Squad', 'Age', 'Gls', 'Sh', 'G/Sh']
        # Si las columnas tienen nombres en español, ajusta aquí
        
        print("\n💎 --- TOP 10 JUGADORES MÁS LETALES (Min. 5 Goles) ---")
        top_10 = ranking[cols_ver].head(10)
        print(top_10.to_string(index=False)) # Imprime bonito sin el índice numérico
        
        # Guardamos el reporte para el jefe
        top_10.to_excel("reporte_scouting_top10.xlsx", index=False)
        print("\n💾 Reporte guardado: reporte_scouting_top10.xlsx")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    buscar_joyas()