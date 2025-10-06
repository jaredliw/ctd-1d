import streamlit as st
from pathlib import Path
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
    .checkout-card {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("SUTD Kopitiam - Checkout", anchor=False)

st.markdown(
        """
        <div style="background-color:#f0f8ff; 
                    border: 0px; 
                    padding: 12px 16px; 
                    border-radius: 8px; 
                    margin-bottom: 16px;">
            <b>💡 Discount Rule:</b><br>
            - Spend <b>$20+</b> → $1 off <br>
            - Spend <b>$30+</b> → $2 off <br>
            - Spend <b>$40+</b> → $3 off
        </div>
        """,
        unsafe_allow_html=True
    )  

cart_items = []
total_items = 0
total_price = 0.0

categories = db.read("categories")
for i, category in enumerate(categories):
    items = db.read(f"items/{i}")
    for item in items:
        if item["id"] in st.session_state.cart and st.session_state.cart[item["id"]] > 0:
            qty = st.session_state.cart[item["id"]]
            subtotal = qty * item["price"]
            cart_items.append((item["name"], category, qty, item["price"], subtotal))
            total_items += qty
            total_price += subtotal

if not cart_items:
    st.info("🛒 Your cart is empty.")
else:
    st.subheader("Order Summary", anchor=False)

    #th
    header_cols = st.columns([1, 3, 2, 1, 1, 1])
    header_cols[0].markdown("**Image**")
    header_cols[1].markdown("**Item**")
    header_cols[2].markdown("**Category**")
    header_cols[3].markdown("**Qty**")
    header_cols[4].markdown("**Price**")
    header_cols[5].markdown("**Subtotal**")


    #td
    for name, category, qty, price, subtotal in cart_items:
        row = st.columns([1, 3, 2, 1, 1, 1])
        img_path = assets_dir / f"{name}.jpg"
        row[0].image(img_path, width=50)
        row[1].write(name)
        row[2].write(category)
        row[3].write(qty)
        row[4].write(f"${price:.2f}")
        row[5].write(f"${subtotal:.2f}")
    
    #discount
    if total_price >= 40:
        discount = 3
    elif total_price >= 30:
        discount = 2
    elif total_price >= 20:
        discount = 1
    else:
        discount = 0

    final_price = max(total_price - discount, 0)

    st.markdown("---")
    st.write(f"**Total Items:** {total_items}")
    st.write(f"**Total Price:** ${total_price:.2f}")
    st.write(f"**Discount Applied:** ${discount:.2f}")
    st.write(f"**Final Price:** ${final_price:.2f}")

#buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Back to Menu"):
        st.switch_page("app.py")

with col2:
    checkout_clicked = st.button("Checkout")

if checkout_clicked:
    if total_price == 0:
        st.markdown(
            """
            <div style="
                background-color:#fff3cd;
                color:#664d03;
                padding:10px 16px;
                border:1px solid #ffeeba;
                border-radius:6px;
                width:450px;
                margin-top:10px;
            ">
            ⚠️ Your cart is empty. Please add items before checkout.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.session_state.cart = {}
        st.markdown(
            """
            <div style="
                background-color:#d4edda;
                color:#155724;
                padding:10px 16px;
                border:1px solid #c3e6cb;
                border-radius:6px;
                width:400px;
                margin-top:10px;
            ">
            Checkout successful!
            </div>
            """,
            unsafe_allow_html=True
        )

# st.write(st.session_state.cart)

# if st.button("Back to Memu", key="back_to_menu"):
#     st.switch_page("app.py")
# if st.button("Checkout", key="checkout"):
#     st.toast("Checkout successful!")
#     st.session_state.cart = {}
