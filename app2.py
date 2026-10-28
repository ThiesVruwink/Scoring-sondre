"""Free Kick Hero - FC Twente vs SC Heerenveen.

A Score Hero style 3D free-kick game. Drag from the ball and draw the path you want
the shot to take. Curve it around the wall and past the keeper.

Streamlit cannot read mouse/touch drags by itself, so the 3D game (Three.js, WebGL)
lives in game/index.html and this app embeds it. Python handles the page, the
settings sidebar and passes the settings into the game.

Run locally:   streamlit run app.py
"""
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

GAME_DIR = Path(__file__).parent / "game"
GAME_FILE = GAME_DIR / "index.html"
THREE_FILE = GAME_DIR / "three.min.js"

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
    html = GAME_FILE.read_text(encoding="utf-8")
    # The game runs inside an iframe, so Three.js is inlined instead of loaded from a file.
    three = THREE_FILE.read_text(encoding="utf-8")
    return html.replace('<script src="three.min.js"></script>', f"<script>{three}</script>")


html = load_game_html().replace(
    "/*__GAME_CONFIG__*/",
    f"window.GAME_CONFIG = {json.dumps(config)};",
)

# The game fills the iframe and adapts its camera to the width and height.
components.html(html, height=780, scrolling=False)

with st.expander("How to play"):
    st.markdown(
        """
        - **Drag from the ball** and draw the path you want the shot to follow, then let go.
        - **Curve it around the wall.** A shot straight at goal hits the wall, so bend it out and back in.
        - **Where you finish matters.** Draw past the goal, high or wide, and the ball keeps going that way.
        - **Flick fast for a harder shot.** Slow drags give the keeper time to react.
        - The keeper reads the ball's current direction, so late curves can fool him.
        - Score as many goals as you can from each round.
        """
    )
