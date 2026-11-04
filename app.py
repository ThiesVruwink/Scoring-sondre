import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Twente: 3D Hero Moments",
    page_icon="⚽",
    layout="centered"
)

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 0.8rem;">
        <h1 style="color: #c90000; margin-bottom: 0.2rem;">🔴 FC Twente 3D: Hero Moments 🔵</h1>
        <p style="font-weight: 500; color: #666; margin: 0;">
            <b>Sondre Ørjasæter</b> & <b>Wout Weghorst</b> vs <b>SC Heerenveen</b>
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
    background-color: #0d1117;
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
    height: 720px;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 15px 40px rgba(0,0,0,0.7);
    background: #000;
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
  #hud-top {
    position: absolute;
    top: 14px;
    left: 14px;
    right: 14px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    z-index: 10;
  }
  .hud-badge {
    background: rgba(13, 17, 23, 0.85);
    backdrop-filter: blur(4px);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
  }
  #tactical-banner {
    position: absolute;
    top: 58px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(201, 0, 0, 0.9);
    padding: 6px 18px;
    border-radius: 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    pointer-events: none;
    z-index: 10;
  }
  #status-bubble {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(13, 17, 23, 0.92);
    padding: 10px 24px;
    border-radius: 25px;
    font-weight: 700;
    font-size: 14px;
    pointer-events: none;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0 6px 15px rgba(0,0,0,0.5);
    z-index: 10;
    text-align: center;
    max-width: 80%;
  }
  #btn-bar {
    margin-top: 10px;
    display: flex;
    gap: 12px;
  }
  .action-btn {
    background: #c90000;
    color: white;
    border: none;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 3px 8px rgba(0,0,0,0.4);
    transition: background 0.2s;
  }
  .action-btn:hover {
    background: #e60000;
  }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="container">
  <div id="hud-top">
    <div class="hud-badge" id="hud-scenario">Scenario: 1 / 3</div>
    <div class="hud-badge" id="hud-score">FC Twente 1 - 0 Heerenveen</div>
  </div>
  <div id="tactical-banner">Cutback or Direct Blast</div>
  <canvas id="overlay-canvas" width="720" height="720"></canvas>
  <div id="status-bubble">Swipe to shoot immediately, or curve a pass to your teammate!</div>
</div>

<div id="btn-bar">
  <button class="action-btn" onclick="retryScenario()">↺ Retry Scenario</button>
  <button class="action-btn" onclick="nextScenario()">Next Scenario ➔</button>
</div>

<script>
// Canvas dimensions
const WIDTH = 720;
const HEIGHT = 720;

// Setup Three.js scene, camera, renderer
const container = document.getElementById('container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb); // Sky blue
scene.fog = new THREE.FogExp2(0x87ceeb, 0.012);

const camera = new THREE.PerspectiveCamera(45, WIDTH / HEIGHT, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(WIDTH, HEIGHT);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

// Setup 2D HUD Canvas for gesture drawing overlay
const overlay = document.getElementById('overlay-canvas');
const ctx = overlay.getContext('2d');

// Lights
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
dirLight.position.set(30, 60, 20);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 1024;
dirLight.shadow.mapSize.height = 1024;
dirLight.shadow.camera.near = 10;
dirLight.shadow.camera.far = 120;
dirLight.shadow.camera.left = -40;
dirLight.shadow.camera.right = 40;
dirLight.shadow.camera.top = 40;
dirLight.shadow.camera.bottom = -40;
scene.add(dirLight);

// Pitch setup (Pitch coordinates: X = lateral [-35 to +35], Z = goal is at Z = -45, midfield is Z = +45)
const pitchGeo = new THREE.PlaneGeometry(70, 95);
const pitchMat = new THREE.MeshLambertMaterial({ color: 0x2b8034 });
const pitch = new THREE.Mesh(pitchGeo, pitchMat);
pitch.rotation.x = -Math.PI / 2;
pitch.receiveShadow = true;
scene.add(pitch);

// Pitch mowing stripe pattern
for (let z = -40; z <= 40; z += 10) {
  const stripeGeo = new THREE.PlaneGeometry(70, 5);
  const stripeMat = new THREE.MeshLambertMaterial({ color: 0x26722e });
  const stripe = new THREE.Mesh(stripeGeo, stripeMat);
  stripe.rotation.x = -Math.PI / 2;
  stripe.position.set(0, 0.01, z);
  stripe.receiveShadow = true;
  scene.add(stripe);
}

// Pitch line markings helper
function createPitchLines() {
  const lineMat = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 });
  
  // Penalty area (x: -18 to 18, z: -45 to -27)
  const boxPts = [
    new THREE.Vector3(-18, 0.05, -45),
    new THREE.Vector3(-18, 0.05, -27),
    new THREE.Vector3(18, 0.05, -27),
    new THREE.Vector3(18, 0.05, -45)
  ];
  const boxGeo = new THREE.BufferGeometry().setFromPoints(boxPts);
  scene.add(new THREE.Line(boxGeo, lineMat));

  // 6-yard box
  const sixPts = [
    new THREE.Vector3(-9, 0.05, -45),
    new THREE.Vector3(-9, 0.05, -39),
    new THREE.Vector3(9, 0.05, -39),
    new THREE.Vector3(9, 0.05, -45)
  ];
  const sixGeo = new THREE.BufferGeometry().setFromPoints(sixPts);
  scene.add(new THREE.Line(sixGeo, lineMat));
  
  // Penalty Spot
  const spotGeo = new THREE.CircleGeometry(0.35, 16);
  const spotMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const spot = new THREE.Mesh(spotGeo, spotMat);
  spot.rotation.x = -Math.PI / 2;
  spot.position.set(0, 0.06, -34);
  scene.add(spot);
}
createPitchLines();

// 3D Goal Frame & Netting
const goalGroup = new THREE.Group();
const postMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.2 });
const postRad = 0.18;
const goalWidth = 14;
const goalHeight = 4.2;

// Left, right posts and crossbar
const pL = new THREE.Mesh(new THREE.CylinderGeometry(postRad, postRad, goalHeight, 16), postMat);
pL.position.set(-goalWidth/2, goalHeight/2, -45);
pL.castShadow = true;
goalGroup.add(pL);

const pR = new THREE.Mesh(new THREE.CylinderGeometry(postRad, postRad, goalHeight, 16), postMat);
pR.position.set(goalWidth/2, goalHeight/2, -45);
pR.castShadow = true;
goalGroup.add(pR);

const crossbar = new THREE.Mesh(new THREE.CylinderGeometry(postRad, postRad, goalWidth, 16), postMat);
crossbar.rotation.z = Math.PI / 2;
crossbar.position.set(0, goalHeight, -45);
crossbar.castShadow = true;
goalGroup.add(crossbar);

// Translucent goal net
const netMat = new THREE.MeshBasicMaterial({ color: 0xdddddd, wireframe: true, transparent: true, opacity: 0.4 });
const net = new THREE.Mesh(new THREE.BoxGeometry(goalWidth, goalHeight, 3.5), netMat);
net.position.set(0, goalHeight / 2, -46.75);
goalGroup.add(net);
scene.add(goalGroup);

// Ball mesh with shadow
const ballGeo = new THREE.SphereGeometry(0.42, 20, 20);
const ballMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });
const ballMesh = new THREE.Mesh(ballGeo, ballMat);
ballMesh.castShadow = true;
scene.add(ballMesh);

// Helper to create 3D Low-Poly Character
function create3DPlayer(shirtColor, isKeeper=false) {
  const group = new THREE.Group();

  // Torso / Jersey
  const torsoGeo = new THREE.CylinderGeometry(0.5, 0.4, 1.2, 8);
  const torsoMat = new THREE.MeshLambertMaterial({ color: shirtColor });
  const torso = new THREE.Mesh(torsoGeo, torsoMat);
  torso.position.y = 1.3;
  torso.castShadow = true;
  group.add(torso);

  // Shorts
  const shortsGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.5, 8);
  const shortsMat = new THREE.MeshLambertMaterial({ color: isKeeper ? 0x222222 : 0xffffff });
  const shorts = new THREE.Mesh(shortsGeo, shortsMat);
  shorts.position.y = 0.85;
  shorts.castShadow = true;
  group.add(shorts);

  // Head
  const headGeo = new THREE.SphereGeometry(0.3, 12, 12);
  const headMat = new THREE.MeshLambertMaterial({ color: 0xffdbac });
  const head = new THREE.Mesh(headGeo, headMat);
  head.position.y = 2.15;
  head.castShadow = true;
  group.add(head);

  // Legs
  const legMat = new THREE.MeshLambertMaterial({ color: 0xffdbac });
  const leftLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.7, 8), legMat);
  leftLeg.position.set(-0.2, 0.35, 0);
  leftLeg.castShadow = true;
  group.add(leftLeg);
  group.leftLeg = leftLeg;

  const rightLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.7, 8), legMat);
  rightLeg.position.set(0.2, 0.35, 0);
  rightLeg.castShadow = true;
  group.add(rightLeg);
  group.rightLeg = rightLeg;

  return group;
}

// Scenarios definition with continuous back-and-forth freedom
const SCENARIOS = [
  {
    title: "1. Flank Overload",
    match: "FC Twente 1 - 0 Heerenveen",
    banner: "Wout in the Box or Ørjasæter Angle",
    orjasaeterPos: { x: -14, z: -10 },
    orjasaeterRun: { x: -10, z: -24, speed: 0.045 },
    weghorstPos: { x: 3, z: -14 },
    weghorstRun: { x: 0, z: -29, speed: 0.035 },
    defenders: [
      { x: -5, z: -15, patrol: 3, speed: 0.03 },
      { x: 5, z: -25, patrol: 4, speed: 0.04 }
    ],
    keeper: { x: 0, z: -43.5, speed: 0.06, minX: -5.5, maxX: 5.5, dir: 1 },
    initialPossessor: 'orjasaeter'
  },
  {
    title: "2. Weghorst Target Hold-Up",
    match: "FC Twente 1 - 1 Heerenveen",
    banner: "Lay off to Sondre or Spin & Fire",
    orjasaeterPos: { x: -18, z: -5 },
    orjasaeterRun: { x: -8, z: -26, speed: 0.05 },
    weghorstPos: { x: 0, z: -16 },
    weghorstRun: { x: 2, z: -22, speed: 0.02 },
    defenders: [
      { x: 0, z: -21, patrol: 4, speed: 0.035 },
      { x: -9, z: -18, patrol: 3, speed: 0.04 },
      { x: 8, z: -28, patrol: 2, speed: 0.03 }
    ],
    keeper: { x: 0, z: -43.5, speed: 0.075, minX: -6, maxX: 6, dir: -1 },
    initialPossessor: 'weghorst'
  },
  {
    title: "3. Rapid Stoppage Counter",
    match: "FC Twente 2 - 2 Heerenveen",
    banner: "90th Min: Unlimited 1-2s to Goal",
    orjasaeterPos: { x: 12, z: -4 },
    orjasaeterRun: { x: 7, z: -28, speed: 0.06 },
    weghorstPos: { x: -4, z: -10 },
    weghorstRun: { x: -1, z: -32, speed: 0.04 },
    defenders: [
      { x: 4, z: -14, patrol: 5, speed: 0.045 },
      { x: -6, z: -22, patrol: 4, speed: 0.04 },
      { x: 5, z: -34, patrol: 3, speed: 0.05 }
    ],
    keeper: { x: 0, z: -43.5, speed: 0.08, minX: -6, maxX: 6, dir: 1 },
    initialPossessor: 'orjasaeter'
  }
];

let scenarioIdx = 0;
let currentScenario = null;
let activePossessor = 'orjasaeter'; // 'orjasaeter' or 'weghorst'

// 3D entities
let orjasaeterMesh = create3DPlayer(0xd40000); // Twente Red
let weghorstMesh = create3DPlayer(0xd40000);   // Twente Red
let keeperMesh = create3DPlayer(0xffba00, true); // GK Yellow
scene.add(orjasaeterMesh);
scene.add(weghorstMesh);
scene.add(keeperMesh);

let defenderMeshes = [];

// Ball Physics / Flight State
let ball3D = { x: 0, y: 0.42, z: 0 };
let isBallInFlight = false;
let flightTrajectory = []; // Array of {x, y, z}
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

  // Clean old defenders
  defenderMeshes.forEach(d => scene.remove(d.mesh));
  defenderMeshes = [];

  // Spawn Heerenveen Blue defenders
  currentScenario.defenders.forEach(def => {
    const mesh = create3DPlayer(0x1a5bb8);
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

  // Position GK
  keeperMesh.position.set(currentScenario.keeper.x, 0, currentScenario.keeper.z);

  // Position Attackers
  orjasaeterMesh.position.set(currentScenario.orjasaeterPos.x, 0, currentScenario.orjasaeterPos.z);
  weghorstMesh.position.set(currentScenario.weghorstPos.x, 0, currentScenario.weghorstPos.z);

  // Ball placed at feet of active carrier
  snapBallToCarrier();

  isBallInFlight = false;
  flightTrajectory = [];
  gesturePoints = [];

  // Update HUD
  document.getElementById('hud-scenario').innerText = `Scenario: ${scenarioIdx + 1} / ${SCENARIOS.length}`;
  document.getElementById('hud-score').innerText = currentScenario.match;
  document.getElementById('tactical-banner').innerText = currentScenario.banner;
  updateStatusInstruction();
}

function snapBallToCarrier() {
  const carrier = activePossessor === 'orjasaeter' ? orjasaeterMesh : weghorstMesh;
  ball3D.x = carrier.position.x;
  ball3D.y = 0.42;
  ball3D.z = carrier.position.z - 0.7; // just ahead
  ballMesh.position.set(ball3D.x, ball3D.y, ball3D.z);
}

function updateStatusInstruction() {
  const name = activePossessor === 'orjasaeter' ? "Ørjasæter" : "Weghorst";
  const other = activePossessor === 'orjasaeter' ? "Weghorst" : "Ørjasæter";
  setStatus(`⚽ ${name} has possession! Swipe directly at goal to score, or pass to ${other}!`, "#fff");
}

function retryScenario() {
  loadScenario(scenarioIdx);
}

function nextScenario() {
  loadScenario(scenarioIdx + 1);
}

// 2D to 3D Raycasting & Projection
const raycaster = new THREE.Raycaster();
const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);

function screenToWorld(screenX, screenY) {
  const mouse = new THREE.Vector2(
    (screenX / WIDTH) * 2 - 1,
    -(screenY / HEIGHT) * 2 + 1
  );
  raycaster.setFromCamera(mouse, camera);
  const intersectPoint = new THREE.Vector3();
  raycaster.ray.intersectPlane(groundPlane, intersectPoint);
  return intersectPoint;
}

function worldToScreen(worldVec) {
  const clone = worldVec.clone().project(camera);
  return {
    x: (clone.x + 1) * WIDTH / 2,
    y: (-clone.y + 1) * HEIGHT / 2
  };
}

// Swipe Drawing Logic (Score! Hero Arc)
let isSwiping = false;
let gesturePoints = []; // 2D points on overlay canvas

container.addEventListener('mousedown', (e) => {
  if (isBallInFlight) return;
  const rect = container.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  // Check if click started near the ball's projected screen position
  const ballScreen = worldToScreen(ballMesh.position);
  const dist = Math.hypot(mouseX - ballScreen.x, mouseY - ballScreen.y);

  if (dist < 60) {
    isSwiping = true;
    gesturePoints = [{ x: mouseX, y: mouseY }];
  }
});

window.addEventListener('mousemove', (e) => {
  if (!isSwiping) return;
  const rect = container.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  const lastPt = gesturePoints[gesturePoints.length - 1];
  if (Math.hypot(mouseX - lastPt.x, mouseY - lastPt.y) > 10) {
    gesturePoints.push({ x: mouseX, y: mouseY });
  }
});

window.addEventListener('mouseup', () => {
  if (isSwiping) {
    isSwiping = false;
    if (gesturePoints.length > 3) {
      executeTrajectory();
    } else {
      gesturePoints = [];
    }
  }
});

// Convert drawn 2D screen curve into realistic curved 3D trajectory with height elevation
function executeTrajectory() {
  flightTrajectory = [];
  const totalPts = gesturePoints.length;

  for (let i = 0; i < totalPts; i++) {
    const pt = gesturePoints[i];
    const worldPt = screenToWorld(pt.x, pt.y);
    if (!worldPt) continue;

    // Add arc height: parabolic lift based on path progress
    const t = i / (totalPts - 1);
    const maxHeight = 2.8 * Math.sin(t * Math.PI); // elevates up to 2.8m in mid-flight

    flightTrajectory.push({
      x: worldPt.x,
      y: 0.42 + maxHeight,
      z: worldPt.z
    });
  }

  // Subdivide trajectory for silky smooth flight
  const refined = [];
  for (let i = 0; i < flightTrajectory.length - 1; i++) {
    const p1 = flightTrajectory[i];
    const p2 = flightTrajectory[i + 1];
    const steps = 3;
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
}

// Tick Game Simulation
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  const elapsed = clock.getElapsedTime();

  // 1. Move Goalkeeper
  if (currentScenario && currentScenario.keeper) {
    const k = currentScenario.keeper;
    keeperMesh.position.x += k.speed * k.dir;
    if (keeperMesh.position.x > k.maxX || keeperMesh.position.x < k.minX) {
      k.dir *= -1;
    }
  }

  // 2. Animate Heerenveen Defenders (side-to-side zonal patrol)
  defenderMeshes.forEach(d => {
    d.mesh.position.x += d.speed * d.dir;
    if (Math.abs(d.mesh.position.x - d.startX) > d.patrol) {
      d.dir *= -1;
    }
    // subtle leg walk swing
    d.mesh.leftLeg.rotation.x = Math.sin(elapsed * 6) * 0.3;
    d.mesh.rightLeg.rotation.x = -Math.sin(elapsed * 6) * 0.3;
  });

  // 3. Move Attacking Players (Forward runs without ball)
  if (currentScenario) {
    // Ørjasæter movement
    if (activePossessor !== 'orjasaeter' || isBallInFlight) {
      const target = currentScenario.orjasaeterRun;
      orjasaeterMesh.position.x += (target.x - orjasaeterMesh.position.x) * target.speed;
      orjasaeterMesh.position.z += (target.z - orjasaeterMesh.position.z) * target.speed;
      orjasaeterMesh.leftLeg.rotation.x = Math.sin(elapsed * 8) * 0.4;
      orjasaeterMesh.rightLeg.rotation.x = -Math.sin(elapsed * 8) * 0.4;
    }

    // Weghorst movement (making runs into the box)
    if (activePossessor !== 'weghorst' || isBallInFlight) {
      const target = currentScenario.weghorstRun;
      weghorstMesh.position.x += (target.x - weghorstMesh.position.x) * target.speed;
      weghorstMesh.position.z += (target.z - weghorstMesh.position.z) * target.speed;
      weghorstMesh.leftLeg.rotation.x = Math.sin(elapsed * 7) * 0.35;
      weghorstMesh.rightLeg.rotation.x = -Math.sin(elapsed * 7) * 0.35;
    }
  }

  // 4. Ball In-Flight & Collision Checks
  if (isBallInFlight && flightTrajectory.length > 0) {
    flightProgress += 2; // Flight speed
    if (flightProgress < flightTrajectory.length) {
      const cur = flightTrajectory[flightProgress];
      ballMesh.position.set(cur.x, cur.y, cur.z);
      ballMesh.rotation.x -= 0.2; // spin

      // Defender Interceptions (only if ball is low enough, y < 1.6m)
      if (cur.y < 1.6) {
        for (const def of defenderMeshes) {
          const distDef = Math.hypot(cur.x - def.mesh.position.x, cur.z - def.mesh.position.z);
          if (distDef < 1.4) {
            isBallInFlight = false;
            setStatus("❌ Intercepted by Heerenveen! Try curving it wide or lofting it.", "#ff5555");
            setTimeout(retryScenario, 1300);
            return;
          }
        }
      }

      // Keeper Save Check
      const distGK = Math.hypot(cur.x - keeperMesh.position.x, cur.z - keeperMesh.position.z);
      if (distGK < 2.0 && cur.z < -41.5) {
        isBallInFlight = false;
        setStatus("🧤 Saved by the Keeper! Find the top corners!", "#ffaa00");
        setTimeout(retryScenario, 1300);
        return;
      }

    } else {
      // Reached trajectory end
      isBallInFlight = false;
      const endPos = flightTrajectory[flightTrajectory.length - 1];

      // A) Check for Direct Goal
      const insideGoalX = endPos.x > -goalWidth / 2 && endPos.x < goalWidth / 2;
      const insideGoalZ = endPos.z <= -44.5;
      const underBarY = endPos.y <= goalHeight + 0.3;

      if (insideGoalX && insideGoalZ && underBarY) {
        const scorer = activePossessor === 'orjasaeter' ? "Sondre Ørjasæter" : "Wout Weghorst";
        setStatus(`⚽ GOOOAL FOR FC TWENTE! Stunner by ${scorer}!`, "#00ff7f");
        celebrationCounter = 90;
        return;
      }

      // B) Check for Pass completion to Sondre Ørjasæter
      const distToOrj = Math.hypot(endPos.x - orjasaeterMesh.position.x, endPos.z - orjasaeterMesh.position.z);
      if (distToOrj < 3.2 && activePossessor !== 'orjasaeter') {
        activePossessor = 'orjasaeter';
        snapBallToCarrier();
        setStatus("🎯 Passed to Ørjasæter! Shoot instantly or pass back to Weghorst!", "#00ff7f");
        return;
      }

      // C) Check for Pass completion to Wout Weghorst
      const distToWeg = Math.hypot(endPos.x - weghorstMesh.position.x, endPos.z - weghorstMesh.position.z);
      if (distToWeg < 3.5 && activePossessor !== 'weghorst') {
        activePossessor = 'weghorst';
        snapBallToCarrier();
        setStatus("🎯 Reached Weghorst! Strike it home or pass it back!", "#00ff7f");
        return;
      }

      // D) Missed everything
      setStatus("❌ Missed target or went out of play. Retrying...", "#ff7777");
      setTimeout(retryScenario, 1100);
    }
  }

  // Goal celebration auto-advance
  if (celebrationCounter > 0) {
    celebrationCounter--;
    if (celebrationCounter === 1) nextScenario();
  }

  // 5. Dynamic 3D Camera Tracking (Score! Hero isometric perspective)
  const focalX = ballMesh.position.x * 0.3;
  const focalZ = ballMesh.position.z;
  camera.position.x = THREE.MathUtils.lerp(camera.position.x, focalX, 0.05);
  camera.position.y = THREE.MathUtils.lerp(camera.position.y, 22, 0.05);
  camera.position.z = THREE.MathUtils.lerp(camera.position.z, focalZ + 32, 0.05);
  camera.lookAt(focalX, 2.5, focalZ - 8);

  // Render Three.js 3D world
  renderer.render(scene, camera);

  // 6. Draw 2D Overlay HUD & Swipe Arc
  renderOverlay();
}

function renderOverlay() {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);

  // Player name indicators on 3D coordinates
  function drawTag(mesh, label, color) {
    const sPos = worldToScreen(new THREE.Vector3(mesh.position.x, 2.8, mesh.position.z));
    ctx.save();
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = color;
    ctx.shadowColor = 'rgba(0,0,0,0.9)';
    ctx.shadowBlur = 4;
    ctx.fillText(label, sPos.x, sPos.y);
    ctx.restore();
  }

  drawTag(orjasaeterMesh, "Ørjasæter", "#ffffff");
  drawTag(weghorstMesh, "Weghorst", "#ffffff");
  drawTag(keeperMesh, "Heerenveen GK", "#ffd700");

  // Highlight available pass target ring
  const targetMesh = activePossessor === 'orjasaeter' ? weghorstMesh : orjasaeterMesh;
  const ringPos = worldToScreen(new THREE.Vector3(targetMesh.position.x, 0.1, targetMesh.position.z));
  ctx.save();
  ctx.beginPath();
  ctx.arc(ringPos.x, ringPos.y, 22 + Math.sin(Date.now() / 200) * 3, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
  ctx.lineWidth = 2.5;
  ctx.setLineDash([6, 4]);
  ctx.stroke();
  ctx.restore();

  // Pulsing ring under the ball when ready to kick
  if (!isBallInFlight) {
    const ballScreen = worldToScreen(ballMesh.position);
    ctx.save();
    ctx.beginPath();
    ctx.arc(ballScreen.x, ballScreen.y, 16 + Math.sin(Date.now() / 200) * 3, 0, Math.PI * 2);
    ctx.strokeStyle = '#ffd700';
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.restore();
  }

  // Draw user's active curved swipe trajectory
  if (gesturePoints.length > 1) {
    ctx.save();
    ctx.strokeStyle = '#ffeb3b';
    ctx.lineWidth = 4.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.shadowColor = 'rgba(0,0,0,0.5)';
    ctx.shadowBlur = 4;

    ctx.beginPath();
    ctx.moveTo(gesturePoints[0].x, gesturePoints[0].y);
    for (let i = 1; i < gesturePoints.length; i++) {
      ctx.lineTo(gesturePoints[i].x, gesturePoints[i].y);
    }
    ctx.stroke();

    // Arrow pointer at head
    const last = gesturePoints[gesturePoints.length - 1];
    ctx.beginPath();
    ctx.arc(last.x, last.y, 6, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.restore();
  }
}

// Initial Boot
loadScenario(0);
requestAnimationFrame(animate);
</script>
</body>
</html>
"""

components.html(game_html, height=800, scrolling=False)

st.markdown(
    """
    ### ⚽ 3D Tactical Controls & Mechanics
    * **3D Trajectory & Curve:** Drag and swipe from the ball. The line lifts into a 3D arc, clearing lower challenges.
    * **Shoot or Pass-Back Freedom:** At any touch, you can curl a shot straight past the keeper into the top corners, or pass back and forth between **Wout Weghorst** and **Sondre Ørjasæter** as they make forward runs into the Heerenveen box.
    * **Dynamic Opponents:** Heerenveen defenders shift across passing lanes while the keeper tracks the angle along the goal line.
    """
)
