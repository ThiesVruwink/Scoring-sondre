# ⚽ Free Kick Hero: FC Twente vs SC Heerenveen

A Score Hero style **3D** free-kick game. You play **Sondre Ørjasæter** (FC Twente) against **SC Heerenveen**.
Drag from the ball with your mouse or finger, draw the path of your shot, curve it around the wall and beat the keeper.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

You can also open `game/index.html` directly in a browser (no Python needed).

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to https://share.streamlit.io and click **Create app**.
3. Pick your repo, branch `main`, and main file path `app.py`. Click **Deploy**.

## Project layout

```
app.py              Streamlit page: sidebar settings + embeds the game
game/index.html     The game itself (Three.js / WebGL, plain JavaScript)
game/three.min.js   Three.js r149 (MIT licence), included so the app works offline
requirements.txt    Python dependencies
.streamlit/         Theme
```

Streamlit cannot read mouse or touch drags by itself, so the 3D game runs in a WebGL canvas that `app.py` embeds
with `streamlit.components.v1.html` (Three.js is inlined into the page). Settings from the sidebar are injected into the game as `window.GAME_CONFIG`.

## How it plays

- Drag from the ball, release to shoot. The ball follows the line you draw as seen from the camera, then keeps going in the direction you finished.
- A shot straight at goal hits the wall. Bend it around, with enough width to clear the wall and enough curl to come back in.
- A faster flick gives a harder shot. Slow drags give the keeper time to react.
- The keeper predicts from the ball's current direction, so curved shots can fool him.
- The wall grows from 3 to 5 players and the keeper gets quicker through each round.

## Tweaking

Constants at the top of the script in `game/index.html` (camera, wall distance, kit colours, keeper behaviour in
`newAttempt`) are easy to change. The game needs `game/three.min.js` next to `index.html`; make sure both get uploaded.

## Notes

This is an unofficial fan project. It uses team colours only, with no logos or official artwork.
