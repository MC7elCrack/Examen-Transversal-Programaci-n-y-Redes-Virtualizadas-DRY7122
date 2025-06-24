import requests
import time

# Reemplaza esto con tu propia API key de OpenRouteService
API_KEY = "TU_API_KEY"

def get_coords(ciudad):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": ciudad,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "DRY7122-Exam-Script"
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    if data:
        return float(data[0]['lon']), float(data[0]['lat'])
    else:
        return None

while True:
    origen_txt = input("Ciudad de Origen (o 's' para salir): ")
    if origen_txt.lower() == "s":
        break
    destino_txt = input("Ciudad de Destino: ")
    medio = input("Medio de transporte (driving-car, foot-walking, cycling-regular): ")

    origen = get_coords(origen_txt)
    destino = get_coords(destino_txt)

    if not origen or not destino:
        print("❌ No se pudo obtener coordenadas para alguna de las ciudades.")
        continue

    url = f"https://api.openrouteservice.org/v2/directions/{medio}/geojson"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [list(origen), list(destino)]
    }

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    try:
        summary = data['features'][0]['properties']['summary']
        distancia_km = summary['distance'] / 1000
        duracion_min = summary['duration'] / 60
        print(f"✅ Distancia: {distancia_km:.2f} km")
        print(f"⏱️ Duración estimada: {duracion_min:.2f} minutos")

        print("\n🧭 Instrucciones:")
        for step in data['features'][0]['properties']['segments'][0]['steps']:
            print(f"- {step['instruction']} ({step['distance']:.0f} m)")
    except Exception as e:
        print("❌ No se pudo calcular la ruta. Verifica los datos.")
        print("Detalle técnico:", e)

    time.sleep(1)
