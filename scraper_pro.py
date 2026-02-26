from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

def operacion_cyborg():
    print("🤖 Iniciando Operación Cyborg...")
    
    with sync_playwright() as p:
        # 1. LANZAR NAVEGADOR (Headless=False OBLIGATORIO para que tú puedas ver y clicar)
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        
        # 2. VIAJAR A LA PREMIER
        url = "https://fbref.com/es/comps/9/shooting/Estadisticas-de-Premier-League"
        print(f"🌍 Viajando a: {url}")
        page.goto(url)
        
        # --- MOMENTO DE LA VERDAD ---
        print("\n🛑 ¡ALTO! MIRA EL NAVEGADOR.")
        print("👉 Si ves el botón 'Soy humano' o un Captcha, ¡DALE CLICK TÚ MISMO!")
        print("⏳ El robot te esperará hasta 60 segundos para que resuelvas el problema...")
        
        try:
            # El robot espera HASTA que aparezca la tabla de estadísticas ('#stats_squads_shooting')
            # Si tú pasas el captcha, la tabla aparecerá y el robot seguirá.
            page.wait_for_selector("table.stats_table", timeout=60000) 
            print("✅ ¡BARRERA SUPERADA! He detectado la tabla de datos.")
        except:
            print("❌ Tiempo agotado. No pudimos pasar la defensa.")
            browser.close()
            return

        # 3. EL ROBO (Extracción)
        html_content = page.content()
        print("📸 Foto de los datos tomada. Cerrando navegador...")
        browser.close()

        # 4. PROCESAMIENTO (Igual que antes)
        print("📊 Procesando Excel...")
        try:
            tablas = pd.read_html(StringIO(html_content))
            tabla_tiros = tablas[0]
            
            # Limpieza de encabezados dobles
            if isinstance(tabla_tiros.columns, pd.MultiIndex):
                nuevas_cols = []
                for col in tabla_tiros.columns.values:
                    # Unimos niveles y limpiamos
                    nombre = ' '.join([str(c) for c in col if "Unnamed" not in str(c)]).strip()
                    nuevas_cols.append(nombre)
                tabla_tiros.columns = nuevas_cols

            # Filtramos basura
            tabla_tiros = tabla_tiros[tabla_tiros['Rk'] != 'Rk']
            
            # Guardamos
            archivo = "premier_league_xg.xlsx"
            tabla_tiros.to_excel(archivo, index=False)
            print(f"\n💾 ¡GOLAZO! Archivo guardado: {archivo}")
            print("📂 Ábrelo y busca la columna 'xG' o 'Esperado xG'.")
            
        except Exception as e:
            print(f"❌ Error procesando el Excel: {e}")

if __name__ == "__main__":
    operacion_cyborg()