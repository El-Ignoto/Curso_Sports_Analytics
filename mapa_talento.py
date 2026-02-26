import pandas as pd
import matplotlib.pyplot as plt
import os

def mapa_colombia():
    # CAMBIO IMPORTANTE: Ahora leemos el archivo de Colombia
    archivo = "colombia_shooting.html" 
    nombre_liga = "Liga BetPlay (Colombia)"
    
    print(f"🇨🇴 Analizando: {archivo}...")
    
    if not os.path.exists(archivo):
        print(f"❌ ERROR: No encuentro '{archivo}'. Asegúrate de haberlo guardado.")
        return

    try:
        # 1. CARGAR
        # header=1 es clave porque FBref usa doble título
        tablas = pd.read_html(archivo, encoding='utf-8', header=1)
        
        # Buscamos la tabla de jugadores
        df = None
        for t in tablas:
            if 'Player' in str(t.columns) or 'Jugador' in str(t.columns):
                df = t
                break
        
        if df is None: df = tablas[0]

        # 2. LIMPIEZA
        if 'Rk' in df.columns: df = df[df['Rk'] != 'Rk'].copy()
        
        cols_num = ['Gls', 'Sh', 'G/Sh']
        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                print(f"⚠️ Alerta: No veo la columna {col}. ¿Seguro que es la tabla de Tiros?")

        # 3. FILTRO (Ajustado para Colombia)
        # Bajamos la vara un poco: Mínimo 2 goles y 5 tiros para que salgan más jugadores
        df_top = df[(df['Gls'] >= 2) & (df['Sh'] >= 5)].copy()
        
        print(f"📊 Jugadores encontrados: {len(df_top)}")

        # 4. GRAFICAR
        plt.figure(figsize=(12, 8))
        
        # Puntos base
        plt.scatter(df_top['Sh'], df_top['Gls'], color='#FDB913', alpha=0.8, s=80, edgecolors='black') # Amarillo Colombia

        # ETIQUETAS
        for i, row in df_top.iterrows():
            nombre = str(row['Player' if 'Player' in df.columns else 'Jugador']).split(' ')[-1]
            goles = row['Gls']
            tiros = row['Sh']
            eficacia = row['G/Sh']
            
            # Destacar a los del Junior (Si el nombre del equipo contiene Junior)
            equipo = str(row['Squad' if 'Squad' in df.columns else 'Equipo'])
            
            if 'Junior' in equipo:
                plt.scatter(tiros, goles, color='red', s=150, edgecolors='white', linewidth=2, zorder=5)
                plt.annotate(nombre.upper(), (tiros, goles), xytext=(0, 10), textcoords='offset points', fontweight='bold', color='red')
            
            # Etiquetar también a los goleadores top de la liga (> 5 goles)
            elif goles >= 5 or eficacia > 0.20:
                plt.annotate(nombre, (tiros, goles), xytext=(5, 5), textcoords='offset points', fontsize=8)

        # 5. DETALLES
        plt.title(f'Mapa de Talento: {nombre_liga}', fontsize=16, fontweight='bold')
        plt.xlabel('Volumen de Tiros (Sh)', fontsize=12)
        plt.ylabel('Goles Marcados (Gls)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.axline((0, 0), slope=0.15, color='gray', linestyle='--', label='Promedio (15%)')
        plt.legend()

        plt.savefig("visualizaciones/mapa_colombia.png")
        print("\n🖼️ ¡Mapa guardado! Revisa 'visualizaciones/mapa_colombia.png'")
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    mapa_colombia()
    