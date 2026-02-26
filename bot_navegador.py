from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("⚙️ INICIANDO EN MODO MANUAL...")

try:
    # 1. OPCIONES BÁSICAS (Sin trucos raros)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    # 2. INSTALAR Y LANZAR
    # Esto busca el driver exacto para tu Chrome 145
    print("📥 Buscando driver compatible...")
    service = Service(ChromeDriverManager().install())
    
    print("🚀 Lanzando navegador...")
    driver = webdriver.Chrome(service=service, options=options)

    # 3. NAVEGAR
    url = "https://fbref.com/es/"
    print(f"🌍 Viajando a: {url}")
    driver.get(url)

    print("\n✅ ¡LISTO! Si ves la página, NO toques nada en el código.")
    
    # --- EL TRUCO MAESTRO ---
    # El script se quedará congelado aquí hasta que tú presiones ENTER en la terminal.
    # Esto obliga a la ventana a seguir abierta.
    input("🛑 PRESIONA LA TECLA [ENTER] AQUÍ EN LA TERMINAL PARA CERRAR EL ROBOT...")

    print("👋 Cerrando...")
    driver.quit()

except Exception as e:
    print(f"❌ ERROR: {e}")