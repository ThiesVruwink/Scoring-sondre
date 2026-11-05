import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FC Twente Score! Hero 3D",
    page_icon="⚽",
    layout="centered",
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
        <h2 style="color: #d00000; margin: 0; font-size: 1.45rem; font-weight: 900;">
            🔴 FC Twente: Score! Hero 3D 🔵
        </h2>
        <p style="font-weight: 600; color: #666; margin-top: 0.1rem; font-size: 0.84rem;">
            Sondre Ørjasæter (11) & Wout Weghorst (9) vs SC Heerenveen • De Grolsch Veste
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

game_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<style>
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body {
    margin: 0; padding: 0; width: 100%;
    background-color: #080b10;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    user-select: none; -webkit-user-select: none;
    overflow-x: hidden; color: white;
    display: flex; flex-direction: column; align-items: center;
    touch-action: manipulation;
  }
  #container {
    position: relative; width: 100%; max-width: 680px;
    aspect-ratio: 1 / 1.08; border-radius: 14px; overflow: hidden;
    box-shadow: 0 16px 42px rgba(0,0,0,0.9), 0 0 0 1px rgba(255,255,255,0.1);
    background: #05080c; touch-action: none;
  }
  #three-canvas { display: block; width: 100%; height: 100%; }
  #overlay-canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5; }
  #slowmo-vignette {
    position: absolute; inset: 0; pointer-events: none; z-index: 4;
    background: radial-gradient(circle at center, transparent 58%, rgba(0, 180, 255, 0.16) 100%);
    box-shadow: inset 0 0 35px rgba(0,0,0,0.75); transition: opacity 0.35s ease; opacity: 1;
  }
  #broadcast-hud {
    position: absolute; top: 10px; left: 10px; right: 10px;
    display: flex; justify-content: space-between; align-items: center; pointer-events: none; z-index: 10;
  }
  .score-bug {
    background: linear-gradient(135deg, rgba(16,20,28,0.95), rgba(8,10,15,0.98));
    border: 1px solid rgba(255,255,255,0.2); border-radius: 7px;
    display: flex; align-items: center; box-shadow: 0 6px 16px rgba(0,0,0,0.6); overflow: hidden;
  }
  .score-team { padding: 5px 9px; font-size: 11px; font-weight: 900; }
  .score-twente { background: linear-gradient(180deg, #d80000, #9a0000); color: #fff; }
  .score-heerenveen { background: linear-gradient(180deg, #0055b3, #003675); color: #fff; }
  .score-val { padding: 5px 10px; font-size: 13px; font-weight: 900; background: #0f131a; color: #fff; min-width: 44px; text-align: center; }
  .score-clock { padding: 5px 8px; font-size: 11px; font-weight: 800; background: #1c222e; color: #00e676; border-left: 1px solid rgba(255,255,255,0.12); }
  .hud-right { display: flex; gap: 6px; align-items: center; }
  .star-box {
    background: rgba(12, 16, 24, 0.92); padding: 4px 10px; border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.18); font-size: 13px; letter-spacing: 2px;
  }
  .hud-badge {
    background: rgba(15, 20, 28, 0.92); padding: 5px 11px; border-radius: 14px;
    font-size: 11px; font-weight: 800; border: 1px solid rgba(255,255,255,0.2);
  }
  #tactical-banner {
    position: absolute; top: 46px; left: 50%; transform: translateX(-50%);
    background: linear-gradient(90deg, rgba(195,0,0,0.95), rgba(135,0,0,0.95));
    border: 1px solid rgba(255,255,255,0.28); padding: 4px 14px; border-radius: 10px;
    font-size: 10px; font-weight: 800; text-transform: uppercase; pointer-events: none; z-index: 10;
    white-space: nowrap; max-width: 92%; overflow: hidden; text-overflow: ellipsis;
  }
  #objectives-bar {
    position: absolute; top: 72px; left: 50%; transform: translateX(-50%);
    display: flex; gap: 6px; pointer-events: none; z-index: 10;
  }
  .obj-pill {
    background: rgba(10, 14, 22, 0.82); border: 1px solid rgba(255,255,255,0.16);
    padding: 2px 8px; border-radius: 8px; font-size: 9.5px; font-weight: 700; color: #cfd8e3;
  }
  .obj-pill.done { border-color: #ffd700; color: #ffd700; background: rgba(40, 34, 10, 0.88); }
  #status-bubble {
    position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
    background: rgba(10, 14, 22, 0.94); backdrop-filter: blur(8px);
    padding: 9px 16px; border-radius: 18px; font-weight: 700; font-size: 11.5px;
    pointer-events: none; border: 1px solid rgba(255,255,255,0.22);
    box-shadow: 0 8px 22px rgba(0,0,0,0.7); z-index: 10; text-align: center; width: 90%; max-width: 540px;
  }
  #btn-bar {
    width: 100%; max-width: 680px; margin-top: 10px; display: flex; justify-content: center; gap: 10px; padding-bottom: 10px;
  }
  .action-btn {
    flex: 1; max-width: 175px; background: linear-gradient(180deg, #cc0000, #990000);
    color: white; border: 1px solid rgba(255,255,255,0.2); padding: 10px 12px;
    font-size: 12px; font-weight: 800; border-radius: 9px; cursor: pointer; touch-action: manipulation;
  }
  .action-btn.secondary { background: linear-gradient(180deg, #1f2937, #111827); }
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
      <div class="hud-badge" id="hud-scenario"><span style="color:#00e676;">●</span> 1 / 3</div>
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

const hemiLight = new THREE.HemisphereLight(0xddeeff, 0x18301a, 0.55);
scene.add(hemiLight);

const mainFlood = new THREE.DirectionalLight(0xfffaf0, 1.25);
mainFlood.position.set(28, 52, 16);
mainFlood.castShadow = true;
mainFlood.shadow.mapSize.width = 2048;
mainFlood.shadow.mapSize.height = 2048;
mainFlood.shadow.bias = -0.0005;
scene.add(mainFlood);

const rimFlood = new THREE.DirectionalLight(0x88b4ff, 0.5);
rimFlood.position.set(-32, 38, -38);
scene.add(rimFlood);

function createGrassTexture() {
  const c = document.createElement('canvas');
  c.width = 512; c.height = 512;
  const cx = c.getContext('2d');
  cx.fillStyle = '#266e2c';
  cx.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 28000; i++) {
    const x = Math.random() * 512, y = Math.random() * 512, g = 92 + Math.random() * 42;
    cx.fillStyle = `rgb(${Math.floor(g * 0.34)}, ${Math.floor(g)}, ${Math.floor(g * 0.36)})`;
    cx.fillRect(x, y, 1.5, 2.5);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(8, 12);
  return tex;
}

function createTwenteKitTexture(numStr) {
  const c = document.createElement('canvas');
  c.width = 256; c.height = 256;
  const cx = c.getContext('2d');
  cx.fillStyle = '#c80000';
  cx.fillRect(0, 0, 256, 256);
  cx.fillStyle = '#ffffff';
  cx.fillRect(0, 0, 256, 16);
  if (numStr) {
    cx.font = '900 76px sans-serif';
    cx.textAlign = 'center';
    cx.textBaseline = 'middle';
    cx.fillText(numStr, 64, 125);
  }
  return new THREE.CanvasTexture(c);
}

function createHeerenveenKitTexture() {
  const c = document.createElement('canvas');
  c.width = 256; c.height = 256;
  const cx = c.getContext('2d');
  cx.fillStyle = '#ffffff';
  cx.fillRect(0, 0, 256, 256);
  cx.fillStyle = '#004b9b';
  for (let x = 0; x < 256; x += 42) cx.fillRect(x, 0, 21, 256);
  cx.fillStyle = '#d4001a';
  for (let y = 45; y < 230; y += 65) {
    for (let x = 31; x < 256; x += 42) {
      cx.beginPath();
      cx.arc(x - 3, y - 2, 4, 0, Math.PI * 2);
      cx.arc(x + 3, y - 2, 4, 0, Math.PI * 2);
      cx.moveTo(x - 6, y); cx.lineTo(x, y + 7); cx.lineTo(x + 6, y);
      cx.fill();
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
  cx.strokeStyle = '#d00000';
  cx.lineWidth = 6;
  cx.beginPath();
  for (let x = 0; x < 512; x += 64) {
    cx.moveTo(x, 0); cx.bezierCurveTo(x + 32, 128, x - 32, 128, x + 16, 256);
  }
  cx.stroke();
  cx.fillStyle = '#141820';
  for (let y = 36; y < 256; y += 85) {
    for (let x = (y % 170 === 36 ? 40 : 120); x < 512; x += 140) {
      cx.beginPath();
      for (let p = 0; p < 5; p++) {
        const a = (p * 2 * Math.PI) / 5 - Math.PI / 2;
        const px = x + 20 * Math.cos(a), py = y + 20 * Math.sin(a);
        if (p === 0) cx.moveTo(px, py); else cx.lineTo(px, py);
      }
      cx.closePath(); cx.fill();
    }
  }
  return new THREE.CanvasTexture(c);
}

const pitch = new THREE.Mesh(
  new THREE.PlaneGeometry(76, 110),
  new THREE.MeshStandardMaterial({ color: 0x2d8636, roughness: 0.86, map: createGrassTexture() })
);
pitch.rotation.x = -Math.PI / 2;
pitch.receiveShadow = true;
scene.add(pitch);

function buildPitchLines() {
  const lineMat = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
  function addStrip(x1, z1, x2, z2, w = 0.16) {
    const dx = x2 - x1, dz = z2 - z1, len = Math.hypot(dx, dz);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, len), lineMat);
    m.rotation.x = -Math.PI / 2;
    m.rotation.z = -Math.atan2(dx, dz);
    m.position.set((x1 + x2) / 2, 0.03, (z1 + z2) / 2);
    scene.add(m);
  }
  addStrip(-32, -45, 32, -45);
  addStrip(-20, -45, -20, -28.5);
  addStrip(20, -45, 20, -28.5);
  addStrip(-20, -28.5, 20, -28.5);
  addStrip(-9.2, -45, -9.2, -39.5);
  addStrip(9.2, -45, 9.2, -39.5);
  addStrip(-9.2, -39.5, 9.2, -39.5);
  const spot = new THREE.Mesh(new THREE.CircleGeometry(0.28, 20), lineMat);
  spot.rotation.x = -Math.PI / 2;
  spot.position.set(0, 0.035, -34);
  scene.add(spot);
}
buildPitchLines();

const goalWidth = 14.4, goalHeight = 4.5, goalDepth = 3.8, goalZ = -45;
const goalGroup = new THREE.Group();
const postMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.35, roughness: 0.2 });
const pRadius = 0.17;

const postL = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalHeight, 16), postMat);
postL.position.set(-goalWidth / 2, goalHeight / 2, goalZ);
goalGroup.add(postL);

const postR = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalHeight, 16), postMat);
postR.position.set(goalWidth / 2, goalHeight / 2, goalZ);
goalGroup.add(postR);

const crossbar = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalWidth + pRadius * 2, 16), postMat);
crossbar.rotation.z = Math.PI / 2;
crossbar.position.set(0, goalHeight, goalZ);
goalGroup.add(crossbar);

const netMat = new THREE.MeshStandardMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.5 });
const backNetGeo = new THREE.PlaneGeometry(goalWidth, goalHeight, 18, 10);
const backNetOrigPos = backNetGeo.attributes.position.clone();
const backNet = new THREE.Mesh(backNetGeo, netMat);
backNet.position.set(0, goalHeight / 2, goalZ - goalDepth);
goalGroup.add(backNet);

const roofNet = new THREE.Mesh(new THREE.PlaneGeometry(goalWidth, goalDepth), netMat);
roofNet.rotation.x = Math.PI / 2;
roofNet.position.set(0, goalHeight - 0.04, goalZ - goalDepth / 2);
goalGroup.add(roofNet);

scene.add(goalGroup);

let netRipple = { active: false, localX: 0, localY: 0, strength: 0, time: 0 };
function triggerNetRipple(worldX, worldY) {
  netRipple.active = true;
  netRipple.localX = THREE.MathUtils.clamp(worldX, -goalWidth / 2, goalWidth / 2);
  netRipple.localY = THREE.MathUtils.clamp(worldY - goalHeight / 2, -goalHeight / 2, goalHeight / 2);
  netRipple.strength = 1.35; netRipple.time = 0;
}
function updateNetRipple(dt) {
  if (!netRipple.active) return;
  netRipple.time += dt * 16;
  netRipple.strength *= Math.pow(0.12, dt);
  const posAttr = backNetGeo.attributes.position;
  for (let i = 0; i < posAttr.count; i++) {
    const ox = backNetOrigPos.getX(i), oy = backNetOrigPos.getY(i);
    const dist = Math.hypot(ox - netRipple.localX, oy - netRipple.localY);
    const wave = Math.exp(-dist * 0.45) * Math.sin(netRipple.time - dist * 0.9) * netRipple.strength;
    posAttr.setZ(i, -Math.abs(wave) * 0.65);
  }
  posAttr.needsUpdate = true;
  if (netRipple.strength < 0.02) netRipple.active = false;
}

const ballRadius = 0.42;
const ballMesh = new THREE.Mesh(
  new THREE.SphereGeometry(ballRadius, 24, 24),
  new THREE.MeshStandardMaterial({ map: createBallTexture(), roughness: 0.22 })
);
ballMesh.castShadow = true;
scene.add(ballMesh);

const previewDots = [];
const previewDotMat = new THREE.MeshBasicMaterial({ color: 0xffea00, transparent: true, opacity: 0.9 });
for (let i = 0; i < 24; i++) {
  const dot = new THREE.Mesh(new THREE.SphereGeometry(0.18 * (1 - (i / 28) * 0.5), 8, 8), previewDotMat);
  dot.visible = false;
  scene.add(dot);
  previewDots.push(dot);
}

function createProPlayer(opts) {
  const root = new THREE.Group();
  root.scale.set(opts.scale || 1, opts.scale || 1, opts.scale || 1);
  let jerseyMat, shortsMat, sockMat;
  if (opts.isGK) {
    jerseyMat = new THREE.MeshStandardMaterial({ color: 0x00e676, roughness: 0.55 });
    shortsMat = new THREE.MeshStandardMaterial({ color: 0x12161f, roughness: 0.65 });
    sockMat = new THREE.MeshStandardMaterial({ color: 0x00e676, roughness: 0.6 });
  } else if (opts.team === 'twente') {
    jerseyMat = new THREE.MeshStandardMaterial({ map: createTwenteKitTexture(opts.number), roughness: 0.55 });
    shortsMat = new THREE.MeshStandardMaterial({ color: 0xb80000, roughness: 0.6 });
    sockMat = new THREE.MeshStandardMaterial({ color: 0xcc0000, roughness: 0.65 });
  } else {
    jerseyMat = new THREE.MeshStandardMaterial({ map: createHeerenveenKitTexture(), roughness: 0.55 });
    shortsMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 });
    sockMat = new THREE.MeshStandardMaterial({ color: 0x003f8a, roughness: 0.65 });
  }
  const skinMat = new THREE.MeshStandardMaterial({ color: opts.skinColor || 0xf2c29b, roughness: 0.75 });
  const bootMat = new THREE.MeshStandardMaterial({ color: opts.bootColor || 0x111111, roughness: 0.35 });

  const bodyPivot = new THREE.Group();
  root.bodyPivot = bodyPivot;
  root.add(bodyPivot);

  const chest = new THREE.Mesh(new THREE.CylinderGeometry(0.52, 0.4, 0.9, 14), jerseyMat);
  chest.position.y = 2.16;
  chest.rotation.y = Math.PI / 2;
  bodyPivot.add(chest);

  const head = new THREE.Mesh(new THREE.SphereGeometry(0.26, 12, 12), skinMat);
  head.position.y = 2.86;
  bodyPivot.add(head);

  function makeArm(isLeft) {
    const g = new THREE.Group();
    g.position.set((isLeft ? -1 : 1) * 0.58, 2.48, 0);
    const m = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.09, 0.65, 8), skinMat);
    m.position.set(0, -0.4, 0);
    g.add(m);
    return g;
  }
  root.leftArm = makeArm(true);
  root.rightArm = makeArm(false);
  bodyPivot.add(root.leftArm); bodyPivot.add(root.rightArm);

  function makeLeg(isLeft) {
    const g = new THREE.Group();
    g.position.set((isLeft ? -1 : 1) * 0.22, 1.42, 0);
    const m = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.1, 0.95, 8), sockMat);
    m.position.y = -0.6;
    g.add(m);
    const boot = new THREE.Mesh(new THREE.BoxGeometry(0.21, 0.15, 0.44), bootMat);
    boot.position.set(0, -1.1, -0.09);
    g.add(boot);
    return g;
  }
  root.leftLeg = makeLeg(true);
  root.rightLeg = makeLeg(false);
  bodyPivot.add(root.leftLeg); bodyPivot.add(root.rightLeg);
  root.kickTimer = 0;
  return root;
}

const SCENARIOS = [
  {
    match: "1 - 0", clock: "34'",
    banner: "Steek Weghorst weg in de diepte of krul vanaf de vleugel",
    objectives: ["★ Scoor een doelpunt", "★ Assist van Ørjasæter", "★ Krul in de hoek"],
    orjasaeterPos: { x: -14, z: -13 },
    orjasaeterRun: { x: -7, z: -27, speed: 5.5 },
    weghorstPos: { x: 3.5, z: -16 },
    weghorstRun: { x: 1.0, z: -33.5, speed: 5.2 },
    defenders: [{ x: -5.5, z: -18.5, patrol: 3.8, speed: 3.6 }, { x: 4.5, z: -26.5, patrol: 4.2, speed: 3.9 }],
    initialPossessor: 'orjasaeter'
  },
  {
    match: "1 - 1", clock: "68'",
    banner: "Kaats op de diepgaande Ørjasæter of draai weg en schiet",
    objectives: ["★ Scoor een doelpunt", "★ Kaats / 1-2 combinatie", "★ Binnenkant paal / Kruising"],
    orjasaeterPos: { x: -15.5, z: -10 },
    orjasaeterRun: { x: -5.5, z: -31, speed: 6.4 },
    weghorstPos: { x: 0.5, z: -17 },
    weghorstRun: { x: 2.0, z: -26.5, speed: 4.2 },
    defenders: [{ x: 0.5, z: -22.5, patrol: 3.2, speed: 3.4 }, { x: -8.0, z: -20.5, patrol: 3.8, speed: 3.9 }],
    initialPossessor: 'weghorst'
  },
  {
    match: "2 - 2", clock: "90+3'",
    banner: "90+3' Winnende treffer: Splijt de Heerenveen-defensie open!",
    objectives: ["★ Scoor de 3-2", "★ Meerdaagse pass-aanval", "★ Bovenhoek (> 2.2m hoog)"],
    orjasaeterPos: { x: 14, z: -8 },
    orjasaeterRun: { x: 6.5, z: -30, speed: 6.6 },
    weghorstPos: { x: -4.5, z: -13.5 },
    weghorstRun: { x: -1.5, z: -34.5, speed: 5.6 },
    defenders: [{ x: 5.0, z: -17.5, patrol: 4.2, speed: 4.3 }, { x: -5.5, z: -24.5, patrol: 4.0, speed: 4.1 }],
    initialPossessor: 'orjasaeter'
  }
];

let scenarioIdx = 0, currentScenario = null, activePossessor = 'orjasaeter';
let passCountInPlay = 0, cameraMode = 'hero';

const orjasaeterMesh = createProPlayer({ team: 'twente', number: '11', scale: 0.99, bootColor: 0x00f0ff });
const weghorstMesh = createProPlayer({ team: 'twente', number: '9', scale: 1.09, bootColor: 0xff5500 });
const keeperMesh = createProPlayer({ team: 'heerenveen', isGK: true, scale: 1.04, bootColor: 0xffffff });
scene.add(orjasaeterMesh); scene.add(weghorstMesh); scene.add(keeperMesh);

let defenderMeshes = [];
const ballPhys = {
  pos: new THREE.Vector3(0, ballRadius, 0),
  vel: new THREE.Vector3(0, 0, 0),
  spinY: 0, inFlight: false, inGoal: false
};
const gkState = {
  homeX: 0, homeZ: -43.7, isDiving: false, diveProgress: 0,
  reactionDelay: 0.14, timeSinceShot: 0, diveStartX: 0, targetX: 0, targetY: 0
};
let looseBallChaser = null, isChasingLooseBall = false, celebrationCounter = 0, retryTimeout = null;

function setStatus(text, color="#ffffff") {
  const el = document.getElementById('status-bubble');
  el.innerText = text; el.style.color = color;
}
function updateStarsUI(s1, s2, s3) {
  const starEl = document.getElementById('hud-stars');
  starEl.innerText = (s1 ? "★" : "☆") + (s2 ? "★" : "☆") + (s3 ? "★" : "☆");
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
  if (retryTimeout) clearTimeout(retryTimeout);
  scenarioIdx = idx % SCENARIOS.length;
  currentScenario = JSON.parse(JSON.stringify(SCENARIOS[scenarioIdx]));
  activePossessor = currentScenario.initialPossessor;
  passCountInPlay = 0; celebrationCounter = 0;

  defenderMeshes.forEach(d => scene.remove(d.mesh));
  defenderMeshes = [];
  currentScenario.defenders.forEach(def => {
    const mesh = createProPlayer({ team: 'heerenveen', scale: 1.02 });
    mesh.position.set(def.x, 0, def.z);
    mesh.rotation.y = Math.PI;
    scene.add(mesh);
    defenderMeshes.push({ mesh: mesh, startX: def.x, startZ: def.z, patrol: def.patrol, speed: def.speed, dir: 1 });
  });

  gkState.isDiving = false; gkState.diveProgress = 0; gkState.timeSinceShot = 0;
  keeperMesh.position.set(0, 0, gkState.homeZ);
  orjasaeterMesh.position.set(currentScenario.orjasaeterPos.x, 0, currentScenario.orjasaeterPos.z);
  weghorstMesh.position.set(currentScenario.weghorstPos.x, 0, currentScenario.weghorstPos.z);

  looseBallChaser = null; isChasingLooseBall = false;
  ballPhys.inFlight = false; ballPhys.inGoal = false;
  ballPhys.vel.set(0, 0, 0);
  hidePreviewArc();
  snapBallToCarrier();

  document.getElementById('hud-scenario').innerHTML = `<span style="color:#00e676;">●</span> ${scenarioIdx + 1} / ${SCENARIOS.length}`;
  document.getElementById('hud-score').innerText = currentScenario.match;
  document.getElementById('hud-clock').innerText = currentScenario.clock;
  document.getElementById('tactical-banner').innerText = currentScenario.banner;
  document.getElementById('obj-1').innerText = currentScenario.objectives[0];
  document.getElementById('obj-2').innerText = currentScenario.objectives[1];
  document.getElementById('obj-3').innerText = currentScenario.objectives[2];
  updateStarsUI(false, false, false);
  const activeName = activePossessor === 'orjasaeter' ? "Sondre Ørjasæter (11)" : "Wout Weghorst (9)";
  setStatus(`⏱️ SLOW-MO: ${activeName} aan de bal. Veeg om te passen of te schieten!`, "#ffffff");
}

function snapBallToCarrier() {
  const carrier = activePossessor === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
  const angle = Math.atan2(-carrier.position.x, goalZ - carrier.position.z);
  carrier.rotation.y = angle;
  ballPhys.pos.set(carrier.position.x + Math.sin(angle) * 0.82, ballRadius, carrier.position.z + Math.cos(angle) * 0.82);
  ballMesh.position.copy(ballPhys.pos);
}

function retryScenario() { loadScenario(scenarioIdx); }
function nextScenario() { loadScenario(scenarioIdx + 1); }

const raycaster = new THREE.Raycaster();
const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
function screenToWorld(sx, sy) {
  const mouse = new THREE.Vector2((sx / viewWidth) * 2 - 1, -(sy / viewHeight) * 2 + 1);
  raycaster.setFromCamera(mouse, camera);
  const intersect = new THREE.Vector3();
  return raycaster.ray.intersectPlane(groundPlane, intersect) ? intersect : null;
}
function worldToScreen(worldVec) {
  const clone = worldVec.clone().project(camera);
  return { x: (clone.x + 1) * viewWidth / 2, y: (-clone.y + 1) * viewHeight / 2 };
}

let isSwiping = false, gesturePoints = [];
function getCoords(e) {
  const rect = container.getBoundingClientRect();
  const touch = e.touches ? e.touches[0] : (e.changedTouches ? e.changedTouches[0] : e);
  return { x: touch.clientX - rect.left, y: touch.clientY - rect.top };
}

function computeShotParameters() {
  if (gesturePoints.length < 3) return null;
  const endScreen = gesturePoints[gesturePoints.length - 1];
  const midScreen = gesturePoints[Math.floor(gesturePoints.length / 2)];
  const startW = ballPhys.pos.clone();
  const endW = screenToWorld(endScreen.x, endScreen.y);
  const midW = screenToWorld(midScreen.x, midScreen.y);
  if (!endW || !midW) return null;

  endW.x = THREE.MathUtils.clamp(endW.x, -30, 30);
  endW.z = THREE.MathUtils.clamp(endW.z, -47.5, 10);
  const dx = endW.x - startW.x, dz = endW.z - startW.z, dist = Math.hypot(dx, dz);
  if (dist < 1.8) return null;

  const toMidX = midW.x - startW.x, toMidZ = midW.z - startW.z;
  const bulge = toMidX * (dz / dist) - toMidZ * (dx / dist);
  const spinY = THREE.MathUtils.clamp(bulge * 2.4, -15, 15);

  const isShotOnGoal = endW.z <= -42.2 && Math.abs(endW.x) < (goalWidth / 2 + 2.5);
  const speed = isShotOnGoal ? THREE.MathUtils.clamp(22 + dist * 0.42, 25, 39) : THREE.MathUtils.clamp(16 + dist * 0.35, 17, 29);
  const flightTime = Math.max(0.32, dist / speed);
  const targetY = isShotOnGoal ? THREE.MathUtils.clamp((-43.2 - endW.z) * 0.85, 0.3, goalHeight - 0.35) : ballRadius;

  const vx = (dx - 0.5 * (-dz / dist) * (spinY * 1.15) * flightTime * flightTime) / flightTime;
  const vz = (dz - 0.5 * (dx / dist) * (spinY * 1.15) * flightTime * flightTime) / flightTime;
  const vy = (targetY - startW.y + 0.5 * 15.8 * flightTime * flightTime) / flightTime + (isShotOnGoal ? 0.85 : Math.min(2.6, dist * 0.08));

  return { vel: new THREE.Vector3(vx, vy, vz), spinY, flightTime, endW, isShotOnGoal };
}

function updatePreviewArc() {
  const p = computeShotParameters();
  if (!p) { hidePreviewArc(); return; }
  const pos = ballPhys.pos.clone(), vel = p.vel.clone();
  const dt = p.flightTime / previewDots.length;
  for (let i = 0; i < previewDots.length; i++) {
    const spXZ = Math.hypot(vel.x, vel.z) || 1;
    vel.x += (-vel.z / spXZ) * (p.spinY * 1.15) * dt;
    vel.z += (vel.x / spXZ) * (p.spinY * 1.15) * dt;
    vel.y -= 15.8 * dt;
    pos.addScaledVector(vel, dt);
    previewDots[i].position.copy(pos);
    previewDots[i].visible = true;
  }
}

function hidePreviewArc() {
  previewDots.forEach(d => d.visible = false);
}

function onTouchStart(e) {
  if (ballPhys.inFlight || isChasingLooseBall || celebrationCounter > 0) return;
  if (e.cancelable) e.preventDefault();
  const pos = getCoords(e);
  const bs = worldToScreen(ballMesh.position);
  if (Math.hypot(pos.x - bs.x, pos.y - bs.y) < 82) {
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
  const p = computeShotParameters();
  hidePreviewArc();
  gesturePoints = [];
  if (p) strikeBall(p);
}

container.addEventListener('touchstart', onTouchStart, { passive: false });
window.addEventListener('touchmove', onTouchMove, { passive: false });
window.addEventListener('touchend', onTouchEnd, { passive: false });
container.addEventListener('mousedown', onTouchStart);
window.addEventListener('mousemove', onTouchMove);
window.addEventListener('mouseup', onTouchEnd);

function strikeBall(p) {
  const carrier = activePossessor === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
  carrier.kickTimer = 0.42;
  ballPhys.vel.copy(p.vel);
  ballPhys.spinY = p.spinY;
  ballPhys.inFlight = true;
  ballPhys.inGoal = false;

  if (!p.isShotOnGoal) {
    const targetKey = activePossessor === 'orjasaeter' ? 'weghorst' : 'orjasaeter';
    const targetMesh = targetKey === 'weghorst' ? weghorstMesh : orjasaeterMesh;
    if (Math.hypot(p.endW.x - targetMesh.position.x, p.endW.z - targetMesh.position.z) < 21.0) {
      looseBallChaser = targetKey; isChasingLooseBall = true;
      setStatus(`🏃 Steekpass op maat! ${looseBallChaser === 'orjasaeter' ? "Ørjasæter" : "Weghorst"} sprint erheen!`, "#00f2ff");
    }
  } else {
    setStatus("🚀 Schot op doel!", "#ffe600");
  }

  gkState.timeSinceShot = 0;
  gkState.diveStartX = keeperMesh.position.x;
  if (p.isShotOnGoal) {
    gkState.targetX = THREE.MathUtils.clamp(p.endW.x * 0.85, -goalWidth / 2 + 0.9, goalWidth / 2 - 0.9);
    gkState.targetY = THREE.MathUtils.clamp(p.vel.y * 0.25, 0.4, goalHeight - 0.5);
    gkState.isDiving = true;
    gkState.diveProgress = 0;
  }
}

const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const rawDt = Math.min(clock.getDelta(), 0.05);
  const elapsed = clock.getElapsedTime();

  const isSlowMo = !ballPhys.inFlight && !isChasingLooseBall && celebrationCounter === 0;
  const gameDt = isSlowMo ? rawDt * 0.15 : rawDt;
  vignette.style.opacity = isSlowMo ? "1" : "0.2";

  updateNetRipple(rawDt);

  if (gkState.isDiving) {
    gkState.timeSinceShot += rawDt;
    if (gkState.timeSinceShot > 0.14) {
      gkState.diveProgress = Math.min(1.0, gkState.diveProgress + rawDt * 2.4);
      const ease = Math.sin(gkState.diveProgress * Math.PI * 0.5);
      keeperMesh.position.x = THREE.MathUtils.lerp(gkState.diveStartX, gkState.targetX, ease);
      keeperMesh.position.y = Math.sin(gkState.diveProgress * Math.PI) * 1.5;
      keeperMesh.rotation.z = -Math.sign(gkState.targetX - gkState.diveStartX) * ease * 1.15;
    }
  } else {
    keeperMesh.position.x = THREE.MathUtils.lerp(keeperMesh.position.x, ballPhys.pos.x * 0.28, 0.08);
  }

  defenderMeshes.forEach(d => {
    d.mesh.position.x += d.speed * d.dir * gameDt;
    if (Math.abs(d.mesh.position.x - d.startX) > d.patrol) d.dir *= -1;
  });

  if (currentScenario) {
    if (isChasingLooseBall) {
      const chaser = looseBallChaser === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
      chaser.position.x += (ballPhys.pos.x - chaser.position.x) * 9.0 * rawDt;
      chaser.position.z += (ballPhys.pos.z - chaser.position.z) * 9.0 * rawDt;
    } else {
      if (activePossessor !== 'orjasaeter' || ballPhys.inFlight) {
        orjasaeterMesh.position.x += (currentScenario.orjasaeterRun.x - orjasaeterMesh.position.x) * currentScenario.orjasaeterRun.speed * 0.18 * gameDt;
        orjasaeterMesh.position.z += (currentScenario.orjasaeterRun.z - orjasaeterMesh.position.z) * currentScenario.orjasaeterRun.speed * 0.18 * gameDt;
      }
      if (activePossessor !== 'weghorst' || ballPhys.inFlight) {
        weghorstMesh.position.x += (currentScenario.weghorstRun.x - weghorstMesh.position.x) * currentScenario.weghorstRun.speed * 0.18 * gameDt;
        weghorstMesh.position.z += (currentScenario.weghorstRun.z - weghorstMesh.position.z) * currentScenario.weghorstRun.speed * 0.18 * gameDt;
      }
    }
  }

  if (ballPhys.inFlight) {
    const spXZ = Math.hypot(ballPhys.vel.x, ballPhys.vel.z) || 1;
    if (!ballPhys.inGoal) {
      ballPhys.vel.x += (-ballPhys.vel.z / spXZ) * (ballPhys.spinY * 1.15) * rawDt;
      ballPhys.vel.z += (ballPhys.vel.x / spXZ) * (ballPhys.spinY * 1.15) * rawDt;
    }
    ballPhys.vel.y -= 15.8 * rawDt;
    ballPhys.pos.addScaledVector(ballPhys.vel, rawDt);

    if (ballPhys.pos.y < ballRadius) {
      ballPhys.pos.y = ballRadius;
      ballPhys.vel.y = Math.abs(ballPhys.vel.y) > 1.6 ? -ballPhys.vel.y * 0.52 : 0;
    }
    ballMesh.position.copy(ballPhys.pos);

    // Goal Check
    if (!ballPhys.inGoal && ballPhys.pos.z <= goalZ && Math.abs(ballPhys.pos.x) < goalWidth / 2 - 0.2 && ballPhys.pos.y < goalHeight) {
      ballPhys.inGoal = true;
      triggerNetRipple(ballPhys.pos.x, ballPhys.pos.y);
      const star1 = true, star2 = passCountInPlay >= 1, star3 = ballPhys.pos.y > 2.0 || Math.abs(ballPhys.spinY) > 4.5;
      updateStarsUI(star1, star2, star3);
      setStatus(`🔴⚽ GOOOAL FC TWENTE! Stunner!`, "#00ff88");
      celebrationCounter = 100;
    }

    if (ballPhys.inGoal && ballPhys.pos.z <= goalZ - goalDepth + ballRadius) {
      ballPhys.vel.set(0, 0, 0);
    }

    // Interception Check
    if (!ballPhys.inGoal && ballPhys.pos.y < 1.75) {
      for (const def of defenderMeshes) {
        if (Math.hypot(ballPhys.pos.x - def.mesh.position.x, ballPhys.pos.z - def.mesh.position.z) < 1.15) {
          ballPhys.inFlight = false; isChasingLooseBall = false;
          setStatus("❌ Onderschept door SC Heerenveen!", "#ff5555");
          retryTimeout = setTimeout(retryScenario, 1200);
          break;
        }
      }
    }

    // Pass Receive Check
    if (!ballPhys.inGoal && ballPhys.inFlight) {
      const recKey = activePossessor === 'orjasaeter' ? 'weghorst' : 'orjasaeter';
      const recMesh = recKey === 'weghorst' ? weghorstMesh : orjasaeterMesh;
      if (Math.hypot(ballPhys.pos.x - recMesh.position.x, ballPhys.pos.z - recMesh.position.z) < 2.25) {
        activePossessor = recKey; passCountInPlay++;
        ballPhys.inFlight = false; isChasingLooseBall = false;
        snapBallToCarrier();
        updateStarsUI(false, true, false);
        setStatus(`🎯 Aangenomen door ${activePossessor === 'orjasaeter' ? "Ørjasæter (11)" : "Weghorst (9)"}! Schiet of kaats!`, "#00ff9d");
      }
    }
  }

  if (celebrationCounter > 0) {
    celebrationCounter--;
    if (celebrationCounter === 1) nextScenario();
  }

  const focusX = ballMesh.position.x * 0.38, focusZ = Math.max(-38, ballMesh.position.z);
  camera.position.x = THREE.MathUtils.lerp(camera.position.x, cameraMode === 'hero' ? focusX : focusX + 16, 0.06);
  camera.position.y = THREE.MathUtils.lerp(camera.position.y, cameraMode === 'hero' ? 17.5 : 22.5, 0.06);
  camera.position.z = THREE.MathUtils.lerp(camera.position.z, focusZ + (cameraMode === 'hero' ? 27.5 : 22), 0.06);
  camera.lookAt(focusX * 0.5, 1.8, focusZ - 11);

  renderer.render(scene, camera);

  ctx.clearRect(0, 0, viewWidth, viewHeight);
  if (gesturePoints.length > 1) {
    ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 4.5; ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(gesturePoints[0].x, gesturePoints[0].y);
    for (let i = 1; i < gesturePoints.length; i++) ctx.lineTo(gesturePoints[i].x, gesturePoints[i].y);
    ctx.stroke();
  }
}

resizeCanvas();
loadScenario(0);
requestAnimationFrame(animate);
</script>
</body>
</html>"""

components.html(game_html, height=760, scrolling=False)

st.markdown(
    """
    ### ⚽ Score! Hero Gameplay Tips:
    * **Tactische Slow-Motion:** Zolang **Ørjasæter (11)** of **Weghorst (9)** de bal aan de voet heeft, vertraagt de tijd en zie je een **blauwe looproute** van je medespeler.
    * **3D-Voortraject & Curve:** Veeg met een boog vanaf de bal; de gele 3D-stippellijn laat zien hoe je pass of krulschot draait.
    * **Combinatievoetbal (☆☆☆):** Speel een assist in de loop voor de tweede ster en krul hem daarna in de kruising voor 3 sterren!
    """
)
