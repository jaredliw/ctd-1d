from pathlib import Path

import streamlit as st

from utils import Database

db = Database()
assets_dir = Path("./assets")
if "cart" not in st.session_state or not isinstance(st.session_state.cart, dict):
    st.session_state.cart = {}
st.set_page_config(page_title="SUTD Kopitiam", page_icon="☕", layout="wide")
st.markdown("""
    <style>
    .stSidebar {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title("SUTD Kopitiam", anchor=False)
st.image(assets_dir / "cover.jpg")

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
                    st.image(assets_dir / f"{item['name']}.jpg")
                    st.subheader(item["name"], divider="gray", anchor=False)
                    st.write(f"Price: ${item['price']:.2f}")
                    st.write(item["desc"])
                    with st.columns([1, 1])[0]:
                        num = st.number_input("No. of Items", min_value=0, step=1, key=item["id"],
                                              label_visibility="collapsed")
                        st.session_state.cart[item["id"]] = num
                        if num <= 0:
                            del st.session_state.cart[item["id"]]
                j += 1

st.divider()
st.write(f"No. of Items in Cart: {sum(st.session_state.cart.values())}")
if st.button("Go to Checkout"):
    st.switch_page("pages/🛒_Checkout.py")
