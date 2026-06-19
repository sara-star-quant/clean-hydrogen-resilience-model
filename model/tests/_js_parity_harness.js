// Headless harness that loads playground/microgrid_sim.js with a stub DOM via
// Node's built-in vm module, exposes the diplomacy math kernel, and prints
// JSON results for parity tests.
//
// Usage: node _js_parity_harness.js <fixturesJsonPath>
// Fixtures shape:
//   { mulberry32: [{seed: int, n: int}, ...],
//     combined_damping: [{shock: str, posture: [str], trust: {bloc: int}|null}, ...],
//     shock_distribution: [{posture: [str]}, ...] }
"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const repoRoot = path.resolve(__dirname, "..", "..");
const htmlPath = path.join(repoRoot, "playground", "microgrid_sim.html");
const jsPath = path.join(repoRoot, "playground", "microgrid_sim.js");

const html = fs.readFileSync(htmlPath, "utf8");
const js = fs.readFileSync(jsPath, "utf8");

const m = html.match(
  /<script type="application\/json" id="diplomacy-constants">([\s\S]*?)<\/script>/,
);
if (!m) {
  console.error("diplomacy-constants block not found");
  process.exit(2);
}
const constantsJson = m[1];

// Stub minimal DOM
function makeEl() {
  return {
    classList: {
      _s: new Set(),
      add(x) { this._s.add(x); },
      remove(...xs) { xs.forEach((x) => this._s.delete(x)); },
      toggle(x, v) { if (v) this._s.add(x); else this._s.delete(x); },
      contains(x) { return this._s.has(x); },
    },
    appendChild() {},
    removeChild() {},
    insertBefore() {},
    addEventListener() {},
    removeEventListener() {},
    setAttribute() {},
    getAttribute() { return null; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    style: {},
    attributes: {},
    dataset: {},
    set textContent(v) { this._t = v; },
    get textContent() { return this._t || ""; },
    set className(v) { this._c = v; },
    get className() { return this._c || ""; },
    set value(v) { this._v = v; },
    get value() { return this._v || ""; },
    set checked(v) { this._k = v; },
    get checked() { return this._k || false; },
    get firstChild() { return null; },
    get firstElementChild() { return makeEl(); },
    get parentElement() { return null; },
    get nextSibling() { return null; },
  };
}
const jsonEl = makeEl();
jsonEl.textContent = constantsJson;
const els = { "diplomacy-constants": jsonEl };
const documentStub = {
  getElementById(id) {
    if (els[id]) return els[id];
    return (els[id] = makeEl());
  },
  createElement() { return makeEl(); },
  createElementNS() { return makeEl(); },
  addEventListener() {},
  body: makeEl(),
  querySelector() { return null; },
  querySelectorAll() { return []; },
};
const windowStub = { addEventListener() {}, innerWidth: 1024, innerHeight: 768 };
const localStorageStub = {
  _s: {},
  getItem(k) { return this._s[k] || null; },
  setItem(k, v) { this._s[k] = v; },
  removeItem(k) { delete this._s[k]; },
};

const sandbox = {
  document: documentStub,
  window: windowStub,
  localStorage: localStorageStub,
  URL: { createObjectURL() { return ""; }, revokeObjectURL() {} },
  Blob: function () {},
  setTimeout: () => 0,
  setInterval: () => 0,
  clearInterval() {},
  clearTimeout() {},
  console: { log() {}, warn() {}, error() {} },
  Set,
  Map,
  Math,
  Object,
  Array,
  JSON,
  Number,
  String,
  Boolean,
  Date,
  Symbol,
  Error,
  Infinity,
  NaN,
  isNaN,
  isFinite,
  parseFloat,
  parseInt,
};
// Append explicit globalThis assignments so vm.runInContext exposes the
// class/const declarations (which otherwise stay in the script's local scope).
const exposeTail = `
; globalThis.Mulberry32 = Mulberry32;
globalThis.combinedDamping = combinedDamping;
globalThis.shockDistribution = shockDistribution;
globalThis.BLOCS = BLOCS;
globalThis.BLOC_REL = BLOC_REL;
globalThis.SHOCK_BASE_PROB = SHOCK_BASE_PROB;
globalThis.SOVEREIGNTY_MAX = SOVEREIGNTY_MAX;
globalThis.state = state;
`;
vm.createContext(sandbox);
vm.runInContext(js + exposeTail, sandbox, { filename: "microgrid_sim.js" });

const fixturesPath = process.argv[2];
if (!fixturesPath) {
  console.error("usage: node _js_parity_harness.js <fixtures.json>");
  process.exit(2);
}
const fixtures = JSON.parse(fs.readFileSync(fixturesPath, "utf8"));

const out = { mulberry32: [], combined_damping: [], shock_distribution: [] };

for (const f of fixtures.mulberry32 || []) {
  const r = new sandbox.Mulberry32(f.seed);
  const seq = [];
  for (let i = 0; i < f.n; i++) seq.push(r.nextFloat());
  out.mulberry32.push(seq);
}

for (const f of fixtures.combined_damping || []) {
  sandbox.state.alliances = new sandbox.Set(f.posture);
  if (f.trust) {
    sandbox.state.campaign = sandbox.state.campaign || { trust: {} };
    sandbox.state.campaign.trust = { ...f.trust };
  } else if (sandbox.state.campaign) {
    sandbox.state.campaign.trust = {};
  }
  out.combined_damping.push(sandbox.combinedDamping(f.shock));
}

for (const f of fixtures.shock_distribution || []) {
  sandbox.state.alliances = new sandbox.Set(f.posture);
  const dist = sandbox.shockDistribution(new sandbox.Set(f.posture));
  out.shock_distribution.push(dist);
}

process.stdout.write(JSON.stringify(out));
