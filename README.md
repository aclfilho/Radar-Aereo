Radar de Tráfego Aéreo em Tempo Real

Visão Geral

Este projeto é um Radar de Tráfego Aéreo que exibe em um mapa interativo a localização de aeronaves em tempo real sobre o Brasil. Os dados são obtidos por meio da API OpenSky Network e atualizados automaticamente a cada 60 segundos.

Tecnologias Utilizadas

Python - Linguagem principal do projeto

Requests - Para realizar chamadas à API OpenSky Network

Pandas - Para estruturar e organizar os dados

Folium - Para gerar um mapa interativo

Time - Para atualizar os dados periodicamente

Como Funciona

O código acessa a API OpenSky Network e obtém dados sobre voos em tempo real.

Os voos são filtrados para exibir apenas os que estão sobre o Brasil.

Cada avião é representado por um marcador no mapa, mostrando altitude, velocidade e código do voo.

O mapa é atualizado automaticamente a cada 60 segundos, garantindo informações sempre atualizadas.

Instalação e Execução

Passo 1: Instalar as dependências

Certifique-se de ter o Python instalado e execute o seguinte comando para instalar as bibliotecas necessárias:

pip install requests folium pandas

Passo 2: Executar o Script

Execute o arquivo radar.py para iniciar o radar de tráfego aéreo:

python radar.py

Passo 3: Visualizar o Mapa

O mapa será gerado no arquivo radar_voos.html. Para visualizá-lo, abra o arquivo em qualquer navegador.

Exemplo de Saída no Mapa

Cada avião será representado por um marcador vermelho.

Clicando no marcador, será possível ver detalhes como altitude, velocidade e código do voo.

Próximas Melhorias

Filtrar por companhia aérea (exibir apenas voos da LATAM, Azul, Gol, etc.)

Exibir histórico de voos (mapear trajetórias anteriores)

Criar alerta para voos abaixo de certa altitude

Adicionar opção de intervalo personalizado para atualização dos dados

Contribuições

Se você deseja contribuir com melhorias neste projeto, sinta-se à vontade para fazer um fork e enviar um pull request!

Projeto criado para exploração de dados de tráfego aéreo e aprendizado sobre APIs e visualização interativa!

