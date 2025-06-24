import urllib.parse
import requests

# Clave API proporcionada
API_KEY = "4mDiNy2sj3smSFacOf4ECKb7Wlf0Gjnu"
MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"

# Modos de transporte disponibles
MODOS_TRANSPORTE = {
    "1": "fastest",      # En auto
    "2": "pedestrian",   # A pie
    "3": "bicycle",      # En bicicleta
    "4": "multimodal"    # Transporte público (donde esté disponible)
}

def menu_transporte():
    print("\nSeleccione el modo de transporte:")
    print("1 - Auto")
    print("2 - A pie")
    print("3 - Bicicleta")
    print("4 - Transporte público")
    modo = input("Opción (1/2/3/4): ")
    return MODOS_TRANSPORTE.get(modo, "fastest")

while True:
    origen = input("\nCiudad de origen (o 's' para salir): ")
    if origen.lower() in ['s', 'quit', 'salir']:
        break

    destino = input("Ciudad de destino (o 's' para salir): ")
    if destino.lower() in ['s', 'quit', 'salir']:
        break

    transporte = menu_transporte()

    parametros = {
        "key": API_KEY,
        "from": origen,
        "to": destino,
        "routeType": transporte,
        "locale": "es_ES"  # 🌐 Establece idioma en español
    }

    url = MAIN_API + urllib.parse.urlencode(parametros)
    print(f"\n🛰 URL enviada: {url}\n")

    response = requests.get(url)
    data = response.json()

    status = data["info"]["statuscode"]

    if status == 0:
        ruta = data["route"]
        print("==============================================")
        print(f"📍 Ruta desde {origen} hasta {destino}")
        print(f"🕒 Duración del viaje: {ruta['formattedTime']}")
        print(f"📏 Distancia: {ruta['distance']} millas ({ruta['distance']*1.61:.2f} km)")
        if 'fuelUsed' in ruta:
            print(f"⛽ Combustible estimado: {ruta['fuelUsed']:.2f} galones ({ruta['fuelUsed']*3.78:.2f} litros)")
        print("==============================================")
        print("🧭 Instrucciones del viaje:")
        for paso in ruta["legs"][0]["maneuvers"]:
            narrativa = paso["narrative"]
            distancia_km = paso["distance"] * 1.61
            print(f" - {narrativa} ({distancia_km:.2f} km)")
        print("==============================================\n")

    elif status == 402:
        print("❌ Error: Entradas inválidas para una o ambas ciudades.\n")
    elif status == 611:
        print("❌ Error: Faltan datos de origen o destino.\n")
    else:
        print(f"⚠ Código de error {status}. Consulte: https://developer.mapquest.com/documentation/directions-api/status-codes\n")
