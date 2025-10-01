import pyrebase
import streamlit as st


class Database:
    def __init__(self):
        db_url = st.secrets["firebase"]["db_url"]
        email = st.secrets["firebase"]["email"]
        password = st.secrets["firebase"]["password"]
        apikey = st.secrets["firebase"]["apikey"]

        config = {
            "apiKey": apikey,
            "authDomain": db_url.replace("https://", ""),
            "databaseURL": db_url,
            "storageBucket": ""
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        self.db = firebase.database()
        self.user = auth.refresh(user["refreshToken"])

    def read(self, key):
        return self.db.child(key).get(self.user["idToken"]).val()

    def write(self, key, value):
        self.db.child(key).set(value, self.user["idToken"])
