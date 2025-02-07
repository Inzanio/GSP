import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Google Stock Predictor",
    page_icon="logo.png",
       
)
st.logo("logo.png")


# GROUPE 2
# -Un modele LSTM de prediction des actions GOOGLE, TESLA, MICROSOFT et
# APPLE
# -Un selecteur de période de predictions(de 3 a 12 mois) et une prediction faite par le
# LSTM
# - le nom des 4 entreprises pourra être selectionné au choix comme input pour un
# chatbot intelligent
# - Utilisez un modele de TimeForecasting de HuggingFace pour effectuer des
# predictions temporelles 




#home = st.Page("pages/test.py",title="Home", icon="🏠",default=True)
actions = st.Page("pages/actions.py",title="Action Evolution", icon="📈")

pages = [actions]
# setting up app navigation
app = st.navigation(pages)
app.run()