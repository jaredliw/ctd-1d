import streamlit as st

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

st.title("SUTD Kopitiam - Checkout", anchor=False)
st.write(st.session_state.cart)

if st.button("Back to Memu", key="back_to_menu"):
    st.switch_page("app.py")
if st.button("Checkout", key="checkout"):
    st.toast("Checkout successful!")
    st.session_state.cart = {}
