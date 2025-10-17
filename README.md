♟️ Chess Analytics Dashboard

Este proyecto presenta un dashboard interactivo en Streamlit que analiza el rendimiento de los 250 mejores jugadores de Chess.com.

🔍 Descripción general

El pipeline combina el uso de la API pública de Chess.com con un breve scrapeo del HTML de las leaderboards oficiales para obtener los nombres y datos de los jugadores top 250.
Posteriormente, se descargan sus partidas de los últimos tres meses, que luego se procesan y transforman para su visualización.

⚙️ Flujo de trabajo

Extracción de datos: combinación de API y web scraping para reunir información actualizada de los jugadores.

Procesamiento: limpieza, normalización y estructuración de los datos de las partidas.

Visualización: construcción del dashboard en Streamlit con una interfaz amigable e interactiva.

📊 Funcionalidades principales

Vista general: métricas agregadas y estadísticas globales de los 250 jugadores.

Detalle por jugador: perfil individual con información de rendimiento, rating, mejores y peores partidas.

Análisis de aperturas: pestaña dedicada al estudio de patrones y frecuencia de aperturas utilizadas.

🧠 Tecnologías utilizadas

Python, Pandas, Requests, BeautifulSoup

Streamlit para el front-end interactivo
