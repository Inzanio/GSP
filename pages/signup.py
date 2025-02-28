import streamlit as st

import re
from firebase.firestore import db
from firebase.auth import auth

# Fonction de validation d'email
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

st.title("Créer un compte")
st.markdown("""
**Bienvenue !**  
Créez un compte pour accéder à des contenu particulier de notre plateforme. Veuillez remplir les informations ci-dessous.
""")

# Utilisation de colonnes pour une disposition plus claire
col1, col2 = st.columns([3, 1])

with col1:
    name = st.text_input("Nom complet", placeholder="Entrez votre nom complet")
    email = st.text_input("Email", placeholder="Entrez votre adresse email")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
    confirm_password = st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••")

with col2:
    st.image("https://www.example.com/path_to_image.jpg", width=150)  # Vous pouvez remplacer par un logo ou une image

# Bouton d'inscription
if st.button("S'inscrire", key="signup_button"):
    if not is_valid_email(email):
        st.error("❌ Adresse email invalide. Veuillez entrer une adresse valide 📧")
    elif len(password) < 6:
        st.error("❌ Le mot de passe doit contenir au moins 6 caractères 🔑")
    elif password != confirm_password:
        st.error("❌ Les mots de passe ne correspondent pas. Veuillez les vérifier 🔄")
    else:
        try:
            # Création de l'utilisateur dans Firebase Auth
            # (
                # email='user@example.com',
                # email_verified=False,
                # phone_number='+15555550100',
                # password='secretPassword',
                # display_name='John Doe',
                # photo_url='http://www.example.com/12345678/photo.png',
                    # disabled=False)
            user = auth.create_user(email=email, password=password,display_name=name)
            
            # Ajouter l'utilisateur dans Firestore
            db.collection("users").document(user.uid).set({"name": name, "role": None})

            # Succès de l'inscription
            st.success(f"✅ Compte créé avec succès, {name} ! Vous pouvez maintenant vous connecter.")
            #st.balloons()  # Effet de ballons pour célébrer la création du compte
            st.switch_page('pages/login.py')  # Optionnel : Recharger la page ou rediriger vers la page de connexion

        except Exception as e:
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                st.error("❌ Cet email est déjà utilisé. Veuillez vous connecter. 🔄")
                st.page_link("pages/login.py") # Redirige vers la page de connexion
            else:
                st.error(f"❌ Erreur lors de l'inscription : {e}")

# Option pour rediriger vers la page de connexion

st.divider()

st.container(border=True).page_link(page="pages/login.py",label="Déjà inscrit ? Connectez-vous !")


