import streamlit as st
import yfinance as yf

st.title("Hello Test !")

ticker = yf.Ticker("GOOG")
data = ticker.history(period="1y")

st.write(data)