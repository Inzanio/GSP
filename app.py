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




#test = st.Page("pages/test.py",title="test", icon="🏠",default=True)
actions = st.Page("pages/actions.py",title="Action Evolution", icon="📈")
predictions = st.Page("pages/prediction.py",title="Predictions", icon="🔮")

login = st.Page("pages/login.py", title="Login", icon="🔐")
signup = st.Page("pages/signup.py", title="Sign Up", icon="🔰")
users =st.Page("pages/user.py", title="Manage Users", icon="🛠️")

special_page = st.Page("pages/special_page.py", title="Special User Content", icon="🌟")

if ("user" not in st.session_state):
    # pas d'utilisateur connecté
    pages = {
        "GSP" : [actions,predictions],
        "Login" : [login,signup]
    }
else : # un utilisateur est connecté
    if ("role" in st.session_state["user"] and st.session_state["user"]["role"] == "ADMIN") :
      pages = {
            "GSP" : [actions,predictions],
            "Login" : [users,special_page]
        } 
    else :
        pages = {
            "GSP" : [actions,predictions],
            "Login" : [special_page]
        } 
# setting up app navigation
app = st.navigation(pages)
app.run()