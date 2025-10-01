import streamlit as st
from utils import Database

db = Database()

st.set_page_config(page_title="SUTD Kopitiam", page_icon="☕", layout="wide")
st.title("SUTD Kopitiam", anchor=False)
st.image("./assets/cover.jpg")

categories = db.read("categories")
tabs = st.tabs(categories)

for i, category in enumerate(categories):
    with tabs[i]:
        st.subheader(category, anchor=False)

        items = db.read(f"items/{i}")  # Get all items in this category

        j = 0
        while j < len(items):
            columns = st.columns([1] * 5)  # 5 equal-width columns
            for col in columns:
                if j >= len(items):
                    break
                item = items[j]

                with col:
                    st.image("./assets/" + item["name"] + ".jpg")
                    st.subheader(item["name"], divider="gray", anchor=False)
                    st.write(f"Price: ${item['price']:.2f}")
                    st.write(item["desc"])
                    with st.columns([1, 1])[0]:
                        st.number_input("", min_value=0, step=1, key=item["name"], label_visibility="collapsed")
                j += 1
