import pandas as pd
import os

def procesar_eficacia_v2():
    archivo = "premier_shooting.html"
    # AQUÍ CAMBIAS EL NOMBRE DEL JUGADOR QUE QUIERAS BUSCAR
    nombre_objetivo = "Haaland" 
    
    print(f"📂 Analizando archivo: {archivo}...")
    
    if not os.path.exists(archivo):
        print("❌ ERROR: No encuentro el archivo 'premier_shooting.html'.")
        return

    try:
        # 1. CARGAR
        tablas = pd.read_html(archivo, encoding='utf-8', header=1)
        
        # Buscamos la tabla correcta
        df = None
        for t in tablas:
            cols = str(t.columns).lower()
            if 'player' in cols or 'jugador' in cols:
                df = t
                break
        
        if df is None: df = tablas[0]

        # 2. LIMPIEZA (Corregimos el Warning aquí usando .copy())
        if 'Rk' in df.columns:
            # Al poner .copy(), creamos una tabla nueva independiente y Pandas deja de molestar
            df = df[df['Rk'] != 'Rk'].copy()
        
        # Convertimos a números
        cols_num = ['Gls', 'Sh', 'G/Sh']
        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 3. BÚSQUEDA DEL JUGADOR
        print(f"\n🔍 BUSCANDO A: {nombre_objetivo.upper()}...")
        
        col_nombre = 'Player' if 'Player' in df.columns else 'Jugador'
        
        # Buscamos el nombre (contiene el texto, ignorando mayúsculas)
        jugador = df[df[col_nombre].str.contains(nombre_objetivo, na=False, case=False)]
        
        if not jugador.empty:
            print(f"\n🤖 --- REPORTE DE {jugador[col_nombre].values[0]} ---")
            
            goles = jugador['Gls'].values[0]
            tiros = jugador['Sh'].values[0]
            eficacia = jugador['G/Sh'].values[0]
            
            print(f"⚽ Goles: {goles}")
            print(f"👟 Tiros: {tiros}")
            print(f"🎯 Efectividad (G/Sh): {eficacia}")
            
            # CÁLCULO DE LETALIDAD
            print("\n🧠 ANÁLISIS:")
            # Un 0.20 significa que mete 1 de cada 5 tiros (Nivel Elite Mundial)
            if eficacia >= 0.25:
                print("👽 NIVEL ALIENÍGENA. Toca el balón y es gol.")
            elif eficacia >= 0.18:
                print("🔥 DELANTERO ELITE. Muy por encima del promedio.")
            elif eficacia >= 0.12:
                print("✅ BUEN DEFINIDOR. Promedio aceptable para un 9.")
            else:
                print("❄️ PÓLVORA MOJADA. Necesita muchas ocasiones.")

        else:
            print(f"⚠️ No encontré a '{nombre_objetivo}'.")
            print("Intenta abrir el HTML y ver cómo escribieron su nombre.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    procesar_eficacia_v2()