import streamlit as st
from firebase.firestore import db
from firebase.auth import auth

st.title("Gestion des utilisateurs")

# Sidebar pour la navigation
st.sidebar.title("Gestion des utilisateurs")
option = st.sidebar.radio("Choisissez une fonctionnalité", ("Ajouter un utilisateur", "Rechercher un utilisateur", "Supprimer un utilisateur", "Liste des utilisateurs"))

# Fonction pour ajouter un utilisateur
def add_user(email, name, password):
    user_ref = db.collection("users").document(email)
    user_ref.set({
        "name": name,
        "email": email,
        "password": password
    })
    st.success(f"Utilisateur {name} ajouté avec succès! ✅")

# Fonction pour récupérer un utilisateur par email
def get_user(email):
    user_ref = db.collection("users").document(email)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict()
    else:
        st.error(f"Aucun utilisateur trouvé pour l'email {email}. ❌")
        return None

# Fonction pour supprimer un utilisateur
def delete_user(email):
    user_ref = db.collection("users").document(email)
    user_ref.delete()
    st.success(f"Utilisateur avec l'email {email} supprimé avec succès! 🗑️")

# Affichage des utilisateurs
def display_users():
    st.subheader("Liste des utilisateurs enregistrés")
    users_ref = db.collection("users")
    users = users_ref.stream()

    user_data = []
    for user in users:
        user_info = user.to_dict()
        user_data.append(user_info)

    if user_data:
        st.table(user_data)  # Affiche les utilisateurs sous forme de tableau
    else:
        st.warning("Aucun utilisateur trouvé dans la base de données.")

# Logique pour chaque fonctionnalité en fonction de l'option choisie dans la sidebar

if option == "Ajouter un utilisateur":
    st.markdown("## Ajouter un utilisateur 📝")
    with st.form(key="add_user_form"):
        email = st.text_input("Email de l'utilisateur")
        name = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        submit_button = st.form_submit_button("Ajouter l'utilisateur")
        if submit_button:
            if email and name and password:
                add_user(email, name, password)
            else:
                st.error("Veuillez remplir tous les champs. ❌")

elif option == "Rechercher un utilisateur":
    st.markdown("## Rechercher un utilisateur 🔍")
    with st.form(key="search_user_form"):
        email_to_search = st.text_input("Email de l'utilisateur à rechercher")
        
        search_button = st.form_submit_button("Rechercher")
        if search_button:
            if email_to_search:
                user = get_user(email_to_search)
                if user:
                    st.write("Informations de l'utilisateur : ", user)
            else:
                st.error("Veuillez entrer un email valide. ❌")

elif option == "Supprimer un utilisateur":
    st.markdown("## Supprimer un utilisateur 🗑️")
    with st.form(key="delete_user_form"):
        email_to_delete = st.text_input("Email de l'utilisateur à supprimer")
        
        delete_button = st.form_submit_button("Supprimer l'utilisateur")
        if delete_button:
            if email_to_delete:
                delete_user(email_to_delete)
            else:
                st.error("Veuillez entrer un email valide. ❌")

elif option == "Liste des utilisateurs":
    display_users()
