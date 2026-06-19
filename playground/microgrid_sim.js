"use strict";

// ---------- Baked tech params (snapshot from data/tech_params.yaml, USD 2023/2025) ----------
const BASE_PARAMS = {
  solar_pv_utility:        { capex_per_kw:1100, opex_per_kw_yr:18, capacity_factor:0.22, lifetime_years:25, kind:"gen" },
  wind_onshore:            { capex_per_kw:1300, opex_per_kw_yr:35, capacity_factor:0.36, lifetime_years:25, kind:"gen" },
  micro_hydro_run_of_river:{ capex_per_kw:4500, opex_per_kw_yr:45, capacity_factor:0.55, lifetime_years:40, kind:"gen" },
  smr_nuclear:             { capex_per_kw:7000, opex_per_kw_yr:130, capacity_factor:0.92, lifetime_years:60, fuel_cost_per_mwh:8, kind:"gen" },
  geothermal_egs:          { capex_per_kw:7500, opex_per_kw_yr:135, capacity_factor:0.85, lifetime_years:30, kind:"gen" },
  biomass_chp:             { capex_per_kw:4200, opex_per_kw_yr:180, capacity_factor:0.80, lifetime_years:25, fuel_cost_per_mwh:28, kind:"gen" },
  tidal_stream:            { capex_per_kw:6500, opex_per_kw_yr:200, capacity_factor:0.32, lifetime_years:25, kind:"gen" },
  pem_electrolyzer:        { capex_per_kw:1500, opex_per_kw_yr:45, efficiency_lhv:0.62, lifetime_years:15, kind:"h2" },
  alkaline_electrolyzer:   { capex_per_kw:1100, opex_per_kw_yr:35, efficiency_lhv:0.60, lifetime_years:15, kind:"h2" },
  pem_fuel_cell_stationary:{ capex_per_kw:2200, opex_per_kw_yr:65, efficiency_lhv:0.50, lifetime_years:15, kind:"h2" },
  h2_storage_buffer:       { capex_per_kg:450, lifetime_years:25, kind:"sto", energy_kwh_per_unit:33.33 },
  li_ion_battery_grid:     { capex_per_kwh:290, opex_per_kw_yr:6, roundtrip_efficiency:0.86, lifetime_years:15, kind:"sto" },
  lfp_battery_grid:        { capex_per_kwh:250, opex_per_kw_yr:5, roundtrip_efficiency:0.88, lifetime_years:18, kind:"sto" },
  na_ion_battery_grid:     { capex_per_kwh:380, opex_per_kw_yr:6, roundtrip_efficiency:0.85, lifetime_years:15, kind:"sto" },
};

const DISTRICT_LOAD_MW = 2.0;
const DISCOUNT_RATE = 0.07;
const BOS_FRAC = 0.20;
const ENVELOPE_USD = 36_000_000;

// ---------- Shock profiles (port of supply.PROFILES) ----------
const SHOCKS = {
  bau: [],
  ir_shortage: [
    ["pem_electrolyzer.capex_per_kw", 1.6],
  ],
  pt_shortage: [
    ["pem_fuel_cell_stationary.capex_per_kw", 1.25],
  ],
  li_shortage: [
    ["li_ion_battery_grid.capex_per_kwh", 2.5],
  ],
  china_decoupling: [
    ["solar_pv_utility.capex_per_kw", 1.30],
    ["li_ion_battery_grid.capex_per_kwh", 1.20],
    ["lfp_battery_grid.capex_per_kwh", 1.20],
    ["pem_electrolyzer.opex_per_kw_yr", 1.10],
    ["alkaline_electrolyzer.opex_per_kw_yr", 1.10],
  ],
  triple_squeeze: [
    ["pem_electrolyzer.capex_per_kw", 1.6],
    ["pem_fuel_cell_stationary.capex_per_kw", 1.25],
    ["li_ion_battery_grid.capex_per_kwh", 2.5],
  ],
  western_only: [
    ["solar_pv_utility.capex_per_kw", 1.25],
    ["pem_electrolyzer.capex_per_kw", 1.25],
    ["alkaline_electrolyzer.capex_per_kw", 1.25],
    ["pem_fuel_cell_stationary.capex_per_kw", 1.25],
    ["li_ion_battery_grid.capex_per_kwh", 1.25],
    ["lfp_battery_grid.capex_per_kwh", 1.25],
  ],
  maritime_blockade: [
    ["solar_pv_utility.capex_per_kw", 1.50],
    ["wind_onshore.capex_per_kw", 1.40],
    ["alkaline_electrolyzer.capex_per_kw", 1.50],
    ["pem_electrolyzer.capex_per_kw", 2.20],
    ["pem_fuel_cell_stationary.capex_per_kw", 2.00],
    ["li_ion_battery_grid.capex_per_kwh", 3.50],
    ["lfp_battery_grid.capex_per_kwh", 1.80],
    ["na_ion_battery_grid.capex_per_kwh", 1.30],
  ],
  regional_autarky: [
    ["pem_electrolyzer.capex_per_kw", 1.50],
    ["pem_fuel_cell_stationary.capex_per_kw", 1.40],
    ["li_ion_battery_grid.capex_per_kwh", 1.30],
    ["solar_pv_utility.capex_per_kw", 1.15],
  ],
};

const SHOCK_NARRATIVE = {
  bau: "Baseline prices. No price changes apply. Use this run as the reference point before testing any shock.",
  ir_shortage: "Iridium supply tightens. PEM electrolyzer capex rises by 60 percent. Alkaline electrolyzers are unaffected. Run this to check if your hydrogen path holds up without rare metals.",
  pt_shortage: "Platinum supply tightens. PEM fuel cell capex rises by 25 percent. Solid oxide and alkaline paths are unaffected. Run this to test fuel cell exposure to platinum group metals.",
  li_shortage: "Lithium supply tightens. Lithium ion battery capex rises by 2.5 times. LFP and sodium ion stay near baseline. Run this to weigh battery chemistry choices.",
  china_decoupling: "Sourcing outside China gets more expensive. Solar capex rises 30 percent, battery capex rises 20 percent, and electrolyzer running costs rise 10 percent. Run this to test trade exposure.",
  triple_squeeze: "Iridium, platinum, and lithium all tighten at once. PEM electrolyzer, PEM fuel cell, and lithium ion battery costs jump together. Run this to validate alkaline plus LFP or sodium ion designs.",
  western_only: "Procurement is restricted to OECD suppliers. Most equipment costs roughly 25 percent more. Run this to model strict allied sourcing rules.",
  maritime_blockade: "Major shipping lanes close. PEM costs rise 2.2 times and lithium ion rises 3.5 times. Sodium ion rises only 30 percent. Run this to test resilience to import cutoffs.",
  regional_autarky: "Each region builds on its own. Anything using platinum group metals costs 30 to 50 percent more. Run this to test fully domestic supply chains.",
};

// ---------- Tech info copy (plain language). Source numbers in tech_params.yaml. ----------
const TECH_INFO = {
  solar_pv_utility: {
    what: "Utility scale solar PV. Panels convert sunlight into direct current power, then an inverter converts it to grid power. Output stops at night.",
    capex: "About $1,100 per kilowatt installed. Costs rise 30 percent under decoupling and up to 50 percent under a shipping blockade.",
    use: "Use in high irradiance regions such as Spain, Texas, or northern Chile. Pair with battery storage to cover evenings.",
    avoid: "Avoid as the sole source. Avoid sites below 1,500 kilowatt hours per square meter per year, or any year with heavy volcanic dimming."
  },
  wind_onshore: {
    what: "Onshore wind turbines. Blades drive a generator whenever wind speed is in range, day or night.",
    capex: "About $1,300 per kilowatt installed. Costs rise around 40 percent under a shipping blockade.",
    use: "Use on coasts, open plains, and ridgelines with a capacity factor of at least 30 percent.",
    avoid: "Avoid sheltered inland valleys and sites with local opposition or strict noise limits."
  },
  micro_hydro_run_of_river: {
    what: "Small run of river hydro. A turbine sits in the river flow with no large dam. Service life is about 40 years.",
    capex: "About $4,500 per kilowatt installed. Most shocks have little effect because components are sourced locally.",
    use: "Use near rivers with steady year round flow, such as Norway, the US Pacific Northwest, or Otago in New Zealand.",
    avoid: "Avoid seasonal rivers that run dry, or sites with sensitive fish habitat."
  },
  smr_nuclear: {
    what: "Small modular nuclear reactor. Runs at near constant output. Service life is about 60 years.",
    capex: "About $7,000 per kilowatt installed. Permitting and construction take several years.",
    use: "Use when the load needs firm 24 hour power and the timeline allows for licensing.",
    avoid: "Avoid under tight budgets or in jurisdictions that do not permit nuclear generation."
  },
  geothermal_egs: {
    what: "Enhanced geothermal. Deep wells extract heat from hot rock to drive a steam turbine. Output runs day and night.",
    capex: "About $7,500 per kilowatt installed. Drilling costs depend on local geology.",
    use: "Use where hot rock is near the surface, such as Iceland, Taupo in New Zealand, or the US Basin and Range.",
    avoid: "Avoid where heat gradients are low, or where injection could trigger induced seismicity."
  },
  biomass_chp: {
    what: "Biomass combined heat and power. Burns wood chips or agricultural residues to produce power and useful heat together.",
    capex: "About $4,200 per kilowatt installed plus $28 per megawatt hour for fuel. Output can be dispatched on demand.",
    use: "Use for black start support after blackouts and for sites that consume both power and heat.",
    avoid: "Avoid where a reliable feedstock supply is not secured year round."
  },
  tidal_stream: {
    what: "Tidal stream turbines submerged in strong tidal currents. Output is predictable but the technology has limited operating history.",
    capex: "About $6,500 per kilowatt installed. Project risk is elevated due to few reference deployments.",
    use: "Use at sites with proven strong tides, such as Brittany, Bass Strait, or the Pentland Firth.",
    avoid: "Avoid coasts with weak tidal flow or projects with tight capex limits."
  },
  pem_electrolyzer: {
    what: "Proton exchange membrane electrolyzer. Splits water into hydrogen and oxygen. Uses iridium and ramps quickly.",
    capex: "About $1,500 per kilowatt installed. Costs rise 60 percent under an iridium shortage and up to 120 percent under a shipping blockade.",
    use: "Use where the load must follow rapid swings in solar or wind output.",
    avoid: "Avoid during iridium shortages. Switch to alkaline electrolyzers instead."
  },
  alkaline_electrolyzer: {
    what: "Alkaline electrolyzer. A mature water splitting technology that uses no platinum group metals. Deployed at industrial scale for decades.",
    capex: "About $1,100 per kilowatt installed. Iridium and platinum shortages do not affect it.",
    use: "Use as the default low risk hydrogen path. It is the cheapest and steadiest option.",
    avoid: "Avoid where output must change in under a second. PEM responds faster."
  },
  pem_fuel_cell_stationary: {
    what: "Stationary PEM fuel cell. Converts stored hydrogen back into electricity on demand. Uses platinum.",
    capex: "About $2,200 per kilowatt installed. Costs rise 25 percent under a platinum shortage and up to 100 percent under a shipping blockade.",
    use: "Use to firm a solar plus hydrogen system across cloudy weeks.",
    avoid: "Avoid during platinum shortages. Solid oxide fuel cells use no platinum and are an alternative."
  },
  h2_storage_buffer: {
    what: "Above ground compressed hydrogen tanks. Each kilogram of hydrogen carries about 33 kilowatt hours of energy.",
    capex: "About $450 per kilogram of storage. Costs are stable across the modeled shocks.",
    use: "Use for long duration energy storage paired with an electrolyzer and a fuel cell.",
    avoid: "Avoid at very large scale where underground salt caverns are available, since they are far cheaper."
  },
  li_ion_battery_grid: {
    what: "Standard lithium ion grid battery. Highest energy density of the battery options modeled here.",
    capex: "About $290 per kilowatt hour of storage. Costs rise 2.5 times under a lithium shortage and up to 3.5 times under a shipping blockade.",
    use: "Use for short bursts where the budget can absorb a price spike.",
    avoid: "Avoid during a lithium shortage or shipping blockade. LFP and sodium ion are safer."
  },
  lfp_battery_grid: {
    what: "Lithium iron phosphate battery. No nickel or cobalt. Roughly 18 year service life. Round trip efficiency near 88 percent.",
    capex: "About $250 per kilowatt hour. Costs rise 20 to 25 percent under a decoupling shock.",
    use: "Use as the default battery. Long life and safer chemistry than standard lithium ion.",
    avoid: "Avoid in very cold climates without a battery heater installed."
  },
  na_ion_battery_grid: {
    what: "Sodium ion battery. Built on sodium, which is abundant from common salt. No lithium content.",
    capex: "About $380 per kilowatt hour. Costs rise only 30 percent under a shipping blockade.",
    use: "Use when shipping is at risk or when the strategy favors common materials.",
    avoid: "Avoid where footprint is constrained or where very long cycle life is required."
  },
};

const PRESET_INFO = {
  inland_solar_h2: "An inland design built on solar plus hydrogen. It pairs 3 megawatts of solar with an alkaline electrolyzer, above ground hydrogen tanks, a PEM fuel cell, and an LFP battery. Suits sunny inland sites such as Spain, where it lands near $214 per megawatt hour.",
  river_adjacent: "A river adjacent design. A small run of river hydro plant provides steady baseload, with solar and a sodium ion battery filling out the mix. Suits sites with reliable year round flow such as Norway, the US Pacific Northwest, or Otago.",
  coastal: "A coastal design. Onshore wind and tidal stream are paired with an LFP battery. Suits coasts with proven strong tides, such as Brittany or Bass Strait. Tidal stream still has limited operating history.",
  autonomy_max: "A resilience first design. It blends solar, wind, an alkaline electrolyzer with no rare metals, hydrogen storage, a PEM fuel cell, and an LFP battery. Suits sites where surviving shocks matters more than minimum cost.",
  smr_baseload: "A small modular nuclear reactor sized at 2 megawatts plus a small LFP battery. Provides firm 24 hour power. Suits sites that accept long licensing timelines and a budget above the standard 36 million dollar cap.",
  no_solar_no_wind: "A backup design for years when sun and wind fail, such as after a major volcanic eruption. It combines geothermal, biomass combined heat and power, and an LFP battery. Suits Iceland, Taupo, or the US Basin and Range."
};

const CHALLENGE_INFO = {
  iberian_default: "Goal: hold availability at or above 99 percent on the inland solar plus hydrogen design, with no shock active. Constraints: build cost at or below $36 million, no shock applied. Scoring: availability score times cost score times resilience bonus times cyber safety bonus.",
  triple_squeeze: "Goal: hold availability at or above 95 percent while iridium, platinum, and lithium all spike. Constraints: build cost at or below $36 million, all three shortages active. Scoring: availability score times cost score times resilience bonus times cyber safety bonus.",
  volcanic_year: "Goal: hold availability at or above 80 percent in a year where solar capacity factor is forced to 0.05. Constraints: build cost at or below $50 million, volcanic dimming active. Scoring: availability score times cost score times resilience bonus times cyber safety bonus.",
  survival_180: "Goal: hold critical load availability at or above 90 percent across a 180 day shipping blockade. Constraints: build cost at or below $36 million, only essentials powered, blockade active. Scoring: availability score times cost score times resilience bonus times cyber safety bonus.",
};

const HEADLINE_FORMULAS = {
  capex: "Build cost equals the sum of equipment costs plus storage costs, then 20 percent on top for cables, foundations, and project work. Budget cap is 36 million dollars.",
  lcoe: "Price per megawatt hour. Adds up build cost, running cost, and fuel over the life of the project, divided by the energy produced.",
  lcoh: "Price per kilo of hydrogen. Uses the electrolyzer running 40 percent of the time for 15 years, with electricity priced at the blended power price.",
  avail: "Availability blends average capacity factor, how much extra generation you have over demand, and how many hours of storage you carry. Cyber safety adds 2 percent. Powering only essentials closes 30 percent of the remaining gap."
};

const CATALOG_ORDER = [
  "solar_pv_utility","wind_onshore","micro_hydro_run_of_river","tidal_stream",
  "smr_nuclear","geothermal_egs","biomass_chp",
  "pem_electrolyzer","alkaline_electrolyzer","pem_fuel_cell_stationary",
  "h2_storage_buffer","li_ion_battery_grid","lfp_battery_grid","na_ion_battery_grid",
];

const PRETTY = {
  solar_pv_utility:"Solar PV (utility)",
  wind_onshore:"Wind onshore",
  micro_hydro_run_of_river:"Micro-hydro (RoR)",
  tidal_stream:"Tidal stream",
  smr_nuclear:"SMR nuclear",
  geothermal_egs:"Geothermal EGS",
  biomass_chp:"Biomass CHP",
  pem_electrolyzer:"Electrolyzer (PEM)",
  alkaline_electrolyzer:"Electrolyzer (alkaline)",
  pem_fuel_cell_stationary:"Fuel cell (PEM stat.)",
  h2_storage_buffer:"H2 buffer storage",
  li_ion_battery_grid:"Li-ion battery",
  lfp_battery_grid:"LFP battery",
  na_ion_battery_grid:"Na-ion battery",
};

const PRESETS = {
  inland_solar_h2: {
    label:"Inland: solar plus hydrogen",
    desc:"3 megawatts of solar, alkaline electrolyzer, hydrogen tanks, LFP battery",
    items:[
      ["solar_pv_utility", 3000],
      ["alkaline_electrolyzer", 800],
      ["h2_storage_buffer", 1500],
      ["pem_fuel_cell_stationary", 600],
      ["lfp_battery_grid", 4000],
    ],
  },
  river_adjacent: {
    label:"By a river",
    desc:"small hydro baseload, solar, sodium ion battery",
    items:[
      ["micro_hydro_run_of_river", 1200],
      ["solar_pv_utility", 1500],
      ["na_ion_battery_grid", 4000],
    ],
  },
  coastal: {
    label:"On the coast: wind plus tides",
    desc:"onshore wind, tidal stream, LFP battery",
    items:[
      ["wind_onshore", 2000],
      ["tidal_stream", 800],
      ["lfp_battery_grid", 5000],
    ],
  },
  autonomy_max: {
    label:"Survive shocks",
    desc:"mixed sources plus long hydrogen storage",
    items:[
      ["solar_pv_utility", 2500],
      ["wind_onshore", 1500],
      ["alkaline_electrolyzer", 600],
      ["h2_storage_buffer", 2000],
      ["pem_fuel_cell_stationary", 600],
      ["lfp_battery_grid", 4000],
    ],
  },
  smr_baseload: {
    label:"Small nuclear baseload",
    desc:"2 megawatt small modular reactor plus a small battery",
    items:[
      ["smr_nuclear", 2000],
      ["lfp_battery_grid", 1000],
    ],
  },
  no_solar_no_wind: {
    label:"No sun, no wind",
    desc:"geothermal, biomass, and a battery",
    items:[
      ["geothermal_egs", 1500],
      ["biomass_chp", 800],
      ["lfp_battery_grid", 2000],
    ],
  },
};

const CHALLENGES = [
  {
    id:"iberian_default", name:"Sunny Spain default",
    desc:"Reach 99 percent availability on the inland solar plus hydrogen design, with no surprise events, under 36 million dollars.",
    objectives:["lights on at least 99 percent of the time", "build cost at or under 36 million dollars", "no surprise events"],
    target_avail:0.99, capex_cap:36e6, shock:"bau",
  },
  {
    id:"triple_squeeze", name:"Triple squeeze",
    desc:"Same town, but iridium, platinum, and lithium all spike at once. Alkaline electrolyzers plus LFP or sodium ion batteries are the way through.",
    objectives:["lights on at least 95 percent of the time", "build cost at or under 36 million dollars", "all three shortages active"],
    target_avail:0.95, capex_cap:36e6, shock:"triple_squeeze",
  },
  {
    id:"volcanic_year", name:"Volcanic year",
    desc:"A volcano dims the sky and solar drops to 5 percent of normal. Keep the lights on at least 80 percent of the time.",
    objectives:["solar capacity factor forced to 0.05", "lights on at least 80 percent of the time", "geothermal, nuclear, or biomass do the heavy lifting"],
    target_avail:0.80, capex_cap:50e6, shock:"bau", solar_kill:true,
  },
  {
    id:"survival_180", name:"Survive 180 days",
    desc:"Shipping is blocked for 180 days. Power only the essentials. Backup covers about 30 percent of normal demand.",
    objectives:["lights on at least 90 percent of the time, essentials only", "build cost at or under 36 million dollars", "shipping blockade active"],
    target_avail:0.90, capex_cap:36e6, shock:"maritime_blockade", critical_only:true,
  },
];

// ---------- LCOE / LCOH ports ----------
function lcoe({capex_total, opex_yr, fuel_yr, energy_mwh_yr, lifetime_years, discount_rate}) {
  if (energy_mwh_yr <= 0 || lifetime_years <= 0) return Infinity;
  const r = discount_rate;
  let cost_pv = capex_total, energy_pv = 0;
  for (let t = 1; t <= lifetime_years; t++) {
    const df = 1 / Math.pow(1 + r, t);
    cost_pv  += (opex_yr + fuel_yr) * df;
    energy_pv += energy_mwh_yr * df;
  }
  return cost_pv / energy_pv;
}

function lcoh({capex_per_kw, kw, opex_per_kw_yr, electricity_price_per_mwh, efficiency_lhv, capacity_factor, lifetime_years, discount_rate}) {
  const H2_LHV = 33.33;
  const annual_kwh_in = kw * capacity_factor * 8760;
  const annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV;
  if (annual_kg_h2 <= 0) return Infinity;
  const annual_elec = (annual_kwh_in / 1000) * electricity_price_per_mwh;
  const capex = capex_per_kw * kw;
  const opex = opex_per_kw_yr * kw;
  const r = discount_rate;
  let cost_pv = capex, h2_pv = 0;
  for (let t = 1; t <= lifetime_years; t++) {
    const df = 1 / Math.pow(1 + r, t);
    cost_pv += (opex + annual_elec) * df;
    h2_pv   += annual_kg_h2 * df;
  }
  return cost_pv / h2_pv;
}

// ---------- Friends Union (diplomacy / coalition layer) ----------
// Constants are loaded from the HTML JSON block so the Python diplomacy module
// can read the same source of truth. See playground/microgrid_sim.html
// <script type="application/json" id="diplomacy-constants">.
const DIPLOMACY_CONSTANTS = (() => {
  const node = document.getElementById("diplomacy-constants");
  if (!node) throw new Error("diplomacy-constants JSON block missing from HTML");
  return JSON.parse(node.textContent);
})();
const BLOCS = DIPLOMACY_CONSTANTS.blocs;
const BLOC_REL = DIPLOMACY_CONSTANTS.blocRelations;          // [[a, b, value], ...] with a < b sorted
const SHOCK_BASE_PROB = DIPLOMACY_CONSTANTS.shockBaseProb;
const SOVEREIGNTY_MAX = DIPLOMACY_CONSTANTS.sovereigntyMax;

// ---------- State ----------
const state = {
  build: [],
  shock: "bau",
  ztaOn: false,
  critOnly: false,
  challengeOn: false,
  challengeIdx: 0,
  shocksSurvived: new Set(),
  region: "",
  alliances: new Set(),
  lastChallengeScore: null,
  lastChallengeVerdict: null,
  campaign: {
    active: false,
    year: 0,
    totalScore: 0,
    history: [],         // [{year, shock, score, accepted, cardId}]
    trust: {},           // bloc -> int counter
    queuedCards: {},     // year -> [cardId,...]
    rngSeed: 42,
    pendingCard: null,   // card object awaiting accept/decline
    cardChoiceMade: false,
    yearTargets: null,   // snapshot of effectiveTargets at year start
    activeBonuses: {},   // run-scoped accumulated bonuses (e.g. ZTA double, lcoh discount)
    maintainedThisYear: new Set(),  // blocs given card attention this year (no decay)
    trustAtYearStart: {},           // trust snapshot to detect maintenance vs neglect
    defected: new Set(),            // blocs that abandoned you this year (no damping/bonus)
    defectingNextYear: new Set(),   // queued defections from trust hitting zero
    retaliationDelta: null,         // shock-odds bias from active defections
    immunities: {},      // shock -> 1 to skip; mutated by cards 4, 15, 16
    // permanent capex multipliers (e.g. card 1/11 chain)
    permMults: { tech_capex_mult: {}, tech_opex_mult: {}, capex_one_time: 0, lcoh_mult: 1, ptc_extra: 0, avail_extra: 0, dampingExtra: {} },
  },
};

// ---------- Mulberry32 PRNG ----------
// Canonical algorithm; cross-surface seed parity required with
// model/src/electicity_model/diplomacy.py::Mulberry32. The middle line is
// `t ^= t + imul(...)` (the leading XOR is load-bearing), not just `t = t + imul(...)`.
class Mulberry32 {
  constructor(seed) { this.state = seed >>> 0; }
  nextU32() {
    let t = (this.state = (this.state + 0x6D2B79F5) >>> 0);
    t = Math.imul(t ^ (t >>> 15), t | 1) >>> 0;
    t = (t ^ (t + Math.imul(t ^ (t >>> 7), t | 61))) >>> 0;
    return ((t ^ (t >>> 14)) >>> 0);
  }
  nextFloat() { return this.nextU32() / 4294967296; }
}

// activeAlliances() returns the active bloc set.
// During campaign mode, the year may snapshot a different posture, but for
// Phases 1 + 2 the active set IS state.alliances.
function activeAlliances() {
  return state.alliances;
}

function sovereigntySpent(activeSet) {
  const set = activeSet || activeAlliances();
  let total = 0;
  for (const bloc of set) total += (BLOCS[bloc] && BLOCS[bloc].sovereignty) || 0;
  return total;
}

// pairwiseAdjustment: reads BLOC_REL (list of [a, b, value] with a < b sorted).
// Returns clamp(1 + sum_pairs, 0.3, 1.5). Multiplied into the combinedDamping
// surviving fraction so synergy reduces and friction amplifies the shock excess.
function pairwiseAdjustment(activeSet) {
  const set = activeSet || activeAlliances();
  if (!set || (set.size === undefined ? set.length === 0 : set.size < 2)) return 1.0;
  let sum = 0;
  for (const triple of BLOC_REL) {
    const a = triple[0], b = triple[1], v = triple[2];
    const has = (set instanceof Set) ? (set.has(a) && set.has(b)) : (set.indexOf(a) >= 0 && set.indexOf(b) >= 0);
    if (has) sum += v;
  }
  let adj = 1 + sum;
  if (adj < 0.3) adj = 0.3;
  if (adj > 1.5) adj = 1.5;
  return adj;
}

function combinedDamping(shockKey, activeSet, trustMap) {
  const set = activeSet || activeAlliances();
  // For an active set of blocs, the surviving fraction of the shock excess is
  // the product of (1 - d_i). E.g. two blocs each damping 0.5 => surviving 0.25.
  let surviving = 1.0;
  for (const bloc of set) {
    let d = (BLOCS[bloc].damping && BLOCS[bloc].damping[shockKey]) || 0;
    // Trust extension: each held bloc adds min(0.25, trust * 0.05) to its damping.
    if (trustMap && trustMap[bloc]) {
      const t = trustMap[bloc];
      d = Math.min(1, d + Math.min(0.25, t * 0.05));
    }
    if (d) surviving *= (1 - d);
  }
  // Friends Union umbrella: 3+ blocs cap remaining excess at 75% of dampened.
  const size = (set instanceof Set) ? set.size : set.length;
  if (size >= 3) surviving *= 0.75;
  // Pairwise relationships modify the surviving fraction (outside the trust
  // application per pipeline).
  surviving *= pairwiseAdjustment(set);
  if (surviving < 0) surviving = 0;
  if (surviving > 1) surviving = 1;
  return surviving;
}

function diplomacyCapex(activeSet) {
  const set = activeSet || activeAlliances();
  let total = 0;
  for (const bloc of set) total += BLOCS[bloc].cost;
  return total;
}

// applyShock: composition pipeline steps 1-3.
// 1. BASE -> 2. bloc tech_capex_mult -> 3. bloc tech_opex_mult -> 4. shock mods (dampened).
// availability_add, lcoh_mult, ptc_capex_rebate_pct apply later in computeDistrict.
function applyShock(profile, activeSet, trustMap) {
  const set = activeSet || activeAlliances();
  const out = JSON.parse(JSON.stringify(BASE_PARAMS));

  // Step 2 + 3: apply bloc baseline bonuses BEFORE shock multipliers.
  for (const bloc of set) {
    const bonus = BLOCS[bloc] && BLOCS[bloc].bonus;
    if (!bonus) continue;
    if (bonus.tech_capex_mult) {
      for (const [tech, mult] of Object.entries(bonus.tech_capex_mult)) {
        if (!out[tech]) continue;
        if ("capex_per_kw" in out[tech]) out[tech].capex_per_kw *= mult;
        if ("capex_per_kwh" in out[tech]) out[tech].capex_per_kwh *= mult;
        if ("capex_per_kg" in out[tech]) out[tech].capex_per_kg *= mult;
      }
    }
    if (bonus.tech_opex_mult) {
      for (const [tech, mult] of Object.entries(bonus.tech_opex_mult)) {
        if (!out[tech]) continue;
        if ("opex_per_kw_yr" in out[tech]) out[tech].opex_per_kw_yr *= mult;
      }
    }
  }

  // Step 4: shock mods, with diplomacy damping the *excess* (mult - 1).
  const mods = SHOCKS[profile] || [];
  const surviving = combinedDamping(profile, set, trustMap);
  for (const [path, mult] of mods) {
    const [tech, field] = path.split(".");
    if (!out[tech] || !(field in out[tech])) continue;
    const dampened = mult > 1 ? 1 + (mult - 1) * surviving : mult;
    out[tech][field] *= dampened;
  }
  return out;
}

// Aggregate a numeric bonus across the active bloc set (additive).
function _bonusSum(activeSet, key) {
  let sum = 0;
  for (const bloc of activeSet) {
    const bonus = BLOCS[bloc] && BLOCS[bloc].bonus;
    if (bonus && typeof bonus[key] === "number") sum += bonus[key];
  }
  return sum;
}
// Aggregate a multiplicative numeric bonus (product).
function _bonusProduct(activeSet, key) {
  let prod = 1;
  for (const bloc of activeSet) {
    const bonus = BLOCS[bloc] && BLOCS[bloc].bonus;
    if (bonus && typeof bonus[key] === "number") prod *= bonus[key];
  }
  return prod;
}

function computeDistrict(opts) {
  opts = opts || {};
  const activeSet = opts.activeSet || activeAlliances();
  const trustMap = opts.trustMap || null;
  const shockKey = opts.shock || state.shock;
  const params = applyShock(shockKey, activeSet, trustMap);
  // Effective targets: campaign or challenge constraints layered on the year.
  const effTargets = opts.effTargets || effectiveTargets();
  if (effTargets.solar_kill) params.solar_pv_utility.capacity_factor = 0.05;

  let capex_eq = 0, capex_sto = 0, opex = 0, fuel = 0;
  let gen_mwh = 0;
  let weighted_lcoe_num = 0, weighted_lcoe_den = 0;
  let weighted_cf_num = 0, weighted_cf_den = 0;
  let storage_kwh = 0, h2_storage_kg = 0;
  let h2_kw = 0, h2_capex_kw = 0, h2_opex_per_kw_yr = 0, h2_eff = 0;
  let has_fc = false;
  const breakdown = [];

  for (const c of state.build) {
    const p = params[c.tech];
    if (!p) continue;
    if (p.kind === "gen") {
      const kw = c.capacity;
      const c_capex = p.capex_per_kw * kw;
      const c_opex = p.opex_per_kw_yr * kw;
      const energy_mwh = kw * p.capacity_factor * 8760 / 1000;
      const c_fuel = (p.fuel_cost_per_mwh || 0) * energy_mwh;
      capex_eq += c_capex; opex += c_opex; fuel += c_fuel;
      gen_mwh += energy_mwh;
      weighted_cf_num += p.capacity_factor * kw;
      weighted_cf_den += kw;
      const tech_lcoe = lcoe({
        capex_total:c_capex, opex_yr:c_opex, fuel_yr:c_fuel,
        energy_mwh_yr:energy_mwh, lifetime_years:p.lifetime_years, discount_rate:DISCOUNT_RATE
      });
      weighted_lcoe_num += tech_lcoe * energy_mwh;
      weighted_lcoe_den += energy_mwh;
      breakdown.push({ tech: c.tech, capacity: kw, unit:"kW", capex_raw: c_capex });
    } else if (p.kind === "sto") {
      if (c.tech === "h2_storage_buffer") {
        const cc = p.capex_per_kg * c.capacity;
        capex_sto += cc;
        h2_storage_kg += c.capacity;
        breakdown.push({ tech: c.tech, capacity: c.capacity, unit:"kg", capex_raw: cc });
      } else {
        const cc = p.capex_per_kwh * c.capacity;
        capex_sto += cc;
        opex += (p.opex_per_kw_yr || 5) * (c.capacity / 4);
        storage_kwh += c.capacity;
        breakdown.push({ tech: c.tech, capacity: c.capacity, unit:"kWh", capex_raw: cc });
      }
    } else if (p.kind === "h2") {
      const kw = c.capacity;
      const c_capex = p.capex_per_kw * kw;
      capex_eq += c_capex;
      opex += p.opex_per_kw_yr * kw;
      if (c.tech.includes("electrolyzer")) {
        h2_kw += kw;
        h2_capex_kw = p.capex_per_kw;
        h2_opex_per_kw_yr = p.opex_per_kw_yr;
        h2_eff = p.efficiency_lhv;
      }
      if (c.tech === "pem_fuel_cell_stationary") has_fc = true;
      breakdown.push({ tech: c.tech, capacity: kw, unit:"kW", capex_raw: c_capex });
    }
  }

  const diplomacy_capex = diplomacyCapex(activeSet);
  // Composition pipeline step 8: ptc_capex_rebate_pct (post-everything else).
  const ptc_rebate = _bonusSum(activeSet, "ptc_capex_rebate_pct");
  const equipment_with_bos = (capex_eq + capex_sto) * (1 + BOS_FRAC);
  const equipment_after_rebate = equipment_with_bos * (1 - ptc_rebate);
  const total_capex = equipment_after_rebate + diplomacy_capex;
  const blended_lcoe = weighted_lcoe_den > 0 ? weighted_lcoe_num / weighted_lcoe_den : null;

  let lcoh_val = null;
  if (h2_kw > 0 && blended_lcoe != null) {
    lcoh_val = lcoh({
      capex_per_kw: h2_capex_kw, kw: h2_kw,
      opex_per_kw_yr: h2_opex_per_kw_yr,
      electricity_price_per_mwh: blended_lcoe,
      efficiency_lhv: h2_eff,
      capacity_factor: 0.40, lifetime_years: 15, discount_rate: DISCOUNT_RATE,
    });
    // lcoh_mult bonus (product across blocs, sub-1 means cheaper).
    const lcoh_mult = _bonusProduct(activeSet, "lcoh_mult");
    if (lcoh_mult !== 1) lcoh_val *= lcoh_mult;
  }

  const avg_cf = weighted_cf_den > 0 ? weighted_cf_num / weighted_cf_den : 0;
  const load_kw = DISTRICT_LOAD_MW * 1000;
  const buffer_hours = (storage_kwh + h2_storage_kg * 33.33 * (has_fc ? 0.50 : 0)) / load_kw;
  const buffer_factor = 1 - Math.exp(-buffer_hours / 12);
  const gen_kw_total = state.build.reduce((s,c)=>{
    const p = params[c.tech]; return p && p.kind==="gen" ? s + c.capacity : s;
  }, 0);
  const headroom = gen_kw_total / load_kw;
  const headroom_term = Math.min(headroom, 3) / 3;
  let avail = avg_cf * (0.45 + 0.55 * headroom_term) + buffer_factor * 0.35;
  // availability_add bonus (additive across blocs).
  avail += _bonusSum(activeSet, "availability_add");
  if (effTargets.critical_only && gen_kw_total > 0) {
    avail = avail + (1 - Math.min(avail, 1)) * 0.30;
  }
  if (state.ztaOn) avail *= 1.02;
  avail = Math.max(0, Math.min(1, avail));

  return {
    total_capex, blended_lcoe, lcoh_val, avail, avg_cf, buffer_hours,
    gen_mwh, gen_kw_total, storage_kwh, h2_storage_kg, params,
    breakdown, capex_eq, capex_sto, diplomacy_capex,
    ptc_rebate, equipment_with_bos,
  };
}

// shockDistribution: water-filling normalization.
// 1. p[shock] = SHOCK_BASE_PROB + sum(active prob_delta).
// 2. Clamp negatives to 0.
// 3. Loop: pin shocks > 0.5 at 0.5, redistribute overflow uniformly to un-pinned.
// 4. Normalize to 1.
function shockDistribution(activeSet) {
  const set = activeSet || activeAlliances();
  const shocks = Object.keys(SHOCK_BASE_PROB);
  const p = {};
  for (const s of shocks) p[s] = SHOCK_BASE_PROB[s] || 0;
  for (const bloc of set) {
    const deltas = (BLOCS[bloc] && BLOCS[bloc].prob_delta) || {};
    for (const [s, d] of Object.entries(deltas)) {
      p[s] = (p[s] || 0) + d;
    }
  }
  // Clamp negatives.
  for (const s of shocks) if (p[s] < 0) p[s] = 0;

  // Water-filling: pin > 0.5 at 0.5, redistribute uniformly.
  const CAP = 0.5;
  const pinned = new Set();
  for (let iter = 0; iter < 50; iter++) {
    let overflow = 0;
    for (const s of shocks) {
      if (p[s] > CAP && !pinned.has(s)) {
        overflow += p[s] - CAP;
        p[s] = CAP;
        pinned.add(s);
      }
    }
    if (overflow < 1e-9) break;
    // Redistribute over un-pinned shocks. If all pinned, dump on cap and stop.
    const unpinned = shocks.filter(s => !pinned.has(s));
    if (unpinned.length === 0) break;
    const share = overflow / unpinned.length;
    for (const s of unpinned) p[s] += share;
  }

  // Normalize to 1.
  let sum = 0;
  for (const s of shocks) sum += p[s];
  if (sum > 0) {
    for (const s of shocks) p[s] /= sum;
  }
  return p;
}

// renderShockOutlook: stable per-shock rows; only updates widths/text.
function renderShockOutlook() {
  const root = $("shockOutlook");
  if (!root) return;
  const dist = shockDistribution(state.alliances);
  const shocks = Object.keys(SHOCK_BASE_PROB);
  // Initial DOM: one row per shock, persistent.
  if (root.childElementCount !== shocks.length) {
    clear(root);
    for (const s of shocks) {
      const row = el("div", { cls: "outlook-bar" + (s === "bau" ? " bau" : ""), attrs: { "data-shock": s } });
      row.appendChild(el("div", { cls: "label", text: s.replace(/_/g, " ") }));
      const track = el("div", { cls: "track" });
      track.appendChild(el("i"));
      row.appendChild(track);
      row.appendChild(el("div", { cls: "pct", text: "0.0%" }));
      root.appendChild(row);
    }
  }
  for (const s of shocks) {
    const row = root.querySelector("[data-shock=\"" + s + "\"]");
    if (!row) continue;
    const p = dist[s] || 0;
    const bar = row.querySelector(".track > i");
    bar.style.width = (p * 100).toFixed(1) + "%";
    row.querySelector(".pct").textContent = (p * 100).toFixed(1) + "%";
  }
}

// effectiveTargets: resolves Challenge + Campaign mode constraints.
// Returns { target_avail, capex_cap, solar_kill, critical_only }.
// Snapshot is taken at year start in campaign mode; for now (rendering),
// we always read live state. Year-snapshot lives in state.campaign.yearTargets.
function effectiveTargets() {
  // Defaults
  let target_avail = 0.95, capex_cap = 36e6;
  let solar_kill = false, critical_only = !!state.critOnly;
  if (state.challengeOn) {
    const ch = CHALLENGES[state.challengeIdx];
    if (ch) {
      target_avail = ch.target_avail;
      capex_cap = ch.capex_cap;
      if (ch.solar_kill) solar_kill = true;
      if (ch.critical_only) critical_only = true;
    }
  }
  // Campaign-only path: keep defaults unless Challenge layered above.
  return { target_avail, capex_cap, solar_kill, critical_only };
}

// ---------- DOM helpers ----------
const $ = id => document.getElementById(id);
function el(tag, opts) {
  const e = document.createElement(tag);
  if (!opts) return e;
  if (opts.cls) e.className = opts.cls;
  if (opts.text != null) e.textContent = opts.text;
  if (opts.id) e.id = opts.id;
  if (opts.title) e.title = opts.title;
  if (opts.attrs) for (const [k,v] of Object.entries(opts.attrs)) e.setAttribute(k, v);
  if (opts.style) for (const [k,v] of Object.entries(opts.style)) e.style[k] = v;
  if (opts.on) for (const [k,v] of Object.entries(opts.on)) e.addEventListener(k, v);
  if (opts.children) for (const c of opts.children) if (c) e.appendChild(c);
  return e;
}
function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

function fmtUSD(x) {
  if (!isFinite(x)) return "-";
  if (x >= 1e9) return "$" + (x/1e9).toFixed(2) + "B";
  if (x >= 1e6) return "$" + (x/1e6).toFixed(2) + "M";
  if (x >= 1e3) return "$" + (x/1e3).toFixed(0) + "k";
  return "$" + x.toFixed(0);
}

// ---------- Info tooltip subsystem (click-to-pin, viewport-aware) ----------
const INFO_SVG_NS = "http://www.w3.org/2000/svg";
function makeInfoSVG() {
  const svg = document.createElementNS(INFO_SVG_NS, "svg");
  svg.setAttribute("viewBox", "0 0 16 16");
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("focusable", "false");
  const t = document.createElementNS(INFO_SVG_NS, "text");
  t.setAttribute("x", "8");
  t.setAttribute("y", "12");
  t.setAttribute("text-anchor", "middle");
  t.setAttribute("font-family", "JetBrains Mono, monospace");
  t.setAttribute("font-size", "11");
  t.setAttribute("font-style", "italic");
  t.setAttribute("font-weight", "bold");
  t.setAttribute("fill", "currentColor");
  t.textContent = "i";
  svg.appendChild(t);
  return svg;
}

// Static info copy keyed by data-info-id slug. Plain language for a wide audience.
const INFO_REGISTRY = {
  "params-snapshot": {
    title: "Parameter snapshot",
    body: "<p>Cost numbers are drawn from public reports published between <span class=\"num\">2023</span> and <span class=\"num\">2025</span>. They are not adjusted for inflation.</p><p>Treat them as a current day baseline for comparison only.</p><span class=\"tip\">Tip: full source citations for every value live in tech_params.yaml in the project repository.</span>"
  },
  "tech-catalog": {
    title: "Technology catalog",
    body: "<p>Click any card to add that component to the build. Each card has a small info icon with plain language notes.</p><p>The notes cover what the technology is, the typical <span class=\"kw\">capex</span> band, when it is a good fit, and when to avoid it.</p>"
  },
  "site-params": {
    title: "Site parameters",
    body: "<p><span class=\"kw\">Average load</span>: <span class=\"num\">2 MW</span>. Typical for a small district.</p><p><span class=\"kw\">Hours per year</span>: <span class=\"num\">8,760</span>. The full calendar year.</p><p><span class=\"kw\">Discount rate</span>: <span class=\"num\">7%</span>. Reflects the cost of capital.</p><p><span class=\"kw\">Balance of plant uplift</span>: <span class=\"num\">20%</span> on top of equipment cost for cables, foundations, and project work.</p><p><span class=\"kw\">Budget cap</span>: <span class=\"num\">$36M</span>.</p><span class=\"tip\">Tip: stay below the budget cap to clear challenges.</span>"
  },
  "region": {
    title: "Region",
    body: "<p>Optional. The selected region tags your exported summary and unlocks water use guidance for arid sites.</p><span class=\"tip\">Tip: the selection is stored locally so the next visit reopens with the same region.</span>"
  },
  "friends-union": {
    title: "Friends Union (diplomacy layer)",
    body: "<p>Friendship is not free. Joining a bloc adds a fixed <span class=\"kw\">diplomacy capex</span> to your build, paying for trade missions, joint working groups, and standards alignment.</p><p>Friendship pays back when shocks hit. Each bloc <span class=\"kw\">softens</span> specific surprise events by sharing supply, alternate shipping routes, or domestic-equivalent OEMs.</p><p>Three or more blocs unlock the <span class=\"kw\">Friends Union</span> umbrella, which trims a further <span class=\"num\">25%</span> off any remaining shock excess.</p><span class=\"tip\">Tip: the cheap insurance is one bloc that matches your worst plausible shock. The full union is a strategic flex, not a default purchase.</span>"
  },
  "metric-capex": {
    title: "Build cost (capex)",
    body: "<p>Total <span class=\"kw\">capex</span> to build the district. Sum every component plus any storage, then apply a <span class=\"num\">20%</span> uplift for cables, foundations, and project work.</p><p>Generators are priced per <span class=\"kw\">kW</span>, hydrogen tanks per <span class=\"kw\">kg</span>, and batteries per <span class=\"kw\">kWh</span>.</p><span class=\"tip\">Tip: the budget cap for this <span class=\"num\">2 MW</span> district is <span class=\"num\">$36M</span>. A healthy build sits below the cap.</span>"
  },
  "metric-lcoe": {
    title: "Levelized cost of electricity (LCOE)",
    body: "<p><span class=\"kw\">LCOE</span> is the average price per unit of energy across the project life, in <span class=\"kw\">$/MWh</span>.</p><p>It accounts for build, running, and fuel costs over the lifetime of each generator. The page blends <span class=\"kw\">LCOE</span> across generators, weighted by annual energy output, at a <span class=\"num\">7%</span> discount rate.</p><span class=\"tip\">Tip: a healthy <span class=\"kw\">LCOE</span> for this district lands between <span class=\"num\">$80</span> and <span class=\"num\">$250/MWh</span>.</span>"
  },
  "metric-lcoh": {
    title: "Levelized cost of hydrogen (LCOH)",
    body: "<p><span class=\"kw\">LCOH</span> is the average price per kilogram of hydrogen, in <span class=\"kw\">$/kg</span>.</p><p>It accounts for <span class=\"kw\">electrolyzer</span> build, running, and electricity costs. The page assumes the <span class=\"kw\">electrolyzer</span> runs <span class=\"num\">40%</span> of the time over a <span class=\"num\">15 year</span> life and buys electricity at the blended power price.</p><span class=\"tip\">Tip: a healthy <span class=\"kw\">LCOH</span> lands between <span class=\"num\">$4</span> and <span class=\"num\">$9/kg</span>.</span>"
  },
  "metric-avail": {
    title: "Availability",
    body: "<p><span class=\"kw\">Availability</span> is the share of hours per year in which demand is met, blending <span class=\"kw\">capacity factor</span>, headroom over demand, and storage hours carried.</p><p>Cyber safety on adds <span class=\"num\">2%</span>. Powering only essentials closes <span class=\"num\">30%</span> of the remaining gap.</p><span class=\"tip\">Tip: a healthy <span class=\"kw\">availability</span> sits at or above <span class=\"num\">95%</span>. The strict challenge requires <span class=\"num\">99%</span>+.</span>"
  },
  "supply-shocks": {
    title: "Supply shocks",
    body: "<p>Each shock raises the price of specific components, such as a lithium shortage or a shipping blockade.</p><p>Open the info icon on any shock to see which inputs change and by how much.</p><span class=\"tip\">Tip: use shocks to stress test the current build.</span>"
  },
  "scenario-presets": {
    title: "Scenario presets",
    body: "<p>One click loads a complete working design. Use any preset as a starting point and adjust from there.</p><span class=\"tip\">Tip: open the info icon on each preset for a plain language summary of the architecture and the type of site it suits best.</span>"
  },
  "ctrl-zta": {
    title: "Zero trust hardening",
    body: "<p>Enables a <span class=\"kw\">Zero Trust Architecture</span> (ZTA) posture for the site. Devices authenticate to each other, software is signed, and a dedicated safety controller is isolated from the wider network.</p><p>Effect: <span class=\"kw\">availability</span> rises by <span class=\"num\">2%</span> and the challenge score gains a <span class=\"num\">5%</span> bonus.</p>"
  },
  "ctrl-critonly": {
    title: "Critical load only",
    body: "<p>Powers only essential loads such as hospitals and water pumps, and sheds the rest.</p><p>Effect: closes <span class=\"num\">30%</span> of the remaining <span class=\"kw\">availability</span> gap.</p><span class=\"tip\">Tip: useful during long duration shocks such as a shipping blockade.</span>"
  },
  "ctrl-challenge": {
    title: "Challenge mode",
    body: "<p>Turns the playground into a scored game. Each challenge defines a clear goal and a set of constraints.</p><p>The final score depends on how close the build comes to the targets and how well it holds up under shocks.</p>"
  }
};

// Tooltip state
const InfoTip = {
  pop: null, body: null, titleEl: null, closeBtn: null, arrow: null,
  preview: null,
  currentSource: null,
  currentSpec: null,
  init() {
    this.pop = document.getElementById("infoPop");
    this.body = document.getElementById("infoPopBody");
    this.titleEl = document.getElementById("infoPopTitle");
    this.closeBtn = document.getElementById("infoPopClose");
    this.arrow = this.pop ? this.pop.querySelector(".info-arrow") : null;
    this.preview = document.getElementById("infoPreview");
    if (!this.pop) return;
    this.closeBtn.addEventListener("click", (e) => { e.stopPropagation(); this.close(); });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.isOpen()) { e.preventDefault(); this.close(); }
    });
    document.addEventListener("mousedown", (e) => {
      if (!this.isOpen()) return;
      if (this.pop.contains(e.target)) return;
      if (this.currentSource && this.currentSource.contains(e.target)) return;
      this.close();
    });
    window.addEventListener("resize", () => { if (this.isOpen()) this.position(); });
    window.addEventListener("scroll", () => { if (this.isOpen()) this.position(); }, true);
    // If the source icon gets detached during a re-render, close the tooltip.
    const observer = new MutationObserver(() => {
      if (this.isOpen() && this.currentSource && !document.contains(this.currentSource)) {
        this.close();
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  },
  isOpen() { return this.pop && this.pop.classList.contains("open"); },
  open(source, spec) {
    if (!this.pop) return;
    if (this.currentSource === source && this.isOpen()) { this.close(); return; }
    if (this.currentSource) this.currentSource.setAttribute("aria-expanded", "false");
    this.currentSource = source;
    this.currentSpec = spec;
    // Render
    clear(this.body);
    const titleText = spec && spec.title ? spec.title : "Info";
    this.titleEl.textContent = titleText;
    if (spec && typeof spec.body === "string") {
      // Trusted static HTML from INFO_REGISTRY and *InfoSpec helpers.
      this.body.innerHTML = spec.body;
    } else if (spec && spec.node instanceof Node) {
      this.body.appendChild(spec.node);
    } else if (spec && Array.isArray(spec.lines)) {
      this.body.appendChild(renderInfoLines(spec.lines));
    } else if (spec && typeof spec.text === "string") {
      const lines = spec.text.split("\n");
      for (const ln of lines) this.body.appendChild(el("div", { text: ln }));
    }
    this.pop.classList.add("open");
    this.pop.setAttribute("aria-hidden", "false");
    source.setAttribute("aria-expanded", "true");
    this.position();
    // Focus close button so Tab cycles within tooltip-ish region
    setTimeout(() => { try { this.closeBtn.focus(); } catch(e) {} }, 0);
  },
  close() {
    if (!this.pop || !this.isOpen()) return;
    this.pop.classList.remove("open");
    this.pop.setAttribute("aria-hidden", "true");
    if (this.currentSource) {
      this.currentSource.setAttribute("aria-expanded", "false");
      try { this.currentSource.focus(); } catch(e) {}
    }
    this.currentSource = null;
    this.currentSpec = null;
  },
  position() {
    if (!this.currentSource) return;
    const r = this.currentSource.getBoundingClientRect();
    // Reset to measure natural size
    this.pop.style.left = "0px";
    this.pop.style.top = "0px";
    this.pop.classList.remove("above","below");
    const pr = this.pop.getBoundingClientRect();
    const ph = pr.height;
    const pw = pr.width;
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const margin = 16;
    const gap = 8;
    // Decide above vs below
    const spaceBelow = vh - r.bottom;
    const spaceAbove = r.top;
    let placeBelow = true;
    if (spaceBelow < ph + gap + margin && spaceAbove > spaceBelow) placeBelow = false;
    let top = placeBelow ? r.bottom + gap : r.top - ph - gap;
    // Clamp top into viewport
    if (top + ph > vh - margin) top = vh - margin - ph;
    if (top < margin) top = margin;
    // Horizontal: prefer centering on icon
    const iconCenter = r.left + r.width / 2;
    let left = iconCenter - pw / 2;
    if (left + pw > vw - margin) left = vw - margin - pw;
    if (left < margin) left = margin;
    this.pop.style.left = left + "px";
    this.pop.style.top = top + "px";
    this.pop.classList.add(placeBelow ? "below" : "above");
    // Arrow position
    if (this.arrow) {
      let ax = iconCenter - left - 7;
      if (ax < 8) ax = 8;
      if (ax > pw - 22) ax = pw - 22;
      this.arrow.style.left = ax + "px";
    }
  },
  showPreview(source, text) {
    // Hover preview removed. The click-to-pin popover is the single source of
    // truth and shows the full content with a scrollbar when long. Hovering an
    // (i) icon now does nothing visible; clicking opens the full tooltip.
    return;
  },
  hidePreview() {
    if (this.preview) this.preview.classList.remove("on");
  }
};

function renderInfoLines(lines) {
  // lines: array of ["b", text] | ["t", text] | ["br"] | ["row", left, right]
  const frag = document.createDocumentFragment();
  let cur = null;
  function ensureRow() {
    if (!cur) { cur = el("div"); frag.appendChild(cur); }
    return cur;
  }
  for (const item of lines) {
    if (item[0] === "br") { cur = null; continue; }
    if (item[0] === "row") {
      cur = null;
      const row = el("div", { cls:"row", children:[
        el("span", { text: item[1] }),
        el("span", { text: item[2] }),
      ]});
      frag.appendChild(row);
      continue;
    }
    const row = ensureRow();
    if (item[0] === "b") row.appendChild(el("b", { text: item[1] }));
    else row.appendChild(document.createTextNode(item[1]));
  }
  return frag;
}

// Build an info-icon button. spec: { title, text|lines|node, name }
// Returns the wrap element. The spec is captured so the tooltip can render on click.
let _infoSeq = 0;
function infoIcon(spec, _alignIgnored, opts) {
  opts = opts || {};
  const wrap = el("span", { cls:"info-wrap" });
  const id = opts.id || ("info-src-" + (++_infoSeq));
  const name = (spec && spec.name) || (spec && spec.title) || "info";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "info-icon";
  btn.setAttribute("aria-label", "More info about " + name);
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-controls", "infoPop");
  btn.setAttribute("data-info-id", id);
  btn.appendChild(makeInfoSVG());
  btn._infoSpec = spec;
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    InfoTip.open(btn, btn._infoSpec);
  });
  function previewFromSpec(s) {
    if (!s) return "";
    if (s.preview) return s.preview;
    if (s.text) return s.text;
    if (Array.isArray(s.lines)) return s.lines.map(x => x[0]==="br"?" ":(x[1]||"")).join(" ");
    if (typeof s.body === "string") {
      const tmp = document.createElement("div");
      tmp.innerHTML = s.body;
      return (tmp.textContent || "").replace(/\s+/g, " ").trim();
    }
    return "";
  }
  btn.addEventListener("mouseenter", () => {
    const preview = previewFromSpec(btn._infoSpec);
    if (preview) InfoTip.showPreview(btn, preview);
  });
  btn.addEventListener("mouseleave", () => InfoTip.hidePreview());
  btn.addEventListener("focus", () => {
    const preview = previewFromSpec(btn._infoSpec);
    if (preview) InfoTip.showPreview(btn, preview);
  });
  btn.addEventListener("blur", () => InfoTip.hidePreview());
  wrap.appendChild(btn);
  return wrap;
}

// Mount info icons on every <span class="info-host" data-info-id="..."> from INFO_REGISTRY.
function mountStaticInfoIcons() {
  const hosts = document.querySelectorAll(".info-host[data-info-id]");
  hosts.forEach(host => {
    const slug = host.getAttribute("data-info-id");
    const spec = INFO_REGISTRY[slug];
    if (!spec) return;
    const specWithName = Object.assign({ name: spec.title }, spec);
    const ic = infoIcon(specWithName, null, { id: slug });
    // tag the source button with the slug for testability
    const btn = ic.querySelector(".info-icon");
    if (btn) btn.setAttribute("data-info-id", slug);
    clear(host);
    host.appendChild(ic);
  });
}

// Escape HTML before we wrap selected substrings with span markup.
function _escHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
// Auto-style numeric values and key technical terms for tooltip bodies.
const _KW_TERMS = [
  "capex","opex","LCOE","LCOH","electrolyzer","fuel cell","alkaline","AEM","PEM","SOFC",
  "LFP","lithium ion","lithium-ion","sodium ion","sodium-ion","iridium","platinum",
  "additionality","RFNBO","45V","ZTA","mTLS","availability","capacity factor"
];
function _enrich(text) {
  let s = _escHtml(text);
  // Numbers and ranges. Preserve units and percent.
  s = s.replace(/(\$[\d,]+(?:\.\d+)?(?:\s*(?:per|\/)\s*[A-Za-z]+)?)/g, '<span class="num">$1</span>');
  s = s.replace(/(\b\d+(?:\.\d+)?\s*(?:percent|%|years?|yr|MW|kW|kWh|MWh|kg|hours?|days?|times)\b)/gi, '<span class="num">$1</span>');
  // Key terms (case-insensitive, longest first to avoid nesting).
  const sorted = _KW_TERMS.slice().sort((a,b) => b.length - a.length);
  for (const term of sorted) {
    const re = new RegExp("(?<![\\w>])(" + term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")(?![\\w<])", "gi");
    s = s.replace(re, '<span class="kw">$1</span>');
  }
  return s;
}

function techInfoSpec(tech) {
  const info = TECH_INFO[tech];
  if (!info) return null;
  const body = "<p>" + _enrich(info.what) + "</p>"
    + "<p><span class=\"kw\">Capex band</span>: " + _enrich(info.capex) + "</p>"
    + "<span class=\"tip\">Tip: " + _enrich(info.use) + "</span>"
    + "<span class=\"warn\">Watch out: " + _enrich(info.avoid) + "</span>";
  return { title: PRETTY[tech], name: PRETTY[tech], body, preview: info.what };
}

function shockInfoSpec(profile) {
  const narrative = SHOCK_NARRATIVE[profile] || "";
  const mods = SHOCKS[profile] || [];
  let body = "<p>" + _enrich(narrative) + "</p>";
  if (mods.length === 0) {
    body += "<span class=\"tip\">Tip: no price changes. This is the normal baseline.</span>";
  } else {
    body += "<p><span class=\"kw\">Price multipliers</span>:</p>";
    for (const [path, mult] of mods) {
      body += "<div class=\"row\"><span>" + _escHtml(path) + "</span><span class=\"num\">x " + mult.toFixed(2) + "</span></div>";
    }
  }
  return { title: "Surprise event: " + profile.replace(/_/g," "), name: profile, body, preview: narrative };
}

function presetInfoSpec(key) {
  const p = PRESETS[key];
  const text = PRESET_INFO[key] || p.desc;
  const body = "<p>" + _enrich(text) + "</p>";
  return { title: p.label, name: p.label, body, preview: text };
}

function challengeInfoSpec(ch) {
  const text = CHALLENGE_INFO[ch.id] || ch.desc;
  // Split on "Goal:", "Constraints:", "Scoring:" so each becomes its own paragraph.
  const parts = text.split(/(?=\b(?:Goal|Constraints|Scoring):)/);
  let body = "";
  for (const raw of parts) {
    const seg = raw.trim();
    if (!seg) continue;
    const m = seg.match(/^(Goal|Constraints|Scoring):\s*([\s\S]*)$/);
    if (m) {
      body += "<p><span class=\"kw\">" + m[1] + "</span>: " + _enrich(m[2]) + "</p>";
    } else {
      body += "<p>" + _enrich(seg) + "</p>";
    }
  }
  if (!body) body = "<p>" + _enrich(text) + "</p>";
  return { title: ch.name, name: ch.name, body, preview: text };
}

// ---------- Catalog rendering ----------
function renderCatalog() {
  const cat = $("catalog");
  clear(cat);
  for (const tech of CATALOG_ORDER) {
    const p = BASE_PARAMS[tech];
    let priceLine, kindTag, metaRight;
    if (p.kind === "gen") {
      priceLine = "$" + p.capex_per_kw + "/kW";
      kindTag = "gen";
      metaRight = p.lifetime_years + "yr | CF " + (p.capacity_factor*100).toFixed(0) + "%";
    } else if (p.kind === "h2") {
      priceLine = "$" + p.capex_per_kw + "/kW";
      kindTag = "h2";
      metaRight = p.lifetime_years + "yr | eta " + (p.efficiency_lhv*100).toFixed(0) + "%";
    } else if (tech === "h2_storage_buffer") {
      priceLine = "$" + p.capex_per_kg + "/kg";
      kindTag = "h2";
      metaRight = p.lifetime_years + "yr";
    } else {
      priceLine = "$" + p.capex_per_kwh + "/kWh";
      kindTag = "sto";
      metaRight = p.lifetime_years + "yr | eta " + (p.roundtrip_efficiency*100).toFixed(0) + "%";
    }
    const tag = el("span", { cls:"tag " + kindTag, text: kindTag });
    const left = el("span", { children:[ tag, document.createTextNode(priceLine) ] });
    const right = el("span", { text: metaRight });
    const meta = el("div", { cls:"meta", children:[ left, right ] });
    const nameInner = el("span", { text: PRETTY[tech] });
    const spec = techInfoSpec(tech) || { title: PRETTY[tech], name: PRETTY[tech], text: tech };
    const info = infoIcon(spec, null, { id: "tech-" + tech });
    const btn = info.querySelector(".info-icon");
    if (btn) btn.setAttribute("data-info-id", "tech-" + tech);
    // Prevent click on info icon from adding to build
    info.addEventListener("click", (e) => e.stopPropagation());
    const name = el("div", { cls:"name", children:[ nameInner, info ] });
    const card = el("div", { cls:"tech-card", children:[ name, meta ], on:{ click:()=>addToBuild(tech) } });
    cat.appendChild(card);
  }
}

function defaultCapacity(tech) {
  const p = BASE_PARAMS[tech];
  if (p.kind === "gen") return 1000;
  if (tech === "h2_storage_buffer") return 1000;
  if (p.kind === "sto") return 2000;
  if (p.kind === "h2") return 500;
  return 1000;
}
function maxCapacity(tech) {
  const p = BASE_PARAMS[tech];
  if (p.kind === "gen") return 8000;
  if (tech === "h2_storage_buffer") return 5000;
  if (p.kind === "sto") return 12000;
  if (p.kind === "h2") return 3000;
  return 5000;
}
function unitLabelFor(tech) {
  const p = BASE_PARAMS[tech];
  if (tech === "h2_storage_buffer") return "kg";
  if (p.kind === "sto") return "kWh";
  return "kW";
}
function formatCap(cap, tech) {
  const u = unitLabelFor(tech);
  if (u === "kW") return cap >= 1000 ? (cap/1000).toFixed(2) + " MW" : cap.toFixed(0) + " kW";
  if (u === "kWh") return cap >= 1000 ? (cap/1000).toFixed(2) + " MWh" : cap.toFixed(0) + " kWh";
  if (u === "kg") return cap >= 1000 ? (cap/1000).toFixed(2) + " t H2" : cap.toFixed(0) + " kg H2";
  return cap.toFixed(0);
}
function compRoleLabel(tech) {
  const p = BASE_PARAMS[tech];
  if (p.kind === "gen") return "generator";
  if (tech.includes("electrolyzer")) return "electrolyzer";
  if (tech.includes("fuel_cell")) return "fuel cell";
  if (tech === "h2_storage_buffer") return "h2 buffer";
  return "battery";
}

function addToBuild(tech) {
  const existing = state.build.find(c => c.tech === tech);
  if (existing) {
    existing.capacity = Math.min(existing.capacity + defaultCapacity(tech) * 0.5, maxCapacity(tech));
    narrate("Increased " + PRETTY[tech] + " to " + formatCap(existing.capacity, tech) + ".");
  } else {
    state.build.push({ tech, capacity: defaultCapacity(tech) });
    narrate("Added " + PRETTY[tech] + " at " + formatCap(defaultCapacity(tech), tech) + ".");
  }
  rerender();
}
function removeFromBuild(idx) {
  const c = state.build[idx];
  state.build.splice(idx, 1);
  narrate("Removed " + PRETTY[c.tech] + " from your build.");
  rerender();
}

function renderBuild() {
  const div = $("build");
  clear(div);
  if (state.build.length === 0) {
    div.appendChild(el("div", { cls:"empty", text:"Click a card on the left to add a piece of equipment to your town." }));
    return;
  }
  state.build.forEach((c, i) => {
    const max = maxCapacity(c.tech);
    const step = Math.max(50, max/200);
    const nameDiv = el("div", { children:[
      el("div", { cls:"name", text: PRETTY[c.tech] }),
      el("div", { cls:"sub",  text: compRoleLabel(c.tech) }),
    ]});
    const range = el("input", { attrs:{ type:"range", min:"0", max:String(max), step:String(step), value:String(c.capacity) } });
    const capSpan = el("span", { cls:"cap", id:"cap-"+i, text: formatCap(c.capacity, c.tech) });
    range.addEventListener("input", e => {
      state.build[i].capacity = +e.target.value;
      capSpan.textContent = formatCap(+e.target.value, c.tech);
      queueRerender();
    });
    const rmBtn = el("button", { cls:"rm", text:"x", title:"remove", on:{ click:()=>removeFromBuild(i) } });
    const ctrls = el("div", { cls:"controls", children:[ range, capSpan, rmBtn ] });
    div.appendChild(el("div", { cls:"comp", children:[ nameDiv, ctrls ] }));
  });
}

function renderStats(d) {
  $("capexVal").textContent = fmtUSD(d.total_capex);
  const pct = d.total_capex / ENVELOPE_USD * 100;
  const overage = d.total_capex - ENVELOPE_USD;
  const bar = $("capexBar");
  bar.firstElementChild.style.width = Math.min(100, pct) + "%";
  bar.classList.remove("warn","bad");
  if (pct > 100) bar.classList.add("bad");
  else if (pct > 85) bar.classList.add("warn");
  const dipNote = d.diplomacy_capex > 0 ? " | diplomacy " + fmtUSD(d.diplomacy_capex) : "";
  $("capexSub").textContent = (pct > 100
    ? "over budget by " + fmtUSD(overage) + " (" + (pct-100).toFixed(0) + " percent)"
    : pct.toFixed(0) + " percent of the 36 million dollar budget") + dipNote;

  $("lcoeVal").textContent = d.blended_lcoe ? "$" + d.blended_lcoe.toFixed(0) + "/MWh" : "- $/MWh";
  $("lcoeSub").textContent = d.gen_mwh > 0 ? (d.gen_mwh/1000).toFixed(1) + " gigawatt hours per year" : "no generators yet";

  $("lcohVal").textContent = d.lcoh_val ? "$" + d.lcoh_val.toFixed(2) + "/kg" : "- $/kg";
  $("lcohSub").textContent = d.lcoh_val ? "based on power price and electrolyzer efficiency" : "needs an electrolyzer plus power";

  const av_pct = d.avail * 100;
  const valEl = $("availVal");
  valEl.textContent = av_pct.toFixed(1) + "%";
  valEl.className = "val " + (av_pct >= 95 ? "ok" : av_pct >= 85 ? "warn" : "bad");
  const aBar = $("availBar");
  aBar.firstElementChild.style.width = Math.max(0, Math.min(100, av_pct)) + "%";
  aBar.classList.remove("warn","bad");
  if (av_pct < 85) aBar.classList.add("bad"); else if (av_pct < 95) aBar.classList.add("warn");
  $("availSub").textContent = "average " + (d.avg_cf*100).toFixed(0) + " percent | " + d.buffer_hours.toFixed(1) + " hours of storage";

  checkConstraintsAndNarrate(d);
}

function narrate(msg, level) {
  level = level || "ok";
  const n = $("narrator");
  n.classList.remove("warn","bad");
  if (level === "warn") n.classList.add("warn");
  if (level === "bad")  n.classList.add("bad");
  const ts = new Date().toLocaleTimeString([], {hour12:false});
  clear(n);
  n.appendChild(el("div", { cls:"ts", text:"[" + ts + "]" }));
  n.appendChild(el("div", { text: msg }));
}

let lastNarrative = "";
function checkConstraintsAndNarrate(d) {
  if (state.build.length === 0) return;
  let key = "", msg = "", level = "ok";
  if (d.total_capex > ENVELOPE_USD * 1.001) {
    const over = d.total_capex - ENVELOPE_USD;
    const has_li = state.build.find(c => c.tech === "li_ion_battery_grid");
    const has_pem = state.build.find(c => c.tech === "pem_electrolyzer");
    const has_solar = state.build.find(c => c.tech === "solar_pv_utility");
    let suggest = "";
    if (has_li) suggest = ". Try swapping the lithium ion battery for an LFP battery, which costs less and lasts longer";
    else if (has_pem && state.shock !== "bau") suggest = ". The alkaline electrolyzer is not affected by this shock";
    else if (has_solar && has_solar.capacity > 2000) suggest = ". Try cutting solar by about " + (over/1100/1.2/1000).toFixed(1) + " megawatts";
    msg = "Over budget by " + fmtUSD(over) + suggest + ".";
    level = "bad"; key = "over:" + Math.round(over/1e5);
  } else if (d.avail < 0.85 && state.build.length > 1) {
    const has_storage = state.build.find(c => BASE_PARAMS[c.tech].kind === "sto");
    if (!has_storage) { msg = "Lights stay on less than 85 percent of the time. You have power sources but no storage. Add an LFP battery or a hydrogen tank."; key="no-sto"; }
    else { msg = "Lights stay on " + (d.avail*100).toFixed(0) + " percent of the time. Try more storage, or add a steady source like geothermal or a small reactor."; key = "low-av:" + Math.round(d.avail*100); }
    level = "warn";
  }
  if (msg && key !== lastNarrative) { lastNarrative = key; narrate(msg, level); }
}

function rerender(skipBuildList) {
  if (!skipBuildList) renderBuild();
  const d = computeDistrict();
  renderStats(d);
  if (state.challengeOn) renderChallenge(d);
  return d;
}

// Coalesce high-frequency renders (slider drags) to one per animation frame so
// a fast drag never queues more compute+DOM work than the screen can show.
let _renderQueued = false;
function queueRerender() {
  if (_renderQueued) return;
  _renderQueued = true;
  const raf = (typeof requestAnimationFrame === "function")
    ? requestAnimationFrame : (cb => setTimeout(cb, 16));
  raf(() => { _renderQueued = false; rerender(true); });
}

function _humanBlocName(k) {
  return (BLOCS[k] && BLOCS[k].label) || k;
}

function renderAlliances() {
  const grid = $("alliances");
  if (!grid) return;
  clear(grid);
  for (const [key, b] of Object.entries(BLOCS)) {
    const card = el("div", { cls: "alliance-card" + (state.alliances.has(key) ? " on" : "") });
    const dampedShocks = Object.keys(b.damping).map(k => k.replace(/_/g, " ")).join(", ");
    card.appendChild(el("div", { cls: "a-name", children: [
      el("span", { text: b.label }),
      el("span", { cls: "a-cost", text: "+" + fmtUSD(b.cost) + " | sov " + b.sovereignty }),
    ]}));
    card.appendChild(el("div", { cls: "a-desc", text: b.desc }));
    card.appendChild(el("div", { cls: "a-desc", text: "softens: " + (dampedShocks || "(none)") }));
    card.addEventListener("click", () => {
      if (state.alliances.has(key)) {
        state.alliances.delete(key);
        narrate("Left " + b.label + ". You save " + fmtUSD(b.cost) + " but lose its protection.", "warn");
      } else {
        // Sovereignty cap is hard.
        const proposed = sovereigntySpent() + b.sovereignty;
        if (proposed > SOVEREIGNTY_MAX) {
          narrate("Cannot join " + b.label + ": sovereignty cap " + SOVEREIGNTY_MAX + " would be exceeded (need " + b.sovereignty + ", " + (SOVEREIGNTY_MAX - sovereigntySpent()) + " left).", "warn");
          return;
        }
        // Mid-campaign join: cost is ceil(1.5 * sovereignty); cap remains hard.
        if (state.campaign && state.campaign.active && state.campaign.year > 0) {
          // (charged to score; just narrate here)
          const extra = Math.ceil(1.5 * b.sovereignty);
          narrate("Joined " + b.label + " mid-campaign for " + fmtUSD(b.cost) + " (mid-run sovereignty premium: " + extra + " sov-points charged at year end).", "warn");
        } else {
          narrate("Joined " + b.label + " for " + fmtUSD(b.cost) + ". Friends share the bill.", "ok");
        }
        state.alliances.add(key);
      }
      saveAlliances();
      renderAlliances();
      renderShockOutlook();
      rerender();
    });
    grid.appendChild(card);
  }
  $("diplomacySpend").textContent = fmtUSD(diplomacyCapex());
  const unionEl = $("friendsUnionState");
  clear(unionEl);
  const pill = el("span", { cls: "union-pill" });
  if (state.alliances.size >= 3) {
    pill.classList.add("on");
    pill.textContent = "UNION ACTIVE";
  } else {
    pill.textContent = state.alliances.size + " of 7 blocs";
  }
  unionEl.appendChild(pill);

  // Sovereignty meter
  const sov = sovereigntySpent();
  const sovText = $("sovSpend");
  if (sovText) sovText.textContent = sov + " / " + SOVEREIGNTY_MAX;
  const sovBar = $("sovBar");
  if (sovBar) {
    const pct = Math.min(100, (sov / SOVEREIGNTY_MAX) * 100);
    sovBar.firstElementChild.style.width = pct + "%";
    sovBar.classList.remove("warn", "bad");
    if (sov >= SOVEREIGNTY_MAX) sovBar.classList.add("bad");
    else if (sov >= SOVEREIGNTY_MAX - 2) sovBar.classList.add("warn");
  }

  // Synergy/friction summary
  const synEl = $("synergyList");
  if (synEl) {
    clear(synEl);
    const set = state.alliances;
    const lines = [];
    for (const triple of BLOC_REL) {
      if (set.has(triple[0]) && set.has(triple[1])) {
        const v = triple[2];
        const tag = v >= 0 ? "synergy" : "friction";
        const sign = v >= 0 ? "+" : "";
        lines.push({
          text: _humanBlocName(triple[0]) + " <-> " + _humanBlocName(triple[1]) + " : " + sign + (v * 100).toFixed(0) + "% (" + tag + ")",
          good: v >= 0,
        });
      }
    }
    if (lines.length === 0) {
      synEl.appendChild(el("div", { cls: "syn-empty", text: "no active pair effects" }));
    } else {
      const adj = pairwiseAdjustment(set);
      synEl.appendChild(el("div", { cls: "syn-summary", text: "pair adjustment: x " + adj.toFixed(2) + " on shock excess" }));
      for (const ln of lines.slice(0, 3)) {
        synEl.appendChild(el("div", { cls: "syn-line " + (ln.good ? "good" : "bad"), text: ln.text }));
      }
    }
  }
}

function renderShocks() {
  const grid = $("shocks");
  clear(grid);
  for (const k of Object.keys(SHOCKS)) {
    const cell = el("div", { cls:"shock-cell" });
    const b = el("button", { text: k.replace(/_/g," ") });
    if (k === "bau") b.classList.add("bau");
    if (k === state.shock) b.classList.add("active");
    b.addEventListener("click", () => {
      state.shock = k;
      $("shockPill").textContent = "shock: " + k.replace(/_/g," ");
      lastNarrative = "";
      renderShocks();
      narrate(SHOCK_NARRATIVE[k] || ("Surprise event applied: " + k.replace(/_/g," ")), k === "bau" ? "ok" : "warn");
      rerender();
    });
    cell.appendChild(b);
    const info = infoIcon(shockInfoSpec(k), null, { id: "shock-" + k });
    const ibtn = info.querySelector(".info-icon");
    if (ibtn) ibtn.setAttribute("data-info-id", "shock-" + k);
    info.style.position = "absolute";
    info.style.top = "4px";
    info.style.right = "4px";
    cell.style.position = "relative";
    cell.appendChild(info);
    grid.appendChild(cell);
  }
}

function renderPresets() {
  const grid = $("presets");
  clear(grid);
  for (const [k, p] of Object.entries(PRESETS)) {
    const cell = el("div", { cls:"preset-cell" });
    const desc = el("span", { cls:"pdesc", text: p.desc });
    const b = el("button");
    b.appendChild(document.createTextNode(p.label));
    b.appendChild(desc);
    b.addEventListener("click", () => {
      state.build = p.items.map(([tech,cap]) => ({ tech, capacity: cap }));
      lastNarrative = "";
      narrate("Loaded the " + p.label + " design. Tweak the sliders to make it your own.");
      rerender();
    });
    cell.appendChild(b);
    const info = infoIcon(presetInfoSpec(k), null, { id: "preset-" + k });
    const ibtn = info.querySelector(".info-icon");
    if (ibtn) ibtn.setAttribute("data-info-id", "preset-" + k);
    info.style.position = "absolute";
    info.style.top = "4px";
    info.style.right = "4px";
    cell.style.position = "relative";
    cell.appendChild(info);
    grid.appendChild(cell);
  }
}

function renderChallenge(d) {
  const ch = CHALLENGES[state.challengeIdx];
  if (!ch) return;
  const titleEl = $("chTitle");
  clear(titleEl);
  titleEl.appendChild(document.createTextNode("Current challenge: " + ch.name + " "));
  const ic = infoIcon(challengeInfoSpec(ch), null, { id: "challenge-" + ch.id });
  const ibtn = ic.querySelector(".info-icon");
  if (ibtn) ibtn.setAttribute("data-info-id", "challenge-" + ch.id);
  titleEl.appendChild(ic);

  const objs = $("chObjectives");
  clear(objs);
  objs.appendChild(el("div", { cls:"desc-line", text: ch.desc }));
  const ul = el("ul");
  for (const o of ch.objectives) ul.appendChild(el("li", { text: o }));
  objs.appendChild(ul);

  if (state.shock !== ch.shock) {
    state.shock = ch.shock;
    $("shockPill").textContent = "shock: " + ch.shock.replace(/_/g," ");
    renderShocks();
  }
  if (ch.critical_only && !state.critOnly) {
    state.critOnly = true;
    $("critOnly").checked = true;
  }

  const avail_score = Math.min(1.5, d.avail / ch.target_avail);
  const cap_over_frac = Math.max(0, (d.total_capex - ch.capex_cap) / ch.capex_cap);
  const cost_score = Math.max(0, 1 - cap_over_frac);
  const resilience = state.shocksSurvived.size;
  const zta_mult = state.ztaOn ? 1.05 : 1.0;
  const final = Math.round(100 * avail_score * cost_score * (1 + resilience/10) * zta_mult);

  const survived = d.avail >= ch.target_avail && d.total_capex <= ch.capex_cap;
  if (survived) state.shocksSurvived.add(state.shock);

  state.lastChallengeScore = final;
  state.lastChallengeVerdict = survived ? "PASS" : "FAIL";
  if (survived) recordScore({ mode: "challenge", name: ch.name, score: final });

  const m = $("chMetrics");
  clear(m);
  const rows = [
    ["power score",  avail_score.toFixed(2)],
    ["cost score",   cost_score.toFixed(2)],
    ["toughness",    resilience + " event" + (resilience===1?"":"s") + " survived"],
    ["safety bonus", state.ztaOn ? "+5 percent" : "-"],
    ["build cost",   fmtUSD(d.total_capex)],
    ["lights on",    (d.avail*100).toFixed(1) + " percent"],
  ];
  for (const [k, v] of rows) {
    m.appendChild(el("div", { children:[
      el("span", { cls:"k", text: k }),
      document.createTextNode(" " + v),
    ]}));
  }

  const verdict = $("chVerdict");
  verdict.style.display = "block";
  if (survived) {
    verdict.className = "verdict pass";
    verdict.textContent = "PASS | score " + final;
  } else {
    verdict.className = "verdict fail";
    const reasons = [];
    if (d.avail < ch.target_avail) reasons.push("lights on " + (d.avail*100).toFixed(0) + " percent, target " + (ch.target_avail*100).toFixed(0) + " percent");
    if (d.total_capex > ch.capex_cap) reasons.push("over budget by " + fmtUSD(d.total_capex - ch.capex_cap));
    verdict.textContent = "FAIL | " + reasons.join(" | ") + " | score " + final;
  }
}

function nextChallenge() {
  state.challengeIdx = (state.challengeIdx + 1) % CHALLENGES.length;
  state.shocksSurvived.clear();
  rerender();
  narrate("Next challenge: " + CHALLENGES[state.challengeIdx].name + ". " + CHALLENGES[state.challengeIdx].desc);
}

// ---------- Onboarding modal ----------
const ONBOARD_KEY = "electicity_onboard_seen";
const ONBOARD_NEVER = "electicity_onboard_never";

const ONBOARD_TABS = {
  what: [
    { type:"p", text:"You get a tiny town to power." },
    { type:"p", text:"Your job is to keep the lights on with clean energy without going over budget. The budget is 36 million dollars." },
    { type:"p", text:"You pick the parts. Solar panels, wind turbines, batteries, and machines that turn spare power into hydrogen for later. Mix and match." },
    { type:"p", text:"The numbers come from a research project on green hydrogen. This page is the easy playground. The full Python model lives under /model in the project repository." }
  ],
  how: [
    { type:"p", text:"Three steps and you are playing." },
    { type:"p", text:"Step 1, build. Click a card on the left to add a piece of equipment. Drag the sliders to set the size. Watch the build cost bar so you do not go over the 36 million dollar budget." },
    { type:"p", text:"Step 2, try a ready-made design. The right panel has presets like 'Inland: solar plus hydrogen' or 'On the coast: wind plus tides'. One click loads a working design you can tweak." },
    { type:"p", text:"Step 3, run a surprise. Pick a surprise event on the right. For example 'lithium gets scarce' or 'shipping is blocked'. Watch your build cost change and see if your design still works." },
    { type:"p", text:"Step 4, make friends. The Friends Union panel on the left lets you join WEST, EAST, SOUTH-CENTRAL, or NORTH FRIEND blocs. Each costs capex up front but softens specific shocks. Three blocs activate a Friends Union umbrella that softens everything further. The point of the game is to feel both the cost and the value of diplomacy." },
    { type:"p", text:"Hover the small i next to any control for a quick hint. Click 'Export results to a text file' to save a plain text report of your run." }
  ],
  score: [
    { type:"callout", text:"Your goal is simple. Power the town with clean energy. Do not break the bank." },
    { type:"h3", text:"The three things your score measures" },
    { type:"ul", cls:"spaced", items:[
      "Power. Did the lights stay on? 99 out of 100 hours is great. 80 out of 100 is rough.",
      "Money. Did you stay inside the 36 million dollar budget? Spending 30 million is fine. Spending 50 million is way over.",
      "Toughness. Can your design survive surprises? If lithium doubles in price and your town still runs, that is tough."
    ] },
    { type:"h3", text:"Numbers to watch" },
    { type:"ul", cls:"watch", items:[
      { b:"Build cost", t:"What it costs to build the whole town." },
      { b:"Power price", t:"How much each unit of power costs over the life of the project." },
      { b:"Lights stay on", t:"What share of the year demand is met." }
    ] },
    { type:"h3", text:"Tips for a great score" },
    { type:"ul", cls:"spaced", items:[
      "Add a battery so you do not run out at night.",
      "If iridium gets scarce, switch from a PEM electrolyzer to an alkaline one.",
      "Mix two sources, like solar plus wind, so a cloudy day does not stop you.",
      "Turn on cyber safety for a small bonus.",
      "Keep an eye on the build cost bar so you do not break the budget."
    ] },
    { type:"h3", text:"Three quick examples" },
    { type:"examples", items:[
      { mark:"1", text:"Low score. Only solar panels, no battery. Lights go off at night and the score drops." },
      { mark:"2", text:"Medium score. Solar plus a small battery. Lights stay on most of the time and the budget is fine." },
      { mark:"3", text:"High score. Solar, wind, a battery, and hydrogen for backup. Lights stay on through surprises and the score climbs." }
    ] },
    { type:"tip", text:"Turn on Challenge mode and see your score. There is no single right answer, just better and worse trade-offs." },
    { type:"h3", text:"Score math, for the curious" },
    { type:"p", text:"Final score equals 100 times the availability score times the cost score times a resilience bonus times a cyber safety bonus. The availability score is your availability divided by the target, capped at 1.5. The cost score is 1 minus the share by which you went over budget, floored at 0. Resilience counts how many surprise events your design has already survived. The cyber safety bonus is 1.05 when cyber safety is on, otherwise 1.0." }
  ]
};

let activeTab = "what";

function renderOnboardBody() {
  const body = $("onboardBody");
  clear(body);
  for (const block of ONBOARD_TABS[activeTab]) {
    if (block.type === "p") {
      body.appendChild(el("p", { text: block.text }));
    } else if (block.type === "h3") {
      body.appendChild(el("h3", { text: block.text }));
    } else if (block.type === "callout") {
      body.appendChild(el("div", { cls:"callout", text: block.text }));
    } else if (block.type === "tip") {
      const d = el("div", { cls:"tip" });
      d.appendChild(el("b", { text:"Try it: " }));
      d.appendChild(document.createTextNode(block.text));
      body.appendChild(d);
    } else if (block.type === "ul") {
      const ul = el("ul", { cls: block.cls || "" });
      for (const it of block.items) {
        if (typeof it === "string") {
          ul.appendChild(el("li", { text: it }));
        } else {
          const li = el("li");
          li.appendChild(el("b", { text: it.b }));
          li.appendChild(document.createTextNode(": " + it.t));
          ul.appendChild(li);
        }
      }
      body.appendChild(ul);
    } else if (block.type === "examples") {
      const ul = el("ul", { cls:"examples" });
      for (const it of block.items) {
        const li = el("li");
        li.appendChild(el("span", { cls:"mark", text: it.mark }));
        li.appendChild(document.createTextNode(it.text));
        ul.appendChild(li);
      }
      body.appendChild(ul);
    }
  }
}

function setActiveTab(tab) {
  activeTab = tab;
  for (const t of document.querySelectorAll("#onboardTabs .tab")) {
    t.classList.toggle("active", t.dataset.tab === tab);
  }
  renderOnboardBody();
}

function showOnboard() {
  setActiveTab("what");
  $("onboardModal").classList.add("on");
}
function hideOnboard() {
  $("onboardModal").classList.remove("on");
}

function maybeShowOnboardOnLoad() {
  let never = false, seen = false;
  try {
    never = localStorage.getItem(ONBOARD_NEVER) === "1";
    seen  = localStorage.getItem(ONBOARD_KEY) === "1";
  } catch(e) { /* localStorage may be unavailable */ }
  if (!never && !seen) showOnboard();
}

// ---------- Region select ----------
const REGION_KEY = "electicity_region";

function loadRegion() {
  try {
    const r = localStorage.getItem(REGION_KEY);
    if (r != null) state.region = r;
  } catch(e) {}
  $("regionSelect").value = state.region || "";
}
function saveRegion() {
  try { localStorage.setItem(REGION_KEY, state.region); } catch(e) {}
}

// ---------- Alliances persistence ----------
const ALLIANCES_KEY = "electicity_alliances";
function loadAlliances() {
  try {
    const s = localStorage.getItem(ALLIANCES_KEY);
    if (s) {
      const arr = JSON.parse(s);
      if (Array.isArray(arr)) {
        for (const k of arr) if (BLOCS[k]) state.alliances.add(k);
      }
    }
  } catch(e) {}
}
function saveAlliances() {
  try { localStorage.setItem(ALLIANCES_KEY, JSON.stringify([...state.alliances])); } catch(e) {}
}

// ---------- Share link (URL permalink) ----------
// Encodes a shareable subset of state into the URL hash so a build plus posture
// can be reopened in another browser. Pure client, no backend. Versioned so older
// links keep parsing as the schema grows; unknown tech or bloc keys are dropped.
const SHARE_VERSION = 1;

function b64urlEncode(str) {
  return btoa(unescape(encodeURIComponent(str)))
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function b64urlDecode(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  return decodeURIComponent(escape(atob(s)));
}

function encodeShareState() {
  const payload = {
    v: SHARE_VERSION,
    b: state.build.map(c => [c.tech, c.capacity]),
    r: state.region || "",
    a: [...state.alliances],
    z: state.ztaOn ? 1 : 0,
    c: state.critOnly ? 1 : 0,
    h: state.challengeOn ? 1 : 0,
    i: state.challengeIdx | 0,
    s: state.shock || "bau",
  };
  return b64urlEncode(JSON.stringify(payload));
}

function applyShareState(payload) {
  if (!payload || payload.v !== SHARE_VERSION) return false;
  if (Array.isArray(payload.b)) {
    state.build = payload.b
      .filter(t => Array.isArray(t) && BASE_PARAMS[t[0]])
      .map(t => ({ tech: t[0], capacity: Number(t[1]) || defaultCapacity(t[0]) }));
  }
  state.region = typeof payload.r === "string" ? payload.r : "";
  state.alliances = new Set(Array.isArray(payload.a) ? payload.a.filter(k => BLOCS[k]) : []);
  state.ztaOn = !!payload.z;
  state.critOnly = !!payload.c;
  state.challengeOn = !!payload.h;
  state.challengeIdx = Math.min(Math.max(payload.i | 0, 0), CHALLENGES.length - 1);
  state.shock = SHOCK_BASE_PROB[payload.s] != null ? payload.s : "bau";
  return true;
}

// Pull DOM controls back into sync after applyShareState mutates state.
function syncControlsToState() {
  $("regionSelect").value = state.region || "";
  $("ztaToggle").checked = state.ztaOn;
  $("critOnly").checked = state.critOnly;
  const ch = $("challengeMode");
  if (ch) { ch.checked = state.challengeOn; $("challengeBox").classList.toggle("on", state.challengeOn); }
}

function loadShareFromHash() {
  const h = location.hash || "";
  if (!h.startsWith("#s=")) return false;
  try {
    return applyShareState(JSON.parse(b64urlDecode(h.slice(3))));
  } catch(e) { return false; }
}

function makeShareURL() {
  return location.origin + location.pathname + "#s=" + encodeShareState();
}

function copyShareLink() {
  const url = makeShareURL();
  try { history.replaceState(null, "", "#s=" + encodeShareState()); } catch(e) {}
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(
      () => narrate("Share link copied. Paste it anywhere to reopen this exact build and posture."),
      () => narrate("Copy this share link: " + url)
    );
  } else {
    narrate("Copy this share link: " + url);
  }
}

// ---------- Leaderboard (local, share-link ready) ----------
// Best score per challenge or campaign, persisted in localStorage. Each entry
// stores its share string, so a row reloads the exact build and a future global
// board can accept the same string with no schema change.
const LEADERBOARD_KEY = "electicity_leaderboard";
const LEADERBOARD_MAX = 10;

function loadLeaderboard() {
  try {
    const a = JSON.parse(localStorage.getItem(LEADERBOARD_KEY) || "[]");
    return Array.isArray(a) ? a : [];
  } catch(e) { return []; }
}
function saveLeaderboard(board) {
  try { localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(board)); } catch(e) {}
}
function recordScore(entry) {
  const board = loadLeaderboard();
  const i = board.findIndex(e => e.mode === entry.mode && e.name === entry.name);
  // Cheap exit on the hot path: only an improvement does the encode/write/sort/render.
  if (i >= 0 && entry.score <= board[i].score) return;
  entry.share = encodeShareState();
  entry.ts = Date.now();
  if (i >= 0) board[i] = entry;
  else board.push(entry);
  board.sort((a, b) => b.score - a.score);
  if (board.length > LEADERBOARD_MAX) board.length = LEADERBOARD_MAX;
  saveLeaderboard(board);
  renderLeaderboard();
}
function renderLeaderboard() {
  const host = $("leaderboard");
  if (!host) return;
  const board = loadLeaderboard();
  clear(host);
  if (!board.length) {
    host.appendChild(el("div", { cls: "lb-empty", text: "No scores yet. Pass a challenge or finish a campaign to land on the board." }));
    return;
  }
  board.forEach((e, idx) => {
    const row = el("div", { cls: "lb-row" });
    row.appendChild(el("span", { cls: "lb-rank", text: "#" + (idx + 1) }));
    row.appendChild(el("span", { cls: "lb-score", text: String(e.score) }));
    row.appendChild(el("span", { cls: "lb-name", text: e.name }));
    const load = el("button", { cls: "lb-load", text: "load" });
    load.addEventListener("click", () => {
      try {
        if (applyShareState(JSON.parse(b64urlDecode(e.share)))) {
          syncControlsToState();
          rerender();
          narrate("Loaded '" + e.name + "' (score " + e.score + ") from the leaderboard.");
        }
      } catch(err) { narrate("That leaderboard entry could not be loaded."); }
    });
    row.appendChild(load);
    host.appendChild(row);
  });
}

// ---------- Export ----------
function pad2(n) { return n < 10 ? "0" + n : "" + n; }
function timestampForFile() {
  const d = new Date();
  const ymd = d.getFullYear() + "-" + pad2(d.getMonth()+1) + "-" + pad2(d.getDate());
  const hms = pad2(d.getHours()) + pad2(d.getMinutes()) + pad2(d.getSeconds());
  return { ymd, hms };
}

function buildGuidance(d) {
  const tips = [];
  const has_pem = state.build.find(c => c.tech === "pem_electrolyzer");
  const has_solar = state.build.find(c => c.tech === "solar_pv_utility");
  const has_battery = state.build.find(c => BASE_PARAMS[c.tech].kind === "sto" && c.tech !== "h2_storage_buffer");
  const gens = state.build.filter(c => BASE_PARAMS[c.tech].kind === "gen");

  if (d.total_capex > 36e6) {
    tips.push("If you are over budget, cut some solar capacity, or swap a PEM electrolyzer for the cheaper alkaline one.");
  }
  if (d.blended_lcoe && d.blended_lcoe > 280 && has_pem) {
    tips.push("If your power price is high and you use a PEM electrolyzer, switch to alkaline. It is cheaper and does not need iridium.");
  }
  if (state.shock === "maritime_blockade" || state.shock === "regional_autarky") {
    tips.push("If shipping is at risk, line up local suppliers and keep one year of spare parts on site.");
  }
  if (gens.length === 1 && gens[0].tech === "solar_pv_utility" && !has_battery) {
    tips.push("If solar is your only source, add a battery. Without one, the lights go off after sunset and on cloudy days.");
  }
  const r = state.region || "";
  if (r === "Pilbara WA (AU, water-stressed)" || r === "New Mexico (US, water-stressed)" || r === "Texas Permian (US, water-stressed)") {
    tips.push("If the region is dry, use dry cooling or treated grey water to save fresh water.");
  }
  if (!state.ztaOn) {
    tips.push("If cyber safety is off, turn it on before launching the site. ZTA controls add a small reliability bonus.");
  }
  return tips.slice(0, 6);
}

function findActiveChallengeName() {
  if (!state.challengeOn) return null;
  const ch = CHALLENGES[state.challengeIdx];
  return ch ? ch.name : null;
}

function buildExportText(d) {
  const { ymd, hms } = timestampForFile();
  const dateStr = ymd;
  const timeStr = pad2(new Date().getHours()) + ":" + pad2(new Date().getMinutes()) + ":" + pad2(new Date().getSeconds());
  const lines = [];
  lines.push("=================================================================");
  lines.push("ELECTICITY FEASIBILITY: Microgrid Playground - run export");
  lines.push("=================================================================");
  lines.push("Date:                " + dateStr);
  lines.push("Time:                " + timeStr);
  lines.push("Params snapshot:     2026-05  -  USD nominal, source years 2023 to 2025  -  playground v0.5.0");
  lines.push("About these numbers: Costs come from public reports written between 2023 and 2025.");
  lines.push("                     They are not adjusted for inflation. Useful as a 'roughly today' baseline.");
  lines.push("                     The exact source for each number is in tech_params.yaml in the project repository.");
  lines.push("");
  lines.push("--- What you set up ---");
  if (state.build.length === 0) {
    lines.push("Build:               (nothing added yet)");
  } else {
    lines.push("Build:");
    for (const c of state.build) {
      const role = compRoleLabel(c.tech);
      lines.push("  - " + PRETTY[c.tech] + " [" + role + "]: " + formatCap(c.capacity, c.tech));
    }
  }
  lines.push("Surprise event:      " + state.shock.replace(/_/g," "));
  lines.push("Cyber safety on:     " + (state.ztaOn ? "yes" : "no"));
  lines.push("Essentials only:     " + (state.critOnly ? "yes" : "no"));
  lines.push("Challenge mode:      " + (state.challengeOn ? "yes (" + (findActiveChallengeName() || "-") + ")" : "no"));
  lines.push("Region:              " + (state.region ? state.region : "not selected"));
  if (state.alliances.size > 0) {
    const blocList = [...state.alliances].map(k => BLOCS[k].label).join(", ");
    lines.push("Friends Union:       " + blocList + " (diplomacy spend " + fmtUSD(diplomacyCapex()) + ")");
    if (state.alliances.size >= 3) lines.push("                     UNION UMBRELLA active: extra 25% damping on all shocks.");
  } else {
    lines.push("Friends Union:       not joined (running solo on shocks)");
  }
  lines.push("");
  lines.push("--- What the model returns ---");
  lines.push("Build cost:          " + fmtUSD(d.total_capex) + " (includes 20 percent for cables, foundations, project work)");
  lines.push("  Equipment:         " + fmtUSD(d.capex_eq));
  lines.push("  Storage:           " + fmtUSD(d.capex_sto));
  lines.push("  Diplomacy:         " + fmtUSD(d.diplomacy_capex || 0));
  lines.push("  Budget cap:        $36.00M (" + (d.total_capex/36e6*100).toFixed(0) + " percent used)");
  lines.push("Cost breakdown (before the 20 percent extra):");
  for (const b of d.breakdown) {
    lines.push("  - " + PRETTY[b.tech] + ": " + b.capacity + " " + b.unit + " -> " + fmtUSD(b.capex_raw));
  }
  lines.push("Power price:         " + (d.blended_lcoe ? "$" + d.blended_lcoe.toFixed(0) + " per megawatt hour" : "not available, no generators"));
  lines.push("Hydrogen price:      " + (d.lcoh_val ? "$" + d.lcoh_val.toFixed(2) + " per kilo" : "not available, needs an electrolyzer plus power"));
  lines.push("Lights stay on:      " + (d.avail*100).toFixed(1) + " percent of the year");
  lines.push("  Average run rate:  " + (d.avg_cf*100).toFixed(0) + " percent");
  lines.push("  Storage hours:     " + d.buffer_hours.toFixed(1) + " hours");
  lines.push("  Total generation:  " + (d.gen_kw_total/1000).toFixed(2) + " megawatts");
  if (state.challengeOn && state.lastChallengeScore != null) {
    lines.push("Challenge result:    " + (findActiveChallengeName() || "-") + " | " + (state.lastChallengeVerdict || "-") + " | score " + state.lastChallengeScore);
  }
  lines.push("");
  lines.push("--- Tips to improve your design ---");
  const tips = buildGuidance(d);
  if (tips.length === 0) {
    lines.push("  No tips to share for this configuration. Looks balanced.");
  } else {
    for (const t of tips) lines.push("  - " + t);
  }
  lines.push("");
  lines.push("--- Notes ---");
  lines.push("Generated by playground/microgrid_sim.html.");
  lines.push("These numbers are for learning. The exact values live in /model/data/tech_params.yaml.");
  lines.push("See DISCLAIMER.md for limits and assumptions.");
  lines.push("=================================================================");
  return lines.join("\n") + "\n";
}

function exportResults() {
  const d = computeDistrict();
  if (state.challengeOn) renderChallenge(d); // refresh score before export
  const text = buildExportText(d);
  const { ymd, hms } = timestampForFile();
  const filename = "electicity_run_" + ymd + "_" + hms + ".txt";
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 0);
  narrate("Saved your run as " + filename + ".");
}

// ---------- Decision cards (16 authored, ASCII-only bodies) ----------
// Each card: { id, title, body, prerequisites(active,state)->bool, weight,
//              accept{ label, effects(state) }, decline{ label, effects(state) },
//              fallback_on_prereq_fail: "decline" | "skip" | "force",
//              spawnsOnAccept?: { id, delay } }
// Effects mutate state.campaign.permMults / activeBonuses / immunities and may
// queue chained cards via state.campaign.queuedCards.
const DECISION_CARDS = [
  {
    id: "latam_lithium_offer",
    title: "LATAM FRIEND offer",
    body: "Chile signals a 10-year lithium offtake at 15 percent below market via a LATAM FRIEND trade pact, in exchange for declining your Pilbara expansion option.",
    prerequisites: () => true,
    weight: 1.0,
    accept: {
      label: "Sign the offtake (-10% Li-ion/LFP capex, -1 sov)",
      effects: (st) => {
        const m = st.campaign.permMults.tech_capex_mult;
        m.li_ion_battery_grid = (m.li_ion_battery_grid || 1) * 0.90;
        m.lfp_battery_grid = (m.lfp_battery_grid || 1) * 0.90;
        st.campaign.activeBonuses.latam_offtake = true;
        // Queue card 11 (LATAM follow-up) in Y+3.
        const future = st.campaign.year + 3;
        if (future <= 5) {
          (st.campaign.queuedCards[future] = st.campaign.queuedCards[future] || []).push("latam_followup");
        }
      },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "gulf_h2_mou",
    title: "GULF-leaning offer",
    body: "NEOM signals a hydrogen MoU. Accepting brings cheaper H2 storage but raises decoupling risk next year.",
    prerequisites: () => true,
    weight: 0.9,
    accept: {
      label: "Sign MoU (-8% H2 storage capex, +0.05 china_decoupling next year)",
      effects: (st) => {
        const m = st.campaign.permMults.tech_capex_mult;
        m.h2_storage_buffer = (m.h2_storage_buffer || 1) * 0.92;
        st.campaign.activeBonuses.gulf_extra_decoupling = 0.05;
      },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "eu_audit",
    title: "EU FRIEND audit",
    body: "RFNBO compliance audit lands. Pass means a 5 percent LCOH bump and an EU trust bonus; failing means EU damping is halved next year.",
    prerequisites: (active) => active.has("EU_FRIEND"),
    weight: 0.8,
    accept: {
      label: "Cooperate (+5% LCOH, +1 EU trust)",
      effects: (st) => {
        st.campaign.permMults.lcoh_mult *= 1.05;
        st.campaign.trust["EU_FRIEND"] = (st.campaign.trust["EU_FRIEND"] || 0) + 1;
      },
    },
    decline: {
      label: "Decline (EU damping halved next year)",
      effects: (st) => { st.campaign.activeBonuses.eu_damping_half_next = true; },
    },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "africa_pgm_strike",
    title: "AFRICA FRIEND disruption",
    body: "A South Africa PGM-mining strike threatens platinum supply. AFRICA FRIEND members can pre-buy stockpile now or take their chances.",
    prerequisites: (active) => active.has("AFRICA_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Pre-buy stockpile (+$1M one-time, immune to next pt_shortage)",
      effects: (st) => {
        st.campaign.permMults.capex_one_time += 1e6;
        st.campaign.immunities.pt_shortage = (st.campaign.immunities.pt_shortage || 0) + 1;
      },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "pacific_cyber_pact",
    title: "WEST + SOUTH-CENTRAL pact",
    body: "Pacific cyber-defence pact (US-AU). ZTA bonus doubles to 4 percent for the run; 1 sovereignty charged.",
    prerequisites: (active) => active.has("WEST_FRIEND") && active.has("SOUTH_CENTRAL_FRIEND"),
    weight: 0.6,
    accept: {
      label: "Sign (ZTA bonus doubles, +1 sov charged)",
      effects: (st) => { st.campaign.activeBonuses.zta_double = true; },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "east_nickel_jv",
    title: "EAST FRIEND JV",
    body: "Indonesian nickel JV proposal. Accepting brings cheaper LFP and a sovereignty rebate.",
    prerequisites: (active) => active.has("EAST_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Sign JV (-8% LFP capex, -1 sov)",
      effects: (st) => {
        const m = st.campaign.permMults.tech_capex_mult;
        m.lfp_battery_grid = (m.lfp_battery_grid || 1) * 0.92;
      },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "sc_indus_treaty",
    title: "SOUTH-CENTRAL FRIEND treaty",
    body: "Indus water treaty extension. Accepting builds SOUTH-CENTRAL trust; declining halves SC damping next year.",
    prerequisites: (active) => active.has("SOUTH_CENTRAL_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Renew (+1 SC trust)",
      effects: (st) => { st.campaign.trust["SOUTH_CENTRAL_FRIEND"] = (st.campaign.trust["SOUTH_CENTRAL_FRIEND"] || 0) + 1; },
    },
    decline: {
      label: "Decline (SC damping halved next year)",
      effects: (st) => { st.campaign.activeBonuses.sc_damping_half_next = true; },
    },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "west_ira_extension",
    title: "WEST FRIEND policy expansion",
    body: "The US Inflation Reduction Act extends the 45V PTC by another 5 years. WEST FRIEND members are eligible for an additional 3 percent capex rebate.",
    prerequisites: (active) => active.has("WEST_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Claim PTC extension (+3% capex rebate)",
      effects: (st) => { st.campaign.permMults.ptc_extra += 0.03; },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "russia_oil_shock",
    title: "External shock",
    body: "Russia oil-shock spillover. Solar capex baseline rises 5 percent next year. This is a forced event with no decline option.",
    prerequisites: () => true,
    weight: 0.5,
    accept: {
      label: "Acknowledge",
      effects: (st) => {
        const m = st.campaign.permMults.tech_capex_mult;
        m.solar_pv_utility = (m.solar_pv_utility || 1) * 1.05;
      },
    },
    decline: {
      label: "Acknowledge",
      effects: (st) => {
        const m = st.campaign.permMults.tech_capex_mult;
        m.solar_pv_utility = (m.solar_pv_utility || 1) * 1.05;
      },
    },
    fallback_on_prereq_fail: "force",
  },
  {
    id: "north_atlantic_cable",
    title: "NORTH FRIEND infrastructure",
    body: "Atlantic cable cut threatens routing. Pay for redundancy now or accept lower availability next year.",
    prerequisites: (active) => active.has("NORTH_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Build redundancy (+$0.8M capex)",
      effects: (st) => { st.campaign.permMults.capex_one_time += 0.8e6; },
    },
    decline: {
      label: "Accept the risk (-10% availability next year)",
      effects: (st) => { st.campaign.activeBonuses.cable_cut_next = true; },
    },
    fallback_on_prereq_fail: "decline",
  },
  // Chain follow-ups
  {
    id: "latam_followup",
    title: "LATAM follow-up",
    body: "Chile renegotiates the offtake price. Accept the 5 percent increase to keep half of the original capex bonus, or decline and lose the whole thing.",
    prerequisites: (active, st) => active.has("LATAM_FRIEND") && st.campaign.activeBonuses.latam_offtake,
    weight: 0,
    accept: {
      label: "Pay the increase (keep -5% Li bonus)",
      effects: (st) => {
        // Reverse half of the original 0.90 multiplier (keep -5% net).
        const m = st.campaign.permMults.tech_capex_mult;
        m.li_ion_battery_grid = (m.li_ion_battery_grid || 1) / 0.90 * 0.95;
        m.lfp_battery_grid = (m.lfp_battery_grid || 1) / 0.90 * 0.95;
      },
    },
    decline: {
      label: "Cancel the offtake (-1 LATAM trust, lose bonus)",
      effects: (st) => {
        const m = st.campaign.permMults.tech_capex_mult;
        m.li_ion_battery_grid = (m.li_ion_battery_grid || 1) / 0.90;
        m.lfp_battery_grid = (m.lfp_battery_grid || 1) / 0.90;
        st.campaign.activeBonuses.latam_offtake = false;
        st.campaign.trust["LATAM_FRIEND"] = Math.max(0, (st.campaign.trust["LATAM_FRIEND"] || 0) - 1);
      },
    },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "africa_phosphate_swap",
    title: "AFRICA FRIEND offer",
    body: "Morocco proposes a phosphate plus green-NH3 swap. Accepting cuts electrolyzer capex; declining keeps your hands free.",
    prerequisites: (active) => active.has("AFRICA_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Sign swap (-5% all-electrolyzer capex, +1 AFRICA trust)",
      effects: (st) => {
        const m = st.campaign.permMults.tech_capex_mult;
        m.pem_electrolyzer = (m.pem_electrolyzer || 1) * 0.95;
        m.alkaline_electrolyzer = (m.alkaline_electrolyzer || 1) * 0.95;
        st.campaign.trust["AFRICA_FRIEND"] = (st.campaign.trust["AFRICA_FRIEND"] || 0) + 1;
        st.campaign.activeBonuses.africa_swap = true;
        const future = st.campaign.year + 2;
        if (future <= 5) {
          (st.campaign.queuedCards[future] = st.campaign.queuedCards[future] || []).push("africa_followup");
        }
      },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "africa_followup",
    title: "AFRICA follow-up",
    body: "Morocco contract renewal. Lock in the bonus for the rest of the run, or let it expire next year.",
    prerequisites: (active, st) => active.has("AFRICA_FRIEND") && st.campaign.activeBonuses.africa_swap,
    weight: 0,
    accept: {
      label: "Renew (lock the -5% bonus permanently)",
      effects: (st) => { st.campaign.activeBonuses.africa_swap_locked = true; },
    },
    decline: {
      label: "Let it expire next year",
      effects: (st) => { st.campaign.activeBonuses.africa_expire_next = true; },
    },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "all_bloc_summit",
    title: "All-bloc summit",
    body: "World Energy Council convenes a summit of major blocs. Sign on for an umbrella boost at a sovereignty cost.",
    prerequisites: (active) => active.size >= 4,
    weight: 0.5,
    accept: {
      label: "Sign (+5% umbrella, -2 sovereignty)",
      effects: (st) => { st.campaign.activeBonuses.summit_umbrella = 0.05; },
    },
    decline: { label: "Decline", effects: () => {} },
    fallback_on_prereq_fail: "decline",
    sovCost: 2,
  },
  {
    id: "sofc_pilot",
    title: "Research grant: SOFC pilot",
    body: "Bloom Energy and Ceres Power propose a solid-oxide demonstrator. SOFC and SOEC use no iridium and no platinum. Y+2 delayed payoff: immunity to the next pt_shortage and ir_shortage.",
    prerequisites: () => true,
    weight: 0.5,
    accept: {
      label: "Fund (-$1M one-time, +1 sov, Y+2 immunity)",
      effects: (st) => {
        st.campaign.permMults.capex_one_time += 1e6;
        st.campaign.activeBonuses.sofc_pending_year = st.campaign.year + 2;
      },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
    sovCost: 1,
  },
  {
    id: "iron_air_pilot",
    title: "Research grant: iron-air pilot",
    body: "Form Energy proposes an iron-air long-duration battery demonstrator. Abundant iron, no lithium. Y+3 delayed payoff: full immunity to the next li_shortage.",
    prerequisites: () => true,
    weight: 0.5,
    accept: {
      label: "Fund (-$1.5M one-time, +1 sov, Y+3 immunity)",
      effects: (st) => {
        st.campaign.permMults.capex_one_time += 1.5e6;
        st.campaign.activeBonuses.iron_air_pending_year = st.campaign.year + 3;
      },
    },
    decline: { label: "Pass", effects: () => {} },
    fallback_on_prereq_fail: "decline",
    sovCost: 1,
  },
  {
    id: "east_reexport_betrayal",
    title: "EAST FRIEND re-export",
    body: "An EAST FRIEND cell processor is quietly re-exporting your stack design to a competing bloc. Confront and re-paper the contract, or let it slide and watch trust erode.",
    prerequisites: (active) => active.has("EAST_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Confront and re-paper (-$1M one-time, hold EAST trust)",
      effects: (st) => { st.campaign.permMults.capex_one_time += 1e6; },
    },
    decline: {
      label: "Let it slide (-2 EAST trust, +6% LCOH)",
      effects: (st) => {
        st.campaign.trust["EAST_FRIEND"] = Math.max(0, (st.campaign.trust["EAST_FRIEND"] || 0) - 2);
        st.campaign.permMults.lcoh_mult *= 1.06;
      },
    },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "sanctions_retaliation",
    title: "Retaliation risk",
    body: "Your WEST FRIEND posture drew a counter-sanction on PGM imports. Hold the line and absorb the cost now, or de-escalate and spend alliance trust. Holding invites an aftermath next year.",
    prerequisites: (active) => active.has("WEST_FRIEND"),
    weight: 0.7,
    accept: {
      label: "Hold the line (+6% LCOH, aftermath queued next year)",
      effects: (st) => {
        st.campaign.permMults.lcoh_mult *= 1.06;
        const future = st.campaign.year + 1;
        if (future <= 5) (st.campaign.queuedCards[future] = st.campaign.queuedCards[future] || []).push("retaliation_aftermath");
      },
    },
    decline: {
      label: "De-escalate (-1 WEST trust)",
      effects: (st) => { st.campaign.trust["WEST_FRIEND"] = Math.max(0, (st.campaign.trust["WEST_FRIEND"] || 0) - 1); },
    },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "retaliation_aftermath",
    title: "Counter-sanction aftermath",
    body: "The counter-sanction matured. A PGM stockpile drawdown can blunt the next pt_shortage, or you can ride it out and keep the cash.",
    prerequisites: () => true,
    weight: 0,
    accept: {
      label: "Draw down stockpile (-$0.8M one-time, immunity to next pt_shortage)",
      effects: (st) => {
        st.campaign.permMults.capex_one_time += 0.8e6;
        st.campaign.immunities["pt_shortage"] = (st.campaign.immunities["pt_shortage"] || 0) + 1;
      },
    },
    decline: { label: "Ride it out", effects: () => {} },
    fallback_on_prereq_fail: "decline",
  },
  {
    id: "alliance_upkeep",
    title: "Alliance upkeep",
    body: "Treaties decay without maintenance. Fund a round of diplomatic upkeep, or skip it and let trust erode across every held bloc.",
    prerequisites: (active) => active.size >= 1,
    weight: 0.6,
    accept: {
      label: "Fund upkeep (-$0.5M one-time, hold all trust)",
      effects: (st) => {
        st.campaign.permMults.capex_one_time += 0.5e6;
        for (const b of (st.alliances || state.alliances)) st.campaign.maintainedThisYear.add(b);
      },
    },
    decline: {
      label: "Skip it (-1 trust on every held bloc)",
      effects: (st) => {
        for (const b of (st.alliances || state.alliances)) {
          st.campaign.trust[b] = Math.max(0, (st.campaign.trust[b] || 0) - 1);
        }
      },
    },
    fallback_on_prereq_fail: "decline",
  },
];

const CARDS_BY_ID = (() => {
  const m = {};
  for (const c of DECISION_CARDS) m[c.id] = c;
  return m;
})();

function eligibleCards(activeSet, st) {
  return DECISION_CARDS.filter(c => {
    try { return c.prerequisites(activeSet, st); } catch (e) { return false; }
  });
}

// Pick a card for the year. Spawn-queued cards take priority. Then weighted draw.
function drawCard(st, rng) {
  const yQueue = st.campaign.queuedCards[st.campaign.year] || [];
  if (yQueue.length > 0) {
    const id = yQueue.shift();
    const card = CARDS_BY_ID[id];
    if (!card) return null;
    if (!card.prerequisites(st.alliances || state.alliances, st)) {
      const fb = card.fallback_on_prereq_fail || "decline";
      if (fb === "decline") {
        narrate("Card '" + card.title + "' auto-declined: prerequisites no longer met.", "warn");
        try { card.decline.effects(st); } catch(e) {}
        st.campaign.history.push({ year: st.campaign.year, cardId: card.id, accepted: false, autoDeclined: true });
      } else if (fb === "force") {
        try { card.accept.effects(st); } catch(e) {}
      }
      return null;
    }
    return card;
  }
  // Weighted pool (cards with weight > 0 only).
  const pool = eligibleCards(state.alliances, st).filter(c => (c.weight || 0) > 0);
  if (pool.length === 0) return null;
  const totalW = pool.reduce((s, c) => s + (c.weight || 0), 0);
  let r = rng.nextFloat() * totalW;
  for (const c of pool) {
    r -= (c.weight || 0);
    if (r <= 0) return c;
  }
  return pool[pool.length - 1];
}

// Hard sovereignty cap on cards: if accepting would push above SOVEREIGNTY_MAX,
// auto-decline with narration.
function cardWouldOverflowSovereignty(card) {
  const sc = card.sovCost || 0;
  if (sc <= 0) return false;
  return (sovereigntySpent() + sc) > SOVEREIGNTY_MAX;
}

// Roll a shock from shockDistribution using the provided RNG. extraDelta is a
// campaign-only bias (e.g. retaliation) layered on top of the shared distribution
// without touching the parity-locked shockDistribution kernel.
function rollShock(activeSet, rng, extraDelta) {
  const dist = shockDistribution(activeSet);
  if (extraDelta) {
    for (const [s, d] of Object.entries(extraDelta)) {
      if (dist[s] != null) dist[s] = Math.max(0, dist[s] + d);
    }
    let sum = 0;
    for (const s in dist) sum += dist[s];
    if (sum > 0) for (const s in dist) dist[s] /= sum;
  }
  let r = rng.nextFloat();
  let cum = 0;
  for (const [s, p] of Object.entries(dist)) {
    cum += p;
    if (r < cum) return s;
  }
  return Object.keys(dist)[0];
}

// Apply per-year activeBonuses + permMults to a deep-cloned BASE_PARAMS during
// score computation. We piggy-back on applyShock by stuffing extra capex multipliers
// into a transient mod table, but it's cleaner to compute capex post-hoc.
function _applyCampaignPermMults(params, st) {
  const m = st.campaign.permMults;
  if (m && m.tech_capex_mult) {
    for (const [tech, mult] of Object.entries(m.tech_capex_mult)) {
      if (!params[tech]) continue;
      if ("capex_per_kw" in params[tech]) params[tech].capex_per_kw *= mult;
      if ("capex_per_kwh" in params[tech]) params[tech].capex_per_kwh *= mult;
      if ("capex_per_kg" in params[tech]) params[tech].capex_per_kg *= mult;
    }
  }
  if (m && m.tech_opex_mult) {
    for (const [tech, mult] of Object.entries(m.tech_opex_mult)) {
      if (!params[tech]) continue;
      if ("opex_per_kw_yr" in params[tech]) params[tech].opex_per_kw_yr *= mult;
    }
  }
  return params;
}

// Score a year given a (snapshot) set of effective targets and applied shock.
function scoreCampaignYear(yearTargets, drawnShock, st) {
  // Compute district with campaign trust + perm mults applied.
  // 1. Use applyShock for bloc capex/opex bonuses + shock dampening (with trust).
  //    Defected blocs give no protection or bonus this year (they still cost capex).
  const protectiveSet = (st.campaign.defected && st.campaign.defected.size)
    ? new Set([...state.alliances].filter(b => !st.campaign.defected.has(b)))
    : state.alliances;
  let params = applyShock(drawnShock, protectiveSet, st.campaign.trust);
  // 2. Apply perm mults (cards-driven).
  params = _applyCampaignPermMults(params, st);
  // 3. Apply per-year transient activeBonuses.
  if (st.campaign.activeBonuses.eu_damping_half_next) {
    // re-run damping at half for EU? simplest: this year's shock got dampened normally.
    // Implementation: skip; the *next-year-only* effect will be cleared at year-end.
  }
  if (yearTargets.solar_kill && params.solar_pv_utility) params.solar_pv_utility.capacity_factor = 0.05;
  // 4. Run a stripped-down compute equivalent to computeDistrict with these params.
  let capex_eq = 0, capex_sto = 0, opex = 0, fuel = 0;
  let gen_mwh = 0, weighted_lcoe_num = 0, weighted_lcoe_den = 0;
  let weighted_cf_num = 0, weighted_cf_den = 0;
  let storage_kwh = 0, h2_storage_kg = 0;
  let h2_kw = 0, h2_capex_kw = 0, h2_opex_per_kw_yr = 0, h2_eff = 0;
  let has_fc = false;
  for (const c of state.build) {
    const p = params[c.tech];
    if (!p) continue;
    if (p.kind === "gen") {
      const kw = c.capacity;
      const c_capex = p.capex_per_kw * kw;
      const c_opex = p.opex_per_kw_yr * kw;
      const energy_mwh = kw * p.capacity_factor * 8760 / 1000;
      const c_fuel = (p.fuel_cost_per_mwh || 0) * energy_mwh;
      capex_eq += c_capex; opex += c_opex; fuel += c_fuel;
      gen_mwh += energy_mwh;
      weighted_cf_num += p.capacity_factor * kw;
      weighted_cf_den += kw;
      const tech_lcoe = lcoe({ capex_total: c_capex, opex_yr: c_opex, fuel_yr: c_fuel,
        energy_mwh_yr: energy_mwh, lifetime_years: p.lifetime_years, discount_rate: DISCOUNT_RATE });
      weighted_lcoe_num += tech_lcoe * energy_mwh;
      weighted_lcoe_den += energy_mwh;
    } else if (p.kind === "sto") {
      if (c.tech === "h2_storage_buffer") {
        capex_sto += p.capex_per_kg * c.capacity;
        h2_storage_kg += c.capacity;
      } else {
        capex_sto += p.capex_per_kwh * c.capacity;
        opex += (p.opex_per_kw_yr || 5) * (c.capacity / 4);
        storage_kwh += c.capacity;
      }
    } else if (p.kind === "h2") {
      const kw = c.capacity;
      capex_eq += p.capex_per_kw * kw;
      opex += p.opex_per_kw_yr * kw;
      if (c.tech.includes("electrolyzer")) {
        h2_kw += kw;
        h2_capex_kw = p.capex_per_kw;
        h2_opex_per_kw_yr = p.opex_per_kw_yr;
        h2_eff = p.efficiency_lhv;
      }
      if (c.tech === "pem_fuel_cell_stationary") has_fc = true;
    }
  }
  const dipCapex = diplomacyCapex(state.alliances);
  // ptc_rebate: bloc bonuses + card-driven extra.
  let ptc_rebate = _bonusSum(state.alliances, "ptc_capex_rebate_pct") + (st.campaign.permMults.ptc_extra || 0);
  if (ptc_rebate < 0) ptc_rebate = 0;
  if (ptc_rebate > 0.5) ptc_rebate = 0.5;
  const equipment_with_bos = (capex_eq + capex_sto) * (1 + BOS_FRAC);
  let total_capex = equipment_with_bos * (1 - ptc_rebate) + dipCapex + (st.campaign.permMults.capex_one_time || 0);
  // Reset capex_one_time after applying for this year? Keep it persistent (one-time cost is paid once)
  // We zero it out after scoring the first year it appears.
  // Availability:
  const blended_lcoe = weighted_lcoe_den > 0 ? weighted_lcoe_num / weighted_lcoe_den : null;
  const avg_cf = weighted_cf_den > 0 ? weighted_cf_num / weighted_cf_den : 0;
  const load_kw = DISTRICT_LOAD_MW * 1000;
  const buffer_hours = (storage_kwh + h2_storage_kg * 33.33 * (has_fc ? 0.50 : 0)) / load_kw;
  const buffer_factor = 1 - Math.exp(-buffer_hours / 12);
  const gen_kw_total = state.build.reduce((s,c)=>{ const p = params[c.tech]; return p && p.kind==="gen" ? s + c.capacity : s; }, 0);
  const headroom = gen_kw_total / load_kw;
  const headroom_term = Math.min(headroom, 3) / 3;
  let avail = avg_cf * (0.45 + 0.55 * headroom_term) + buffer_factor * 0.35;
  avail += _bonusSum(state.alliances, "availability_add");
  avail += (st.campaign.permMults.avail_extra || 0);
  if (st.campaign.activeBonuses.cable_cut_next) avail -= 0.10;
  if (yearTargets.critical_only && gen_kw_total > 0) avail = avail + (1 - Math.min(avail, 1)) * 0.30;
  if (state.ztaOn) avail *= (st.campaign.activeBonuses.zta_double ? 1.04 : 1.02);
  if (st.campaign.activeBonuses.summit_umbrella) avail *= (1 + st.campaign.activeBonuses.summit_umbrella);
  if (avail < 0) avail = 0;
  if (avail > 1) avail = 1;
  // Score: same shape as challenge (avail / target * cost_score * 100), bounded.
  const avail_score = Math.min(1.5, avail / yearTargets.target_avail);
  const over = Math.max(0, (total_capex - yearTargets.capex_cap) / yearTargets.capex_cap);
  const cost_score = Math.max(0, 1 - over);
  const score = Math.round(100 * avail_score * cost_score);
  return {
    score: isFinite(score) ? score : 0,
    avail, total_capex, blended_lcoe, drawnShock,
  };
}

// Trust dynamics (code constants; mirrors diplomacy.py). A held bloc that gets
// decision-card attention in a year is maintained and gains trust; a neglected
// held bloc decays toward zero. The alliance_upkeep card maintains every bloc.
const TRUST_MAINTAIN_GAIN = 1;
const TRUST_DECAY = 1;

// Reset campaign state when activated.
function resetCampaign(seed) {
  state.campaign.active = true;
  state.campaign.year = 0;
  state.campaign.totalScore = 0;
  state.campaign.history = [];
  state.campaign.trust = {};
  state.campaign.queuedCards = {};
  state.campaign.rngSeed = (typeof seed === "number") ? seed : 42;
  state.campaign.pendingCard = null;
  state.campaign.cardChoiceMade = false;
  state.campaign.yearTargets = null;
  state.campaign.activeBonuses = {};
  state.campaign.immunities = {};
  state.campaign.maintainedThisYear = new Set();
  state.campaign.trustAtYearStart = {};
  state.campaign.defected = new Set();
  state.campaign.defectingNextYear = new Set();
  state.campaign.retaliationDelta = null;
  state.campaign.permMults = { tech_capex_mult: {}, tech_opex_mult: {}, capex_one_time: 0, lcoh_mult: 1, ptc_extra: 0, avail_extra: 0, dampingExtra: {} };
}

function startNextCampaignYear() {
  if (!state.campaign.active) return;
  if (state.campaign.year >= 5) return;
  state.campaign.year += 1;
  // Snapshot effective targets for this year.
  state.campaign.yearTargets = effectiveTargets();
  // Snapshot trust and reset maintenance tracking; trust is settled at year end.
  state.campaign.trustAtYearStart = { ...state.campaign.trust };
  state.campaign.maintainedThisYear = new Set();
  // Activate queued defections: blocs whose trust hit zero abandon you this year.
  state.campaign.defected = new Set(state.campaign.defectingNextYear);
  state.campaign.defectingNextYear = new Set();
  if (state.campaign.defected.size > 0) {
    // Defection invites retaliation: hostile shocks get more likely this year.
    state.campaign.retaliationDelta = { maritime_blockade: 0.10, china_decoupling: 0.08 };
    const names = [...state.campaign.defected].map(_humanBlocName).join(", ");
    narrate("Neglected to zero trust: " + names + " defects this year. No protection, and retaliation raises hostile-shock odds.", "warn");
  } else {
    state.campaign.retaliationDelta = null;
  }
  // Card phase: draw a card.
  const rng = new Mulberry32(state.campaign.rngSeed + state.campaign.year);
  const card = drawCard(state, rng);
  state.campaign.pendingCard = card;
  state.campaign.cardChoiceMade = !card;
  renderCampaign();
}

function resolveCard(accepted) {
  const card = state.campaign.pendingCard;
  if (!card) return;
  if (accepted && cardWouldOverflowSovereignty(card)) {
    narrate("Card '" + card.title + "' auto-declined: sovereignty cap " + SOVEREIGNTY_MAX + " would be exceeded.", "warn");
    accepted = false;
  }
  try {
    if (accepted) card.accept.effects(state);
    else card.decline.effects(state);
  } catch (e) {
    narrate("Card effects errored: " + e.message, "bad");
  }
  state.campaign.history.push({ year: state.campaign.year, cardId: card.id, accepted });
  state.campaign.pendingCard = null;
  state.campaign.cardChoiceMade = true;
  renderCampaign();
}

function endCampaignYear() {
  if (!state.campaign.active) return;
  if (!state.campaign.cardChoiceMade) {
    narrate("Resolve the decision card first.", "warn");
    return;
  }
  const rng = new Mulberry32(state.campaign.rngSeed + state.campaign.year + 1000);
  let drawnShock = rollShock(state.alliances, rng, state.campaign.retaliationDelta);
  // Apply immunities.
  if (state.campaign.immunities[drawnShock] && state.campaign.immunities[drawnShock] > 0) {
    state.campaign.immunities[drawnShock] -= 1;
    drawnShock = "bau";
  }
  // SOFC / iron-air pending immunities: armed at year >= the pending year.
  if (state.campaign.activeBonuses.sofc_pending_year && state.campaign.year >= state.campaign.activeBonuses.sofc_pending_year) {
    if (drawnShock === "pt_shortage" || drawnShock === "ir_shortage") {
      drawnShock = "bau";
      state.campaign.activeBonuses.sofc_pending_year = 0;
    }
  }
  if (state.campaign.activeBonuses.iron_air_pending_year && state.campaign.year >= state.campaign.activeBonuses.iron_air_pending_year) {
    if (drawnShock === "li_shortage") {
      drawnShock = "bau";
      state.campaign.activeBonuses.iron_air_pending_year = 0;
    }
  }
  const yt = state.campaign.yearTargets || effectiveTargets();
  const res = scoreCampaignYear(yt, drawnShock, state);
  state.campaign.totalScore += res.score;
  // Settle trust: blocs whose trust rose this year (card attention) or covered by
  // upkeep are maintained and gain; neglected held blocs decay toward zero.
  for (const b of state.alliances) {
    const rose = (state.campaign.trust[b] || 0) > (state.campaign.trustAtYearStart[b] || 0);
    if (rose || state.campaign.maintainedThisYear.has(b)) {
      state.campaign.trust[b] = (state.campaign.trust[b] || 0) + TRUST_MAINTAIN_GAIN;
      state.campaign.defectingNextYear.delete(b);
    } else {
      state.campaign.trust[b] = Math.max(0, (state.campaign.trust[b] || 0) - TRUST_DECAY);
      // Trust ground to zero by neglect: the bloc defects next year.
      if (state.campaign.trust[b] === 0) state.campaign.defectingNextYear.add(b);
    }
  }
  // Push history (year was already started; the prior 'card' history entry shares the same year)
  // Update last entry with shock+score, or push fresh if no card.
  let last = state.campaign.history.find(h => h.year === state.campaign.year && h.shock == null);
  if (last) {
    last.shock = drawnShock;
    last.score = res.score;
    last.avail = res.avail;
    last.total_capex = res.total_capex;
  } else {
    state.campaign.history.push({ year: state.campaign.year, shock: drawnShock, score: res.score, accepted: null, cardId: null, avail: res.avail, total_capex: res.total_capex });
  }
  // Capex one-time costs are amortized across years (paid once over remaining years).
  // For simplicity: treat as paid in the year card fired -> zero out after scoring.
  state.campaign.permMults.capex_one_time = 0;
  // Clear next-year-only bonuses now that they've fired.
  state.campaign.activeBonuses.cable_cut_next = false;
  state.campaign.activeBonuses.eu_damping_half_next = false;
  state.campaign.activeBonuses.sc_damping_half_next = false;
  state.campaign.activeBonuses.gulf_extra_decoupling = 0;
  // Africa swap expiry.
  if (state.campaign.activeBonuses.africa_expire_next) {
    if (state.campaign.activeBonuses.africa_swap && !state.campaign.activeBonuses.africa_swap_locked) {
      state.campaign.activeBonuses.africa_swap = false;
      const m = state.campaign.permMults.tech_capex_mult;
      m.pem_electrolyzer = (m.pem_electrolyzer || 1) / 0.95;
      m.alkaline_electrolyzer = (m.alkaline_electrolyzer || 1) / 0.95;
    }
    state.campaign.activeBonuses.africa_expire_next = false;
  }
  // Move on
  if (state.campaign.year >= 5) {
    narrate("Campaign complete. Total score: " + state.campaign.totalScore + ".", "ok");
    recordScore({ mode: "campaign", name: "Campaign seed " + state.campaign.rngSeed, score: state.campaign.totalScore });
    renderCampaign();
  } else {
    startNextCampaignYear();
  }
}

function renderCampaign() {
  const box = $("campaignBox");
  if (!box) return;
  box.classList.toggle("on", !!state.campaign.active);
  if (!state.campaign.active) return;
  const titleEl = $("campTitle");
  if (titleEl) {
    titleEl.textContent = "Campaign" + (state.challengeOn ? " + " + (CHALLENGES[state.challengeIdx].name) : "");
  }
  $("campClock").textContent = "Year " + state.campaign.year + " / 5 | Total score " + state.campaign.totalScore + " | seed " + state.campaign.rngSeed;
  const cardEl = $("campCard");
  clear(cardEl);
  if (state.campaign.pendingCard) {
    const c = state.campaign.pendingCard;
    cardEl.appendChild(el("div", { cls: "ct-title", text: c.title }));
    cardEl.appendChild(el("div", { cls: "ct-body", text: c.body }));
    $("campAccept").textContent = c.accept.label;
    $("campDecline").textContent = c.decline.label;
    $("campAccept").disabled = false;
    $("campDecline").disabled = false;
    $("campEndYear").disabled = true;
  } else if (state.campaign.year === 0) {
    cardEl.appendChild(el("div", { cls: "ct-body", text: "Press 'End year' to begin year 1." }));
    $("campAccept").disabled = true;
    $("campDecline").disabled = true;
    $("campAccept").textContent = "Accept";
    $("campDecline").textContent = "Decline";
    $("campEndYear").disabled = false;
    $("campEndYear").textContent = "Begin year 1";
  } else if (state.campaign.year >= 5 && state.campaign.cardChoiceMade && state.campaign.history.some(h => h.year === 5 && h.shock != null)) {
    cardEl.appendChild(el("div", { cls: "ct-body", text: "Run complete. Final score: " + state.campaign.totalScore + "." }));
    $("campAccept").disabled = true;
    $("campDecline").disabled = true;
    $("campEndYear").disabled = true;
    $("campEndYear").textContent = "Done";
  } else {
    cardEl.appendChild(el("div", { cls: "ct-body", text: "No card this year. Press 'End year' to roll the shock." }));
    $("campAccept").disabled = true;
    $("campDecline").disabled = true;
    $("campAccept").textContent = "Accept";
    $("campDecline").textContent = "Decline";
    $("campEndYear").disabled = false;
    $("campEndYear").textContent = "End year " + state.campaign.year;
  }
  // History
  const histEl = $("campHistory");
  clear(histEl);
  for (const h of state.campaign.history) {
    if (h.shock == null) continue;
    const row = el("div", { cls: "h-row" });
    row.appendChild(el("span", { cls: "y", text: "Y" + h.year }));
    const desc = (h.cardId ? (CARDS_BY_ID[h.cardId] ? CARDS_BY_ID[h.cardId].title : h.cardId) + " | " : "") + h.shock.replace(/_/g, " ");
    row.appendChild(el("span", { text: desc }));
    row.appendChild(el("span", { cls: "s", text: String(h.score) }));
    histEl.appendChild(row);
  }
  if (state.campaign.year >= 5 && histEl.childElementCount > 0) {
    histEl.appendChild(el("div", { cls: "camp-final", text: "Total: " + state.campaign.totalScore }));
  }
}

// ---------- Init ----------
function init() {
  InfoTip.init();
  mountStaticInfoIcons();
  loadRegion();
  loadAlliances();
  const fromShare = loadShareFromHash();
  renderCatalog();
  renderAlliances();
  renderShocks();
  renderShockOutlook();
  renderPresets();
  renderBuild();
  renderStats(computeDistrict());
  renderLeaderboard();

  if (fromShare) {
    syncControlsToState();
    if (state.challengeOn) renderChallenge(computeDistrict());
    narrate("Loaded a shared build from the link. Tweak it, or press 'Copy share link' to pass on your own.");
  } else {
    narrate("Welcome. This is a learning playground, not the full model. Add a power source like utility solar, then add storage like an LFP battery or a hydrogen tank. Try a surprise event to watch the bill change.");
  }

  $("ztaToggle").addEventListener("change", e => { state.ztaOn = e.target.checked; rerender(true); });
  $("critOnly").addEventListener("change", e => { state.critOnly = e.target.checked; rerender(true); });
  $("challengeMode").addEventListener("change", e => {
    state.challengeOn = e.target.checked;
    $("challengeBox").classList.toggle("on", state.challengeOn);
    if (state.challengeOn) {
      state.challengeIdx = 0;
      state.shocksSurvived.clear();
      narrate("Challenge mode is on. First challenge: " + CHALLENGES[0].name + ". " + CHALLENGES[0].desc);
    } else {
      narrate("Challenge mode is off. You are back in free play.");
    }
    rerender();
  });
  $("chNext").addEventListener("click", nextChallenge);

  const campToggle = $("campaignMode");
  if (campToggle) {
    campToggle.addEventListener("change", e => {
      if (e.target.checked) {
        // Reset queuedCards and per-run state.
        resetCampaign(state.campaign.rngSeed || 42);
        narrate("Campaign mode is on. Build a posture, then press 'Begin year 1'.");
      } else {
        state.campaign.active = false;
        narrate("Campaign mode is off.");
      }
      renderCampaign();
    });
  }
  if ($("campAccept")) $("campAccept").addEventListener("click", () => resolveCard(true));
  if ($("campDecline")) $("campDecline").addEventListener("click", () => resolveCard(false));
  if ($("campEndYear")) $("campEndYear").addEventListener("click", () => {
    if (state.campaign.year === 0) {
      startNextCampaignYear();
    } else {
      endCampaignYear();
    }
  });

  $("regionSelect").addEventListener("change", e => {
    state.region = e.target.value || "";
    saveRegion();
    narrate(state.region ? ("Region set to " + state.region + ".") : "Region cleared.");
  });

  $("exportBtn").addEventListener("click", exportResults);
  $("shareBtn").addEventListener("click", copyShareLink);

  // Onboarding wiring
  for (const t of document.querySelectorAll("#onboardTabs .tab")) {
    t.addEventListener("click", () => setActiveTab(t.dataset.tab));
  }
  $("helpBtn").addEventListener("click", showOnboard);
  $("onboardOK").addEventListener("click", () => {
    try { localStorage.setItem(ONBOARD_KEY, "1"); } catch(e) {}
    hideOnboard();
  });
  $("onboardLater").addEventListener("click", () => {
    hideOnboard();
  });
  $("onboardNever").addEventListener("click", () => {
    try {
      localStorage.setItem(ONBOARD_NEVER, "1");
      localStorage.setItem(ONBOARD_KEY, "1");
    } catch(e) {}
    hideOnboard();
  });
  $("onboardModal").addEventListener("click", (e) => {
    if (e.target === $("onboardModal")) hideOnboard();
  });

  maybeShowOnboardOnLoad();
}

document.addEventListener("DOMContentLoaded", init);

// ---------- Self-test (LOUD on failure) ----------
function _selfTestFail(msg) {
  // In a browser, render a red banner. Always throw.
  if (typeof document !== "undefined" && document.body) {
    const banner = document.createElement("div");
    banner.className = "selftest-banner";
    banner.textContent = "SELF-TEST FAILURE: " + msg;
    document.body.insertBefore(banner, document.body.firstChild);
  }
  throw new Error("Self-test failure: " + msg);
}

(function selfTest() {
  // BASE_PARAMS immutability under applyShock.
  const before = JSON.stringify(BASE_PARAMS);
  applyShock("bau", new Set(), null);
  const after = JSON.stringify(BASE_PARAMS);
  if (before !== after) _selfTestFail("BASE_PARAMS mutated by applyShock");

  // LCOE sanity.
  const test = lcoe({ capex_total: 1.1e6, opex_yr: 18000, fuel_yr: 0, energy_mwh_yr: 1928, lifetime_years: 25, discount_rate: 0.07 });
  if (!(test > 30 && test < 90)) _selfTestFail("LCOE sanity off: " + test);

  // Composition invariant: capex equals BASE * prod(bloc_capex_mults) * shock_dampened * (1 - ptc).
  // Hand-picked postures:
  const postures = [
    { active: new Set(), shock: "bau" },
    { active: new Set(["LATAM_FRIEND"]), shock: "li_shortage" },
    { active: new Set(["WEST_FRIEND", "EAST_FRIEND"]), shock: "china_decoupling" },
  ];
  for (const p of postures) {
    const params = applyShock(p.shock, p.active, null);
    // compute predicted multiplier on solar capex_per_kw under the same posture/shock.
    let predicted = BASE_PARAMS.solar_pv_utility.capex_per_kw;
    for (const bloc of p.active) {
      const m = (BLOCS[bloc].bonus && BLOCS[bloc].bonus.tech_capex_mult && BLOCS[bloc].bonus.tech_capex_mult.solar_pv_utility);
      if (typeof m === "number") predicted *= m;
    }
    const surviving = combinedDamping(p.shock, p.active, null);
    const mods = SHOCKS[p.shock] || [];
    for (const [path, mult] of mods) {
      const [tech, field] = path.split(".");
      if (tech === "solar_pv_utility" && field === "capex_per_kw") {
        const dampened = mult > 1 ? 1 + (mult - 1) * surviving : mult;
        predicted *= dampened;
      }
    }
    const got = params.solar_pv_utility.capex_per_kw;
    if (Math.abs(got - predicted) > 1e-6) {
      _selfTestFail("Composition invariant for solar capex (" + p.shock + "): got " + got + " expected " + predicted);
    }
  }

  // Shock distribution sums to 1, all values in [0, 0.5].
  for (const posture of [new Set(), new Set(["EAST_FRIEND"]), new Set(["WEST_FRIEND", "EAST_FRIEND", "LATAM_FRIEND"])]) {
    const dist = shockDistribution(posture);
    let sum = 0;
    for (const v of Object.values(dist)) {
      sum += v;
      if (v < 0 || v > 0.5 + 1e-6) _selfTestFail("shockDistribution out-of-range value " + v);
      if (!isFinite(v)) _selfTestFail("shockDistribution NaN/Infinity");
    }
    if (Math.abs(sum - 1) > 1e-3) _selfTestFail("shockDistribution sum != 1: " + sum);
  }

  // combinedDamping in [0, 1] for any posture x shock.
  for (const posture of [new Set(), new Set(["EAST_FRIEND"]), new Set(["WEST_FRIEND", "EAST_FRIEND", "LATAM_FRIEND", "EU_FRIEND"])]) {
    for (const sh of Object.keys(SHOCK_BASE_PROB)) {
      const d = combinedDamping(sh, posture, null);
      if (d < 0 || d > 1 + 1e-9 || !isFinite(d)) _selfTestFail("combinedDamping out of [0,1]: " + d + " posture=" + [...posture] + " shock=" + sh);
    }
  }

  // Mulberry32 sanity: deterministic.
  const r1 = new Mulberry32(42);
  const r2 = new Mulberry32(42);
  for (let i = 0; i < 10; i++) {
    if (r1.nextU32() !== r2.nextU32()) _selfTestFail("Mulberry32 not deterministic");
  }

  // Pairwise clamp.
  const adj = pairwiseAdjustment(new Set(["WEST_FRIEND", "EAST_FRIEND"]));
  if (adj < 0.3 || adj > 1.5) _selfTestFail("pairwiseAdjustment out of clamp: " + adj);
})();
