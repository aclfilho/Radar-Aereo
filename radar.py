import requests
import folium
import pandas as pd
import time


# URL da API
URL = "https://opensky-network.org/api/states/all"

# Requisição para obter os dados
response = requests.get(URL)
data = response.json()

# Extraindo apenas os dados dos voos
voos = data["states"]

# Lista para armazenar os voos dentro do Brasil
voos_brasil = []

# Filtrando voos dentro das coordenadas do Brasil
for voo in voos:
    try:
        icao = voo[0]
        chamada = voo[1]
        latitude = voo[6]
        longitude = voo[5]
        altitude = voo[7]
        velocidade = voo[9]
        
        # Verificando se o voo ta dentro dos limites do país
        if latitude and longitude:
            if -35 <= latitude <= 5 and -74<= longitude <= -32:
                voos_brasil.append([icao, chamada, latitude, longitude, altitude, velocidade])
    
    except Exception as e:
        print(f"Erro ao processar voo: {e}")
        
        
# Criando um dataframe com os voos do Brasil
df_voos = pd.DataFrame(voos_brasil, columns=["ICAO", "Chamada", "Latitude", "Longitude", "Altitude", "Velocidade"])


# Mapa centralizado no Brasil
mapa = folium.Map(location=[-14.235, -51.9253])

# Adicionando os aviões no mapa
for index, row in df_voos.iterrows():
    folium.Marker(
    location=[row["Latitude"], row["Longitude"]],
    popup=f"Voo: {row['Chamada']}<br>Altitude: {row['Altitude']}m<br>Velocidade: {row['Velocidade']} km/h",
    icon=folium.Icon(color="blue", icon="plane", prefix="fa")  # Cor e ícone ajustados
).add_to(mapa)
    
# Salvando o mapa em um arquivo HTML
mapa.save("radar_voos.html")
print("Mapa gerado! Abra 'radar_voos.html' no navegador.")