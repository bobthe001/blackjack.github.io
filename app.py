import streamlit as st

# 1. Web Page Title & Setup
st.set_page_config(page_title="AI Blackjack Bot", page_icon="🃏")
st.title("🃏 Simple AI Blackjack Advisor")
st.write("Adjust the sliders to match the current game, then ask the AI what to do.")

---

# 2. The User Interface (Sliders for the game state)
player_score = st.slider("Your Current Hand Total", min_value=4, max_value=21, value=12)
dealer_card = st.slider("Dealer's Visible Card (Ace = 11)", min_value=2, max_value=11, value=6)
usable_ace = st.toggle("Do you have a usable Ace?")

---

# 3. The AI "Brain" Placeholder
# (Once you train your neural network, you will replace this logic with your model)
def ask_ai(score, dealer):
    if score < 17:
        return "HIT 🟢"
    else:
        return "STAND 🔴"

# 4. The Action Button
if st.button("Ask the Bot", type="primary"):
    decision = ask_ai(player_score, dealer_card)
    
    # Display the result in a nice box
    st.success(f"The Neural Network advises you to: **{decision}**")
