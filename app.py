"""Free Kick Hero - FC Twente vs SC Heerenveen.

A Score Hero style free-kick game. Drag from the ball and draw the path you want
the shot to take. Curve it around the wall and past the keeper.

Streamlit cannot read mouse/touch drags by itself, so the game loop runs in an
HTML5 canvas (game/index.html) that this app embeds. Python handles the page,
the settings sidebar and passes the settings into the game.

Run locally:   streamlit run app.py
"""
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

GAME_FILE = Path(__file__).parent / "game" / "index.html"

st.set_page_config(
    page_title="Free Kick Hero | FC Twente vs SC Heerenveen",
    page_icon="⚽",
    layout="centered",
)

st.markdown(
    """
    <style>
      .block-container { padding-top: 1.2rem; padding-bottom: 0.5rem; max-width: 560px; }
      header[data-testid="stHeader"] { background: transparent; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.header("Settings")
    shots = st.slider("Free kicks per round", min_value=3, max_value=10, value=5)
    keeper_skill = st.slider(
        "Goalkeeper skill", min_value=1, max_value=5, value=3,
        help="1 = easy, 5 = hard. A better keeper reacts faster and moves quicker.",
    )
    st.caption("Changing a setting restarts the game.")

# ---------------------------------------------------------------- page
st.title("⚽ Free Kick Hero")
st.caption("FC Twente vs SC Heerenveen · You are Sondre Ørjasæter")

config = {
    "shots": shots,
    "keeperSkill": keeper_skill,
    "playerName": "Ørjasæter",
    "homeTeam": "FC TWENTE",
    "awayTeam": "SC HEERENVEEN",
}


@st.cache_data
def load_game_html() -> str:
    return GAME_FILE.read_text(encoding="utf-8")


html = load_game_html().replace(
    "/*__GAME_CONFIG__*/",
    f"window.GAME_CONFIG = {json.dumps(config)};",
)

# The game scales itself to fit the iframe (480x800 aspect ratio).
components.html(html, height=800, scrolling=False)

with st.expander("How to play"):
    st.markdown(
        """
        - **Drag from the ball** and draw the path you want the shot to follow, then let go.
        - **Curve it around the wall** - the ball keeps going in the direction you finished.
        - **Flick fast for a harder shot.** Slow drags give the keeper time to react.
        - The keeper reads the ball's current direction, so late curves can fool him.
        - Score as many goals as you can from each round.
        """
    )
