import streamlit as st
from .auth import service_account_json
from google.cloud import firestore


# {
#   "type": "service_account",
#   "project_id": "prediction-84f71",
#   "private_key_id": "",
#   "private_key": "",
#   "client_email": "",
#   "client_id": "",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "",
#   "universe_domain": "googleapis.com"
# }


db = firestore.Client.from_service_account_info(service_account_json)

@st.cache_data
def get_all_data(db_name):
  
    doc_ref = db.collection(db_name)
    # Then get the data at that reference.
    return [doc.to_dict() for doc in doc_ref.get()]