# 8. Final Results
if st.session_state.player_done and st.session_state.ai_done:
    # Dealer only plays out their hand if AT LEAST one player is still alive
    if player_score <= 21 or ai_score <= 21:
        while calculate_score(st.session_state.dealer_hand) < 17:
            st.session_state.dealer_hand.append(deal_card())
    
    dealer_score = calculate_score(st.session_state.dealer_hand)
    st.write(f"**Final Dealer Hand:** {st.session_state.dealer_hand} (Total: {dealer_score})")
    
    # ---- EVALUATE PLAYER ----
    st.write("### Your Result:")
    if player_score > 21:
        st.error("You Busted! ❌ (Dealer wins automatically)")
    elif dealer_score > 21:
        st.success("Dealer Busted! You Win! 🎉")
    elif player_score > dealer_score:
        st.success("You Win! 🎉")
    elif player_score < dealer_score:
        st.error("Dealer Wins! ❌")
    else:
        st.warning("You Tied with the Dealer! 🪙")
        
    # ---- EVALUATE AI ----
    st.write("### AI Result:")
    if ai_score > 21:
        st.error("🤖 AI Busted! ❌ (Dealer wins automatically)")
    elif dealer_score > 21:
        st.success("🤖 Dealer Busted! AI Wins! 🎉")
    elif ai_score > dealer_score:
        st.success("🤖 AI Wins! 🎉")
    elif ai_score < dealer_score:
        st.error("🤖 AI Lost to Dealer! ❌")
    else:
        st.warning("🤖 AI Tied with the Dealer! 🪙")