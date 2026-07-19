export const meta = {
  name: 'capacity-recap',
  description: 'Targeted re-research of the annual GWh nameplate for plants missing capacity',
  phases: [{ title: 'Capacity', detail: 'one agent per plant, capacity only' }],
}

// args = array of { id, plant_name, operator, country, region }
let _args = args
if (typeof _args === 'string') { try { _args = JSON.parse(_args) } catch (e) { _args = [] } }
const items = Array.isArray(_args) ? _args : []

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['id', 'capacity_found'],
  properties: {
    id:                     { type: 'string' },
    capacity_found:         { type: 'boolean' },
    nameplate_capacity_gwh: { type: ['number', 'null'] },
    capacity_ref_year:      { type: ['integer', 'null'] },
    capacity_by_year_json:  { type: ['string', 'null'] },
    source_url:             { type: ['string', 'null'] },
    source_date:            { type: ['string', 'null'] },
    note:                   { type: ['string', 'null'] },
  },
}

function prompt(c) {
  return `Find ONLY the annual nameplate capacity (GWh per year) of this specific battery cell plant. Web + read tools.

PLANT:
  plant_name: ${c.plant_name}
  operator:   ${c.operator}
  country:    ${c.country}

Return the plant's ANNUAL nameplate capacity in GWh/year (full/eventual nameplate), the year that figure refers to (capacity_ref_year), and — if it ramps in phases — a capacity_by_year_json string like "{\\"2025\\":10,\\"2026\\":20}" in GWh/yr.

RULES:
- This must be a SINGLE physical site's capacity, NOT a company-wide or hub aggregate. If the only figure you can find is company-wide or spans multiple sites, set capacity_found=false and explain in note.
- GWh/YEAR only. Do not convert cell counts to GWh by guessing. Do not invent a number.
- Many of these are small pilot / lab / next-gen (solid-state, sodium, flow, HEV) lines with NO published GWh figure. If you cannot find a sourced site-level annual GWh nameplate, set capacity_found=false, nameplate_capacity_gwh=null, and say why in note. A null is the correct answer when unpublished.
- If you DO find it, set capacity_found=true and give source_url + source_date (YYYY-MM-DD).

Return the object now. Keep id EXACTLY as: ${c.id}`
}

phase('Capacity')

const results = await pipeline(
  items,
  (c) => agent(prompt(c), {
    label: `cap:${(c.plant_name || '?').slice(0, 34)}`,
    phase: 'Capacity',
    schema: SCHEMA,
    agentType: 'general-purpose',
  })
)

const ok = results.filter(Boolean)
const found = ok.filter(r => r.capacity_found && r.nameplate_capacity_gwh != null)
log(`Capacity recap: ${found.length}/${items.length} plants got a sourced nameplate`)
return { total: items.length, found: found.length, results: ok }
