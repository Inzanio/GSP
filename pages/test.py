import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Titre de l'application
st.title("Graphique en Bougies (Candlestick) avec Streamlit")

# Exemple de DataFrame (remplacez cela par vos données)
data = {
    'Date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05'],
    'Open': [100, 105, 110, 108, 115],
    'High': [110, 112, 115, 118, 120],
    'Low': [95, 100, 105, 107, 110],
    'Close': [105, 110, 108, 115, 118]
}
df = pd.DataFrame(data)

# Convertir la colonne 'Date' en type datetime
df['Date'] = pd.to_datetime(df['Date'])

# Afficher le DataFrame
st.write("Données utilisées :")
st.dataframe(df)

# Créer le graphique en bougies avec Plotly
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],  # Axe des dates
    open=df['Open'],  # Prix d'ouverture
    high=df['High'],  # Prix le plus haut
    low=df['Low'],  # Prix le plus bas
    close=df['Close']  # Prix de clôture
)])

# Mise en forme du graphique
fig.update_layout(
    title="Graphique en Bougies",
    xaxis_title="Date",
    yaxis_title="Prix",
    xaxis_rangeslider_visible=True  # Ajouter un curseur de plage
)

# Afficher le graphique dans Streamlit
st.plotly_chart(fig)