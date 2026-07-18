export const meta = {
  name: 'factory-research',
  description: 'Research a batch of battery cell plants in parallel and return structured JSON per plant',
  phases: [{ title: 'Research', detail: 'one factory-researcher agent per plant' }],
}

// args = array of { plant_name, operator, country, region }
const candidates = Array.isArray(args) ? args : []

// JSON schema matching the factories table (nullable everywhere except the
// three identity fields + required source). The agent is FORCED to return this.
const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['plant_name', 'operator', 'country', 'region',
             'status', 'source_url', 'source_date', 'confidence'],
  properties: {
    plant_name:             { type: 'string' },
    operator:               { type: ['string', 'null'] },
    parent_company:         { type: ['string', 'null'] },
    country:                { type: 'string' },
    region:                 { type: 'string', enum: ['China','USA','Europe','South Korea','Japan','India','Southeast Asia','Rest of World'] },
    latitude:               { type: ['number', 'null'] },
    longitude:              { type: ['number', 'null'] },
    status:                 { type: ['string', 'null'], enum: ['announced','under_construction','operational', null] },
    announced_year:         { type: ['integer', 'null'] },
    start_year:             { type: ['integer', 'null'] },
    nameplate_capacity_gwh: { type: ['number', 'null'] },
    capacity_ref_year:      { type: ['integer', 'null'] },
    capacity_by_year_json:  { type: ['string', 'null'] },
    chemistry:              { type: ['string', 'null'] },
    cell_format:            { type: ['string', 'null'] },
    end_market:             { type: ['string', 'null'] },
    jv_partners:            { type: ['string', 'null'] },
    source_url:             { type: 'string' },
    source_date:            { type: 'string' },
    confidence:             { type: 'number' },
    is_cell_manufacturer:   { type: 'boolean' },
    research_notes:         { type: ['string', 'null'] },
  },
}

function prompt(c) {
  return `You research a SINGLE battery cell manufacturing plant and return ONE structured object. Web + read tools only.

PLANT TO RESEARCH:
  plant_name: ${c.plant_name}
  operator:   ${c.operator}
  country:    ${c.country}
That is the ONLY context you get.

Use WebSearch/WebFetch (company IR pages, Benchmark Mineral Intelligence, BloombergNEF, Reuters/Bloomberg, government releases, Wikipedia, local trade press). Prefer primary/company sources and recent reputable trackers. Cross-check capacity and status.

NON-NEGOTIABLE RULES:
1. status is EXACTLY one of announced | under_construction | operational (or null if truly unknown). Never blend statuses; pick the current one.
2. nameplate_capacity_gwh is the ANNUAL GWh/year figure at full nameplate. Put the year that figure refers to in capacity_ref_year. Never mix cumulative and annual numbers.
3. This is ONE physical site. If it is a JV, set jv_partners and pick a single operator. Do not split it.
4. If capacity ramps in phases, record the ramp in capacity_by_year_json as a JSON string like "{\\"2025\\":10,\\"2026\\":20,\\"2027\\":40}" in GWh/yr. nameplate_capacity_gwh is the full/eventual nameplate.
5. EVERY non-null substantive value (capacity, coordinates, status, dates) must be backed by a source. If you cannot confirm a value, set it null and lower confidence. NEVER invent a number, coordinate, date, or URL. A null is better than a guess.

is_cell_manufacturer: set true if this site actually manufactures battery CELLS (any chemistry: Li-ion, LFP, sodium-ion, solid-state, flow, zinc, iron-air). Set false if it is only pack/module assembly, only cathode/anode/electrolyte/separator/precursor material, or only recycling. If false, still fill what you can and set low confidence.

chemistry: record the true chemistry honestly (e.g. LFP, NMC, NCA, sodium-ion, solid-state, lithium-sulfur, zinc, vanadium flow, iron-air). For lab/pilot lines that are not commercial scale, note that in research_notes and keep nameplate null unless a real figure is sourced.

region: use exactly one of China | USA | Europe | South Korea | Japan | India | Southeast Asia | Rest of World. The candidate's region is "${c.region}" — keep it unless clearly wrong.

source_url + source_date (YYYY-MM-DD) are REQUIRED. If you truly cannot find any source, return the best you have with low confidence; numbers you cannot source must be null.

confidence: 0.9-1.0 confirmed by company/official or multiple reputable sources; 0.6-0.8 single reputable tracker/news; 0.3-0.5 inferred/dated/conflicting; <0.3 speculative.

Return the structured object now.`
}

phase('Research')

const results = await pipeline(
  candidates,
  (c, orig, i) => agent(prompt(c), {
    label: `research:${(c.operator || '?').slice(0, 20)}/${(c.plant_name || '?').slice(0, 24)}`,
    phase: 'Research',
    schema: SCHEMA,
    agentType: 'general-purpose',
  }).then(r => {
    // carry the candidate identity so the loader can reconcile
    if (r && typeof r === 'object') {
      r._candidate = { plant_name: c.plant_name, operator: c.operator, country: c.country, region: c.region }
    }
    return r
  })
)

const ok = results.filter(Boolean)
log(`Researched ${ok.length}/${candidates.length} plants`)
return { count: ok.length, total: candidates.length, results: ok }
