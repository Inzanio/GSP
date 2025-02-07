import streamlit as st
from ml.companies import companies_tickers,period


st.title("💰See :blue[Google] stocks actions in real times 📊")
#col1 , col2 = st.columns(2)
companie = "Google" #col1.selectbox("Companie",options=list(companies_tickers.keys()))
cols = st.multiselect("Data",["Open","Close","High","Low","Volume","Dividends","Stock Splits"], default="Close")

c = st.container()

per = st.pills("Period", options=list(period.keys()), default=list(period.keys())[0] , format_func= lambda k: period.get(k) )

import yfinance as yf
ticker = yf.Ticker(companies_tickers[companie])
data = ticker.history(period=per).reset_index()

import pandas as pd
c.line_chart(data, x="Date",y=cols)

