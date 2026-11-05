import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FC Twente Score! Hero 3D - De Grolsch Veste Edition",
    page_icon="⚽",
    layout="centered"
)

st.markdown(
    """
    <style>
      .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 0.8rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
      }
    </style>
    <div style="text-align: center; margin-bottom: 0.35rem;">
        <h2 style="color: #d00000; margin: 0; font-size: 1.45rem; letter-spacing: -0.5px; font-weight: 900;">
            🔴 FC Twente: Score! Hero 3D 🔵
        </h2>
        <p style="font-weight: 600; color: #666; margin-top: 0.1rem; font-size: 0.84rem;">
            Sondre Ørjasæter (11) & Wout Weghorst (9) vs SC Heerenveen • De Grolsch Veste
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<style>
  * {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
  }
  html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    background-color: #080b10;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    user-select: none;
    -webkit-user-select: none;
    overflow-x: hidden;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    touch-action: manipulation;
  }
  #container {
    position: relative;
    width: 100%;
    max-width: 680px;
    aspect-ratio: 1 / 1.08;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 16px 42px rgba(0,0,0,0.9), 0 0 0 1px rgba(255,255,255,0.1);
    background: #05080c;
    touch-action: none;
  }
  #three-canvas {
    display: block;
    width: 100%;
    height: 100%;
  }
  #overlay-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 5;
  }
  #slowmo-vignette {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 4;
    background: radial-gradient(circle at center, transparent 58%, rgba(0, 180, 255, 0.16) 100%);
    box-shadow: inset 0 0 35px rgba(0,0,0,0.75);
    transition: opacity 0.35s ease;
    opacity: 1;
  }
  #broadcast-hud {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    pointer-events: none;
    z-index: 10;
  }
  .score-bug {
    background: linear-gradient(135deg, rgba(16,20,28,0.95), rgba(8,10,15,0.98));
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 7px;
    display: flex;
    align-items: center;
    box-shadow: 0 6px 16px rgba(0,0,0,0.6);
    overflow: hidden;
  }
  .score-team {
    padding: 5px 9px;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 0.4px;
  }
  .score-twente { background: linear-gradient(180deg, #d80000, #9a0000); color: #fff; }
  .score-heerenveen { background: linear-gradient(180deg, #0055b3, #003675); color: #fff; }
  .score-val {
    padding: 5px 10px;
    font-size: 13px;
    font-weight: 900;
    background: #0f131a;
    color: #fff;
    min-width: 44px;
    text-align: center;
  }
  .score-clock {
    padding: 5px 8px;
    font-size: 11px;
    font-weight: 800;
    background: #1c222e;
    color: #00e676;
    border-left: 1px solid rgba(255,255,255,0.12);
  }
  .hud-right {
    display: flex;
    gap: 6px;
    align-items: center;
  }
  .star-box {
    background: rgba(12, 16, 24, 0.92);
    padding: 4px 10px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.18);
    font-size: 13px;
    letter-spacing: 2px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.45);
  }
  .hud-badge {
    background: rgba(15, 20, 28, 0.92);
    padding: 5px 11px;
    border-radius: 14px;
    font-size: 11px;
    font-weight: 800;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 10px rgba(0,0,0,0.45);
    display: flex;
    align-items: center;
    gap: 5px;
  }
  #tactical-banner {
    position: absolute;
    top: 46px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(90deg, rgba(195,0,0,0.95), rgba(135,0,0,0.95));
    border: 1px solid rgba(255,255,255,0.28);
    padding: 4px 14px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    pointer-events: none;
    z-index: 10;
    white-space: nowrap;
    max-width: 92%;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  #objectives-bar {
    position: absolute;
    top: 72px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 6px;
    pointer-events: none;
    z-index: 10;
    flex-wrap: nowrap;
  }
  .obj-pill {
    background: rgba(10, 14, 22, 0.82);
    border: 1px solid rgba(255,255,255,0.16);
    padding: 2px 8px;
    border-radius: 8px;
    font-size: 9.5px;
    font-weight: 700;
    color: #cfd8e3;
    white-space: nowrap;
  }
  .obj-pill.done {
    border-color: #ffd700;
    color: #ffd700;
    background: rgba(40, 34, 10, 0.88);
  }
  #status-bubble {
    position: absolute;
    bottom: 12px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(10, 14, 22, 0.94);
    backdrop-filter: blur(8px);
    padding: 9px 16px;
    border-radius: 18px;
    font-weight: 700;
    font-size: 11.5px;
    pointer-events: none;
    border: 1px solid rgba(255,255,255,0.22);
    box-shadow: 0 8px 22px rgba(0,0,0,0.7);
    z-index: 10;
    text-align: center;
    width: 90%;
    max-width: 540px;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }
  #btn-bar {
    width: 100%;
    max-width: 680px;
    margin-top: 10px;
    display: flex;
    justify-content: center;
    gap: 10px;
    padding-bottom: 10px;
  }
  .action-btn {
    flex: 1;
    max-width: 175px;
    background: linear-gradient(180deg, #cc0000, #990000);
    color: white;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 10px 12px;
    font-size: 12px;
    font-weight: 800;
    border-radius: 9px;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.45);
    touch-action: manipulation;
  }
  .action-btn.secondary {
    background: linear-gradient(180deg, #1f2937, #111827);
  }
  .action-btn:active {
    transform: translateY(1px);
    filter: brightness(1.15);
  }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="container">
  <div id="slowmo-vignette"></div>
  <div id="broadcast-hud">
    <div class="score-bug">
      <div class="score-team score-twente">TWE</div>
      <div class="score-val" id="hud-score">1 - 0</div>
      <div class="score-team score-heerenveen">HEE</div>
      <div class="score-clock" id="hud-clock">34'</div>
    </div>
    <div class="hud-right">
      <div class="star-box" id="hud-stars">☆☆☆</div>
      <div class="hud-badge" id="hud-scenario">
        <span style="color:#00e676;">●</span> 1 / 3
      </div>
    </div>
  </div>
  <div id="tactical-banner">Steekpass & Afmaken in de Zestien</div>
  <div id="objectives-bar">
    <div class="obj-pill" id="obj-1">★ Scoor</div>
    <div class="obj-pill" id="obj-2">★ Assist op maat</div>
    <div class="obj-pill" id="obj-3">★ Krulbal / Bovenhoek</div>
  </div>
  <canvas id="overlay-canvas"></canvas>
  <div id="status-bubble">Veeg vanaf de bal om met effect te passen of in de kruising te krullen!</div>
</div>

<div id="btn-bar">
  <button class="action-btn secondary" onclick="retryScenario()">↺ Herstel Situatie</button>
  <button class="action-btn secondary" onclick="toggleCameraMode()" id="cam-btn">🎥 Camera: Hero</button>
  <button class="action-btn" onclick="nextScenario()">Volgende Scenario ➔</button>
</div>

<script>
const container = document.getElementById('container');
const overlay = document.getElementById('overlay-canvas');
const ctx = overlay.getContext('2d');
const vignette = document.getElementById('slowmo-vignette');

let viewWidth = container.clientWidth || 380;
let viewHeight = container.clientHeight || 410;

// ==========================================
// 1. SCENE, CAMERA & RENDERER
// ==========================================
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x090e17);
scene.fog = new THREE.FogExp2(0x090e17, 0.0065);

const camera = new THREE.PerspectiveCamera(42, viewWidth / viewHeight, 0.1, 500);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.domElement.id = 'three-canvas';
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.18;
container.appendChild(renderer.domElement);

function resizeCanvas() {
  viewWidth = container.clientWidth;
  viewHeight = container.clientHeight;
  const dpr = Math.min(window.devicePixelRatio, 2);
  overlay.width = viewWidth * dpr;
  overlay.height = viewHeight * dpr;
  ctx.resetTransform();
  ctx.scale(dpr, dpr);

  renderer.setSize(viewWidth, viewHeight);
  camera.aspect = viewWidth / viewHeight;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resizeCanvas);
window.addEventListener('orientationchange', () => setTimeout(resizeCanvas, 150));

// ==========================================
// 2. STADIUM LIGHTING
// ==========================================
const hemiLight = new THREE.HemisphereLight(0xddeeff, 0x18301a, 0.55);
scene.add(hemiLight);

const mainFlood = new THREE.DirectionalLight(0xfffaf0, 1.25);
mainFlood.position.set(28, 52, 16);
mainFlood.castShadow = true;
mainFlood.shadow.mapSize.width = 2048;
mainFlood.shadow.mapSize.height = 2048;
mainFlood.shadow.camera.near = 10;
mainFlood.shadow.camera.far = 140;
mainFlood.shadow.camera.left = -36;
mainFlood.shadow.camera.right = 36;
mainFlood.shadow.camera.top = 36;
mainFlood.shadow.camera.bottom = -42;
mainFlood.shadow.bias = -0.0005;
scene.add(mainFlood);

const rimFlood = new THREE.DirectionalLight(0x88b4ff, 0.5);
rimFlood.position.set(-32, 38, -38);
scene.add(rimFlood);

// ==========================================
// 3. PROCEDURAL TEXTURES (KITS, GRASS, BALL)
// ==========================================
function createGrassTexture() {
  const c = document.createElement('canvas');
  c.width = 512; c.height = 512;
  const cx = c.getContext('2d');
  cx.fillStyle = '#266e2c';
  cx.fillRect(0, 0, 512, 512);

  // Subtle cross-mowing bands
  for (let y = 0; y < 512; y += 64) {
    cx.fillStyle = (y / 64) % 2 === 0 ? 'rgba(255,255,255,0.035)' : 'rgba(0,0,0,0.035)';
    cx.fillRect(0, y, 512, 32);
  }
  for (let x = 0; x < 512; x += 64) {
    cx.fillStyle = (x / 64) % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.02)';
    cx.fillRect(x, 0, 32, 512);
  }

  for (let i = 0; i < 28000; i++) {
    const x = Math.random() * 512;
    const y = Math.random() * 512;
    const g = 92 + Math.random() * 42;
    cx.fillStyle = `rgb(${Math.floor(g * 0.34)}, ${Math.floor(g)},${Math.floor(g * 0.36)})`;
    cx.fillRect(x, y, 1.5, 2.5);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(8, 12);
  return tex;
}

function createTwenteKitTexture(numberStr) {
  const c = document.createElement('canvas');
  c.width = 256; c.height = 256;
  const cx = c.getContext('2d');
  cx.fillStyle = '#c80000';
  cx.fillRect(0, 0, 256, 256);

  // Darker vertical fabric weave
  cx.fillStyle = 'rgba(0,0,0,0.08)';
  for (let x = 0; x < 256; x += 16) cx.fillRect(x, 0, 6, 256);

  // White collar & trim
  cx.fillStyle = '#ffffff';
  cx.fillRect(0, 0, 256, 16);
  cx.fillRect(0, 242, 256, 8);

  // Back number (on UV wrap)
  if (numberStr) {
    cx.fillStyle = '#ffffff';
    cx.font = '900 76px sans-serif';
    cx.textAlign = 'center';
    cx.textBaseline = 'middle';
    cx.fillText(numberStr, 64, 125);
  }
  return new THREE.CanvasTexture(c);
}

function createHeerenveenKitTexture() {
  const c = document.createElement('canvas');
  c.width = 256; c.height = 256;
  const cx = c.getContext('2d');
  cx.fillStyle = '#ffffff';
  cx.fillRect(0, 0, 256, 256);

  // Blue vertical stripes
  cx.fillStyle = '#004b9b';
  for (let x = 0; x < 256; x += 42) {
    cx.fillRect(x, 0, 21, 256);
  }

  // Iconic Red Pompeblêden (Waterlily leaves / hearts)
  cx.fillStyle = '#d4001a';
  const drawPompebled = (px, py, size) => {
    cx.beginPath();
    cx.arc(px - size * 0.35, py - size * 0.2, size * 0.45, 0, Math.PI * 2);
    cx.arc(px + size * 0.35, py - size * 0.2, size * 0.45, 0, Math.PI * 2);
    cx.moveTo(px - size * 0.75, py);
    cx.lineTo(px, py + size * 0.85);
    cx.lineTo(px + size * 0.75, py);
    cx.fill();
  };
  for (let y = 45; y < 230; y += 65) {
    for (let x = 31; x < 256; x += 42) {
      drawPompebled(x, y, 8);
    }
  }
  return new THREE.CanvasTexture(c);
}

function createBallTexture() {
  const c = document.createElement('canvas');
  c.width = 512; c.height = 256;
  const cx = c.getContext('2d');
  cx.fillStyle = '#f8f9fa';
  cx.fillRect(0, 0, 512, 256);

  // Modern Eredivisie matchball graphic trims
  cx.strokeStyle = '#d00000';
  cx.lineWidth = 6;
  cx.beginPath();
  for (let x = 0; x < 512; x += 64) {
    cx.moveTo(x, 0);
    cx.bezierCurveTo(x + 32, 128, x - 32, 128, x + 16, 256);
  }
  cx.stroke();

  cx.fillStyle = '#141820';
  for (let y = 36; y < 256; y += 85) {
    for (let x = (y % 170 === 36 ? 40 : 120); x < 512; x += 140) {
      cx.beginPath();
      for (let p = 0; p < 5; p++) {
        const a = (p * 2 * Math.PI) / 5 - Math.PI / 2;
        const px = x + 22 * Math.cos(a);
        const py = y + 22 * Math.sin(a);
        if (p === 0) cx.moveTo(px, py); else cx.lineTo(px, py);
      }
      cx.closePath();
      cx.fill();
    }
  }
  return new THREE.CanvasTexture(c);
}

function createCrowdTexture() {
  const c = document.createElement('canvas');
  c.width = 512; c.height = 128;
  const cx = c.getContext('2d');
  cx.fillStyle = '#181014';
  cx.fillRect(0, 0, 512, 128);
  const colors = ['#d00000', '#ff2222', '#ffffff', '#990000', '#222630', '#ffcccc'];
  for (let i = 0; i < 3500; i++) {
    cx.fillStyle = colors[Math.floor(Math.random() * colors.length)];
    const x = Math.random() * 512;
    const y = Math.random() * 128;
    cx.fillRect(x, y, 3, 4);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(6, 2);
  return tex;
}

function createAdBoardTexture() {
  const c = document.createElement('canvas');
  c.width = 1024; c.height = 64;
  const cx = c.getContext('2d');
  cx.fillStyle = '#b80000';
  cx.fillRect(0, 0, 1024, 64);
  cx.fillStyle = '#ffffff';
  cx.font = '900 32px sans-serif';
  cx.textBaseline = 'middle';
  const msg = "   🔴 DE GROLSCH VESTE   •   FC TWENTE ENSCHEDE   •   VAK-P   •   COTE D'OR EREDIVISIE   ";
  cx.fillText(msg + msg, 10, 34);
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = THREE.RepeatWrapping;
  tex.repeat.set(2, 1);
  return tex;
}

// ==========================================
// 4. PITCH, MARKINGS & DE GROLSCH VESTE STADIUM
// ==========================================
const pitchGeo = new THREE.PlaneGeometry(76, 110);
const pitchMat = new THREE.MeshStandardMaterial({
  color: 0x2d8636,
  roughness: 0.86,
  map: createGrassTexture()
});
const pitch = new THREE.Mesh(pitchGeo, pitchMat);
pitch.rotation.x = -Math.PI / 2;
pitch.receiveShadow = true;
scene.add(pitch);

// Mowed pitch stripes
for (let z = -48; z <= 48; z += 8) {
  const sGeo = new THREE.PlaneGeometry(64, 4);
  const sMat = new THREE.MeshStandardMaterial({
    color: 0x236f2b,
    roughness: 0.88,
    transparent: true,
    opacity: 0.42
  });
  const stripe = new THREE.Mesh(sGeo, sMat);
  stripe.rotation.x = -Math.PI / 2;
  stripe.position.set(0, 0.015, z);
  stripe.receiveShadow = true;
  scene.add(stripe);
}

function buildPitchLines() {
  const lineMat = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
  function addFieldStrip(x1, z1, x2, z2, width = 0.16) {
    const dx = x2 - x1;
    const dz = z2 - z1;
    const len = Math.hypot(dx, dz);
    const geo = new THREE.PlaneGeometry(width, len);
    const mesh = new THREE.Mesh(geo, lineMat);
    mesh.rotation.x = -Math.PI / 2;
    mesh.rotation.z = -Math.atan2(dx, dz);
    mesh.position.set((x1 + x2) / 2, 0.03, (z1 + z2) / 2);
    scene.add(mesh);
  }

  // Outer lines
  addFieldStrip(-32, -45, 32, -45, 0.18);
  addFieldStrip(-32, -45, -32, 45, 0.18);
  addFieldStrip(32, -45, 32, 45, 0.18);
  addFieldStrip(-32, 0, 32, 0, 0.16);

  // 18-yard Penalty Box
  addFieldStrip(-20, -45, -20, -28.5);
  addFieldStrip(20, -45, 20, -28.5);
  addFieldStrip(-20, -28.5, 20, -28.5);

  // 6-yard Goal Area
  addFieldStrip(-9.2, -45, -9.2, -39.5);
  addFieldStrip(9.2, -45, 9.2, -39.5);
  addFieldStrip(-9.2, -39.5, 9.2, -39.5);

  // Penalty Spot
  const spot = new THREE.Mesh(new THREE.CircleGeometry(0.28, 20), lineMat);
  spot.rotation.x = -Math.PI / 2;
  spot.position.set(0, 0.035, -34);
  scene.add(spot);

  // Penalty Arc ("The D")
  const arcCurve = new THREE.RingGeometry(9.05, 9.22, 40, 1, -0.92, 1.84);
  const arcMesh = new THREE.Mesh(arcCurve, lineMat);
  arcMesh.rotation.x = -Math.PI / 2;
  arcMesh.rotation.z = Math.PI;
  arcMesh.position.set(0, 0.035, -34);
  scene.add(arcMesh);

  // Center Circle
  const centerCircle = new THREE.Mesh(new THREE.RingGeometry(9.05, 9.22, 48), lineMat);
  centerCircle.rotation.x = -Math.PI / 2;
  centerCircle.position.set(0, 0.035, 0);
  scene.add(centerCircle);
}
buildPitchLines();

// Stadium Environment (De Grolsch Veste Stands & LED Boards)
function buildStadium() {
  const adTex = createAdBoardTexture();
  const adMat = new THREE.MeshStandardMaterial({
    map: adTex,
    emissive: 0x330000,
    roughness: 0.4
  });

  // Back LED board (split around goal)
  const adBackL = new THREE.Mesh(new THREE.BoxGeometry(26, 1.1, 0.3), adMat);
  adBackL.position.set(-21, 0.55, -49.5);
  scene.add(adBackL);

  const adBackR = new THREE.Mesh(new THREE.BoxGeometry(26, 1.1, 0.3), adMat);
  adBackR.position.set(21, 0.55, -49.5);
  scene.add(adBackR);

  const adSideL = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.1, 95), adMat);
  adSideL.position.set(-34.5, 0.55, -2);
  scene.add(adSideL);

  const adSideR = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.1, 95), adMat);
  adSideR.position.set(34.5, 0.55, -2);
  scene.add(adSideR);

  // Vak-P Steep Stadium Stand behind the goal
  const crowdMat = new THREE.MeshStandardMaterial({
    map: createCrowdTexture(),
    roughness: 0.9
  });
  const standNorth = new THREE.Mesh(new THREE.PlaneGeometry(92, 26), crowdMat);
  standNorth.position.set(0, 11, -61);
  standNorth.rotation.x = 0.42;
  scene.add(standNorth);

  const standWest = new THREE.Mesh(new THREE.PlaneGeometry(110, 24), crowdMat);
  standWest.position.set(-46, 10, -5);
  standWest.rotation.y = Math.PI / 2;
  standWest.rotation.x = 0.35;
  scene.add(standWest);

  const standEast = new THREE.Mesh(new THREE.PlaneGeometry(110, 24), crowdMat);
  standEast.position.set(46, 10, -5);
  standEast.rotation.y = -Math.PI / 2;
  standEast.rotation.x = 0.35;
  scene.add(standEast);

  // Red Stadium Roof Overhang
  const roofMat = new THREE.MeshStandardMaterial({ color: 0x8a0000, metalness: 0.5, roughness: 0.4 });
  const roofNorth = new THREE.Mesh(new THREE.BoxGeometry(96, 1.2, 16), roofMat);
  roofNorth.position.set(0, 23.5, -58);
  roofNorth.rotation.x = 0.12;
  scene.add(roofNorth);

  // Stadium Floodlight Glow Orbs
  const bulbMat = new THREE.MeshBasicMaterial({ color: 0xfff8e7 });
  [[-36, 26, -54], [36, 26, -54], [-18, 25, -54], [18, 25, -54]].forEach(pos => {
    const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.9, 12, 12), bulbMat);
    lamp.position.set(pos[0], pos[1], pos[2]);
    scene.add(lamp);
  });
}
buildStadium();

// ==========================================
// 5. 3D GOAL WITH DEFORMABLE RIPPLE NET
// ==========================================
function createNetTexture() {
  const c = document.createElement('canvas');
  c.width = 64; c.height = 64;
  const cx = c.getContext('2d');
  cx.strokeStyle = 'rgba(255, 255, 255, 0.9)';
  cx.lineWidth = 2.2;
  cx.beginPath();
  cx.moveTo(32, 0); cx.lineTo(64, 32); cx.lineTo(32, 64); cx.lineTo(0, 32); cx.closePath();
  cx.stroke();
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(28, 12);
  return tex;
}

const goalWidth = 14.4;
const goalHeight = 4.5;
const goalDepth = 3.8;
const goalZ = -45;
const goalGroup = new THREE.Group();

const postMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.35, roughness: 0.2 });
const pRadius = 0.17;

const postL = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalHeight, 20), postMat);
postL.position.set(-goalWidth / 2, goalHeight / 2, goalZ);
postL.castShadow = true;
goalGroup.add(postL);

const postR = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalHeight, 20), postMat);
postR.position.set(goalWidth / 2, goalHeight / 2, goalZ);
postR.castShadow = true;
goalGroup.add(postR);

const crossbar = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalWidth + pRadius * 2, 20), postMat);
crossbar.rotation.z = Math.PI / 2;
crossbar.position.set(0, goalHeight, goalZ);
crossbar.castShadow = true;
goalGroup.add(crossbar);

// Red stanchion support poles behind goal
const stanchionMat = new THREE.MeshStandardMaterial({ color: 0xb80000, metalness: 0.6, roughness: 0.3 });
[-goalWidth / 2, goalWidth / 2].forEach(xPos => {
  const backPole = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, goalHeight, 12), stanchionMat);
  backPole.position.set(xPos, goalHeight / 2, goalZ - goalDepth);
  goalGroup.add(backPole);
});

const netMat = new THREE.MeshStandardMaterial({
  map: createNetTexture(),
  transparent: true,
  opacity: 0.82,
  roughness: 0.7,
  side: THREE.DoubleSide,
  alphaTest: 0.05
});

// Subdivided back net so it can physically ripple on goal impact!
const backNetGeo = new THREE.PlaneGeometry(goalWidth, goalHeight, 18, 10);
const backNetOrigPos = backNetGeo.attributes.position.clone();
const backNet = new THREE.Mesh(backNetGeo, netMat);
backNet.position.set(0, goalHeight / 2, goalZ - goalDepth);
goalGroup.add(backNet);

const roofNet = new THREE.Mesh(new THREE.PlaneGeometry(goalWidth, goalDepth), netMat);
roofNet.rotation.x = Math.PI / 2;
roofNet.position.set(0, goalHeight - 0.04, goalZ - goalDepth / 2);
goalGroup.add(roofNet);

const sideNetL = new THREE.Mesh(new THREE.PlaneGeometry(goalDepth, goalHeight), netMat);
sideNetL.rotation.y = Math.PI / 2;
sideNetL.position.set(-goalWidth / 2, goalHeight / 2, goalZ - goalDepth / 2);
goalGroup.add(sideNetL);

const sideNetR = new THREE.Mesh(new THREE.PlaneGeometry(goalDepth, goalHeight), netMat);
sideNetR.rotation.y = -Math.PI / 2;
sideNetR.position.set(goalWidth / 2, goalHeight / 2, goalZ - goalDepth / 2);
goalGroup.add(sideNetR);

scene.add(goalGroup);

let netRipple = { active: false, localX: 0, localY: 0, strength: 0, time: 0 };

function triggerNetRipple(worldX, worldY) {
  netRipple.active = true;
  netRipple.localX = THREE.MathUtils.clamp(worldX, -goalWidth / 2, goalWidth / 2);
  netRipple.localY = THREE.MathUtils.clamp(worldY - goalHeight / 2, -goalHeight / 2, goalHeight / 2);
  netRipple.strength = 1.35;
  netRipple.time = 0;
}

function updateNetRipple(dt) {
  if (!netRipple.active) return;
  netRipple.time += dt * 16;
  netRipple.strength *= Math.pow(0.12, dt);

  const posAttr = backNetGeo.attributes.position;
  for (let i = 0; i < posAttr.count; i++) {
    const ox = backNetOrigPos.getX(i);
    const oy = backNetOrigPos.getY(i);
    const dist = Math.hypot(ox - netRipple.localX, oy - netRipple.localY);
    const edgeFactor = (1 - Math.pow(ox / (goalWidth / 2), 4)) * (1 - Math.pow(oy / (goalHeight / 2), 4));
    const wave = Math.exp(-dist * 0.45) * Math.sin(netRipple.time - dist * 0.9) * netRipple.strength * Math.max(0, edgeFactor);
    posAttr.setZ(i, -Math.abs(wave) * 0.65 + wave * 0.35);
  }
  posAttr.needsUpdate = true;
  if (netRipple.strength < 0.02) {
    netRipple.active = false;
  }
}

// ==========================================
// 6. BALL, RIBBON TRAIL & 3D PREVIEW ARC
// ==========================================
const ballRadius = 0.42;
const ballMesh = new THREE.Mesh(
  new THREE.SphereGeometry(ballRadius, 28, 28),
  new THREE.MeshStandardMaterial({ map: createBallTexture(), roughness: 0.22, metalness: 0.05 })
);
ballMesh.castShadow = true;
scene.add(ballMesh);

// 3D Dotted Trajectory Preview Spheres (shown while aiming)
const previewDots = [];
const previewDotMat = new THREE.MeshBasicMaterial({ color: 0xffea00, transparent: true, opacity: 0.9 });
for (let i = 0; i < 24; i++) {
  const s = 0.19 * (1 - (i / 28) * 0.5);
  const dot = new THREE.Mesh(new THREE.SphereGeometry(s, 10, 10), previewDotMat.clone());
  dot.visible = false;
  scene.add(dot);
  previewDots.push(dot);
}

// Ball flight aerodynamic trail
const MAX_TRAIL = 26;
const trailPoints = [];
const trailLineGeo = new THREE.BufferGeometry();
const trailLineMat = new THREE.LineBasicMaterial({ color: 0xfff380, transparent: true, opacity: 0.65 });
const trailLine = new THREE.Line(trailLineGeo, trailLineMat);
scene.add(trailLine);

// ==========================================
// 7. REALISTIC PLAYER BUILDER
// ==========================================
function createProPlayer(options) {
  const {
    team = 'twente',
    number = '',
    hairColor = 0x3b2618,
    skinColor = 0xf2c29b,
    bootColor = 0xff3300,
    scale = 1.0,
    isGK = false
  } = options;

  const root = new THREE.Group();
  root.scale.set(scale, scale, scale);

  let jerseyMat, shortsMat, sockMat;
  if (isGK) {
    jerseyMat = new THREE.MeshStandardMaterial({ color: 0x00e676, roughness: 0.55 });
    shortsMat = new THREE.MeshStandardMaterial({ color: 0x12161f, roughness: 0.65 });
    sockMat = new THREE.MeshStandardMaterial({ color: 0x00e676, roughness: 0.6 });
  } else if (team === 'twente') {
    jerseyMat = new THREE.MeshStandardMaterial({ map: createTwenteKitTexture(number), roughness: 0.55 });
    shortsMat = new THREE.MeshStandardMaterial({ color: 0xb80000, roughness: 0.6 });
    sockMat = new THREE.MeshStandardMaterial({ color: 0xcc0000, roughness: 0.65 });
  } else {
    jerseyMat = new THREE.MeshStandardMaterial({ map: createHeerenveenKitTexture(), roughness: 0.55 });
    shortsMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 });
    sockMat = new THREE.MeshStandardMaterial({ color: 0x003f8a, roughness: 0.65 });
  }

  const skinMat = new THREE.MeshStandardMaterial({ color: skinColor, roughness: 0.75 });
  const bootMat = new THREE.MeshStandardMaterial({ color: bootColor, roughness: 0.35 });
  const hairMat = new THREE.MeshStandardMaterial({ color: hairColor, roughness: 0.85 });

  // Ground contact shadow ring
  const shadowRing = new THREE.Mesh(
    new THREE.CircleGeometry(0.62, 20),
    new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.32 })
  );
  shadowRing.rotation.x = -Math.PI / 2;
  shadowRing.position.y = 0.025;
  root.add(shadowRing);

  // Torso group for upper-body lean during sprints & shots
  const bodyPivot = new THREE.Group();
  root.bodyPivot = bodyPivot;
  root.add(bodyPivot);

  const hips = new THREE.Mesh(new THREE.CylinderGeometry(0.39, 0.36, 0.42, 14), shortsMat);
  hips.position.y = 1.55;
  hips.castShadow = true;
  bodyPivot.add(hips);

  const chest = new THREE.Mesh(new THREE.CylinderGeometry(0.52, 0.4, 0.9, 16), jerseyMat);
  chest.position.y = 2.16;
  chest.rotation.y = Math.PI / 2;
  chest.castShadow = true;
  bodyPivot.add(chest);

  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.15, 0.18, 10), skinMat);
  neck.position.y = 2.66;
  bodyPivot.add(neck);

  const head = new THREE.Mesh(new THREE.SphereGeometry(0.26, 16, 16), skinMat);
  head.position.y = 2.86;
  head.castShadow = true;
  bodyPivot.add(head);

  const hair = new THREE.Mesh(new THREE.SphereGeometry(0.272, 14, 14, 0, Math.PI * 2, 0, Math.PI * 0.58), hairMat);
  hair.position.y = 2.89;
  hair.rotation.x = -0.18;
  bodyPivot.add(hair);

  function createArm(isLeft) {
    const armGroup = new THREE.Group();
    armGroup.position.set((isLeft ? -1 : 1) * 0.58, 2.48, 0);
    const sleeve = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.13, 0.28, 10), jerseyMat);
    sleeve.position.y = -0.12;
    armGroup.add(sleeve);

    const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.09, 0.58, 10), isGK ? jerseyMat : skinMat);
    forearm.position.set(0, -0.5, 0.04);
    armGroup.add(forearm);

    if (isGK) {
      const glove = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.28, 0.14), new THREE.MeshStandardMaterial({ color: 0xffffff }));
      glove.position.set(0, -0.86, 0.08);
      armGroup.add(glove);
    }
    return armGroup;
  }
  root.leftArm = createArm(true);
  root.rightArm = createArm(false);
  bodyPivot.add(root.leftArm);
  bodyPivot.add(root.rightArm);

  function createLeg(isLeft) {
    const legGroup = new THREE.Group();
    legGroup.position.set((isLeft ? -1 : 1) * 0.22, 1.42, 0);
    const shortsLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.16, 0.32, 10), shortsMat);
    shortsLeg.position.y = -0.15;
    legGroup.add(shortsLeg);

    const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.13, 0.35, 10), skinMat);
    thigh.position.y = -0.42;
    legGroup.add(thigh);

    const calf = new THREE.Mesh(new THREE.CylinderGeometry(0.135, 0.1, 0.58, 10), sockMat);
    calf.position.y = -0.84;
    legGroup.add(calf);

    const boot = new THREE.Mesh(new THREE.BoxGeometry(0.21, 0.15, 0.46), bootMat);
    boot.position.set(0, -1.14, -0.09);
    legGroup.add(boot);
    return legGroup;
  }
  root.leftLeg = createLeg(true);
  root.rightLeg = createLeg(false);
  bodyPivot.add(root.leftLeg);
  bodyPivot.add(root.rightLeg);

  root.kickTimer = 0;
  return root;
}

// ==========================================
// 8. SCENARIOS & MATCH DATA
// ==========================================
const SCENARIOS = [
  {
    title: "1. Flankcombinatie & Steekpass",
    match: "1 - 0",
    clock: "34'",
    banner: "Steek Weghorst weg in de diepte of krul vanaf de vleugel",
    objectives: ["★ Scoor een doelpunt", "★ Assist van Ørjasæter", "★ Krul in de hoek"],
    orjasaeterPos: { x: -14, z: -13 },
    orjasaeterRun: { x: -7, z: -27, speed: 5.5 },
    weghorstPos: { x: 3.5, z: -16 },
    weghorstRun: { x: 1.0, z: -33.5, speed: 5.2 },
    defenders: [
      { x: -5.5, z: -18.5, patrol: 3.8, speed: 3.6 },
      { x: 4.5, z: -26.5, patrol: 4.2, speed: 3.9 }
    ],
    initialPossessor: 'orjasaeter'
  },
  {
    title: "2. Weghorst Aanspeelpunt & Kaats",
    match: "1 - 1",
    clock: "68'",
    banner: "Kaats op de diepgaande Ørjasæter of draai weg en schiet",
    objectives: ["★ Scoor een doelpunt", "★ Kaats / 1-2 combinatie", "★ Binnenkant paal / Kruising"],
    orjasaeterPos: { x: -15.5, z: -10 },
    orjasaeterRun: { x: -5.5, z: -31, speed: 6.4 },
    weghorstPos: { x: 0.5, z: -17 },
    weghorstRun: { x: 2.0, z: -26.5, speed: 4.2 },
    defenders: [
      { x: 0.5, z: -22.5, patrol: 3.2, speed: 3.4 },
      { x: -8.0, z: -20.5, patrol: 3.8, speed: 3.9 },
      { x: 6.5, z: -30.5, patrol: 3.2, speed: 3.6 }
    ],
    initialPossessor: 'weghorst'
  },
  {
    title: "3. Blessuretijd Beslissing voor Vak-P",
    match: "2 - 2",
    clock: "90+3'",
    banner: "90+3' Winnende treffer: Splijt de Heerenveen-defensie open!",
    objectives: ["★ Scoor de 3-2", "★ Meerdaagse pass-aanval", "★ Bovenhoek (> 2.2m hoog)"],
    orjasaeterPos: { x: 14, z: -8 },
    orjasaeterRun: { x: 6.5, z: -30, speed: 6.6 },
    weghorstPos: { x: -4.5, z: -13.5 },
    weghorstRun: { x: -1.5, z: -34.5, speed: 5.6 },
    defenders: [
      { x: 5.0, z: -17.5, patrol: 4.2, speed: 4.3 },
      { x: -5.5, z: -24.5, patrol: 4.0, speed: 4.1 },
      { x: 3.0, z: -35.0, patrol: 3.2, speed: 4.4 }
    ],
    initialPossessor: 'orjasaeter'
  }
];

let scenarioIdx = 0;
let currentScenario = null;
let activePossessor = 'orjasaeter';
let passCountInPlay = 0;
let cameraMode = 'hero'; // 'hero' or 'broadcast'

// Instantiate Players
const orjasaeterMesh = createProPlayer({
  team: 'twente',
  number: '11',
  hairColor: 0xd8b467,
  bootColor: 0x00f0ff,
  scale: 0.99
});
const weghorstMesh = createProPlayer({
  team: 'twente',
  number: '9',
  hairColor: 0x3b2718,
  bootColor: 0xff5500,
  scale: 1.09 // 1.97m target striker
});
const keeperMesh = createProPlayer({
  team: 'heerenveen',
  isGK: true,
  hairColor: 0x241810,
  bootColor: 0xffffff,
  scale: 1.04
});

scene.add(orjasaeterMesh);
scene.add(weghorstMesh);
scene.add(keeperMesh);

let defenderMeshes = [];

// Physics & State
const ballPhys = {
  pos: new THREE.Vector3(0, ballRadius, 0),
  vel: new THREE.Vector3(0, 0, 0),
  spinY: 0, // Magnus horizontal curl
  spinX: 0, // Topspin / dip
  inFlight: false,
  inGoal: false
};

const gkState = {
  homeX: 0,
  homeZ: -43.7,
  isDiving: false,
  diveProgress: 0,
  reactionDelay: 0.14,
  timeSinceShot: 0,
  diveStartX: 0,
  targetX: 0,
  targetY: 0
};

let looseBallChaser = null;
let isChasingLooseBall = false;
let celebrationCounter = 0;
let retryTimeout = null;

function setStatus(text, color = "#ffffff") {
  const el = document.getElementById('status-bubble');
  el.innerText = text;
  el.style.color = color;
}

function updateStarsUI(s1, s2, s3) {
  const starsStr = (s1 ? "★" : "☆") + (s2 ? "★" : "☆") + (s3 ? "★" : "☆");
  const starEl = document.getElementById('hud-stars');
  starEl.innerText = starsStr;
  starEl.style.color = (s1 || s2 || s3) ? "#ffd700" : "#ffffff";

  document.getElementById('obj-1').className = "obj-pill" + (s1 ? " done" : "");
  document.getElementById('obj-2').className = "obj-pill" + (s2 ? " done" : "");
  document.getElementById('obj-3').className = "obj-pill" + (s3 ? " done" : "");
}

function toggleCameraMode() {
  cameraMode = cameraMode === 'hero' ? 'broadcast' : 'hero';
  document.getElementById('cam-btn').innerText = cameraMode === 'hero' ? "🎥 Camera: Hero" : "🎥 Camera: TV";
}

function loadScenario(idx) {
  if (retryTimeout) {
    clearTimeout(retryTimeout);
    retryTimeout = null;
  }
  scenarioIdx = idx % SCENARIOS.length;
  currentScenario = JSON.parse(JSON.stringify(SCENARIOS[scenarioIdx]));
  activePossessor = currentScenario.initialPossessor;
  passCountInPlay = 0;
  celebrationCounter = 0;

  defenderMeshes.forEach(d => scene.remove(d.mesh));
  defenderMeshes = [];

  currentScenario.defenders.forEach(def => {
    const mesh = createProPlayer({
      team: 'heerenveen',
      hairColor: 0x2b1d12,
      bootColor: 0x111111,
      scale: 1.02
    });
    mesh.position.set(def.x, 0, def.z);
    mesh.rotation.y = Math.PI;
    scene.add(mesh);
    defenderMeshes.push({
      mesh: mesh,
      startX: def.x,
      startZ: def.z,
      patrol: def.patrol,
      speed: def.speed,
      dir: 1
    });
  });

  gkState.isDiving = false;
  gkState.diveProgress = 0;
  gkState.timeSinceShot = 0;
  gkState.targetX = 0;
  gkState.targetY = 0;
  keeperMesh.position.set(0, 0, gkState.homeZ);
  keeperMesh.rotation.set(0, Math.PI, 0);

  orjasaeterMesh.position.set(currentScenario.orjasaeterPos.x, 0, currentScenario.orjasaeterPos.z);
  orjasaeterMesh.rotation.set(0, 0, 0);
  weghorstMesh.position.set(currentScenario.weghorstPos.x, 0, currentScenario.weghorstPos.z);
  weghorstMesh.rotation.set(0, 0, 0);

  looseBallChaser = null;
  isChasingLooseBall = false;
  ballPhys.inFlight = false;
  ballPhys.inGoal = false;
  ballPhys.vel.set(0, 0, 0);
  trailPoints.length = 0;
  trailLineGeo.setFromPoints([]);
  hidePreviewArc();

  snapBallToCarrier();

  document.getElementById('hud-scenario').innerHTML = `<span style="color:#00e676;">●</span> ${scenarioIdx + 1} /${SCENARIOS.length}`;
  document.getElementById('hud-score').innerText = currentScenario.match;
  document.getElementById('hud-clock').innerText = currentScenario.clock;
  document.getElementById('tactical-banner').innerText = currentScenario.banner;
  document.getElementById('obj-1').innerText = currentScenario.objectives[0];
  document.getElementById('obj-2').innerText = currentScenario.objectives[1];
  document.getElementById('obj-3').innerText = currentScenario.objectives[2];
  updateStarsUI(false, false, false);
  updateStatusInstruction();
}

function snapBallToCarrier() {
  const carrier = activePossessor === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
  // Orient carrier toward the goal
  const angleToGoal = Math.atan2(0 - carrier.position.x, goalZ - carrier.position.z);
  carrier.rotation.y = angleToGoal;

  ballPhys.pos.set(
    carrier.position.x + Math.sin(angleToGoal) * 0.82,
    ballRadius,
    carrier.position.z + Math.cos(angleToGoal) * 0.82
  );
  ballMesh.position.copy(ballPhys.pos);
}

function updateStatusInstruction() {
  const activeName = activePossessor === 'orjasaeter' ? "Sondre Ørjasæter (11)" : "Wout Weghorst (9)";
  const partner = activePossessor === 'orjasaeter' ? "Weghorst (9)" : "Ørjasæter (11)";
  setStatus(`⏱️ TACTISCHE SLOW-MO: ${activeName} aan de bal. Steek ${partner} weg of krul op doel!`, "#ffffff");
}

function retryScenario() {
  loadScenario(scenarioIdx);
}

function nextScenario() {
  loadScenario(scenarioIdx + 1);
}

// ==========================================
// 9. RAYCASTING & REAL-TIME 3D SHOT PHYSICS
// ==========================================
const raycaster = new THREE.Raycaster();
const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);

function screenToWorld(sx, sy) {
  const mouse = new THREE.Vector2((sx / viewWidth) * 2 - 1, -(sy / viewHeight) * 2 + 1);
  raycaster.setFromCamera(mouse, camera);
  const intersect = new THREE.Vector3();
  const hit = raycaster.ray.intersectPlane(groundPlane, intersect);
  return hit ? intersect : null;
}

function worldToScreen(worldVec) {
  const clone = worldVec.clone().project(camera);
  return {
    x: (clone.x + 1) * viewWidth / 2,
    y: (-clone.y + 1) * viewHeight / 2
  };
}

let isSwiping = false;
let gesturePoints = [];

function getCoords(e) {
  const rect = container.getBoundingClientRect();
  const touch = e.touches ? e.touches[0] : (e.changedTouches ? e.changedTouches[0] : e);
  return {
    x: touch.clientX - rect.left,
    y: touch.clientY - rect.top
  };
}

function computeShotParametersFromGesture() {
  if (gesturePoints.length < 3) return null;

  const endScreen = gesturePoints[gesturePoints.length - 1];
  const midScreen = gesturePoints[Math.floor(gesturePoints.length / 2)];

  const startW = ballPhys.pos.clone();
  const endW = screenToWorld(endScreen.x, endScreen.y);
  const midW = screenToWorld(midScreen.x, midScreen.y);
  if (!endW || !midW) return null;

  // Clamp overly distant raycast points near the horizon
  endW.x = THREE.MathUtils.clamp(endW.x, -30, 30);
  endW.z = THREE.MathUtils.clamp(endW.z, -47.5, 10);

  const dx = endW.x - startW.x;
  const dz = endW.z - startW.z;
  const dist = Math.hypot(dx, dz);
  if (dist < 1.8) return null;

  // Calculate perpendicular midpoint deviation in world space for authentic Magnus curve
  const lineVecX = dx / dist;
  const lineVecZ = dz / dist;
  const toMidX = midW.x - startW.x;
  const toMidZ = midW.z - startW.z;
  // Cross product gives signed lateral deviation
  const lateralBulge = toMidX * lineVecZ - toMidZ * lineVecX;
  const spinY = THREE.MathUtils.clamp(lateralBulge * 2.4, -15, 15);

  // Determine flight time & initial velocity so ball lands/reaches endW accurately
  const isShotOnGoal = endW.z <= -42.2 && Math.abs(endW.x) < (goalWidth / 2 + 2.5);
  const speed = isShotOnGoal
    ? THREE.MathUtils.clamp(22 + dist * 0.42, 25, 39)
    : THREE.MathUtils.clamp(16 + dist * 0.35, 17, 29);

  const flightTime = Math.max(0.32, dist / speed);
  const gravity = 15.8;

  // Target elevation: shots drawn higher up into the goal area rise toward the top corner!
  let targetY = ballRadius;
  if (isShotOnGoal) {
    const goalOvershoot = THREE.MathUtils.clamp((-43.2 - endW.z) * 0.85, 0.3, goalHeight - 0.35);
    targetY = goalOvershoot;
  }

  // Compensate initial horizontal velocity for Magnus acceleration (0.5 * a_magnus * T^2)
  // Lateral acceleration is perpendicular to velocity
  const perpX = -lineVecZ;
  const perpZ = lineVecX;
  const magnusAccel = spinY * 1.15;

  const vx = (dx - 0.5 * perpX * magnusAccel * flightTime * flightTime) / flightTime;
  const vz = (dz - 0.5 * perpZ * magnusAccel * flightTime * flightTime) / flightTime;

  // Loft factor based on distance & whether it's a pass or shot
  const extraLoft = isShotOnGoal ? 0.85 : Math.min(2.6, dist * 0.08);
  const vy = (targetY - startW.y + 0.5 * gravity * flightTime * flightTime) / flightTime + extraLoft;

  return {
    vel: new THREE.Vector3(vx, vy, vz),
    spinY: spinY,
    flightTime: flightTime,
    endW: endW,
    isShotOnGoal: isShotOnGoal
  };
}

function updatePreviewArc() {
  const params = computeShotParametersFromGesture();
  if (!params) {
    hidePreviewArc();
    return;
  }

  const gravity = 15.8;
  const simPos = ballPhys.pos.clone();
  const simVel = params.vel.clone();
  const totalTime = params.flightTime;
  const dt = totalTime / previewDots.length;

  for (let i = 0; i < previewDots.length; i++) {
    const speedXZ = Math.hypot(simVel.x, simVel.z) || 1;
    const perpX = -simVel.z / speedXZ;
    const perpZ = simVel.x / speedXZ;
    const magnusAccel = params.spinY * 1.15;

    simVel.x += perpX * magnusAccel * dt;
    simVel.z += perpZ * magnusAccel * dt;
    simVel.y -= gravity * dt;

    simPos.x += simVel.x * dt;
    simPos.y = Math.max(ballRadius, simPos.y + simVel.y * dt);
    simPos.z += simVel.z * dt;

    previewDots[i].position.copy(simPos);
    previewDots[i].visible = true;
  }
}

function hidePreviewArc() {
  for (let i = 0; i < previewDots.length; i++) {
    previewDots[i].visible = false;
  }
}

function onTouchStart(e) {
  if (ballPhys.inFlight || isChasingLooseBall || celebrationCounter > 0) return;
  if (e.cancelable) e.preventDefault();

  const pos = getCoords(e);
  const ballScreen = worldToScreen(ballMesh.position);
  if (Math.hypot(pos.x - ballScreen.x, pos.y - ballScreen.y) < 82) {
    isSwiping = true;
    gesturePoints = [{ x: pos.x, y: pos.y }];
  }
}

function onTouchMove(e) {
  if (!isSwiping) return;
  if (e.cancelable) e.preventDefault();

  const pos = getCoords(e);
  const last = gesturePoints[gesturePoints.length - 1];
  if (Math.hypot(pos.x - last.x, pos.y - last.y) > 5) {
    gesturePoints.push({ x: pos.x, y: pos.y });
    updatePreviewArc();
  }
}

function onTouchEnd(e) {
  if (!isSwiping) return;
  if (e.cancelable) e.preventDefault();
  isSwiping = false;

  const params = computeShotParametersFromGesture();
  hidePreviewArc();
  gesturePoints = [];

  if (params) {
    strikeBall(params);
  }
}

container.addEventListener('touchstart', onTouchStart, { passive: false });
window.addEventListener('touchmove', onTouchMove, { passive: false });
window.addEventListener('touchend', onTouchEnd, { passive: false });
window.addEventListener('touchcancel', onTouchEnd, { passive: false });

container.addEventListener('mousedown', onTouchStart);
window.addEventListener('mousemove', onTouchMove);
window.addEventListener('mouseup', onTouchEnd);

function strikeBall(params) {
  // Trigger kick animation on active carrier
  const carrier = activePossessor === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
  carrier.kickTimer = 0.42;
  carrier.rotation.y = Math.atan2(params.vel.x, params.vel.z);

  ballPhys.vel.copy(params.vel);
  ballPhys.spinY = params.spinY;
  ballPhys.inFlight = true;
  ballPhys.inGoal = false;
  trailPoints.length = 0;

  // Check if it's a through-ball to teammate
  if (!params.isShotOnGoal) {
    const targetKey = activePossessor === 'orjasaeter' ? 'weghorst' : 'orjasaeter';
    const targetMesh = targetKey === 'weghorst' ? weghorstMesh : orjasaeterMesh;
    const distToRunner = Math.hypot(params.endW.x - targetMesh.position.x, params.endW.z - targetMesh.position.z);
    if (distToRunner < 21.0) {
      looseBallChaser = targetKey;
      isChasingLooseBall = true;
      const chaserName = looseBallChaser === 'orjasaeter' ? "Ørjasæter (11)" : "Weghorst (9)";
      setStatus(`🏃 Steekpass op maat! ${chaserName} sprint de vrije ruimte in!`, "#00f2ff");
    } else {
      setStatus(`⚽ Bal onderweg...`, "#ffffff");
    }
  } else {
    const curveTxt = Math.abs(params.spinY) > 4.2 ? " met veel effect" : "";
    setStatus(`🚀 Schot op doel${curveTxt}!`, "#ffe600");
  }

  triggerKeeperPrediction(params);
}

function triggerKeeperPrediction(params) {
  gkState.timeSinceShot = 0;
  gkState.diveStartX = keeperMesh.position.x;

  // Simulate forward to see where the ball crosses the goal line (z = -44.6)
  const simPos = ballPhys.pos.clone();
  const simVel = params.vel.clone();
  const dt = 0.016;
  let crossingPoint = null;

  for (let s = 0; s < 140; s++) {
    const speedXZ = Math.hypot(simVel.x, simVel.z) || 1;
    const perpX = -simVel.z / speedXZ;
    const perpZ = simVel.x / speedXZ;
    simVel.x += perpX * (params.spinY * 1.15) * dt;
    simVel.z += perpZ * (params.spinY * 1.15) * dt;
    simVel.y -= 15.8 * dt;
    simPos.addScaledVector(simVel, dt);
    if (simPos.y < ballRadius) {
      simPos.y = ballRadius;
      simVel.y *= -0.52;
    }
    if (simPos.z <= -44.2) {
      crossingPoint = simPos.clone();
      break;
    }
  }

  if (crossingPoint && Math.abs(crossingPoint.x) < goalWidth / 2 + 1.5) {
    // Keeper reach depends on shot distance & one-two passes
    const shotDist = Math.hypot(ballPhys.pos.x, ballPhys.pos.z - goalZ);
    gkState.reactionDelay = THREE.MathUtils.clamp(0.22 - shotDist * 0.003 + (passCountInPlay > 0 ? 0.05 : 0), 0.09, 0.24);
    const maxReach = 4.9;
    const desiredX = THREE.MathUtils.clamp(crossingPoint.x, gkState.diveStartX - maxReach, gkState.diveStartX + maxReach);
    gkState.targetX = THREE.MathUtils.clamp(desiredX, -goalWidth / 2 + 0.9, goalWidth / 2 - 0.9);
    gkState.targetY = THREE.MathUtils.clamp(crossingPoint.y, 0.4, goalHeight - 0.5);
    gkState.isDiving = true;
    gkState.diveProgress = 0;
  } else {
    gkState.isDiving = false;
  }
}

// ==========================================
// 10. ANIMATION & PHYSICS LOOP (BULLET-TIME)
// ==========================================
const clock = new THREE.Clock();

function animatePlayerLimbs(mesh, speedMag, elapsed, dt) {
  if (mesh.kickTimer > 0) {
    mesh.kickTimer = Math.max(0, mesh.kickTimer - dt);
    const phase = (0.42 - mesh.kickTimer) / 0.42;
    const swing = Math.sin(phase * Math.PI * 1.35);
    mesh.rightLeg.rotation.x = -swing * 1.25;
    mesh.leftLeg.rotation.x = swing * 0.45;
    mesh.bodyPivot.rotation.x = -swing * 0.18;
    mesh.leftArm.rotation.x = -swing * 0.7;
    mesh.rightArm.rotation.x = swing * 0.6;
    return;
  }

  if (speedMag > 0.25) {
    const freq = 9 + speedMag * 0.9;
    const amp = Math.min(0.68, 0.22 + speedMag * 0.06);
    mesh.leftLeg.rotation.x = Math.sin(elapsed * freq) * amp;
    mesh.rightLeg.rotation.x = -Math.sin(elapsed * freq) * amp;
    mesh.leftArm.rotation.x = -Math.sin(elapsed * freq) * (amp * 0.75);
    mesh.rightArm.rotation.x = Math.sin(elapsed * freq) * (amp * 0.75);
    mesh.bodyPivot.rotation.x = Math.min(0.18, speedMag * 0.022);
  } else {
    // Idle breathing
    mesh.leftLeg.rotation.x = THREE.MathUtils.lerp(mesh.leftLeg.rotation.x, 0, 0.15);
    mesh.rightLeg.rotation.x = THREE.MathUtils.lerp(mesh.rightLeg.rotation.x, 0, 0.15);
    mesh.leftArm.rotation.x = Math.sin(elapsed * 3) * 0.06;
    mesh.rightArm.rotation.x = -Math.sin(elapsed * 3) * 0.06;
    mesh.bodyPivot.rotation.x = THREE.MathUtils.lerp(mesh.bodyPivot.rotation.x, 0, 0.15);
  }
}

function moveAndOrientPlayer(mesh, targetX, targetZ, speed, dt, elapsed) {
  const dx = targetX - mesh.position.x;
  const dz = targetZ - mesh.position.z;
  const dist = Math.hypot(dx, dz);

  if (dist > 0.25) {
    const step = Math.min(dist, speed * dt);
    mesh.position.x += (dx / dist) * step;
    mesh.position.z += (dz / dist) * step;

    const targetAngle = Math.atan2(dx, dz);
    let diff = targetAngle - mesh.rotation.y;
    while (diff > Math.PI) diff -= Math.PI * 2;
    while (diff < -Math.PI) diff += Math.PI * 2;
    mesh.rotation.y += diff * Math.min(1, dt * 10);

    animatePlayerLimbs(mesh, speed, elapsed, dt);
  } else {
    animatePlayerLimbs(mesh, 0, elapsed, dt);
  }
}

function animate() {
  requestAnimationFrame(animate);
  const rawDt = Math.min(clock.getDelta(), 0.05);
  const elapsed = clock.getElapsedTime();

  // Score! Hero Tactical Slow-Motion when waiting for user input
  const isWaitingForCommand = !ballPhys.inFlight && !isChasingLooseBall && celebrationCounter === 0;
  const timeScale = isWaitingForCommand ? 0.15 : 1.0;
  vignette.style.opacity = isWaitingForCommand ? "1" : "0.2";

  const gameDt = rawDt * timeScale;

  updateNetRipple(rawDt);
  updateGoalkeeperAI(rawDt, elapsed);

  // Update Heerenveen Defenders
  defenderMeshes.forEach(d => {
    if (ballPhys.inFlight && !ballPhys.inGoal && ballPhys.pos.y < 2.2) {
      // Defenders react and step toward ball path
      const dx = ballPhys.pos.x - d.mesh.position.x;
      const dz = ballPhys.pos.z - d.mesh.position.z;
      const distToBall = Math.hypot(dx, dz);
      if (distToBall < 9.0) {
        moveAndOrientPlayer(d.mesh, ballPhys.pos.x, d.startZ, d.speed * 1.25, gameDt, elapsed);
        return;
      }
    }
    const patrolTargetX = d.startX + d.dir * d.patrol;
    moveAndOrientPlayer(d.mesh, patrolTargetX, d.startZ, d.speed, gameDt, elapsed);
    if (Math.abs(d.mesh.position.x - patrolTargetX) < 0.35) {
      d.dir *= -1;
    }
  });

  // Update Twente Attackers (Ørjasæter & Weghorst)
  if (currentScenario) {
    if (isChasingLooseBall) {
      const chaserMesh = looseBallChaser === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
      const otherMesh = looseBallChaser === 'orjasaeter' ? weghorstMesh : orjasaeterMesh;
      const sprintSpeed = looseBallChaser === 'orjasaeter' ? 9.4 : 8.5;

      // Predict slightly ahead of rolling ball
      const interceptX = ballPhys.pos.x + ballPhys.vel.x * 0.18;
      const interceptZ = Math.max(-42.5, ballPhys.pos.z + ballPhys.vel.z * 0.18);
      moveAndOrientPlayer(chaserMesh, interceptX, interceptZ, sprintSpeed, rawDt, elapsed);
      moveAndOrientPlayer(otherMesh, otherMesh.position.x, Math.max(-38, otherMesh.position.z - 5), 5.2, rawDt, elapsed);
    } else {
      // Teammate off-the-ball runs
      if (activePossessor !== 'orjasaeter' || ballPhys.inFlight) {
        const tgt = currentScenario.orjasaeterRun;
        moveAndOrientPlayer(orjasaeterMesh, tgt.x, tgt.z, tgt.speed, gameDt, elapsed);
      } else {
        animatePlayerLimbs(orjasaeterMesh, 0, elapsed, rawDt);
      }

      if (activePossessor !== 'weghorst' || ballPhys.inFlight) {
        const tgt = currentScenario.weghorstRun;
        moveAndOrientPlayer(weghorstMesh, tgt.x, tgt.z, tgt.speed, gameDt, elapsed);
      } else {
        animatePlayerLimbs(weghorstMesh, 0, elapsed, rawDt);
      }
    }
  }

  // Real-time 3D Ball Physics
  if (ballPhys.inFlight) {
    const speedXZ = Math.hypot(ballPhys.vel.x, ballPhys.vel.z) || 0.001;
    const perpX = -ballPhys.vel.z / speedXZ;
    const perpZ = ballPhys.vel.x / speedXZ;

    // Magnus curve force + air drag
    if (!ballPhys.inGoal) {
      const magnusAccel = ballPhys.spinY * 1.15;
      ballPhys.vel.x += perpX * magnusAccel * rawDt;
      ballPhys.vel.z += perpZ * magnusAccel * rawDt;
    }

    // Air resistance
    ballPhys.vel.multiplyScalar(Math.pow(0.92, rawDt));
    // Gravity
    ballPhys.vel.y -= 15.8 * rawDt;

    const prevZ = ballPhys.pos.z;
    ballPhys.pos.addScaledVector(ballPhys.vel, rawDt);

    // Ground bounce & grass rolling friction
    if (ballPhys.pos.y < ballRadius) {
      ballPhys.pos.y = ballRadius;
      if (Math.abs(ballPhys.vel.y) > 1.6) {
        ballPhys.vel.y = -ballPhys.vel.y * 0.52;
        ballPhys.vel.x *= 0.88;
        ballPhys.vel.z *= 0.88;
      } else {
        ballPhys.vel.y = 0;
        // Rolling turf friction
        ballPhys.vel.x *= Math.pow(0.28, rawDt);
        ballPhys.vel.z *= Math.pow(0.28, rawDt);
      }
    }

    ballMesh.position.copy(ballPhys.pos);
    ballMesh.rotation.x += (ballPhys.vel.z * 0.9) * rawDt;
    ballMesh.rotation.y += ballPhys.spinY * rawDt;
    ballMesh.rotation.z -= (ballPhys.vel.x * 0.9) * rawDt;

    // Update aerodynamic ribbon trail
    trailPoints.push(ballPhys.pos.clone());
    if (trailPoints.length > MAX_TRAIL) trailPoints.shift();
    trailLineGeo.setFromPoints(trailPoints);

    // Check Goalpost & Crossbar collisions near z = -45
    if (!ballPhys.inGoal && prevZ > goalZ - 0.4 && ballPhys.pos.z <= goalZ + 0.4) {
      const distPostL = Math.hypot(ballPhys.pos.x - (-goalWidth / 2), ballPhys.pos.z - goalZ);
      const distPostR = Math.hypot(ballPhys.pos.x - (goalWidth / 2), ballPhys.pos.z - goalZ);
      const distBar = Math.hypot(ballPhys.pos.y - goalHeight, ballPhys.pos.z - goalZ);

      if ((distPostL < ballRadius + pRadius && ballPhys.pos.y <= goalHeight) ||
          (distPostR < ballRadius + pRadius && ballPhys.pos.y <= goalHeight)) {
        ballPhys.vel.z = -ballPhys.vel.z * 0.65;
        ballPhys.vel.x = -ballPhys.vel.x * 0.7;
        setStatus("💥 OP DE PAAL! Wat een pech!", "#ffaa00");
      } else if (distBar < ballRadius + pRadius && Math.abs(ballPhys.pos.x) <= goalWidth / 2 + 0.2) {
        ballPhys.vel.z = -ballPhys.vel.z * 0.6;
        ballPhys.vel.y = Math.abs(ballPhys.vel.y) * 0.7 + 3.0;
        setStatus("💥 OP DE LAT! Bijna een wereldgoal!", "#ffaa00");
      }
    }

    // Check Goal Scoring & Net Containment
    if (!ballPhys.inGoal &&
        ballPhys.pos.z <= goalZ - 0.15 &&
        ballPhys.pos.z >= goalZ - goalDepth &&
        Math.abs(ballPhys.pos.x) < (goalWidth / 2 - 0.18) &&
        ballPhys.pos.y < (goalHeight - 0.12)) {

      ballPhys.inGoal = true;
      isChasingLooseBall = false;

      const scorer = activePossessor === 'orjasaeter' ? "Sondre Ørjasæter (11)" : "Wout Weghorst (9)";
      const star1 = true;
      const star2 = passCountInPlay >= 1;
      const star3 = ballPhys.pos.y > 2.0 || Math.abs(ballPhys.spinY) > 4.5 || Math.abs(ballPhys.pos.x) > 4.6;
      updateStarsUI(star1, star2, star3);

      setStatus(`🔴⚽ DO
