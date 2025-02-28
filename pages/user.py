import streamlit as st
from firebase.firestore import db
from firebase.auth import auth
import pandas as pd

ROLE = [None,"ADMIN"]

st.title("Gestion des utilisateurs")

# Sidebar pour la navigation
st.sidebar.title("Gestion des utilisateurs")
option = st.sidebar.radio("Choisissez une fonctionnalité", ("Gérer les utilisateurs existants", "Ajouter un utilisateur" ))

# Fonction pour ajouter un utilisateur
def add_user(email, name, password,role = None):
    
    user = auth.create_user(email=email, password=password,display_name=name)        
    # Ajouter l'utilisateur dans Firestore
    db.collection("users").document(user.uid).set({"name": name, "role": role})

    st.success(f"Utilisateur {name} ajouté avec succès! ✅")

# Fonction pour récupérer un utilisateur par email
def get_user(email):
    user = auth.get_user_by_email(email)
    # Si l'email est 'email@gmail.com' et le mot de passe est 'carnel', rediriger vers user.py
    user_ref = db.collection("users").document(user.uid)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        return user_doc.to_dict()
    else:
        st.error(f"Aucun utilisateur trouvé pour l'email {email}. ❌")
        return None

def update_user_data(uid,update_data : dict = {}):
    user_ref = db.collection("users").document(uid)
    user_ref.update(update_data)

# Fonction pour supprimer un utilisateur
def delete_user(email):
    user = auth.get_user_by_email(email)
    user_ref = db.collection("users").document(user.uid)
    user_ref.delete()
    auth.delete_user(user.uid)
    
    st.success(f"Utilisateur avec l'email {email} supprimé avec succès! 🗑️")

# Affichage des utilisateurs
def get_users_data():
    # Iterate through all users. This will still retrieve users in batches,
    # buffering no more than 1000 users in memory at a time.
    
    # Récupération des utilisateurs d'authentification Firebase
    firebase_users = auth.list_users().iterate_all()
    firebase_users_data = [{"uid": user.uid, "email": user.email} for user in firebase_users]
    df_auth = pd.DataFrame(firebase_users_data)

    # Récupération des données supplémentaires dans Firestore
    users_ref = db.collection("users")
    users = users_ref.stream()
    firestore_users_data = [{"uid": user.id, **user.to_dict()} for user in users]
    df_firestore = pd.DataFrame(firestore_users_data)

    # Merge des données
    df_merged = pd.merge(df_auth, df_firestore, on="uid")

    # Affichage du DataFrame

    return df_merged
 
    
    
    # for user in auth.list_users().iterate_all():
    #     print('User: ' + user.uid)
        
    # st.subheader("Liste des utilisateurs enregistrés")
    # users_ref = db.collection("users")
    # users = users_ref.stream()

    # user_data = []
    # for user in users:
    #     user_info = user.to_dict()
    #     user_data.append(user_info)

    # if user_data:
    #     st.table(user_data)  # Affiche les utilisateurs sous forme de tableau
    # else:
    #     st.warning("Aucun utilisateur trouvé dans la base de données.")

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

# elif option == "Rechercher un utilisateur":
#     st.markdown("## Rechercher un utilisateur 🔍")
#     with st.form(key="search_user_form"):
#         email_to_search = st.text_input("Email de l'utilisateur à rechercher")
        
#         search_button = st.form_submit_button("Rechercher")
#         if search_button:
#             if email_to_search:
#                 user = get_user(email_to_search)
#                 if user:
#                     st.write("Informations de l'utilisateur : ", user)
#             else:
#                 st.error("Veuillez entrer un email valide. ❌")

# elif option == "Supprimer un utilisateur":
#     st.markdown("## Supprimer un utilisateur 🗑️")
#     with st.form(key="delete_user_form"):
#         email_to_delete = st.text_input("Email de l'utilisateur à supprimer")
        
#         delete_button = st.form_submit_button("Supprimer l'utilisateur")
#         if delete_button:
#             if email_to_delete:
#                 delete_user(email_to_delete)
#             else:
#                 st.error("Veuillez entrer un email valide. ❌")

elif option == "Gérer les utilisateurs existants":
    users_data = get_users_data()
    
    if (not users_data.empty) :
 
        selected_user = st.dataframe(users_data, on_select="rerun",selection_mode="single-row")

        if len(selected_user["selection"]["rows"]) >0 :
            
            user = users_data.loc[selected_user["selection"]["rows"][0]].to_dict()
            st.text_input("Email:",value=user["email"],disabled=True)
            col1,col2 = st.columns(2)
            user_name = col1.text_input("Nom complet", value=user["name"])
            user_role = col2.selectbox("Role",options=ROLE, index=ROLE.index(user["role"]))
            
            if (col1.button("Modifier")):
                update_user_data(user["uid"],update_data = {"name":user_name, "role": user_role})
            if (col2.button("Supprimer")):
                delete_user(user["email"])
                
            
    else :
        st.warning("Aucun utilisateur Trouvé")