import random
import streamlit as st
import logic_utils

st.set_page_config(page_title="AI Guesser", page_icon="🤖")

st.title("🤖 The Persona Guesser")

# --- Sidebar ---
st.sidebar.header("Game Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
persona = st.sidebar.selectbox(
    "Choose AI Personality", 
    ["Grumpy Math Teacher", "Hyperactive Robot", "Mystic Fortune Teller", "Passive-Aggressive Butler"]
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = logic_utils.get_range_for_difficulty(difficulty)

# --- Session State ---
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_feedback = ""

# --- Game Interface ---
st.info(f"Target: {low}-{high} | Attempts: {st.session_state.attempts}/{attempt_limit}")

raw_guess = st.text_input("What is your guess?", key="input")

col1, col2 = st.columns(2)

if col1.button("Submit Guess 🚀") and st.session_state.status == "playing":
    ok, guess_int, err = logic_utils.parse_guess(raw_guess)
    
    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)
        
        # Win/Loss Check
        if guess_int == st.session_state.secret:
            outcome = "Win"
            st.session_state.status = "won"
        else:
            outcome = "Too High" if guess_int > st.session_state.secret else "Too Low"
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
        
        # AI Feedback Call
        with st.spinner(f"The {persona} is responding..."):
            feedback = logic_utils.get_ai_feedback(
                guess_int, st.session_state.secret, low, high, st.session_state.history, persona
            )
            with st.spinner(f"The {persona} is responding..."):
                # Calculate Certainty Score
                cert_value = logic_utils.calculate_certainty(
                    guess_int, st.session_state.secret, low, high
                )
                st.session_state.certainty = cert_value
                st.session_state.last_feedback = feedback

        st.session_state.score = logic_utils.update_score(st.session_state.score, outcome, st.session_state.attempts)

if col2.button("New Game 🔁"):
    for key in ["secret", "attempts", "score", "status", "history", "last_feedback"]:
        if key in st.session_state: del st.session_state[key]
    st.rerun()

# --- Feedback Area ---
if st.session_state.last_feedback:
    with st.chat_message("assistant"):
        st.write(f"**{persona} says:**")
        st.write(st.session_state.last_feedback)
        
        # Adding the visual Certainty Score
        cols = st.columns([1, 4])
        with cols[0]:
            st.metric("Certainty", f"{int(st.session_state.certainty * 100)}%")
        with cols[1]:
            # Visual progress bar for a 'loading' or 'scanning' feel
            st.progress(st.session_state.certainty)

if st.session_state.status == "won":
    st.balloons()
    st.success(f"You got it! Final Score: {st.session_state.score}")
elif st.session_state.status == "lost":
    st.error(f"Game Over. The secret was {st.session_state.secret}.")