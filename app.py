import streamlit as st
import random
import torch
import torch.nn as nn

# 1. Page Setup
st.set_page_config(page_title="Play Against AI Blackjack", page_icon="🃏")
st.title("🃏 Play Blackjack Against a Neural Network")

# 2. A Simple Neural Network Architecture for the AI
class BlackjackNN(nn.Module):
    def __init__(self):
        super(BlackjackNN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 2) # Outputs 2 values: [Stay Confidence, Hit Confidence]
        )
    def forward(self, x):
        return self.fc(x)

# Initialize the model with random weights (it will make chaotic/random choices for now!)
@st.cache_resource
def load_model():
    return BlackjackNN()

ai_model = load_model()

# 3. Game Logic Helper Functions
def deal_card():
    card = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])
    return card

def calculate_score(hand):
    score = sum(hand)
    # Handle Aces (11 changing to 1 if busting)
    while score > 21 and 11 in hand:
        hand[hand.index(11)] = 1
        score = sum(hand)
    return score

def has_usable_ace(hand):
    return 1 if (11 in hand and sum(hand) <= 21) else 0

# 4. Initialize Game State Memory
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.player_hand = []
    st.session_state.ai_hand = []
    st.session_state.dealer_hand = []
    st.session_state.player_done = False
    st.session_state.ai_done = False

# 5. Start Game Button
if st.button("Deal New Hand", type="primary") or not st.session_state.game_started:
    st.session_state.player_hand = [deal_card(), deal_card()]
    st.session_state.ai_hand = [deal_card(), deal_card()]
    st.session_state.dealer_hand = [deal_card(), deal_card()]
    st.session_state.player_done = False
    st.session_state.ai_done = False
    st.session_state.game_started = True

# 6. Display the Table
st.write("---")
st.write(f"**Dealer's Face-Up Card:** {st.session_state.dealer_hand[0]}")
st.write(f"🤖 **AI Hand:** {st.session_state.ai_hand} (Total: {calculate_score(st.session_state.ai_hand)})")
st.write(f"🧑‍💻 **Your Hand:** {st.session_state.player_hand} (Total: {calculate_score(st.session_state.player_hand)})")
st.write("---")

player_score = calculate_score(st.session_state.player_hand)
ai_score = calculate_score(st.session_state.ai_hand)
dealer_score = calculate_score(st.session_state.dealer_hand)

# 7. Game Rounds
if player_score < 21 and not st.session_state.player_done:
    # Player's Turn Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hit 🟢"):
            st.session_state.player_hand.append(deal_card())
            st.rerun()
    with col2:
        if st.button("Stand 🔴"):
            st.session_state.player_done = True
            st.rerun()
else:
    st.session_state.player_done = True

# AI's Turn (Runs automatically once you stand or bust)
if st.session_state.player_done and not st.session_state.ai_done:
    if ai_score < 21:
        # Prepare inputs for Neural Network: [AI Score, Dealer Visible Card, Usable Ace]
        inputs = torch.tensor([float(ai_score), float(st.session_state.dealer_hand[0]), float(has_usable_ace(st.session_state.ai_hand))])
        
        # Neural Network makes the choice!
        with torch.no_grad():
            outputs = ai_model(inputs)
            action = torch.argmax(outputs).item() # 0 = Stand, 1 = Hit
            
        if action == 1:
            st.info("🤖 AI decides to HIT!")
            st.session_state.ai_hand.append(deal_card())
            st.rerun()
        else:
            st.info("🤖 AI decides to STAND.")
            st.session_state.ai_done = True
    else:
        st.session_state.ai_done = True

# 8. Final Results
if st.session_state.player_done and st.session_state.ai_done:
    # Dealer plays out their hand (Must hit until 17)
    while calculate_score(st.session_state.dealer_hand) < 17:
        st.session_state.dealer_hand.append(deal_card())
    dealer_score = calculate_score(st.session_state.dealer_hand)
    
    st.write(f"**Final Dealer Hand:** {st.session_state.dealer_hand} (Total: {dealer_score})")
    
    # Determine Winner for Player
    if player_score > 21:
        st.error("You Busted! ❌")
    elif dealer_score > 21 or player_score > dealer_score:
        st.success("You Win! 🎉")
    elif player_score < dealer_score:
        st.error("Dealer Wins against you! ❌")
    else:
        st.warning("You Tied with the Dealer! 🪙")
        
    # Determine Winner for AI
    if ai_score > 21:
        st.error("🤖 AI Busted!")
    elif dealer_score > 21 or ai_score > dealer_score:
        st.success("🤖 AI Wins!")
    elif ai_score < dealer_score:
        st.error("🤖 AI Lost to Dealer!")
    else:
        st.warning("🤖 AI Tied with the Dealer!")