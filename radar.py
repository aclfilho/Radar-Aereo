import requests
import folium
import pandas as pd
import time

# URL da API OpenSky Network
URL = "https://opensky-network.org/api/states/all"

# 🔹 Definir filtros
FILTRO_COMPANHIA = []  # Deixe vazio [] para mostrar todas as companhias
ALTITUDE_MINIMA = 5000  # Exibir apenas aviões acima de 5000 metros
VELOCIDADE_MINIMA = 200  # Exibir apenas aviões acima de 200 km/h

def obter_voos_brasil():
    """Obtém os voos em tempo real sobre o Brasil, aplicando filtros e tratando valores None."""
    
    response = requests.get(URL)
    if response.status_code != 200:
        print("Erro ao acessar a API:", response.status_code)
        return pd.DataFrame()  

    data = response.json()
    voos = data.get("states", [])  
    voos_brasil = []

    for voo in voos:
        try:
            icao = voo[0] or "N/A"  
            chamada = voo[1] or "Desconhecido"
            latitude = voo[6]
            longitude = voo[5]
            altitude = voo[7] if voo[7] is not None else 0  # Define altitude como 0 se for None
            velocidade = voo[9] if voo[9] is not None else 0  # Define velocidade como 0 se for None

            # Verifica se o voo está dentro do Brasil
            if latitude and longitude:
                if -35 <= latitude <= 5 and -74 <= longitude <= -32:
                    # Aplicando os filtros com segurança
                    if (not FILTRO_COMPANHIA or any(comp in chamada for comp in FILTRO_COMPANHIA)) and \
                       (altitude >= ALTITUDE_MINIMA) and (velocidade >= VELOCIDADE_MINIMA):
                        voos_brasil.append([icao, chamada, latitude, longitude, altitude, velocidade])

        except Exception as e:
            print(f"Erro ao processar voo: {e}")

    print(f"Total de voos capturados no Brasil: {len(voos_brasil)}")
    return pd.DataFrame(voos_brasil, columns=["ICAO", "Chamada", "Latitude", "Longitude", "Altitude", "Velocidade"])

def gerar_mapa():
    """Gera um mapa atualizado com os voos filtrados."""
    df_voos = obter_voos_brasil()

    if df_voos.empty:
        print("Nenhum voo encontrado! Verifique se a API está respondendo corretamente.")
        return

    # Criando o mapa centralizado no Brasil
    mapa = folium.Map(location=[-14.235, -51.9253], zoom_start=4)

    # Adicionando os aviões no mapa
    for _, row in df_voos.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"Voo: {row['Chamada']}<br>Altitude: {row['Altitude']}m<br>Velocidade: {row['Velocidade']} km/h",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")
        ).add_to(mapa)

    # Salvando o mapa atualizado
    mapa.save("radar_voos_filtrado.html")
    print("Mapa atualizado! Abra 'radar_voos_filtrado.html' no navegador.")

# Loop de atualização automática
intervalo = 10  # Tempo em segundos para atualizar

while True:
    gerar_mapa()
    time.sleep(intervalo)
