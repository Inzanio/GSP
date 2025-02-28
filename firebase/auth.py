import firebase_admin.auth
import streamlit as st

firebase_config = {
    "apiKey": "AIzaSyBaeLzmGO5sPdjblUMOKW4xydOF_8pDmgA",
    "authDomain": "prediction-84f71.firebaseapp.com",
    "databaseURL": "https://prediction-google.firebaseio.com",
    "projectId": "prediction-84f71",
    "storageBucket": "prediction-84f71.firebasestorage.app",
    "messagingSenderId": "243437994671",
    "appId": "1:243437994671:web:b515ff422c11bd953aca5a"
}
service_account_json  = {
  "type": "service_account",
  "project_id": "prediction-84f71",
  "private_key_id":  st.secrets["private_key_id"],
  "private_key": st.secrets["private_key"],
  "client_email": st.secrets["client_email"],
  "client_id": st.secrets["client_id"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url":st.secrets["client_x509_cert_url"] ,
  "universe_domain": "googleapis.com"
}

import firebase_admin
from firebase_admin import credentials, auth
# Initialiser Firebase Admin SDK pour Firestore



# Charger la configuration Firebase
if not firebase_admin._apps:
     
    cred = credentials.Certificate(service_account_json)
    firebase_admin.initialize_app(cred)
