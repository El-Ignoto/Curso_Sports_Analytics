import pandas as pd
import matplotlib.pyplot as plt
import os

def crear_mapa_talento():
    archivo = "premier_shooting.html"
    print(f"🎨 Preparando lienzo con datos de: {archivo}...")
    
    if not os.path.exists(archivo):
        print("❌ Error: Falta el archivo HTML.")
        return

    try:
        # 1. CARGAR Y LIMPIAR (Lo mismo que ya sabes hacer)
        tablas = pd.read_html(archivo, encoding='utf-8', header=1)
        df = tablas[0]
        
        # Buscar la tabla correcta si hay varias
        for t in tablas:
            if 'Player' in str(t.columns) or 'Jugador' in str(t.columns):
                df = t
                break

        if 'Rk' in df.columns: df = df[df['Rk'] != 'Rk'].copy()
        
        cols_num = ['Gls', 'Sh', 'G/Sh']
        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 2. FILTRAR JUGADORES (Para no graficar a los que tienen 0 goles)
        # Nos interesan los que tengan al menos 3 goles y 10 tiros
        df_top = df[(df['Gls'] >= 3) & (df['Sh'] >= 10)].copy()
        
        print(f"📊 Graficando a {len(df_top)} jugadores destacados...")

        # 3. CREAR EL GRÁFICO (SCATTER PLOT)
        plt.figure(figsize=(12, 8))
        
        # Eje X: Tiros, Eje Y: Goles
        # alpha=0.7 hace los puntos un poco transparentes
        plt.scatter(df_top['Sh'], df_top['Gls'], color='dodgerblue', alpha=0.7, s=80, edgecolors='black')

        # 4. ETIQUETAR A LOS CRACKS (La parte difícil)
        # Vamos a ponerle nombre SOLO a los que destaquen mucho
        for i, row in df_top.iterrows():
            nombre = row['Player'].split(' ')[-1] # Solo el apellido para ahorrar espacio
            goles = row['Gls']
            tiros = row['Sh']
            efectividad = row['G/Sh']
            
            # Condición: Etiquetar si tiene muchos goles (>10) O mucha efectividad (>0.20)
            if goles > 12 or efectividad > 0.20:
                plt.annotate(nombre, (tiros, goles), 
                             xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')
                
                # Si es tu descubrimiento Kroupi, lo pintamos de ROJO
                if "Kroupi" in row['Player'] or "Brobbey" in row['Player']:
                     plt.scatter(tiros, goles, color='red', s=150, edgecolors='black', zorder=5)

        # 5. MAQUILLAJE DEL GRÁFICO
        plt.title('Mapa de Talento: Goles vs Tiros (Premier League)', fontsize=16, fontweight='bold')
        plt.xlabel('Cantidad de Tiros (Volumen)', fontsize=12)
        plt.ylabel('Cantidad de Goles (Definición)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        
        # Línea de promedio (Opcional, para ver quién está por encima)
        plt.axline((0, 0), slope=0.15, color='gray', linestyle='--', label='Promedio (15%)')
        plt.legend()

        # Guardar
        ruta = "visualizaciones/mapa_talento_premier.png"
        plt.savefig(ruta)
        print(f"\n🖼️ ¡Obra de arte guardada! Busca: {ruta}")
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    crear_mapa_talento()