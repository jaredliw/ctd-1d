from pathlib import Path

import streamlit as st

from utils import Database

db = Database()
assets_dir = Path("./assets")

if "cart" not in st.session_state or not isinstance(st.session_state.cart, dict):
    st.session_state.cart = {}
st.set_page_config(page_title="SUTD Kopitiam", page_icon="☕", layout="wide")

st.title("SUTD Kopitiam - Checkout", anchor=False)

st.warning("""**Discount Rule**
- Spend **\$20+** -> $1 off
- Spend **\$30+** -> $2 off
- Spend **\$40+** -> $3 off
""", icon="💡")

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

    # th
    header_cols = st.columns([1, 3, 2, 1, 1, 1])
    header_cols[0].markdown("**Image**")
    header_cols[1].markdown("**Item**")
    header_cols[2].markdown("**Category**")
    header_cols[3].markdown("**Qty**")
    header_cols[4].markdown("**Price**")
    header_cols[5].markdown("**Subtotal**")

    # td
    for name, category, qty, price, subtotal in cart_items:
        row = st.columns([1, 3, 2, 1, 1, 1])
        img_path = assets_dir / f"{name}.jpg"
        row[0].image(img_path, width=50)
        row[1].write(name)
        row[2].write(category)
        row[3].write(qty)
        row[4].write(f"${price:.2f}")
        row[5].write(f"${subtotal:.2f}")

    # Discount
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

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Back to Menu"):
        st.switch_page("☕_Menu.py")

with col2:
    checkout_clicked = st.button("Checkout")

if checkout_clicked:
    if total_price == 0:
        st.error("Your cart is empty. Please add items before checkout.", icon="⚠️")
    else:
        st.session_state.cart = {}
        st.success("Checkout successful! Please proceed to the menu for the next transaction.", icon="✅")
