import requests
import folium
import pandas as pd
import time

# URL da API
URL = "https://opensky-network.org/api/states/all"

# 🔹 Definir filtros (Altere conforme necessário)
FILTRO_COMPANHIA = []  # Lista de companhias aéreas desejadas (ou deixe vazia para todas)
ALTITUDE_MINIMA = 1  # Exibir apenas aviões acima de 5000 metros
VELOCIDADE_MINIMA = 1  # Exibir apenas aviões acima de 200 km/h


def obter_voos_brasil():
    """Obtém os voos em tempo real sobre o Brasil, aplicando filtros."""
    
    response = requests.get(URL)
    data = response.json()
    voos = data["states"]
    voos_brasil = []

    # Filtrando voos dentro das coordenadas do Brasil
    for voo in voos:
        try:
            icao = voo[0]
            chamada = voo[1] or ""  # Se o nome estiver vazio, evita erro
            latitude = voo[6]
            longitude = voo[5]
            altitude = voo[7]
            velocidade = voo[9]
            
            # Verificando se o voo está dentro dos limites do Brasil
            if latitude and longitude:
                if -35 <= latitude <= 5 and -74 <= longitude <= -32:
                    # Aplicando os filtros
                    if (not FILTRO_COMPANHIA or any(comp in chamada for comp in FILTRO_COMPANHIA)) and \
                       (altitude >= ALTITUDE_MINIMA) and (velocidade >= VELOCIDADE_MINIMA):
                        voos_brasil.append([icao, chamada, latitude, longitude, altitude, velocidade])
        
        except Exception as e:
            print(f"Erro ao processar voo: {e}")

    return pd.DataFrame(voos_brasil, columns=["ICAO", "Chamada", "Latitude", "Longitude", "Altitude", "Velocidade"])


def gerar_mapa():
    """Gera um mapa atualizado com os voos filtrados."""
    df_voos = obter_voos_brasil()
    
    # Criando o mapa centralizado no Brasil
    mapa = folium.Map(location=[-14.235, -51.9253], zoom_start=4)

    # Adicionando os aviões no mapa
    for _, row in df_voos.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"Voo: {row['Chamada']}<br>Altitude: {row['Altitude']}m<br>Velocidade: {row['Velocidade']} km/h",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")  # Ícone e cor ajustados
        ).add_to(mapa)

    # Salvando o mapa atualizado
    mapa.save("radar_voos_filtrado.html")
    print("Mapa atualizado! Abra 'radar_voos_filtrado.html' no navegador.")


# Loop de atualização automática
intervalo = 60  # Tempo em segundos para atualizar

while True:
    gerar_mapa()
    time.sleep(intervalo)  # Aguarda o intervalo antes de atualizar novamente
