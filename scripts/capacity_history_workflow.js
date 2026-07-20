export const meta = {
  name: 'capacity-history',
  description: 'Reconstruct each plant\'s REAL dated, sourced capacity commissioning history (no modelling)',
  phases: [{ title: 'History', detail: 'one agent per plant, sourced datapoints only' }],
}

// args = array of { id, plant_name, operator, country, current_nameplate_gwh, current_ref_year, current_start_year }
let _args = args
if (typeof _args === 'string') { try { _args = JSON.parse(_args) } catch (e) { _args = [] } }
const items = Array.isArray(_args) ? _args : []

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['id', 'timeline', 'is_single_physical_site', 'coverage'],
  properties: {
    id: { type: 'string' },
    // REAL, dated, sourced observations only. Empty array if none can be sourced.
    timeline: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['year', 'cumulative_gwh', 'basis', 'source_url', 'source_date'],
        properties: {
          year:           { type: 'integer' },              // calendar year the observation refers to
          cumulative_gwh: { type: ['number', 'null'] },     // total annual GWh/yr nameplate online AS OF that year
          added_gwh:      { type: ['number', 'null'] },      // GWh/yr added that year, if the source states it
          basis:          { type: 'string', enum: ['operational', 'commissioned', 'announced_target', 'planned'] },
          event:          { type: ['string', 'null'] },      // e.g. "phase 1 line online"
          source_url:     { type: 'string' },
          source_date:    { type: 'string' },
        },
      },
    },
    is_single_physical_site: { type: 'boolean' },  // false if the figure is a multi-site hub/company aggregate
    hub_note:               { type: ['string', 'null'] },
    coverage: { type: 'string', enum: ['full', 'partial', 'single_point', 'none'] },
    notes:    { type: ['string', 'null'] },
  },
}

function prompt(c) {
  return `Reconstruct the REAL, DATED, SOURCED capacity build-out history of ONE battery cell plant. Web + read tools only.

PLANT (id must be returned EXACTLY): ${c.id}
  plant_name: ${c.plant_name}
  operator:   ${c.operator}
  country:    ${c.country}
  (for context only — our current single-point record says ~${c.current_nameplate_gwh} GWh/yr, ref year ${c.current_ref_year}, start ${c.current_start_year}. Do NOT just echo this; verify from sources.)

GOAL: a timeline of how this ONE physical site's annual manufacturing capacity (GWh/year) grew over time, as a list of dated observations EACH backed by a specific source.

PRIORITY FOR THIS PASS: find the MOST RECENT (2024 or 2025) dated, sourced OPERATIONAL cumulative-GWh figure for this site, and attach the GWh number to the operational/commissioned datapoint itself — do NOT leave the operational point's numbers null with the figure sitting only on an announced/planned point. If the site genuinely only commissioned in 2025 (or is not yet operational), say so and give the real dated operational point; do not invent a 2024 figure.

ABSOLUTE RULES — this must be real data, not modelling:
1. Only record a datapoint if a SPECIFIC, DATED source states the plant's capacity or a phase/line commissioning at that time. Every datapoint needs source_url + source_date (YYYY-MM-DD).
2. NEVER interpolate, ramp, extrapolate, or invent intermediate years. If a source says "15 GWh phase 1 online June 2021" and "reached 55 GWh in 2023", record exactly those two points — do NOT fabricate a 2022 value.
3. cumulative_gwh = total annual GWh/yr nameplate ONLINE at that site as of that year (per the source). added_gwh = the increment that year, ONLY if the source states it (else null).
4. 'basis': use 'operational'/'commissioned' for capacity actually in production; 'announced_target'/'planned' for future/announced figures. Keep future targets clearly separated — do not present a 2027 target as if online in 2024.
5. This is ONE physical site. If the capacity figures you find are a company-wide or multi-base HUB aggregate (e.g. "CATL's Ningde-city bases total 330 GWh"), set is_single_physical_site=false and explain in hub_note; still record what you can but flag it.
6. If sources conflict, prefer company/official and dated provincial/government approvals over trackers; note the conflict and lower to the more conservative value.
7. If you genuinely cannot find dated capacity history, return timeline=[] and coverage="none". A null/empty answer is correct when the data is not published — do NOT fill the gap with guesses.

GOOD SOURCES: company IR / press releases, provincial & municipal government project approvals and groundbreaking/commissioning notices (especially in China — these are dated and specific), Benchmark Mineral Intelligence, BloombergNEF, Reuters/Bloomberg, electrive, CnEVPost, local trade press, Wikipedia gigafactory lists (follow through to primary sources).

coverage: 'full' = several dated points capturing the ramp; 'partial' = a couple of points; 'single_point' = only one dated capacity figure; 'none' = nothing datable.

Return the object now, id EXACTLY as given. Your entire reply is the JSON object.`
}

phase('History')

const results = await pipeline(
  items,
  (c) => agent(prompt(c), {
    label: `hist:${(c.plant_name || '?').slice(0, 34)}`,
    phase: 'History',
    schema: SCHEMA,
    agentType: 'general-purpose',
  })
)

const ok = results.filter(Boolean)
const withData = ok.filter(r => Array.isArray(r.timeline) && r.timeline.length > 0)
const multi = ok.filter(r => Array.isArray(r.timeline) && r.timeline.length >= 2)
log(`Capacity history: ${withData.length}/${items.length} plants got >=1 sourced datapoint; ${multi.length} got >=2`)
return { total: items.length, with_data: withData.length, multi_point: multi.length, results: ok }
