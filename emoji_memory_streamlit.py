import streamlit as st
import random
import time

# Initialize session state variables
if 'emojis' not in st.session_state:
    EMOJIS = ['🍎', '🍌', '🍇', '🍉', '🍒', '🍍', '🥝', '🍑']
    EMOJIS *= 2
    random.shuffle(EMOJIS)
    st.session_state.emojis = EMOJIS
    st.session_state.revealed = [False] * len(EMOJIS)
    st.session_state.first_click = None
    st.session_state.matched = [False] * len(EMOJIS)
    st.session_state.moves = 0

GRID_SIZE = 4
HIDDEN = '❓'

st.title("🧠 Emoji Memory Match")

def reset_game():
    EMOJIS = ['🍎', '🍌', '🍇', '🍉', '🍒', '🍍', '🥝', '🍑']
    EMOJIS *= 2
    random.shuffle(EMOJIS)
    st.session_state.emojis = EMOJIS
    st.session_state.revealed = [False] * len(EMOJIS)
    st.session_state.first_click = None
    st.session_state.matched = [False] * len(EMOJIS)
    st.session_state.moves = 0

def check_win():
    return all(st.session_state.matched)

def handle_click(index):
    if st.session_state.revealed[index] or st.session_state.matched[index]:
        return

    st.session_state.revealed[index] = True

    if st.session_state.first_click is None:
        st.session_state.first_click = index
    else:
        second_click = index
        first_click = st.session_state.first_click
        st.session_state.moves += 1
        if st.session_state.emojis[first_click] == st.session_state.emojis[second_click]:
            st.session_state.matched[first_click] = True
            st.session_state.matched[second_click] = True
        else:
            time.sleep(1)
            st.session_state.revealed[first_click] = False
            st.session_state.revealed[second_click] = False
        st.session_state.first_click = None

# Display the grid
for i in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for j in range(GRID_SIZE):
        idx = i * GRID_SIZE + j
        if st.session_state.revealed[idx] or st.session_state.matched[idx]:
            cols[j].button(st.session_state.emojis[idx], key=idx)
        else:
            if cols[j].button(HIDDEN, key=idx):
                handle_click(idx)

st.write(f"Moves: {st.session_state.moves}")

if check_win():
    st.success("🎉 You won the game!")
    if st.button("🔄 Play Again"):
        reset_game()
