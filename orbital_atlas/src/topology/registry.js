// Topology registry: where shape sets are declared, loaded, and decoded.
// Nothing here knows what a county or a state is. It reads that from the registry entry.
// Nothing here touches a canvas. Geometry comes out as plain arrays.

import { feature, mesh, neighbors } from '../vendor/topojson-client.js';

/**
 * @typedef {Object} Place
 * @property {number} idx            position in the places array
 * @property {string} id             cleaned geo_id
 * @property {string} name
 * @property {string|null} parentId
 * @property {number[][][][]} polygons   polygons -> rings -> [x, y]
 * @property {[number, number, number, number]} bbox   x0, y0, x1, y1
 * @property {number[]} neighbors    idx of touching places
 */

/**
 * @typedef {Object} Topology
 * @property {string} id
 * @property {Object} entry          the registry entry, untouched
 * @property {Place[]} places
 * @property {Map<string, number>} indexById
 * @property {Place[]} parents       same shape as places; empty if none declared
 * @property {Map<string, number>} parentIndexById
 * @property {{places: number[][][], parents: number[][][], outline: number[][][]}} meshes   lists of lines
 * @property {number[][][][]} outlinePolygons
 * @property {[number, number, number, number]} bbox   measured, never assumed
 */

/** Apply a registry id_rule to a raw id. */
export function cleanId(raw, rule) {
  let s = String(raw ?? '').trim().replace(/^"|"$/g, '');
  if (rule && rule.pad_left && s.length < rule.pad_left) s = s.padStart(rule.pad_left, rule.char || '0');
  return s;
}

/** Find a place's parent id using the registry's parent rule. */
export function parentIdOf(id, props, rule) {
  if (!rule) return null;
  if (rule.by === 'prefix') return id.slice(0, rule.length);
  if (rule.by === 'property') return props && props[rule.field] != null ? String(props[rule.field]) : null;
  return null;
}

function polygonsOf(geometry) {
  if (!geometry) return [];
  if (geometry.type === 'Polygon') return [geometry.coordinates];
  if (geometry.type === 'MultiPolygon') return geometry.coordinates;
  return [];
}

function linesOf(geometry) {
  if (!geometry) return [];
  if (geometry.type === 'LineString') return [geometry.coordinates];
  if (geometry.type === 'MultiLineString') return geometry.coordinates;
  return [];
}

function bboxOf(polygons) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const poly of polygons) {
    const outer = poly[0];
    if (!outer) continue;
    for (const [x, y] of outer) {
      if (x < x0) x0 = x; if (x > x1) x1 = x;
      if (y < y0) y0 = y; if (y > y1) y1 = y;
    }
  }
  return [x0, y0, x1, y1];
}

function toPlaces(topo, objectName, entry, withParent) {
  const obj = topo.objects[objectName];
  if (!obj) throw new Error(`Topology object "${objectName}" is not in the file.`);
  const feats = feature(topo, obj).features;
  const nb = neighbors(obj.geometries);
  const idRule = withParent ? entry.id_rule : null;
  return feats.map((f, idx) => {
    const id = cleanId(f.id, idRule);
    const props = f.properties || {};
    const polygons = polygonsOf(f.geometry);
    return {
      idx, id,
      name: props[entry.name_field || 'name'] != null ? String(props[entry.name_field || 'name']) : id,
      parentId: withParent ? parentIdOf(id, props, entry.parent) : null,
      polygons,
      bbox: bboxOf(polygons),
      neighbors: nb[idx] || []
    };
  });
}

/**
 * Decode a raw TopoJSON file using its registry entry.
 * Pure: no fetch, no DOM. Runs the same in a browser and in a test.
 * @returns {Topology}
 */
export function decodeTopology(id, entry, topo) {
  if (entry.projected === false) {
    throw new Error(`Topology "${id}" is not pre-projected. Runtime projection is not built yet.`);
  }
  const places = toPlaces(topo, entry.object, entry, true);
  const parents = entry.parent_object ? toPlaces(topo, entry.parent_object, entry, false) : [];

  const indexById = new Map();
  const clashes = [];
  for (const p of places) {
    if (indexById.has(p.id)) clashes.push(p.id);
    indexById.set(p.id, p.idx);
  }
  if (clashes.length) throw new Error(`Topology "${id}" has repeated ids: ${clashes.slice(0, 5).join(', ')}`);
  const parentIndexById = new Map(parents.map(p => [p.id, p.idx]));

  const placeObj = topo.objects[entry.object];
  const meshes = {
    places: linesOf(mesh(topo, placeObj, (a, b) => a !== b)),
    parents: entry.parent_object ? linesOf(mesh(topo, topo.objects[entry.parent_object], (a, b) => a !== b)) : [],
    outline: linesOf(mesh(topo, placeObj, (a, b) => a === b))
  };
  const outlinePolygons = entry.outline_object && topo.objects[entry.outline_object]
    ? feature(topo, topo.objects[entry.outline_object]).features.flatMap(f => polygonsOf(f.geometry))
    : [];

  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const p of places) {
    if (p.bbox[0] < x0) x0 = p.bbox[0]; if (p.bbox[1] < y0) y0 = p.bbox[1];
    if (p.bbox[2] > x1) x1 = p.bbox[2]; if (p.bbox[3] > y1) y1 = p.bbox[3];
  }

  return { id, entry, places, indexById, parents, parentIndexById, meshes, outlinePolygons, bbox: [x0, y0, x1, y1] };
}

/** Fetch the registry file. */
export async function loadRegistry(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Could not load the topology registry at ${url} (${res.status}).`);
  const registry = await res.json();
  registry.baseUrl = new URL('.', new URL(url, globalThis.location ? globalThis.location.href : undefined)).href;
  return registry;
}

/** Fetch and decode one topology named in the registry. */
export async function loadTopology(registry, id) {
  const key = id || registry.default;
  const entry = registry.topologies[key];
  if (!entry) throw new Error(`Topology "${key}" is not in the registry. Known: ${Object.keys(registry.topologies).join(', ')}`);
  const res = await fetch(new URL(entry.url, registry.baseUrl));
  if (!res.ok) throw new Error(`Could not load topology file ${entry.url} (${res.status}).`);
  return decodeTopology(key, entry, await res.json());
}
