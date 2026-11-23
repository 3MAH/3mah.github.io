// Live TPMS morphing hero: the minimal surface (f = 0) meshed by marching cubes, drawn as an
// orange wireframe, continuously blending between surface families.
// Usage: <canvas class="tpms-hero__canvas" data-color="#ee7d30"></canvas>
// Options (data-*): colors="#a,#b,#c" (one colour per family, cycled),
// scale (object size), align="right" (push the object right on wide screens),
// fit="fill" (zoom so the whole mesh spans the canvas height, centred, behind the text),
// theme="page" (colours taken from the page, follows light/dark),
// periods (unit cells across the box), opacity (line opacity),
// background (fog colour, should match the backdrop).
import * as THREE from "three";
import { MarchingCubes } from "three/addons/objects/MarchingCubes.js";

const RES = 30;        // grid resolution (RES^3 samples): coarse = readable mesh
const PERIODS = 1.25;  // unit cells across the box
const HOLD = 2.2;      // seconds on each family
const BLEND = 2.6;     // seconds of morphing between two families

const { sin: s, cos: c } = Math;
const FAMILIES = [
  ["Gyroid", (x, y, z) => s(x) * c(y) + s(y) * c(z) + s(z) * c(x)],
  ["Schwarz P", (x, y, z) => c(x) + c(y) + c(z)],
  ["Schwarz D", (x, y, z) =>
    s(x) * s(y) * s(z) + s(x) * c(y) * c(z) + c(x) * s(y) * c(z) + c(x) * c(y) * s(z)],
  ["Neovius", (x, y, z) => 3 * (c(x) + c(y) + c(z)) + 4 * c(x) * c(y) * c(z)],
  ["Schoen IWP", (x, y, z) =>
    2 * (c(x) * c(y) + c(y) * c(z) + c(z) * c(x)) - (c(2 * x) + c(2 * y) + c(2 * z))],
  ["Fischer-Koch S", (x, y, z) =>
    c(2 * x) * s(y) * c(z) + c(x) * c(2 * y) * s(z) + s(x) * c(y) * c(2 * z)],
  ["Lidinoid", (x, y, z) =>
    0.5 * (s(2 * x) * c(y) * s(z) + s(2 * y) * c(z) * s(x) + s(2 * z) * c(x) * s(y))
    - 0.5 * (c(2 * x) * c(2 * y) + c(2 * y) * c(2 * z) + c(2 * z) * c(2 * x)) + 0.15],
];

// Sample every family once on the grid, normalized to unit amplitude.
function sampleFields(periods) {
  const n = RES ** 3;
  const k = (2 * Math.PI * periods) / (RES - 1);
  return FAMILIES.map(([, f]) => {
    const field = new Float32Array(n);
    let max = 0;
    for (let z = 0, i = 0; z < RES; z++)
      for (let y = 0; y < RES; y++)
        for (let x = 0; x < RES; x++, i++) {
          const v = f(x * k, y * k, z * k);
          field[i] = v;
          max = Math.max(max, Math.abs(v));
        }
    for (let i = 0; i < n; i++) field[i] /= max;
    return field;
  });
}

// A plain linear blend a + w (b - a) moves the surface in bursts: most grid points change side
// around the same w, which reads as a visual jump. Each point changes side at w* = a / (a - b);
// the quantiles of w* give the blend weight as a function of the swept volume fraction, so that
// the surface sweeps the box at a steady pace.
const STEPS = 64;
function paceTable(a, b) {
  const ws = [];
  for (let i = 0; i < a.length; i++) {
    if (a[i] * b[i] < 0) ws.push(a[i] / (a[i] - b[i]));
  }
  const sorted = Float32Array.from(ws).sort();
  const table = new Float32Array(STEPS + 1);
  for (let j = 1; j < STEPS; j++) {
    table[j] = sorted.length ? sorted[Math.floor((j / STEPS) * (sorted.length - 1))] : j / STEPS;
  }
  table[STEPS] = 1;
  return table;
}
const pace = (table, e) => {
  const x = Math.min(Math.max(e, 0), 1) * STEPS;
  const j = Math.min(Math.floor(x), STEPS - 1);
  return table[j] + (x - j) * (table[j + 1] - table[j]);
};

const fieldCache = new Map(); // periods -> { fields, tables }
const smooth = (t) => t * t * (3 - 2 * t);

function mount(canvas) {
  if (canvas.dataset.mounted) return;
  canvas.dataset.mounted = "1";
  const periods = Number(canvas.dataset.periods) || PERIODS;
  if (!fieldCache.has(periods)) {
    const sampled = sampleFields(periods);
    fieldCache.set(periods, {
      fields: sampled,
      tables: sampled.map((f, i) => paceTable(f, sampled[(i + 1) % sampled.length])),
    });
  }
  const { fields, tables } = fieldCache.get(periods);

  const palette = (canvas.dataset.colors || canvas.dataset.color || "#ee7d30")
    .split(",").map((h) => new THREE.Color(h.trim()));
  const color = palette[0].clone();
  const scale = Number(canvas.dataset.scale) || 0.82;
  const alignRight = canvas.dataset.align === "right";
  const fill = canvas.dataset.fit === "fill";
  const opacity = Number(canvas.dataset.opacity) || 0.7;
  const bg = new THREE.Color(canvas.dataset.background || "#0a1428");
  const label = canvas.parentElement.querySelector(".tpms-hero__label");

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: location.search.includes("snapshot") });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(bg, 3.2, 5.6); // depth cue: far lines fade out
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 20);
  camera.position.set(0, 0, 4.2);

  const material = new THREE.MeshBasicMaterial({
    color, wireframe: true, transparent: true, opacity, fog: true,
  });
  if (canvas.dataset.theme === "page") {
    // follow the page: line colour from CSS `color`, fade towards the page background
    const applyTheme = () => {
      palette[0].set(getComputedStyle(canvas).color);
      material.color.copy(palette[0]);
      scene.fog.color.set(getComputedStyle(document.body).backgroundColor);
    };
    applyTheme();
    new MutationObserver(applyTheme).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  }
  const mc = new MarchingCubes(RES, material, false, false, 200000);
  mc.isolation = 0;
  const group = new THREE.Group();
  group.add(mc);
  group.rotation.set(0.5, 0.6, 0);
  group.scale.setScalar(scale);
  scene.add(group);

  const resize = () => {
    const { clientWidth: w, clientHeight: h } = canvas;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    const halfH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.position.z;
    // fill: zoom so the mesh (projected half-size ~1.6 x scale) slightly overflows the canvas height
    camera.zoom = fill ? halfH / (1.0 * scale) : 1;
    camera.updateProjectionMatrix();
    if (alignRight) {
      // half-width of the view at the object's depth, minus half its height
      group.position.x = Math.max(0, Math.min(1.9, (halfH * camera.aspect - halfH) * 0.9));
    }
  };
  new ResizeObserver(resize).observe(canvas);
  resize();

  // Gentle parallax with the pointer
  let tx = 0, ty = 0;
  canvas.parentElement.addEventListener("pointermove", (e) => {
    const r = canvas.getBoundingClientRect();
    tx = ((e.clientX - r.left) / r.width - 0.5) * 0.6;
    ty = ((e.clientY - r.top) / r.height - 0.5) * 0.4;
  });

  const field = mc.field;
  const update = (time) => {
    const cycle = HOLD + BLEND;
    const step = Math.floor(time / cycle);
    const a = step % FAMILIES.length;
    const b = (a + 1) % FAMILIES.length;
    const local = time - step * cycle;
    const e = local < HOLD ? 0 : smooth((local - HOLD) / BLEND); // eased progress
    const w = pace(tables[a], e);                                // blend weight
    const fa = fields[a], fb = fields[b];
    for (let i = 0; i < field.length; i++) {
      const v = fa[i] + w * (fb[i] - fa[i]);
      field[i] = v; // level set f = 0: the minimal surface itself
    }
    mc.update();
    if (palette.length > 1) {
      material.color.copy(palette[a % palette.length]).lerp(palette[b % palette.length], e);
    }
    if (label) label.textContent = e < 0.5 ? FAMILIES[a][0] : FAMILIES[b][0];
  };

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);

  const clock = new THREE.Clock();
  let t = Number(new URLSearchParams(location.search).get("t")) || 0; // ?t= for snapshots
  const frame = () => {
    if (!canvas.isConnected) { renderer.dispose(); return; } // page changed
    requestAnimationFrame(frame);
    if (!visible) return;
    const dt = Math.min(clock.getDelta(), 0.1);
    if (!reduced) t += dt;
    update(t);
    group.rotation.y += reduced ? 0 : dt * 0.12;
    group.rotation.x += (0.5 + ty - group.rotation.x) * 0.04;
    group.rotation.z += (tx * 0.3 - group.rotation.z) * 0.04;
    renderer.render(scene, camera);
  };
  frame();
}

const init = () => document.querySelectorAll(".tpms-hero__canvas").forEach(mount);
if (window.document$) window.document$.subscribe(init); // instant navigation
else init();
