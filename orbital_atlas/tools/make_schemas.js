// Writes configs/schema/*.json from the engine's own word lists and defaults, so editors can autocomplete configs.
// Run from the orbital_atlas folder:   node tools/make_schemas.js
// A test rebuilds these in memory and fails if the files on disk have drifted from the engine.

import { writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { WORDS, VIEW_SCHEMA, THEME_SCHEMA, ZOOM_MS_CAP } from '../src/engine/config.js';
import { DEFAULT_VIEW, DEFAULT_THEME } from '../src/engine/defaults.js';

const hex = { type: 'string', pattern: '^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$' };
const hexList = { type: 'array', items: hex, minItems: 1 };
const orNull = s => ({ anyOf: [s, { type: 'null' }] });
const word = (list, description, dflt) => ({ enum: list, description, ...(dflt === undefined ? {} : { default: dflt }) });

export function viewSchema() {
  const d = DEFAULT_VIEW;
  return {
    $schema: 'http://json-schema.org/draft-07/schema#',
    $id: 'orbital.view.1.json',
    title: 'Orbital Atlas view',
    description: 'What the map means. Change a field here and the reader learns a different fact.',
    type: 'object',
    required: ['schema'],
    properties: {
      schema: { const: VIEW_SCHEMA },
      id: { type: 'string' },
      title: { type: 'string' },
      note: orNull({ type: 'string', description: 'One line of context for the margin.' }),
      topology: orNull({ type: 'string', description: 'A registered topology id.' }),
      layer: orNull({ type: 'string', description: 'Which table. null is the empty state.' }),
      layer_b: orNull({ type: 'string', description: 'Second table, for two-layer views. Not built yet.' }),
      period: { type: 'string', default: d.period, description: 'A period string, or "latest".' },
      measure: word(WORDS.measure, 'What number drives the colour.', d.measure),
      measure_locked: { type: 'boolean', default: d.measure_locked, description: 'If true, slicers cannot switch the measure. The readout still shows everything.' },
      scale: {
        type: 'object',
        properties: {
          type: word(WORDS.scale_type, 'How numbers become positions on the palette.', d.scale.type),
          bins: { type: 'integer', minimum: 0, default: d.scale.bins, description: '0 for smooth, or a class count of 2 or more.' },
          ties: word(WORDS.ties, 'share: equal values get equal colour. spread is what v1 did by accident.', d.scale.ties),
          domain: orNull({ type: 'array', items: { type: 'number' }, minItems: 2, maxItems: 2 }),
          midpoint: orNull({ type: 'number', description: 'Centre of a diverging scale.' }),
          thresholds: orNull({ type: 'array', items: { type: 'number' }, minItems: 1 }),
          zero_class: { type: 'boolean', default: d.scale.zero_class, description: 'Zero gets its own class first, then the rest are scaled.' },
          invert: { type: 'boolean', default: d.scale.invert }
        }
      },
      highlight: { type: 'object', properties: { rule: word(WORDS.highlight_rule, 'Which places are called out. The view picks who. The theme picks how.', d.highlight.rule), value: orNull({ type: 'number' }) } },
      confidence: { type: 'object', properties: { field: word(WORDS.confidence_field, 'What makes a place shaky: a small sample, or a small base.', d.confidence.field), low_below: orNull({ type: 'number' }) } },
      filter: { type: 'object', properties: { tier_in: orNull({ type: 'array', items: { type: 'string' }, minItems: 1 }) } },
      frame: { type: 'object', properties: { type: word(WORDS.frame_type, 'What the camera fits to.', d.frame.type), id: orNull({ type: 'string' }) } },
      on_click: word(WORDS.on_click, 'Default click behaviour. The event always fires as well.', d.on_click),
      readout: { type: 'object', properties: { always: { type: 'array', items: { enum: WORDS.readout_key } }, on_demand: { type: 'array', items: { enum: WORDS.readout_key } } } },
      labels: { type: 'object', properties: { top: { type: 'integer', minimum: 0 } } },
      empty_message: orNull({ type: 'string' })
    }
  };
}

export function themeSchema() {
  const d = DEFAULT_THEME;
  const role = name => ({
    type: 'object',
    properties: { style: word(WORDS.role_style[name], `How the ${name} role is painted.`, d.roles[name].style), color: hex, width: { type: 'number', minimum: 0 }, amount: { type: 'number', minimum: 0, maximum: 1 },
      spacing: { type: 'number', minimum: 0.5 }, angle: { enum: [45, -45] }, offset: { type: 'array', items: { type: 'number' }, minItems: 2, maxItems: 2 } }
  });
  const line = { type: 'object', properties: { color: hex, opacity: { type: 'number', minimum: 0, maximum: 1 }, width: { type: 'number', minimum: 0 } } };
  return {
    $schema: 'http://json-schema.org/draft-07/schema#',
    $id: 'orbital.theme.1.json',
    title: 'Orbital Atlas theme',
    description: 'How the map looks. Change a field here and the reader learns nothing new.',
    type: 'object',
    required: ['schema', 'id'],
    properties: {
      schema: { const: THEME_SCHEMA },
      id: { type: 'string' },
      label: { type: 'string' },
      base: orNull({ type: 'string', description: 'The id of a theme to build on. Only the fields that differ need writing.' }),
      ground: { type: 'object', properties: { background: hex, land_empty: hex, texture: word(WORDS.texture, 'Static surface. Never animated.', d.ground.texture),
        shadow: orNull({ type: 'object', description: 'A soft shadow under the whole land shape.', properties: { color: hex, blur: { type: 'number', minimum: 0 }, dx: { type: 'number' }, dy: { type: 'number' } }, required: ['color'] }) } },
      palettes: {
        type: 'object',
        description: 'One per scale family. A complete theme supplies all four.',
        properties: {
          sequential: hexList,
          diverging: { type: 'object', properties: { low: hexList, mid: hex, high: hexList }, required: ['low', 'mid', 'high'] },
          binary: { type: 'object', properties: { zero: hex, nonzero: hexList }, required: ['zero', 'nonzero'] },
          categorical: hexList
        }
      },
      encoding: word(WORDS.encoding, `How a value becomes ink. Built: ${WORDS.built_encoding.join(', ')}. The engine refuses size encodings on rates.`, d.encoding),
      ink: {
        type: 'object',
        description: 'How the stipple and hatch encodings lay ink down. Sizes are screen pixels.',
        properties: {
          under: word(WORDS.ink_under, 'What sits beneath the ink: empty land, or the ramp colour.', d.ink.under),
          color: orNull(hex),
          budget: { type: 'integer', minimum: 1, maximum: 250000, default: d.ink.budget, description: 'Stipple: total dots across the map.' },
          gamma: { type: 'number', minimum: 0.1, default: d.ink.gamma, description: 'Stipple: how hard dot density leans toward the top of the scale.' },
          radius: { type: 'number', minimum: 0.1, default: d.ink.radius },
          bloom: { type: 'number', minimum: 0, default: d.ink.bloom, description: 'Stipple: a soft static halo under the dots, in pixels. 0 is off.' },
          bloom_strength: { type: 'number', minimum: 0, maximum: 1, default: d.ink.bloom_strength },
          blend: word(WORDS.ink_blend, 'How the ink mixes with what is under it.', d.ink.blend),
          spacing: { type: 'array', items: { type: 'number', minimum: 0.5 }, minItems: 2, maxItems: 2, description: 'Hatch: line gap at the bottom and at the top of the scale.' },
          width: { type: 'number', minimum: 0.1, default: d.ink.width },
          angle: { enum: [45, -45], default: d.ink.angle },
          classes: { type: 'integer', minimum: 2, maximum: 12, default: d.ink.classes, description: 'Hatch: how many bands of line spacing.' },
          cell: { type: 'number', minimum: 1, maximum: 20, default: d.ink.cell, description: 'Field encodings: grid size in map units. Smaller is finer and slower.' },
          smooth: { type: 'integer', minimum: 1, maximum: 12, default: d.ink.smooth, description: 'Field encodings: how far neighbours are blended, in cells.' },
          levels: { type: 'integer', minimum: 2, maximum: 40, default: d.ink.levels, description: 'Contour: how many lines between the bottom and top of the scale.' },
          index_every: { type: 'integer', minimum: 1, default: d.ink.index_every, description: 'Contour: every nth line is drawn heavier.' },
          rows: { type: 'integer', minimum: 8, maximum: 200, default: d.ink.rows, description: 'Ridge: how many slices from top to bottom.' },
          amp: { type: 'number', minimum: 0, default: d.ink.amp, description: 'Ridge: how far the top of the scale lifts a line, in pixels.' },
          count: { type: 'integer', minimum: 1, maximum: 20000, default: d.ink.count, description: 'Current: how many flow strokes.' },
          steps: { type: 'integer', minimum: 4, maximum: 400, default: d.ink.steps, description: 'Current: how long each stroke runs.' },
          opacity: { type: 'number', minimum: 0, maximum: 1, default: d.ink.opacity },
          fill: orNull(hex)
        }
      },
      layout: { type: 'object', description: 'Screen space the map keeps clear for type.', properties: {
        inset: { type: 'object', properties: { top: { type: 'number' }, right: { type: 'number' }, bottom: { type: 'number' }, left: { type: 'number' } } },
        callout_gutter: { type: 'number', minimum: 0, default: d.layout.callout_gutter } } },
      roles: { type: 'object', properties: Object.fromEntries(WORDS.role.map(r => [r, role(r)])) },
      light: { type: 'object', properties: { type: word(WORDS.light_type, 'hillshade may only use the value as its height.', d.light.type), strength: { type: 'number', minimum: 0, maximum: 1 }, source: orNull({ const: 'value' }) } },
      glow: { type: 'object', properties: { on: word(WORDS.glow_on, 'Glow can only ever attach to highlighted places.', d.glow.on), blur: { type: 'number', minimum: 0 } } },
      lines: { type: 'object', properties: { places: line, parents: line, outline: line } },
      type: { type: 'object', properties: { display: { type: 'string', description: 'Headlines and place names, on the page and on the map.' }, text: { type: 'string', description: 'Sentences.' }, display_weight: { type: 'integer', minimum: 100, maximum: 900, default: d.type.display_weight }, data: { type: 'string', description: 'Numbers, labels, captions.' }, numerals: { enum: ['tabular', 'proportional'] } } },
      motion: { type: 'object', properties: { zoom_ms: { type: 'integer', minimum: 0, maximum: ZOOM_MS_CAP, default: d.motion.zoom_ms, description: 'The only motion setting. 0 is a hard cut.' } }, additionalProperties: false }
    }
  };
}

export const render = schema => JSON.stringify(schema, null, 2) + '\n';

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const dir = join(dirname(fileURLToPath(import.meta.url)), '..', 'configs', 'schema');
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'orbital.view.1.json'), render(viewSchema()));
  writeFileSync(join(dir, 'orbital.theme.1.json'), render(themeSchema()));
  console.log('wrote 2 schema files to', dir);
}
