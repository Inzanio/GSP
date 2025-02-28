import streamlit as st
from firebase.auth import auth
from firebase.firestore import db
import re

# Fonction pour valider l'email
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


st.title("Connexion à votre compte")
st.markdown("""
Bienvenue sur notre plateforme. Veuillez entrer vos informations pour vous connecter.
""")

# Formulaire de connexion
col1, col2 = st.columns([3, 2])

with col1:
    email = st.text_input("Email", placeholder="Entrez votre email", key="email")
    
with col2:
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="password")

if st.button("Se connecter", key="login_button"):
    if not email or not password:
        st.error("Veuillez remplir tous les champs. 🚨")
    elif not is_valid_email(email):
        st.error("Adresse email invalide. 📧")
    else:
        try:
            user = auth.get_user_by_email(email)
            # Si l'email est 'email@gmail.com' et le mot de passe est 'carnel', rediriger vers user.py
            user_ref = db.collection("users").document(user.uid)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                    user_data = user_doc.to_dict()
                    
                    st.session_state["user"] = user_data  # Stocker l'utilisateur en session
                    
                    if ("role" in user_data and user_data["role"]=="ADMIN"):
                        st.success("✅ Connexion réussie ! Bienvenue, administrateur 👋")
                        users =st.Page("pages/user.py", title="Manage Users", icon="🛠️")
                        st.switch_page(users)  # Redirection vers la page "user.py"
                    
                    else :
                        st.success(f"✅ Connexion réussie ! Bienvenue, {user_data['name']} 👋")
                        st.balloons()  # Effet de ballons pour célébrer la connexion
                        special_page = st.Page("pages/special_page.py", title="Special User Content", icon="🌟")
                        st.switch_page(special_page)  # Rediriger vers la page des prédictions
            else:
                st.error("❌ Utilisateur non trouvé.")

        except Exception as e:
            st.error(f"❌ Erreur lors de la connexion : {str(e)}")

# Lien vers l'inscription
st.divider()

st.container(border=True).page_link(page="pages/signup.py",label="Pas de Compte ? Créez en Un !")

# Ajout de visuels et de style
# st.image("https://www.example.com/path_to_image.jpg", width=700)  # Utilisez une image de fond ou un logo ici
