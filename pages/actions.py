import streamlit as st
from ml.companies import companies_tickers,period


st.title("💰See :blue[Google] stocks actions in real times 📊")
#col1 , col2 = st.columns(2)
companie = "Google" #col1.selectbox("Companie",options=list(companies_tickers.keys()))
#cols = st.multiselect("Data",["Open","Close","High","Low","Volume","Dividends","Stock Splits"], default="Close")

c = st.container()

per = st.pills("Period", options=list(period.keys()), default=list(period.keys())[0] , format_func= lambda k: period.get(k) )

import yfinance as yf
ticker = yf.Ticker(companies_tickers[companie])
df = ticker.history(period=per).reset_index()



import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Convertir la colonne 'Date' en type datetime
#df['Date'] = pd.to_datetime(df['Date'])

# Afficher le DataFrame
#st.write("Données utilisées :")
#st.dataframe(df)

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
    xaxis_rangeslider_visible=False  # Ajouter un curseur de plage
)

# Afficher le graphique dans Streamlit
c.plotly_chart(fig)
