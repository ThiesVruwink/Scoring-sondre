import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Twente: Hero Moments",
    page_icon="⚽",
    layout="centered"
)

# Custom title and header
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="color: #c90000; margin-bottom: 0;">🔴 FC Twente vs SC Heerenveen 🔵</h1>
        <p style="font-weight: 500; color: #555;">Score! Hero Matchday: Ørjasæter & Weghorst Attack</p>
    </div>
    """,
    unsafe_allow_html=True
)

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 0;
    background-color: #121820;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    user-select: none;
    -webkit-user-select: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: white;
  }
  #game-container {
    position: relative;
    width: 650px;
    height: 780px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    border-radius: 12px;
    overflow: hidden;
    background: #2b7a32;
  }
  canvas {
    display: block;
    cursor: crosshair;
  }
  #hud {
    position: absolute;
    top: 15px;
    left: 15px;
    right: 15px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    z-index: 10;
  }
  .hud-badge {
    background: rgba(18, 24, 32, 0.85);
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 14px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  }
  #scenario-banner {
    position: absolute;
    top: 60px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(201, 0, 0, 0.9);
    padding: 6px 18px;
    border-radius: 15px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    pointer-events: none;
    z-index: 10;
  }
  #status-overlay {
    position: absolute;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(18, 24, 32, 0.9);
    padding: 10px 24px;
    border-radius: 25px;
    font-weight: 700;
    font-size: 16px;
    pointer-events: none;
    border: 1px solid rgba(255,255,255,0.2);
    transition: opacity 0.3s;
    z-index: 10;
  }
  #btn-controls {
    margin-top: 12px;
    display: flex;
    gap: 15px;
  }
  .ctrl-btn {
    background: #c90000;
    color: white;
    border: none;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 3px 6px rgba(0,0,0,0.3);
  }
  .ctrl-btn:hover {
    background: #a50000;
  }
</style>
</head>
<body>

<div id="game-container">
  <div id="hud">
    <div class="hud-badge" id="hud-scenario">Scenario: 1 / 3</div>
    <div class="hud-badge" id="hud-match">FC Twente 1 - 0 Heerenveen</div>
  </div>
  <div id="scenario-banner">Cutback to the Edge</div>
  <canvas id="gameCanvas" width="650" height="780"></canvas>
  <div id="status-overlay">Swipe from the ball to pass or shoot!</div>
</div>

<div id="btn-controls">
  <button class="ctrl-btn" onclick="retryScenario()">Retry Scenario</button>
  <button class="ctrl-btn" onclick="nextScenario()">Next Scenario</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const GOAL = { x1: 245, x2: 405, y: 70 };

// Scenario definitions
const SCENARIOS = [
  {
    title: "1. Flank Cutback & Finish",
    match: "FC Twente 1 - 0 Heerenveen",
    passer: { name: "Ørjasæter (LW)", x: 130, y: 380, targetDist: 40 },
    receiver: { name: "Weghorst (ST)", x: 340, y: 320, isStriker: true },
    defenders: [
      { x: 260, y: 360, r: 16 },
      { x: 350, y: 220, r: 16 }
    ],
    keeper: { x: 325, y: 85, r: 18, origX: 325, minX: 260, maxX: 390, dir: 1, speed: 1.5 },
    phase: 1, // 1: pass from Ørjasæter to Weghorst; 2: shot from Weghorst to Goal
    guideText: "Ørjasæter has beaten the fullback! Curve a pass into Weghorst."
  },
  {
    title: "2. Wing Cross to Towering Target",
    match: "FC Twente 1 - 1 Heerenveen",
    passer: { name: "Ørjasæter (LW)", x: 100, y: 460, targetDist: 45 },
    receiver: { name: "Weghorst (ST)", x: 325, y: 210, isStriker: true },
    defenders: [
      { x: 220, y: 360, r: 16 },
      { x: 325, y: 280, r: 16 },
      { x: 250, y: 190, r: 16 }
    ],
    keeper: { x: 325, y: 85, r: 18, origX: 325, minX: 250, maxX: 400, dir: 1, speed: 2.0 },
    phase: 1,
    guideText: "Cross deep from wide! Bend it around the defensive block."
  },
  {
    title: "3. Quick 1-2 Combination",
    match: "FC Twente 2 - 2 Heerenveen",
    passer: { name: "Weghorst (ST)", x: 325, y: 440, targetDist: 40 },
    receiver: { name: "Ørjasæter (LW)", x: 200, y: 250, isStriker: true },
    defenders: [
      { x: 270, y: 360, r: 16 },
      { x: 380, y: 300, r: 16 },
      { x: 260, y: 170, r: 16 }
    ],
    keeper: { x: 325, y: 85, r: 18, origX: 325, minX: 260, maxX: 390, dir: -1, speed: 2.2 },
    phase: 1,
    guideText: "Weghorst holds off Heerenveen CBs. Lay off into Ørjasæter's run!"
  }
];

let currentIdx = 0;
let scenario = JSON.parse(JSON.stringify(SCENARIOS[currentIdx]));

let ball = { x: scenario.passer.x, y: scenario.passer.y, r: 8, moving: false };
let isDrawing = false;
let currentPath = [];
let ballProgress = 0;
let pathPoints = [];
let gamePaused = true;
let celebrationTimer = 0;

function loadScenario(index) {
  currentIdx = index % SCENARIOS.length;
  scenario = JSON.parse(JSON.stringify(SCENARIOS[currentIdx]));
  scenario.phase = 1;
  ball.x = scenario.passer.x;
  ball.y = scenario.passer.y;
  ball.moving = false;
  currentPath = [];
  pathPoints = [];
  gamePaused = true;

  document.getElementById('hud-scenario').innerText = `Scenario: ${currentIdx + 1} / ${SCENARIOS.length}`;
  document.getElementById('hud-match').innerText = scenario.match;
  document.getElementById('scenario-banner').innerText = scenario.title;
  setStatus(scenario.guideText);
}

function setStatus(msg, color="#fff") {
  const el = document.getElementById('status-overlay');
  el.innerText = msg;
  el.style.color = color;
}

// Input listeners for swipe trajectory
canvas.addEventListener('mousedown', (e) => {
  if (ball.moving) return;
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  const distToBall = Math.hypot(x - ball.x, y - ball.y);
  if (distToBall < 55) {
    isDrawing = true;
    currentPath = [{ x: ball.x, y: ball.y }];
  }
});

canvas.addEventListener('mousemove', (e) => {
  if (!isDrawing) return;
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  const lastPt = currentPath[currentPath.length - 1];
  if (Math.hypot(x - lastPt.x, y - lastPt.y) > 10) {
    currentPath.push({ x, y });
  }
});

window.addEventListener('mouseup', () => {
  if (isDrawing) {
    isDrawing = false;
    if (currentPath.length > 3) {
      launchBallAlongPath();
    } else {
      currentPath = [];
    }
  }
});

function launchBallAlongPath() {
  pathPoints = [];
  for (let i = 0; i < currentPath.length - 1; i++) {
    const p1 = currentPath[i];
    const p2 = currentPath[i + 1];
    const segDist = Math.hypot(p2.x - p1.x, p2.y - p1.y);
    const steps = Math.max(1, Math.floor(segDist / 4));
    for (let s = 0; s < steps; s++) {
      const t = s / steps;
      pathPoints.push({
        x: p1.x + (p2.x - p1.x) * t,
        y: p1.y + (p2.y - p1.y) * t
      });
    }
  }
  pathPoints.push(currentPath[currentPath.length - 1]);
  currentPath = [];
  ballProgress = 0;
  ball.moving = true;
  gamePaused = false;
}

function retryScenario() {
  loadScenario(currentIdx);
}

function nextScenario() {
  loadScenario(currentIdx + 1);
}

// Game Loop
function update() {
  // Animate Goalkeeper
  if (scenario.keeper) {
    const k = scenario.keeper;
    k.x += k.speed * k.dir;
    if (k.x > k.maxX || k.x < k.minX) {
      k.dir *= -1;
    }
  }

  // Animate Ball along drawn curve
  if (ball.moving && pathPoints.length > 0) {
    const stepSpeed = 2; // path advance speed
    ballProgress += stepSpeed;
    if (ballProgress < pathPoints.length) {
      ball.x = pathPoints[ballProgress].x;
      ball.y = pathPoints[ballProgress].y;

      // Check defender tackle
      for (const def of scenario.defenders) {
        if (Math.hypot(ball.x - def.x, ball.y - def.y) < def.r + ball.r) {
          ball.moving = false;
          setStatus("❌ Intercepted by SC Heerenveen! Try a wider curve.", "#ff5555");
          setTimeout(() => resetPhase(), 1200);
          return;
        }
      }

      // Check Goalkeeper save
      const gk = scenario.keeper;
      if (Math.hypot(ball.x - gk.x, ball.y - gk.y) < gk.r + ball.r) {
        ball.moving = false;
        setStatus("🧤 Saved by the Keeper! Aim closer to the corners.", "#ffaa00");
        setTimeout(() => resetPhase(), 1200);
        return;
      }

    } else {
      // Reached trajectory terminus
      ball.moving = false;
      const endPt = pathPoints[pathPoints.length - 1];

      if (scenario.phase === 1) {
        // Did we hit the intended target player?
        const rec = scenario.receiver;
        const d = Math.hypot(endPt.x - rec.x, endPt.y - rec.y);
        if (d < 50) {
          // Pass completed!
          scenario.phase = 2;
          ball.x = rec.x;
          ball.y = rec.y;
          setStatus(`🎯 Great pass! Now shoot past the keeper with ${rec.name}!`, "#00ff7f");
        } else {
          setStatus("⚠️ Pass overhit or misplaced. Retrying touch...", "#ff9999");
          setTimeout(() => resetPhase(), 1000);
        }
      } else if (scenario.phase === 2) {
        // Checking for Goal inside the net bounds
        if (endPt.x >= GOAL.x1 && endPt.x <= GOAL.x2 && endPt.y <= GOAL.y + 15) {
          setStatus("⚽ GOAL FOR FC TWENTE! What a finish!", "#00ff7f");
          celebrationTimer = 70;
        } else {
          setStatus("❌ Off target! The shot missed the net.", "#ff9999");
          setTimeout(() => resetPhase(), 1000);
        }
      }
    }
  }

  if (celebrationTimer > 0) {
    celebrationTimer--;
    if (celebrationTimer === 1) {
      nextScenario();
    }
  }
}

function resetPhase() {
  if (scenario.phase === 1) {
    ball.x = scenario.passer.x;
    ball.y = scenario.passer.y;
    setStatus(scenario.guideText);
  } else {
    ball.x = scenario.receiver.x;
    ball.y = scenario.receiver.y;
    setStatus(`Take the shot with ${scenario.receiver.name}!`, "#00ff7f");
  }
  ball.moving = false;
  currentPath = [];
  pathPoints = [];
}

// Drawing routines
function drawPitch() {
  // Turf base & stripes
  ctx.fillStyle = '#2d8a36';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#297d31';
  for (let i = 0; i < canvas.height; i += 70) {
    if ((i / 70) % 2 === 0) ctx.fillRect(0, i, canvas.width, 35);
  }

  // Pitch Lines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)';
  ctx.lineWidth = 3;

  // Touchlines
  ctx.strokeRect(30, 70, 590, 680);

  // Penalty Box
  ctx.strokeRect(145, 70, 360, 240);

  // 6-yard Box
  ctx.strokeRect(220, 70, 210, 80);

  // Penalty Spot
  ctx.beginPath();
  ctx.arc(325, 230, 4, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
  ctx.fill();

  // Penalty Arc
  ctx.beginPath();
  ctx.arc(325, 230, 80, 0.65, Math.PI - 0.65);
  ctx.stroke();

  // Goal Structure
  ctx.fillStyle = 'rgba(230, 230, 230, 0.3)';
  ctx.fillRect(GOAL.x1, GOAL.y - 45, GOAL.x2 - GOAL.x1, 45);
  ctx.strokeStyle = '#fff';
  ctx.lineWidth = 5;
  ctx.strokeRect(GOAL.x1, GOAL.y - 45, GOAL.x2 - GOAL.x1, 45);
}

function drawPlayer(x, y, name, isTwente=true, isStriker=false) {
  ctx.save();
  ctx.shadowColor = 'rgba(0,0,0,0.4)';
  ctx.shadowBlur = 6;
  ctx.shadowOffsetY = 4;

  // Body / Shirt
  ctx.beginPath();
  ctx.arc(x, y, 15, 0, Math.PI * 2);
  ctx.fillStyle = isTwente ? '#e00000' : '#1e5bb8'; // Red for Twente, Blue/White for Heerenveen
  ctx.fill();

  // Trim
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = isTwente ? '#ffffff' : '#ffffff';
  ctx.stroke();

  ctx.restore();

  // Player Name Tag
  ctx.font = 'bold 12px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillStyle = '#ffffff';
  ctx.shadowColor = 'rgba(0,0,0,0.8)';
  ctx.shadowBlur = 4;
  ctx.fillText(name, x, y + 27);
  ctx.shadowBlur = 0;
}

function drawGoalie(gk) {
  ctx.save();
  ctx.beginPath();
  ctx.arc(gk.x, gk.y, gk.r, 0, Math.PI * 2);
  ctx.fillStyle = '#ffbe00'; // Heerenveen GK jersey
  ctx.fill();
  ctx.lineWidth = 2;
  ctx.strokeStyle = '#222';
  ctx.stroke();

  ctx.font = 'bold 11px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillStyle = '#fff';
  ctx.shadowColor = 'rgba(0,0,0,0.8)';
  ctx.shadowBlur = 4;
  ctx.fillText("GK", gk.x, gk.y + 24);
  ctx.restore();
}

function render() {
  drawPitch();

  // Draw Defending Team (SC Heerenveen)
  scenario.defenders.forEach((def, idx) => {
    drawPlayer(def.x, def.y, `DF ${idx + 1}`, false);
  });
  drawGoalie(scenario.keeper);

  // Draw Attacking Team (FC Twente)
  const isPhase1 = scenario.phase === 1;
  drawPlayer(scenario.passer.x, scenario.passer.y, scenario.passer.name, true);
  drawPlayer(scenario.receiver.x, scenario.receiver.y, scenario.receiver.name, true);

  // Target receiver pulsing ring during pass phase
  if (isPhase1) {
    ctx.save();
    ctx.beginPath();
    ctx.arc(scenario.receiver.x, scenario.receiver.y, 28 + Math.sin(Date.now() / 200) * 4, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.stroke();
    ctx.restore();
  }

  // Draw Target Corners during shooting phase
  if (!isPhase1) {
    ctx.fillStyle = 'rgba(255, 215, 0, 0.4)';
    ctx.beginPath();
    ctx.arc(GOAL.x1 + 25, GOAL.y - 15, 20, 0, Math.PI * 2);
    ctx.arc(GOAL.x2 - 25, GOAL.y - 15, 20, 0, Math.PI * 2);
    ctx.fill();
  }

  // Draw In-Flight / Static Ball
  ctx.save();
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2);
  ctx.fillStyle = '#ffffff';
  ctx.fill();
  ctx.lineWidth = 2;
  ctx.strokeStyle = '#111';
  ctx.stroke();

  // Ball ring indicator if idle
  if (!ball.moving) {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r + 6 + Math.sin(Date.now() / 250) * 3, 0, Math.PI * 2);
    ctx.strokeStyle = '#ffeb3b';
    ctx.lineWidth = 2;
    ctx.stroke();
  }
  ctx.restore();

  // Draw User's Drag Curve (Score! Hero arc)
  if (currentPath.length > 1) {
    ctx.save();
    ctx.strokeStyle = '#ffd700';
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(currentPath[0].x, currentPath[0].y);
    for (let i = 1; i < currentPath.length; i++) {
      ctx.lineTo(currentPath[i].x, currentPath[i].y);
    }
    ctx.stroke();

    // Trajectory head arrow
    const last = currentPath[currentPath.length - 1];
    ctx.beginPath();
    ctx.arc(last.x, last.y, 6, 0, Math.PI * 2);
    ctx.fillStyle = '#ffd700';
    ctx.fill();
    ctx.restore();
  }

  update();
  requestAnimationFrame(render);
}

// Initial boot
loadScenario(0);
requestAnimationFrame(render);
</script>
</body>
</html>
"""

components.html(game_html, height=870, scrolling=False)

st.markdown(
    """
    ### 🎮 How to Play
    * **Click & Drag (Swipe):** Press down near the active ball carrier, draw a curved line to bypass defenders, and release to shoot or pass.
    * **Unlimited Retries:** If Heerenveen blocks the pass or the keeper stops your shot, you can instantly redraw without losing energy.
    * **Attacking Duo:** Build combinations starting with **Sondre Ørjasæter** hugging the touchline and feed **Wout Weghorst** inside the 18-yard box.
    """
)
