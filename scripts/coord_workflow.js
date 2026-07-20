export const meta = {
  name: 'coord-research',
  description: 'Find real, sourced coordinates for battery cell sites still missing them',
  phases: [{ title: 'Coords', detail: 'one agent per site, sourced lat/long only' }],
}

// args = array of { id, plant_name, operator, country }
let _args = args
if (typeof _args === 'string') { try { _args = JSON.parse(_args) } catch (e) { _args = [] } }
const items = Array.isArray(_args) ? _args : []

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['id', 'found', 'latitude', 'longitude', 'precision'],
  properties: {
    id:        { type: 'string' },
    found:     { type: 'boolean' },                 // false if no real located site exists (speculative / cancelled with no site)
    latitude:  { type: ['number', 'null'] },        // decimal degrees, WGS-84
    longitude: { type: ['number', 'null'] },
    precision: { type: 'string', enum: ['site', 'town', 'none'] },  // 'site'=exact plant, 'town'=named town centroid
    source_url:  { type: ['string', 'null'] },
    source_date: { type: ['string', 'null'] },
    note:        { type: ['string', 'null'] },
  },
}

function prompt(c) {
  return `Find the geographic COORDINATES (latitude, longitude, WGS-84 decimal degrees) of ONE battery cell manufacturing site. Web + read tools only.

SITE (return id EXACTLY): ${c.id}
  plant_name: ${c.plant_name}
  operator:   ${c.operator}
  country:    ${c.country}

GOAL: the real location of THIS physical site.
PRIORITY ORDER:
1. EXACT plant coordinates from a real source — Wikipedia (GeoHack coords), company/press releases,
   government project approvals, industrial-park pages, or a maps listing for the specific plant.
   Return precision="site" with the source_url + source_date.
2. If you cannot confirm the exact plant point but CAN confirm the specific TOWN/locality it is in
   (the plant_name and known facts usually name it — e.g. a specific town, district or industrial
   park), return that town's centroid with precision="town" and a source for the town↔plant link.
3. If the site is speculative, only "under consideration", or a CANCELLED project with NO identified
   location, return found=false, precision="none", null coordinates. This is the correct answer when
   there is no real located site — do NOT invent a point.

ABSOLUTE RULES:
- NEVER invent or guess coordinates. Every non-null coordinate needs a source_url + source_date (YYYY-MM-DD).
- Coordinates must be plausible for the stated country (sanity-check the hemisphere/range).
- Prefer official/primary sources; Wikipedia GeoHack is acceptable for a site's published coordinates.
- Some pages may return HTTP 403 in this environment; if a fetch fails, use search-result snippets and
  well-established public knowledge of the named town, and say so in note.

Return the object now, id EXACTLY as given. Your entire reply is the JSON object.`
}

phase('Coords')

const results = await pipeline(
  items,
  (c) => agent(prompt(c), {
    label: `coord:${(c.plant_name || '?').slice(0, 30)}`,
    phase: 'Coords',
    schema: SCHEMA,
    agentType: 'general-purpose',
  })
)

const ok = results.filter(Boolean)
const found = ok.filter(r => r.found && r.latitude != null && r.longitude != null)
log(`Coordinates: ${found.length}/${items.length} sites located (${ok.length - found.length} no-site/unfound)`)
return { total: items.length, found: found.length, results: ok }
