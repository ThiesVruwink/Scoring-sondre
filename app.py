import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FC Twente Hero 3D - Realistic Edition",
    page_icon="⚽",
    layout="centered"
)

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 0.6rem;">
        <h1 style="color: #c90000; margin: 0; font-size: 1.8rem; letter-spacing: -0.5px;">
            🔴 FC Twente 3D: Hero Matchday 🔵
        </h1>
        <p style="font-weight: 600; color: #555; margin-top: 0.2rem; font-size: 0.95rem;">
            Sondre Ørjasæter (27) & Wout Weghorst (9) vs SC Heerenveen
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
<style>
  body {
    margin: 0;
    padding: 0;
    background-color: #0b0f14;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    user-select: none;
    -webkit-user-select: none;
    overflow: hidden;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  #container {
    position: relative;
    width: 720px;
    height: 740px;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.85);
    background: #05080c;
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
  #broadcast-hud {
    position: absolute;
    top: 14px;
    left: 14px;
    right: 14px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    z-index: 10;
  }
  .score-bug {
    background: linear-gradient(135deg, rgba(20,24,33,0.92), rgba(10,12,18,0.95));
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 8px;
    display: flex;
    align-items: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    overflow: hidden;
  }
  .score-team {
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.5px;
  }
  .score-twente { background: #b80000; color: #fff; }
  .score-heerenveen { background: #004494; color: #fff; }
  .score-val {
    padding: 6px 12px;
    font-size: 15px;
    font-weight: 900;
    background: #11151c;
    color: #fff;
    min-width: 44px;
    text-align: center;
  }
  .hud-badge {
    background: rgba(15, 20, 28, 0.9);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    gap: 6px;
  }
  #tactical-banner {
    position: absolute;
    top: 64px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(90deg, rgba(184,0,0,0.95), rgba(140,0,0,0.95));
    border: 1px solid rgba(255,255,255,0.25);
    padding: 5px 20px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
    pointer-events: none;
    z-index: 10;
  }
  #status-bubble {
    position: absolute;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(12, 16, 24, 0.94);
    backdrop-filter: blur(8px);
    padding: 10px 24px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 13px;
    pointer-events: none;
    border: 1px solid rgba(255,255,255,0.22);
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    z-index: 10;
    text-align: center;
    white-space: nowrap;
    transition: all 0.25s ease;
  }
  #btn-bar {
    margin-top: 10px;
    display: flex;
    gap: 12px;
  }
  .action-btn {
    background: #b80000;
    color: white;
    border: none;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 3px 8px rgba(0,0,0,0.4);
    transition: background 0.15s, transform 0.1s;
  }
  .action-btn:hover {
    background: #dc0000;
    transform: translateY(-1px);
  }
  .action-btn:active {
    transform: translateY(1px);
  }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="container">
  <div id="broadcast-hud">
    <div class="score-bug">
      <div class="score-team score-twente">TWE</div>
      <div class="score-val" id="hud-score">1 - 0</div>
      <div class="score-team score-heerenveen">HEE</div>
    </div>
    <div class="hud-badge" id="hud-scenario">
      <span style="color:#00e676;">●</span> SCENARIO 1 / 3
    </div>
  </div>
  <div id="tactical-banner">Cutback Cross & Box Domination</div>
  <canvas id="overlay-canvas" width="720" height="740"></canvas>
  <div id="status-bubble">Swipe to shoot immediately or bend a pass to your teammate!</div>
</div>

<div id="btn-bar">
  <button class="action-btn" onclick="retryScenario()">↺ Retry Touch</button>
  <button class="action-btn" onclick="nextScenario()">Next Scenario ➔</button>
</div>

<script>
const WIDTH = 720;
const HEIGHT = 740;

const container = document.getElementById('container');
const scene = new THREE.Scene();

// Atmosphere & Sky
scene.background = new THREE.Color(0x0e141d);
scene.fog = new THREE.FogExp2(0x0e141d, 0.009);

const camera = new THREE.PerspectiveCamera(42, WIDTH / HEIGHT, 0.1, 800);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(WIDTH, HEIGHT);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
container.appendChild(renderer.domElement);

const overlay = document.getElementById('overlay-canvas');
const ctx = overlay.getContext('2d');

// Lighting: 4 Stadium Floodlights + Sun fill
const hemiLight = new THREE.HemisphereLight(0xe8f0f8, 0x1b301c, 0.55);
scene.add(hemiLight);

const mainFlood = new THREE.DirectionalLight(0xffffff, 1.1);
mainFlood.position.set(25, 45, 10);
mainFlood.castShadow = true;
mainFlood.shadow.mapSize.width = 2048;
mainFlood.shadow.mapSize.height = 2048;
mainFlood.shadow.camera.near = 10;
mainFlood.shadow.camera.far = 130;
mainFlood.shadow.camera.left = -40;
mainFlood.shadow.camera.right = 40;
mainFlood.shadow.camera.top = 40;
mainFlood.shadow.camera.bottom = -40;
mainFlood.shadow.bias = -0.0005;
scene.add(mainFlood);

const fillLight = new THREE.DirectionalLight(0x7ea0d4, 0.45);
fillLight.position.set(-30, 30, -25);
scene.add(fillLight);

// Procedural Grass & Striping Texture
function createGrassTexture() {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 512;
  const cx = c.getContext('2d');
  cx.fillStyle = '#2b7a32';
  cx.fillRect(0, 0, 512, 512);

  // Micro blade noise
  for (let i = 0; i < 40000; i++) {
    const x = Math.random() * 512;
    const y = Math.random() * 512;
    const g = 100 + Math.random() * 40;
    cx.fillStyle = `rgb(${g * 0.35}, ${g}, ${g * 0.4})`;
    cx.fillRect(x, y, 1.5, 2.5);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(16, 24);
  return tex;
}

// Procedural Football Texture (Pentagons)
function createBallTexture() {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 256;
  const cx = c.getContext('2d');
  cx.fillStyle = '#f5f5f5';
  cx.fillRect(0, 0, 512, 256);

  cx.fillStyle = '#111111';
  for (let y = 30; y < 256; y += 75) {
    for (let x = (y % 150 === 30 ? 30 : 100); x < 512; x += 140) {
      cx.beginPath();
      for (let p = 0; p < 5; p++) {
        const a = (p * 2 * Math.PI) / 5 - Math.PI / 2;
        const px = x + 20 * Math.cos(a);
        const py = y + 20 * Math.sin(a);
        if (p === 0) cx.moveTo(px, py);
        else cx.lineTo(px, py);
      }
      cx.closePath();
      cx.fill();
    }
  }
  return new THREE.CanvasTexture(c);
}

// Pitch Setup
const pitchGeo = new THREE.PlaneGeometry(68, 100);
const pitchMat = new THREE.MeshStandardMaterial({
  color: 0x247a2d,
  roughness: 0.85,
  metalness: 0.05,
  map: createGrassTexture()
});
const pitch = new THREE.Mesh(pitchGeo, pitchMat);
pitch.rotation.x = -Math.PI / 2;
pitch.receiveShadow = true;
scene.add(pitch);

// Pitch Cut Stripes
for (let z = -45; z <= 45; z += 9) {
  const sGeo = new THREE.PlaneGeometry(68, 4.5);
  const sMat = new THREE.MeshStandardMaterial({
    color: 0x1f6d27,
    roughness: 0.9,
    transparent: true,
    opacity: 0.45
  });
  const stripe = new THREE.Mesh(sGeo, sMat);
  stripe.rotation.x = -Math.PI / 2;
  stripe.position.set(0, 0.02, z);
  stripe.receiveShadow = true;
  scene.add(stripe);
}

// White Pitch Markings
function buildPitchLines() {
  const lineMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.85 });

  function addPoly(pts) {
    const geo = new THREE.BufferGeometry().setFromPoints(pts);
    scene.add(new THREE.Line(geo, lineMat));
  }

  // 18-yard box (x: -18 to 18, z: -45 to -27)
  addPoly([
    new THREE.Vector3(-18, 0.05, -45),
    new THREE.Vector3(-18, 0.05, -27),
    new THREE.Vector3(18, 0.05, -27),
    new THREE.Vector3(18, 0.05, -45)
  ]);

  // 6-yard box
  addPoly([
    new THREE.Vector3(-8.5, 0.05, -45),
    new THREE.Vector3(-8.5, 0.05, -39.5),
    new THREE.Vector3(8.5, 0.05, -39.5),
    new THREE.Vector3(8.5, 0.05, -45)
  ]);

  // Goal line & sidelines
  addPoly([
    new THREE.Vector3(-30, 0.05, -45),
    new THREE.Vector3(30, 0.05, -45),
    new THREE.Vector3(30, 0.05, 45),
    new THREE.Vector3(-30, 0.05, 45),
    new THREE.Vector3(-30, 0.05, -45)
  ]);

  // Penalty Spot
  const spot = new THREE.Mesh(
    new THREE.CircleGeometry(0.32, 24),
    new THREE.MeshBasicMaterial({ color: 0xffffff })
  );
  spot.rotation.x = -Math.PI / 2;
  spot.position.set(0, 0.06, -34);
  scene.add(spot);
}
buildPitchLines();

// Realistic 3D Goal with Hexagonal Net
const goalWidth = 14.2;
const goalHeight = 4.4;
const goalZ = -45;
const goalGroup = new THREE.Group();

const postMat = new THREE.MeshStandardMaterial({
  color: 0xf5f5f5,
  metalness: 0.4,
  roughness: 0.25
});
const pRadius = 0.16;

const postL = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalHeight, 20), postMat);
postL.position.set(-goalWidth / 2, goalHeight / 2, goalZ);
postL.castShadow = true;
goalGroup.add(postL);

const postR = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalHeight, 20), postMat);
postR.position.set(goalWidth / 2, goalHeight / 2, goalZ);
postR.castShadow = true;
goalGroup.add(postR);

const bar = new THREE.Mesh(new THREE.CylinderGeometry(pRadius, pRadius, goalWidth, 20), postMat);
bar.rotation.z = Math.PI / 2;
bar.position.set(0, goalHeight, goalZ);
bar.castShadow = true;
goalGroup.add(bar);

// Back support bars
const backBarL = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 4.5), postMat);
backBarL.position.set(-goalWidth/2, 2.2, goalZ - 2.2);
backBarL.rotation.x = Math.PI / 4;
goalGroup.add(backBarL);

const backBarR = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 4.5), postMat);
backBarR.position.set(goalWidth/2, 2.2, goalZ - 2.2);
backBarR.rotation.x = Math.PI / 4;
goalGroup.add(backBarR);

// Realistic Goal Netting
const netMat = new THREE.MeshBasicMaterial({
  color: 0xcccccc,
  wireframe: true,
  transparent: true,
  opacity: 0.35
});
const netBox = new THREE.Mesh(new THREE.BoxGeometry(goalWidth, goalHeight, 3.8), netMat);
netBox.position.set(0, goalHeight / 2, goalZ - 1.9);
goalGroup.add(netBox);
scene.add(goalGroup);

// Ball Mesh with Physics Rig
const ballRadius = 0.42;
const ballGeo = new THREE.SphereGeometry(ballRadius, 32, 32);
const ballMat = new THREE.MeshStandardMaterial({
  map: createBallTexture(),
  roughness: 0.25,
  metalness: 0.1
});
const ballMesh = new THREE.Mesh(ballGeo, ballMat);
ballMesh.castShadow = true;
scene.add(ballMesh);

// Player Builder: Proportioned Rig with Limbs, Head, Hair & Boots
function createRealisticPlayer(primaryColor, shortsColor, skinColor=0xf5c39e, isGK=false) {
  const root = new THREE.Group();

  // Materials
  const jerseyMat = new THREE.MeshStandardMaterial({ color: primaryColor, roughness: 0.6 });
  const shortsMat = new THREE.MeshStandardMaterial({ color: shortsColor, roughness: 0.65 });
  const skinMat = new THREE.MeshStandardMaterial({ color: skinColor, roughness: 0.8 });
  const bootMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.4 });
  const sockMat = new THREE.MeshStandardMaterial({ color: primaryColor, roughness: 0.7 });

  // Pelvis / Hips
  const hips = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.35, 0.4, 16), shortsMat);
  hips.position.y = 1.6;
  hips.castShadow = true;
  root.add(hips);

  // Chest / Torso
  const chest = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.4, 0.85, 16), jerseyMat);
  chest.position.y = 2.15;
  chest.castShadow = true;
  root.add(chest);

  // Neck & Head
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.26, 16, 16), skinMat);
  head.position.y = 2.82;
  head.castShadow = true;
  root.add(head);

  // Hair
  const hairMat = new THREE.MeshStandardMaterial({ color: isGK ? 0x2b1c11 : 0xd4a359, roughness: 0.9 });
  const hair = new THREE.Mesh(new THREE.SphereGeometry(0.27, 16, 16, 0, Math.PI * 2, 0, Math.PI * 0.55), hairMat);
  hair.position.y = 2.88;
  root.add(hair);

  // Arms (Jointed)
  function createArm(isLeft) {
    const armGroup = new THREE.Group();
    const sign = isLeft ? -1 : 1;
    armGroup.position.set(sign * 0.55, 2.45, 0);

    const shoulder = new THREE.Mesh(new THREE.SphereGeometry(0.14, 12, 12), jerseyMat);
    armGroup.add(shoulder);

    const bicep = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.1, 0.45, 12), skinMat);
    bicep.position.set(0, -0.25, 0);
    armGroup.add(bicep);

    const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.09, 0.45, 12), isGK ? jerseyMat : skinMat);
    forearm.position.set(0, -0.65, 0.05);
    armGroup.add(forearm);

    if (isGK) {
      // Goalkeeper Gloves
      const glove = new THREE.Mesh(new THREE.SphereGeometry(0.14, 12, 12), new THREE.MeshStandardMaterial({ color: 0x00ff88 }));
      glove.position.set(0, -0.9, 0.08);
      armGroup.add(glove);
    }
    return armGroup;
  }

  const leftArm = createArm(true);
  const rightArm = createArm(false);
  root.add(leftArm);
  root.add(rightArm);
  root.leftArm = leftArm;
  root.rightArm = rightArm;

  // Legs (Jointed)
  function createLeg(isLeft) {
    const legGroup = new THREE.Group();
    const sign = isLeft ? -1 : 1;
    legGroup.position.set(sign * 0.22, 1.45, 0);

    const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.13, 0.55, 12), skinMat);
    thigh.position.y = -0.28;
    thigh.castShadow = true;
    legGroup.add(thigh);

    const calf = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.1, 0.55, 12), sockMat);
    calf.position.y = -0.78;
    calf.castShadow = true;
    legGroup.add(calf);

    const boot = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.14, 0.42), bootMat);
    boot.position.set(0, -1.06, 0.08);
    boot.castShadow = true;
    legGroup.add(boot);

    return legGroup;
  }

  const leftLeg = createLeg(true);
  const rightLeg = createLeg(false);
  root.add(leftLeg);
  root.add(rightLeg);
  root.leftLeg = leftLeg;
  root.rightLeg = rightLeg;

  return root;
}

// Scenarios setup
const SCENARIOS = [
  {
    title: "1. Flank Overload & Box Finish",
    match: "1 - 0",
    banner: "Ørjasæter crosses or strikes; Weghorst attacks far post",
    orjasaeterPos: { x: -14, z: -12 },
    orjasaeterRun: { x: -8, z: -25, speed: 0.04 },
    weghorstPos: { x: 3, z: -15 },
    weghorstRun: { x: 1, z: -32, speed: 0.035 },
    defenders: [
      { x: -5, z: -17, patrol: 3.5, speed: 0.035 },
      { x: 5, z: -26, patrol: 4.0, speed: 0.04 }
    ],
    initialPossessor: 'orjasaeter'
  },
  {
    title: "2. Weghorst Target Hold-Up",
    match: "1 - 1",
    banner: "Wout holds up center-backs; lay off to Sondre or spin & shoot",
    orjasaeterPos: { x: -16, z: -8 },
    orjasaeterRun: { x: -6, z: -27, speed: 0.05 },
    weghorstPos: { x: 0, z: -16 },
    weghorstRun: { x: 2, z: -24, speed: 0.02 },
    defenders: [
      { x: 0, z: -22, patrol: 3.5, speed: 0.03 },
      { x: -8, z: -19, patrol: 4.0, speed: 0.04 },
      { x: 7, z: -29, patrol: 3.0, speed: 0.035 }
    ],
    initialPossessor: 'weghorst'
  },
  {
    title: "3. Stoppage-Time Decider",
    match: "2 - 2",
    banner: "90+2' Counter: Unlimited 1-2 passing combinations",
    orjasaeterPos: { x: 13, z: -6 },
    orjasaeterRun: { x: 6, z: -29, speed: 0.055 },
    weghorstPos: { x: -4, z: -12 },
    weghorstRun: { x: -1, z: -33, speed: 0.045 },
    defenders: [
      { x: 4, z: -16, patrol: 4.5, speed: 0.045 },
      { x: -6, z: -24, patrol: 4.0, speed: 0.04 },
      { x: 4, z: -35, patrol: 3.0, speed: 0.05 }
    ],
    initialPossessor: 'orjasaeter'
  }
];

let scenarioIdx = 0;
let currentScenario = null;
let activePossessor = 'orjasaeter';

// Realistic 3D Players
const orjasaeterMesh = createRealisticPlayer(0xcc0000, 0xffffff); // Red jersey, white shorts
const weghorstMesh = createRealisticPlayer(0xcc0000, 0xffffff);
weghorstMesh.scale.set(1.08, 1.08, 1.08); // Weghorst is 1.97m tall physical presence

// Heerenveen Keeper: Bright fluo jersey + black shorts
const keeperMesh = createRealisticPlayer(0x00ff77, 0x111111, 0xdfb490, true);

scene.add(orjasaeterMesh);
scene.add(weghorstMesh);
scene.add(keeperMesh);

let defenderMeshes = [];

// Reactive Goalkeeper State
const gkState = {
  homeX: 0,
  homeZ: -43.2,
  currentX: 0,
  currentY: 0,
  currentZ: -43.2,
  vx: 0,
  vy: 0,
  isDiving: false,
  diveProgress: 0,
  targetX: 0,
  targetY: 0
};

// Ball Trajectory State
let ball3D = { x: 0, y: ballRadius, z: 0 };
let isBallInFlight = false;
let flightTrajectory = [];
let flightProgress = 0;
let celebrationCounter = 0;

function setStatus(text, color="#fff") {
  const el = document.getElementById('status-bubble');
  el.innerText = text;
  el.style.color = color;
}

function loadScenario(idx) {
  scenarioIdx = idx % SCENARIOS.length;
  currentScenario = JSON.parse(JSON.stringify(SCENARIOS[scenarioIdx]));
  activePossessor = currentScenario.initialPossessor;

  // Clear previous defenders
  defenderMeshes.forEach(d => scene.remove(d.mesh));
  defenderMeshes = [];

  // Spawn Heerenveen (Blue/White striped colors)
  currentScenario.defenders.forEach(def => {
    const mesh = createRealisticPlayer(0x0a4ab8, 0xffffff);
    mesh.position.set(def.x, 0, def.z);
    mesh.rotation.y = Math.PI;
    scene.add(mesh);
    defenderMeshes.push({
      mesh: mesh,
      startX: def.x,
      z: def.z,
      patrol: def.patrol,
      speed: def.speed,
      dir: 1
    });
  });

  // Reset Goalkeeper state
  gkState.homeX = 0;
  gkState.homeZ = -43.2;
  gkState.currentX = 0;
  gkState.currentY = 0;
  gkState.currentZ = -43.2;
  gkState.isDiving = false;
  gkState.diveProgress = 0;
  keeperMesh.position.set(0, 0, gkState.homeZ);
  keeperMesh.rotation.set(0, 0, 0);

  // Position Twente Attackers
  orjasaeterMesh.position.set(currentScenario.orjasaeterPos.x, 0, currentScenario.orjasaeterPos.z);
  weghorstMesh.position.set(currentScenario.weghorstPos.x, 0, currentScenario.weghorstPos.z);

  snapBallToCarrier();

  isBallInFlight = false;
  flightTrajectory = [];
  gesturePoints = [];

  // Update HUD
  document.getElementById('hud-scenario').innerHTML = `<span style="color:#00e676;">●</span> SCENARIO ${scenarioIdx + 1} / ${SCENARIOS.length}`;
  document.getElementById('hud-score').innerText = currentScenario.match;
  document.getElementById('tactical-banner').innerText = currentScenario.banner;
  updateStatusInstruction();
}

function snapBallToCarrier() {
  const carrier = activePossessor === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
  ball3D.x = carrier.position.x;
  ball3D.y = ballRadius;
  ball3D.z = carrier.position.z - 0.75;
  ballMesh.position.set(ball3D.x, ball3D.y, ball3D.z);
}

function updateStatusInstruction() {
  const activeName = activePossessor === 'orjasaeter' ? "Sondre Ørjasæter (11)" : "Wout Weghorst (9)";
  const partner = activePossessor === 'orjasaeter' ? "Weghorst" : "Ørjasæter";
  setStatus(`⚽ ${activeName} on the ball. Swipe towards goal or pass back to ${partner}!`, "#ffffff");
}

function retryScenario() {
  loadScenario(scenarioIdx);
}

function nextScenario() {
  loadScenario(scenarioIdx + 1);
}

// Raycasting Screen <-> World
const raycaster = new THREE.Raycaster();
const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);

function screenToWorld(sx, sy) {
  const mouse = new THREE.Vector2((sx / WIDTH) * 2 - 1, -(sy / HEIGHT) * 2 + 1);
  raycaster.setFromCamera(mouse, camera);
  const intersect = new THREE.Vector3();
  raycaster.ray.intersectPlane(groundPlane, intersect);
  return intersect;
}

function worldToScreen(worldVec) {
  const clone = worldVec.clone().project(camera);
  return {
    x: (clone.x + 1) * WIDTH / 2,
    y: (-clone.y + 1) * HEIGHT / 2
  };
}

// Swipe Gesture Handler
let isSwiping = false;
let gesturePoints = [];

container.addEventListener('mousedown', (e) => {
  if (isBallInFlight) return;
  const rect = container.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  const ballScreen = worldToScreen(ballMesh.position);
  if (Math.hypot(mx - ballScreen.x, my - ballScreen.y) < 65) {
    isSwiping = true;
    gesturePoints = [{ x: mx, y: my }];
  }
});

window.addEventListener('mousemove', (e) => {
  if (!isSwiping) return;
  const rect = container.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  const last = gesturePoints[gesturePoints.length - 1];
  if (Math.hypot(mx - last.x, my - last.y) > 8) {
    gesturePoints.push({ x: mx, y: my });
  }
});

window.addEventListener('mouseup', () => {
  if (isSwiping) {
    isSwiping = false;
    if (gesturePoints.length > 3) {
      launchBallAlongGesture();
    } else {
      gesturePoints = [];
    }
  }
});

// Convert Swipe to 3D Parabolic Curve & Signal Goalkeeper
function launchBallAlongGesture() {
  flightTrajectory = [];
  const total = gesturePoints.length;

  for (let i = 0; i < total; i++) {
    const pt = gesturePoints[i];
    const wPt = screenToWorld(pt.x, pt.y);
    if (!wPt) continue;

    const t = i / (total - 1);
    // Parabolic height arc
    const arcHeight = 3.2 * Math.sin(t * Math.PI);

    flightTrajectory.push({
      x: wPt.x,
      y: ballRadius + arcHeight,
      z: wPt.z
    });
  }

  // Smooth interpolation
  const refined = [];
  for (let i = 0; i < flightTrajectory.length - 1; i++) {
    const p1 = flightTrajectory[i];
    const p2 = flightTrajectory[i + 1];
    const steps = 4;
    for (let s = 0; s < steps; s++) {
      const alpha = s / steps;
      refined.push({
        x: THREE.MathUtils.lerp(p1.x, p2.x, alpha),
        y: THREE.MathUtils.lerp(p1.y, p2.y, alpha),
        z: THREE.MathUtils.lerp(p1.z, p2.z, alpha)
      });
    }
  }
  refined.push(flightTrajectory[flightTrajectory.length - 1]);

  flightTrajectory = refined;
  flightProgress = 0;
  isBallInFlight = true;
  gesturePoints = [];

  // Reactive Goalkeeper AI Decision
  predictAndTriggerKeeperReaction();
}

// Reactive Goalkeeper AI: Intercept calculation
function predictAndTriggerKeeperReaction() {
  // Find where the trajectory crosses the goal line plane (z = -45)
  let arrivalPoint = null;
  for (let i = 0; i < flightTrajectory.length; i++) {
    const pt = flightTrajectory[i];
    if (pt.z <= -43.0) {
      arrivalPoint = pt;
      break;
    }
  }

  if (arrivalPoint && Math.abs(arrivalPoint.x) < (goalWidth / 2 + 1.5)) {
    // Shot is headed towards the net!
    gkState.targetX = THREE.MathUtils.clamp(arrivalPoint.x, -goalWidth / 2 + 0.5, goalWidth / 2 - 0.5);
    gkState.targetY = THREE.MathUtils.clamp(arrivalPoint.y, 0, goalHeight - 0.2);
    gkState.isDiving = true;
    gkState.diveProgress = 0;
  } else {
    // Pass or wide shot - GK repositions subtly to cut the near post angle
    const last = flightTrajectory[flightTrajectory.length - 1];
    gkState.targetX = THREE.MathUtils.clamp(last.x * 0.25, -3, 3);
    gkState.targetY = 0;
    gkState.isDiving = false;
  }
}

// Animation Clock & Game Tick
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  const elapsed = clock.getElapsedTime();

  // 1. Reactive Goalkeeper Physics & Animation
  updateGoalkeeperAI(delta, elapsed);

  // 2. Animate Heerenveen Defenders (Zonal patrol & limb swing)
  defenderMeshes.forEach(d => {
    d.mesh.position.x += d.speed * d.dir;
    if (Math.abs(d.mesh.position.x - d.startX) > d.patrol) {
      d.dir *= -1;
    }
    d.mesh.leftLeg.rotation.x = Math.sin(elapsed * 7) * 0.35;
    d.mesh.rightLeg.rotation.x = -Math.sin(elapsed * 7) * 0.35;
  });

  // 3. Dynamic Forward Runs for Attacking Players
  if (currentScenario) {
    if (activePossessor !== 'orjasaeter' || isBallInFlight) {
      const tgt = currentScenario.orjasaeterRun;
      orjasaeterMesh.position.x += (tgt.x - orjasaeterMesh.position.x) * tgt.speed;
      orjasaeterMesh.position.z += (tgt.z - orjasaeterMesh.position.z) * tgt.speed;
      orjasaeterMesh.leftLeg.rotation.x = Math.sin(elapsed * 9) * 0.45;
      orjasaeterMesh.rightLeg.rotation.x = -Math.sin(elapsed * 9) * 0.45;
    }
    if (activePossessor !== 'weghorst' || isBallInFlight) {
      const tgt = currentScenario.weghorstRun;
      weghorstMesh.position.x += (tgt.x - weghorstMesh.position.x) * tgt.speed;
      weghorstMesh.position.z += (tgt.z - weghorstMesh.position.z) * tgt.speed;
      weghorstMesh.leftLeg.rotation.x = Math.sin(elapsed * 8) * 0.4;
      weghorstMesh.rightLeg.rotation.x = -Math.sin(elapsed * 8) * 0.4;
    }
  }

  // 4. Ball Flight & Reactive Interception Checking
  if (isBallInFlight && flightTrajectory.length > 0) {
    flightProgress += 2;
    if (flightProgress < flightTrajectory.length) {
      const cur = flightTrajectory[flightProgress];
      ballMesh.position.set(cur.x, cur.y, cur.z);
      ballMesh.rotation.x -= 0.25;
      ballMesh.rotation.z += 0.08;

      // Defender Interceptions (low trajectory only)
      if (cur.y < 1.7) {
        for (const def of defenderMeshes) {
          const dDist = Math.hypot(cur.x - def.mesh.position.x, cur.z - def.mesh.position.z);
          if (dDist < 1.35) {
            isBallInFlight = false;
            setStatus("❌ Heerenveen defender clears the danger! Try bending it wide.", "#ff5555");
            setTimeout(retryScenario, 1300);
            return;
          }
        }
      }

      // Dynamic Goalkeeper Save Check (based on actual glove/hand reach in 3D)
      const distToGK = Math.hypot(cur.x - keeperMesh.position.x, cur.y - (keeperMesh.position.y + 1.8), cur.z - keeperMesh.position.z);
      if (distToGK < 1.75 && cur.z < -42.2) {
        isBallInFlight = false;
        setStatus("🧤 SENSATIONAL SAVE! The keeper leaped to tip it away!", "#ffb700");
        setTimeout(retryScenario, 1400);
        return;
      }

    } else {
      // End of flight
      isBallInFlight = false;
      const endPos = flightTrajectory[flightTrajectory.length - 1];

      // Direct Goal Evaluation
      const inGoalX = endPos.x > -goalWidth / 2 + 0.3 && endPos.x < goalWidth / 2 - 0.3;
      const inGoalZ = endPos.z <= -44.5;
      const inGoalY = endPos.y <= goalHeight + 0.2;

      if (inGoalX && inGoalZ && inGoalY) {
        const scorer = activePossessor === 'orjasaeter' ? "Sondre Ørjasæter" : "Wout Weghorst";
        setStatus(`⚽ GOOOAL FOR FC TWENTE! What a finish by ${scorer}!`, "#00ff77");
        celebrationCounter = 85;
        return;
      }

      // Check Pass Completion to Ørjasæter
      const distOrj = Math.hypot(endPos.x - orjasaeterMesh.position.x, endPos.z - orjasaeterMesh.position.z);
      if (distOrj < 3.2 && activePossessor !== 'orjasaeter') {
        activePossessor = 'orjasaeter';
        snapBallToCarrier();
        setStatus("🎯 Passed to Ørjasæter! Shoot first-time or play back to Weghorst!", "#00e676");
        return;
      }

      // Check Pass Completion to Weghorst
      const distWeg = Math.hypot(endPos.x - weghorstMesh.position.x, endPos.z - weghorstMesh.position.z);
      if (distWeg < 3.4 && activePossessor !== 'weghorst') {
        activePossessor = 'weghorst';
        snapBallToCarrier();
        setStatus("🎯 Found Weghorst! Fire past the keeper or return the 1-2 pass!", "#00e676");
        return;
      }

      setStatus("❌ Shot off target or pass misplaced. Retrying...", "#ff7777");
      setTimeout(retryScenario, 1100);
    }
  }

  if (celebrationCounter > 0) {
    celebrationCounter--;
    if (celebrationCounter === 1) nextScenario();
  }

  // 5. Broadcast Camera Tracking
  const camTgtX = ballMesh.position.x * 0.25;
  const camTgtZ = ballMesh.position.z;
  camera.position.x = THREE.MathUtils.lerp(camera.position.x, camTgtX, 0.05);
  camera.position.y = THREE.MathUtils.lerp(camera.position.y, 20.5, 0.05);
  camera.position.z = THREE.MathUtils.lerp(camera.position.z, camTgtZ + 30.5, 0.05);
  camera.lookAt(camTgtX, 2.0, camTgtZ - 8);

  renderer.render(scene, camera);
  renderOverlay();
}

// Dedicated Reactive Keeper Physics Engine
function updateGoalkeeperAI(delta, elapsed) {
  if (gkState.isDiving) {
    gkState.diveProgress = Math.min(1.0, gkState.diveProgress + delta * 2.8);
    const ease = Math.sin(gkState.diveProgress * Math.PI * 0.5);

    // Spring/Leap towards predicted intercept
    keeperMesh.position.x = THREE.MathUtils.lerp(gkState.homeX, gkState.targetX, ease);
    keeperMesh.position.y = Math.sin(gkState.diveProgress * Math.PI) * (gkState.targetY * 0.6);

    // Dynamic diving body tilt & outstretched arms
    const diveDir = Math.sign(gkState.targetX - gkState.homeX) || 1;
    keeperMesh.rotation.z = -diveDir * ease * 1.15;
    keeperMesh.leftArm.rotation.z = -diveDir * 1.6;
    keeperMesh.rightArm.rotation.z = -diveDir * 1.6;

  } else {
    // Lateral shuffle positioning
    keeperMesh.position.x = THREE.MathUtils.lerp(keeperMesh.position.x, gkState.targetX, 0.08);
    keeperMesh.position.y = THREE.MathUtils.lerp(keeperMesh.position.y, 0, 0.1);
    keeperMesh.rotation.z = THREE.MathUtils.lerp(keeperMesh.rotation.z, 0, 0.15);

    // Ready stance idle animation
    keeperMesh.leftArm.rotation.x = Math.sin(elapsed * 4) * 0.15 + 0.4;
    keeperMesh.rightArm.rotation.x = Math.sin(elapsed * 4) * 0.15 + 0.4;
  }
}

// 2D Tactical Overlay & Swipe Arc
function renderOverlay() {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);

  function drawPlayerBadge(mesh, name, number, color) {
    const sp = worldToScreen(new THREE.Vector3(mesh.position.x, 3.4, mesh.position.z));
    ctx.save();
    ctx.font = '800 11px sans-serif';
    ctx.textAlign = 'center';
    
    // Background pill
    const txt = `${number} ${name}`;
    const tw = ctx.measureText(txt).width + 14;
    ctx.fillStyle = 'rgba(10, 14, 20, 0.85)';
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(sp.x - tw / 2, sp.y - 12, tw, 18, 9);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.fillText(txt, sp.x, sp.y + 1);
    ctx.restore();
  }

  drawPlayerBadge(orjasaeterMesh, "Ørjasæter", "27", "#ff3333");
  drawPlayerBadge(weghorstMesh, "Weghorst", "9", "#ff3333");
  drawPlayerBadge(keeperMesh, "Heerenveen GK", "1", "#00ff88");

  // Pulsing Target Pass Ring
  const targetMesh = activePossessor === 'orjasaeter' ? weghorstMesh : orjasaeterMesh;
  const ringPos = worldToScreen(new THREE.Vector3(targetMesh.position.x, 0.1, targetMesh.position.z));
  ctx.save();
  ctx.beginPath();
  ctx.arc(ringPos.x, ringPos.y, 24 + Math.sin(Date.now() / 200) * 3, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
  ctx.lineWidth = 2.5;
  ctx.setLineDash([6, 5]);
  ctx.stroke();
  ctx.restore();

  // Active Ball Ready Indicator
  if (!isBallInFlight) {
    const bs = worldToScreen(ballMesh.position);
    ctx.save();
    ctx.beginPath();
    ctx.arc(bs.x, bs.y, 16 + Math.sin(Date.now() / 180) * 3, 0, Math.PI * 2);
    ctx.strokeStyle = '#ffeb3b';
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.restore();
  }

  // Draw User's Score! Hero Trajectory Curve
  if (gesturePoints.length > 1) {
    ctx.save();
    ctx.strokeStyle = '#ffd700';
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.shadowColor = 'rgba(0,0,0,0.6)';
    ctx.shadowBlur = 6;

    ctx.beginPath();
    ctx.moveTo(gesturePoints[0].x, gesturePoints[0].y);
    for (let i = 1; i < gesturePoints.length; i++) {
      ctx.lineTo(gesturePoints[i].x, gesturePoints[i].y);
    }
    ctx.stroke();

    const last = gesturePoints[gesturePoints.length - 1];
    ctx.beginPath();
    ctx.arc(last.x, last.y, 7, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.restore();
  }
}

// Initial Kick-off
loadScenario(0);
requestAnimationFrame(animate);
</script>
</body>
</html>
"""

components.html(game_html, height=830, scrolling=False)

st.markdown(
    """
    ### 🎮 Pro Broadcast & Goalkeeper Mechanics
    * **Reactive Goalkeeper AI:** The goalkeeper no longer patrols like a pendulum. When you release a shot, the AI calculates the arrival trajectory at the goal plane and physically dives or leaps toward the top/bottom corners.
    * **Beating the Keeper:** To score, bend the ball with severe curl away from his reach into the side netting or dip it over his outstretched gloves.
    * **Realistic 3D Rigs:** Authentic proportions, kit numbers (**27 Ørjasæter** and **9 Weghorst**), multi-jointed arms/legs, and procedural pitch bump textures.
    * **Fluid Freedom:** Retain full freedom to pass back and forth between Weghorst and Ørjasæter or strike directly on goal at any moment.
    """
)
