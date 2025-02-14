import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("📊 Prédiction du cours des actions de Google sur 5 jours")

period = {
    "1y": "1 Year",
    "2y": "2 Years",
    "5y": "5 Years",
    "max": "Maximum",
    "1d": "1 Day",
    "1wk": "1 Week",
    "5d": "5 Days",
    "1mo": "1 Month",
    "3mo": "3 Months",
    "6mo": "6 Months",
}
per = st.pills("🕰️ Période de visualisation des données ⏪", options=list(period.keys()), default=list(period.keys())[5] , format_func= lambda k: period.get(k) )

import yfinance as yf
ticker = yf.Ticker("GOOG")

df = ticker.history(period=per, interval ="1d").reset_index()
periode_map = {
    "1 Jour": 1,
    "2 Jours": 2,
    "3 Jours": 3,
    "4 Jours": 4,
    "5 Jours": 5,
    "6 Jours": 6,
    "7 Jours": 7
}
periodes = list(periode_map.keys())
periode = st.pills("Période de prédiction", options=periodes, default=periodes[4])

# Affichage dans Streamlit

#st.write("Voici la prédiction des cours des actions pour les 5 prochains jours.")

# Afficher le tableau des données
st.write(df)




# Afficher le graphique dans Streamlit
# Créer le graphique en chandeliers avec Plotly
# Créer le graphique en chandeliers avec Plotly
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name = "Actuel"
)])

targets = ["Open","High","Low","Close"]

import torch
from chronos import ChronosPipeline
df = df.set_index("Date")
df_predict = pd.DataFrame()
for target in targets :

    pipeline = ChronosPipeline.from_pretrained(
        "amazon/chronos-t5-mini",
        #device_map="cuda",
        torch_dtype=torch.bfloat16,
        
        )
    
    context = torch.tensor(df[target])
    
    prediction_length = periode_map.get(periode)
    forecast = pipeline.predict(context, prediction_length,1,temperature=0.3)  # shape [num_series, num_samples, prediction_length]
    forecast = forecast[0].numpy().reshape(-1)
    
    future_df = pd.DataFrame({target: forecast , "Date" :pd.date_range(start=df.index[-1],periods=len(forecast),freq="D")} )
    if (df_predict.empty):
        df_predict = future_df
    else :
        df_predict[target] = future_df[target]
    



fig.add_trace(go.Candlestick(
    x=df_predict['Date'],
    open=df_predict['Open'],
    high=df_predict['High'],
    low=df_predict['Low'],
    close=df_predict['Close'],
    name = "Prédictions"

))

# Ajouter des titres et labels
fig.update_layout(title="Graphique en Chandeliers Prédiction sur 5 jours",
                  xaxis_title="Date",
                  yaxis_title="Prix (en dollars)",
                  xaxis_rangeslider_visible=False )

color_hi_fill = 'rgba(0, 128, 0, 1)'
color_hi_line = 'rgba(0, 128, 0, 1)'

color_lo_fill = 'rgba(255, 0, 0, 1)'
color_lo_line = 'rgba(255, 0, 0, 1)'

fig.data[0].increasing.fillcolor = color_hi_fill
fig.data[0].increasing.line.color = color_hi_line
fig.data[0].decreasing.fillcolor = color_lo_fill
fig.data[0].decreasing.line.color = color_lo_line

st.plotly_chart(fig)

st.write(df_predict)