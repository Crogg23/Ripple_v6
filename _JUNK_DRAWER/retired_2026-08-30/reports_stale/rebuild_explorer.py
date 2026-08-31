"""
rebuild_explorer.py — Generates the_library_explorer.html from live Snowflake metadata.

Run after any pour/data change to keep the explorer current:
    python reports/rebuild_explorer.py

Requires: snowflake-connector-python (pip install snowflake-connector-python)
Uses the default Snowflake connection from ~/.snowflake/connections.toml
"""

import json
import os
import sys
from pathlib import Path

try:
    import snowflake.connector
except ImportError:
    print("ERROR: pip install snowflake-connector-python")
    sys.exit(1)


def get_connection():
    """Connect using the Snowflake connection from connections.toml."""
    # Try known connection names in order of preference
    for name in ["ONEAFDA-UMB20733", "default"]:
        try:
            return snowflake.connector.connect(connection_name=name)
        except Exception:
            continue
    # Fallback: externalbrowser with env vars
    return snowflake.connector.connect(
        authenticator="externalbrowser",
        account=os.environ.get("SNOWFLAKE_ACCOUNT", ""),
        user=os.environ.get("SNOWFLAKE_USER", ""),
    )


def fetch_nodes(cur):
    """Fetch table metadata from FRIENDLY_LAYER."""
    cur.execute("""
        SELECT FRIENDLY_SCHEMA, FRIENDLY_NAME, ONE_LINER, COMMENT, ROW_COUNT,
               UPPER(SOURCE_ID) as SOURCE_ID, THE_LIBRARY_FQN
        FROM LIBRARY_META.REGISTRY.FRIENDLY_LAYER
        ORDER BY FRIENDLY_SCHEMA, FRIENDLY_NAME
    """)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def fetch_edges(cur):
    """Fetch relationships between THE_LIBRARY tables."""
    cur.execute("""
        WITH ls AS (
          SELECT DISTINCT UPPER(SOURCE_ID) as SRC, FRIENDLY_SCHEMA, FRIENDLY_NAME
          FROM LIBRARY_META.REGISTRY.FRIENDLY_LAYER
          WHERE SOURCE_ID IS NOT NULL AND SOURCE_ID != ''
        )
        SELECT a.FRIENDLY_SCHEMA as SCHEMA_A, a.FRIENDLY_NAME as TABLE_A,
               b.FRIENDLY_SCHEMA as SCHEMA_B, b.FRIENDLY_NAME as TABLE_B,
               e.KEY, e.TIER, e.MATCHED, e.CONFIDENCE
        FROM LIBRARY_META."CONNECT".CONNECT_EDGES e
        JOIN ls a ON e.A = a.SRC
        JOIN ls b ON e.B = b.SRC
        ORDER BY e.KEY, a.FRIENDLY_SCHEMA, a.FRIENDLY_NAME
    """)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def fetch_columns(cur):
    """Fetch column metadata for all non-snapshot tables in THE_LIBRARY."""
    cur.execute("""
        SELECT table_schema, table_name, column_name, data_type
        FROM THE_LIBRARY.INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema NOT IN ('INFORMATION_SCHEMA', 'PUBLIC')
          AND table_name NOT LIKE 'FT_SNAPSHOT%%'
        ORDER BY table_schema, table_name, ordinal_position
    """)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def build_html(nodes, edges, columns, vendor_dir):
    """Assemble the complete standalone HTML."""
    # Read vendor JS
    cytoscape_js = (vendor_dir / "cytoscape.min.js").read_text(encoding="utf-8")
    # cose-bilkent removed — using built-in 'cose' layout instead
    cosebilkent_js = "// cose-bilkent not needed - using built-in cose layout"

    # Build data blob
    data = {
        "nodes": nodes,
        "edges": edges,
        "columns": columns,
    }
    data_json = json.dumps(data, default=str, ensure_ascii=False)

    # Compute stats
    schemas = list(set(n["FRIENDLY_SCHEMA"] for n in nodes))
    total_cols = len(columns)
    entity_keys = {"NPI", "EIN", "BIOGUIDE", "CIK", "CCN", "CCN~NPI", "DOCKET",
                   "LEI", "ICPSR", "CIK~EIN", "DUNS", "DUNS~UEI", "EIN~UEI",
                   "UEI", "PATENT"}
    entity_edges = [e for e in edges if e["KEY"] in entity_keys]
    geo_edges = [e for e in edges if e["KEY"] not in entity_keys]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>THE LIBRARY — Data Explorer</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
  background: #0f0f1a;
  color: #e0e0e0;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}}
#header {{
  background: #16162a;
  border-bottom: 1px solid #2a2a4a;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  z-index: 100;
}}
#header h1 {{
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #fff;
}}
#header h1 span {{
  color: #6c8cff;
}}
.stats {{
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: #8888aa;
}}
.stats .stat-val {{
  color: #b0b0d0;
  font-weight: 600;
}}
#search-box {{
  margin-left: auto;
  position: relative;
}}
#search-box input {{
  background: #1e1e3a;
  border: 1px solid #3a3a5a;
  border-radius: 6px;
  padding: 8px 14px 8px 36px;
  color: #e0e0e0;
  font-size: 13px;
  width: 280px;
  outline: none;
  transition: border-color 0.2s;
}}
#search-box input:focus {{
  border-color: #6c8cff;
}}
#search-box::before {{
  content: '\\1F50D';
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  opacity: 0.5;
}}
#main {{
  display: flex;
  flex: 1;
  overflow: hidden;
}}
#cy {{
  flex: 1;
  background: #0f0f1a;
}}
#sidebar {{
  width: 380px;
  background: #16162a;
  border-left: 1px solid #2a2a4a;
  overflow-y: auto;
  padding: 0;
  transition: transform 0.3s ease;
  transform: translateX(100%);
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 50;
}}
#sidebar.open {{
  transform: translateX(0);
}}
#sidebar-content {{
  padding: 24px;
}}
#sidebar .close-btn {{
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  color: #8888aa;
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}}
#sidebar .close-btn:hover {{
  background: #2a2a4a;
  color: #fff;
}}
#sidebar h2 {{
  font-size: 16px;
  color: #fff;
  margin-bottom: 4px;
  padding-right: 30px;
}}
#sidebar .schema-badge {{
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  background: #2a2a4a;
  color: #8888aa;
  margin-bottom: 12px;
}}
#sidebar .one-liner {{
  font-size: 14px;
  color: #b0b0d0;
  margin-bottom: 16px;
  line-height: 1.5;
}}
#sidebar .description {{
  font-size: 13px;
  color: #9090b0;
  line-height: 1.6;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #2a2a4a;
}}
#sidebar .row-count {{
  font-size: 12px;
  color: #6c8cff;
  margin-bottom: 16px;
}}
#sidebar h3 {{
  font-size: 13px;
  color: #8888aa;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 16px 0 8px 0;
}}
#sidebar .col-table {{
  width: 100%;
  font-size: 12px;
  border-collapse: collapse;
}}
#sidebar .col-table th {{
  text-align: left;
  color: #6666aa;
  font-weight: 600;
  padding: 4px 8px;
  border-bottom: 1px solid #2a2a4a;
}}
#sidebar .col-table td {{
  padding: 3px 8px;
  color: #b0b0d0;
  border-bottom: 1px solid #1a1a2e;
}}
#sidebar .col-table td:last-child {{
  color: #6c8cff;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 11px;
}}
#sidebar .connections {{
  margin-top: 12px;
}}
#sidebar .conn-group {{
  margin-bottom: 12px;
}}
#sidebar .conn-key {{
  font-size: 11px;
  font-weight: 600;
  color: #6c8cff;
  margin-bottom: 4px;
}}
#sidebar .conn-item {{
  font-size: 12px;
  color: #b0b0d0;
  padding: 3px 0;
  cursor: pointer;
  transition: color 0.2s;
}}
#sidebar .conn-item:hover {{
  color: #fff;
}}
#controls {{
  position: absolute;
  bottom: 20px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 50;
}}
#controls button {{
  background: #1e1e3a;
  border: 1px solid #3a3a5a;
  color: #b0b0d0;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}}
#controls button:hover {{
  background: #2a2a4a;
  border-color: #6c8cff;
  color: #fff;
}}
#filters {{
  position: absolute;
  top: 70px;
  left: 20px;
  z-index: 50;
  display: flex;
  flex-direction: column;
  gap: 6px;
}}
#filters label {{
  font-size: 12px;
  color: #8888aa;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}}
#filters input[type="checkbox"] {{
  accent-color: #6c8cff;
}}
#legend {{
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: #16162a;
  border: 1px solid #2a2a4a;
  border-radius: 8px;
  padding: 12px 16px;
  z-index: 50;
  font-size: 11px;
}}
#legend h4 {{
  color: #8888aa;
  margin-bottom: 8px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
#legend .legend-item {{
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  color: #b0b0d0;
}}
#legend .legend-dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
}}
.tooltip {{
  position: absolute;
  background: #1e1e3a;
  border: 1px solid #3a3a5a;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 12px;
  color: #e0e0e0;
  pointer-events: none;
  z-index: 200;
  max-width: 300px;
  display: none;
}}
</style>
</head>
<body>

<div id="header">
  <h1><span>THE LIBRARY</span> &mdash; Data Explorer</h1>
  <div class="stats">
    <span><span class="stat-val">{len(nodes)}</span> datasets</span>
    <span><span class="stat-val">{len(schemas)}</span> domains</span>
    <span><span class="stat-val">{total_cols:,}</span> columns</span>
    <span><span class="stat-val">{len(entity_edges)}</span> entity connections</span>
  </div>
  <div id="search-box">
    <input type="text" id="search" placeholder="Search tables, columns, descriptions..." />
  </div>
</div>

<div id="main">
  <div id="cy"></div>
  <div id="sidebar">
    <button class="close-btn" id="close-sidebar">&times;</button>
    <div id="sidebar-content"></div>
  </div>
</div>

<div id="filters">
  <label><input type="checkbox" id="toggle-geo" /> Show geographic connections</label>
</div>

<div id="controls">
  <button id="zoom-in" title="Zoom in">+</button>
  <button id="zoom-out" title="Zoom out">&minus;</button>
  <button id="fit" title="Fit to screen">&#x26F6;</button>
  <button id="relayout" title="Re-layout">&#x21BB;</button>
</div>

<div id="legend">
  <h4>Connection Keys</h4>
  <div class="legend-item"><div class="legend-dot" style="background:#6c8cff"></div>NPI (provider)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ff6c6c"></div>EIN (organization)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#6cffb8"></div>BIOGUIDE (legislator)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ffb86c"></div>CIK (SEC filer)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#b86cff"></div>CCN (facility)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#444466"></div>Geographic (ZIP/FIPS)</div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>{cytoscape_js}</script>
<!-- Using built-in cose layout - no plugin needed -->
<script>
(function() {{
  "use strict";
  var cy;
  window._debugCy = function() {{ return cy; }};

  const DATA = {data_json};

  // Key type classification
  const ENTITY_KEYS = new Set(['NPI','EIN','BIOGUIDE','CIK','CCN','CCN~NPI','DOCKET','LEI','ICPSR','CIK~EIN','DUNS','DUNS~UEI','EIN~UEI','UEI','PATENT']);
  const KEY_COLORS = {{
    'NPI': '#6c8cff', 'CCN~NPI': '#6c8cff', 'CCN': '#b86cff',
    'EIN': '#ff6c6c', 'EIN~UEI': '#ff6c6c',
    'BIOGUIDE': '#6cffb8', 'ICPSR': '#6cffb8',
    'CIK': '#ffb86c', 'CIK~EIN': '#ffb86c',
    'LEI': '#ffff6c', 'DOCKET': '#ff6cff',
    'DUNS': '#6cffff', 'DUNS~UEI': '#6cffff', 'UEI': '#6cffff',
    'PATENT': '#ff9966',
    '_GEO': '#444466'
  }};

  // Schema color palette (24 distinct muted colors)
  const SCHEMA_COLORS = [
    '#3d5a80','#98c1d9','#ee6c4d','#293241','#e0fbfc',
    '#8d99ae','#2b2d42','#edf2f4','#d90429','#ef233c',
    '#006d77','#83c5be','#ffddd2','#e29578','#264653',
    '#2a9d8f','#e9c46a','#f4a261','#e76f51','#606c38',
    '#283618','#dda15e','#bc6c25','#457b9d'
  ];

  // Build column lookup: schema.table -> [{{name, type}}]
  const colLookup = {{}};
  DATA.columns.forEach(c => {{
    const key = c.TABLE_SCHEMA + '.' + c.TABLE_NAME;
    if (!colLookup[key]) colLookup[key] = [];
    colLookup[key].push({{ name: c.COLUMN_NAME, type: c.DATA_TYPE }});
  }});

  // Build connection lookup: table -> [{{peer, key, schema}}]
  const connLookup = {{}};
  DATA.edges.forEach(e => {{
    const keyA = e.SCHEMA_A + '.' + e.TABLE_A;
    const keyB = e.SCHEMA_B + '.' + e.TABLE_B;
    if (!connLookup[keyA]) connLookup[keyA] = [];
    if (!connLookup[keyB]) connLookup[keyB] = [];
    connLookup[keyA].push({{ peer: e.TABLE_B, peerSchema: e.SCHEMA_B, key: e.KEY }});
    connLookup[keyB].push({{ peer: e.TABLE_A, peerSchema: e.SCHEMA_A, key: e.KEY }});
  }});

  // Get unique schemas and assign colors
  const schemas = [...new Set(DATA.nodes.map(n => n.FRIENDLY_SCHEMA))].sort();
  const schemaColorMap = {{}};
  schemas.forEach((s, i) => {{ schemaColorMap[s] = SCHEMA_COLORS[i % SCHEMA_COLORS.length]; }});

  // Build cytoscape elements
  const elements = [];

  // Table nodes (flat - no compound parents)
  DATA.nodes.forEach(n => {{
    elements.push({{
      data: {{
        id: n.FRIENDLY_SCHEMA + '.' + n.FRIENDLY_NAME,
        label: n.FRIENDLY_NAME.replace(/_/g, ' ').substring(0, 30),
        fullLabel: n.FRIENDLY_NAME,
        schema: n.FRIENDLY_SCHEMA,
        oneLiner: n.ONE_LINER || '',
        description: n.COMMENT || '',
        rowCount: n.ROW_COUNT || 0,
        fqn: n.THE_LIBRARY_FQN || ''
      }},
      classes: 'table-node'
    }});
  }});

  // Edges
  DATA.edges.forEach((e, i) => {{
    const isGeo = !ENTITY_KEYS.has(e.KEY);
    const color = KEY_COLORS[e.KEY] || KEY_COLORS['_GEO'];
    elements.push({{
      data: {{
        id: 'edge_' + i,
        source: e.SCHEMA_A + '.' + e.TABLE_A,
        target: e.SCHEMA_B + '.' + e.TABLE_B,
        key: e.KEY,
        isGeo: isGeo,
        matched: e.MATCHED || 0,
        edgeColor: color
      }},
      classes: isGeo ? 'geo-edge' : 'entity-edge'
    }});
  }});

  // Initialize cytoscape
  cy = cytoscape({{
    container: document.getElementById('cy'),
    elements: elements,
    style: [
      {{
        selector: '.table-node',
        style: {{
          'background-color': function(ele) {{ return schemaColorMap[ele.data('schema')] || '#555'; }},
          'width': function(ele) {{ var rc = ele.data('rowCount') || 0; return Math.max(14, Math.min(30, 14 + Math.log10(rc + 1) * 3)); }},
          'height': function(ele) {{ var rc = ele.data('rowCount') || 0; return Math.max(14, Math.min(30, 14 + Math.log10(rc + 1) * 3)); }},
          'label': '',
          'border-width': 1,
          'border-color': function(ele) {{ var c = schemaColorMap[ele.data('schema')] || '#555'; return c; }},
          'border-opacity': 0.4,
          'opacity': 0.9
        }}
      }},
      {{
        selector: '.table-node:active, .table-node:selected',
        style: {{
          'border-width': 3,
          'border-color': '#fff',
          'width': 26,
          'height': 26,
          'opacity': 1
        }}
      }},
      {{
        selector: '.entity-edge',
        style: {{
          'line-color': 'data(edgeColor)',
          'width': 1.5,
          'opacity': 0.7,
          'curve-style': 'bezier',
          'target-arrow-shape': 'none'
        }}
      }},
      {{
        selector: '.geo-edge',
        style: {{
          'line-color': '#444466',
          'width': 0.8,
          'opacity': 0.15,
          'curve-style': 'bezier',
          'target-arrow-shape': 'none'
        }}
      }},
      {{
        selector: '.geo-edge.hidden',
        style: {{
          'display': 'none'
        }}
      }},
      {{
        selector: '.highlighted',
        style: {{
          'border-width': 3,
          'border-color': '#6c8cff',
          'width': 22,
          'height': 22,
          'opacity': 1,
          'z-index': 100,
          'label': 'data(label)',
          'font-size': 10,
          'color': '#fff',
          'text-background-color': '#1e1e3a',
          'text-background-opacity': 0.9,
          'text-background-padding': '3px'
        }}
      }},
      {{
        selector: '.faded',
        style: {{
          'opacity': 0.1
        }}
      }},
      {{
        selector: '.neighbor-highlighted',
        style: {{
          'opacity': 1,
          'border-width': 2,
          'border-color': '#6c8cff',
          'width': 18,
          'height': 18,
          'label': 'data(label)',
          'font-size': 9,
          'color': '#b0b0d0',
          'text-background-color': '#1e1e3a',
          'text-background-opacity': 0.9,
          'text-background-padding': '2px'
        }}
      }},
      {{
        selector: '.edge-highlighted',
        style: {{
          'opacity': 1,
          'width': 2.5
        }}
      }}
    ],
    layout: {{ name: 'preset' }},
    minZoom: 0.01,
    maxZoom: 5,
    wheelSensitivity: 0.2
  }});

  // Run layout after init
  cy.layout({{
    name: 'cose',
    nodeDimensionsIncludeLabels: true,
    animate: false,
    randomize: true,
    idealEdgeLength: function(edge) {{ return 50; }},
    nodeRepulsion: function(node) {{ return 8000; }},
    edgeElasticity: function(edge) {{ return 45; }},
    nestingFactor: 0.1,
    gravity: 1.0,
    numIter: 1500,
    padding: 30,
    componentSpacing: 60,
    fit: true
  }}).run();

  // After layout: hide geo edges by default (they were used for positioning)
  cy.edges('.geo-edge').addClass('hidden');

  // Tooltip on hover
  const tooltip = document.getElementById('tooltip');
  cy.on('mouseover', '.table-node', function(e) {{
    const node = e.target;
    const d = node.data();
    tooltip.innerHTML = '<strong>' + d.fullLabel.replace(/_/g, ' ') + '</strong><br>' + (d.oneLiner || '');
    tooltip.style.display = 'block';
  }});
  cy.on('mousemove', '.table-node', function(e) {{
    tooltip.style.left = e.renderedPosition.x + 20 + 'px';
    tooltip.style.top = e.renderedPosition.y + 80 + 'px';
  }});
  cy.on('mouseout', '.table-node', function() {{
    tooltip.style.display = 'none';
  }});

  // Click table node -> show sidebar
  cy.on('tap', '.table-node', function(e) {{
    const node = e.target;
    const d = node.data();
    const tableKey = d.schema + '.' + d.fullLabel;
    showSidebar(d, tableKey);
    highlightNode(node);
  }});

  // Click background -> close sidebar, clear highlights
  cy.on('tap', function(e) {{
    if (e.target === cy) {{
      closeSidebar();
      clearHighlights();
    }}
  }});

  function highlightNode(node) {{
    clearHighlights();
    cy.elements().addClass('faded');
    node.removeClass('faded').addClass('highlighted');
    const neighborhood = node.neighborhood();
    neighborhood.nodes().removeClass('faded').addClass('neighbor-highlighted');
    neighborhood.edges().removeClass('faded').addClass('edge-highlighted');
    // Keep parent schemas visible
    // (no compound nodes in this version)
  }}

  function clearHighlights() {{
    cy.elements().removeClass('faded highlighted neighbor-highlighted edge-highlighted');
  }}

  function showSidebar(d, tableKey) {{
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('sidebar-content');
    const cols = colLookup[tableKey] || [];
    const conns = connLookup[tableKey] || [];

    // Group connections by key
    const grouped = {{}};
    conns.forEach(c => {{
      if (!grouped[c.key]) grouped[c.key] = [];
      // Deduplicate
      if (!grouped[c.key].find(x => x.peer === c.peer)) {{
        grouped[c.key].push(c);
      }}
    }});

    let html = '';
    html += '<span class="schema-badge">' + d.schema + '</span>';
    html += '<h2>' + d.fullLabel.replace(/_/g, ' ') + '</h2>';
    if (d.oneLiner) html += '<p class="one-liner">' + escHtml(d.oneLiner) + '</p>';
    if (d.description) html += '<p class="description">' + escHtml(d.description) + '</p>';
    if (d.rowCount) html += '<p class="row-count">' + Number(d.rowCount).toLocaleString() + ' rows</p>';
    if (d.fqn) html += '<p style="font-size:11px;color:#6666aa;margin-bottom:16px;font-family:monospace;">' + escHtml(d.fqn) + '</p>';

    // Columns
    if (cols.length > 0) {{
      html += '<h3>Columns (' + cols.length + ')</h3>';
      html += '<table class="col-table"><thead><tr><th>Name</th><th>Type</th></tr></thead><tbody>';
      cols.forEach(c => {{
        html += '<tr><td>' + escHtml(c.name) + '</td><td>' + escHtml(c.type) + '</td></tr>';
      }});
      html += '</tbody></table>';
    }}

    // Connections
    const keyNames = Object.keys(grouped);
    if (keyNames.length > 0) {{
      html += '<div class="connections"><h3>Connected To</h3>';
      keyNames.forEach(k => {{
        html += '<div class="conn-group"><div class="conn-key">via ' + k + '</div>';
        grouped[k].forEach(c => {{
          html += '<div class="conn-item" data-target="' + c.peerSchema + '.' + c.peer + '">' + c.peerSchema + ' / ' + c.peer.replace(/_/g, ' ') + '</div>';
        }});
        html += '</div>';
      }});
      html += '</div>';
    }}

    content.innerHTML = html;
    sidebar.classList.add('open');

    // Click connection -> navigate to that node
    content.querySelectorAll('.conn-item').forEach(el => {{
      el.addEventListener('click', function() {{
        const targetId = this.getAttribute('data-target');
        const targetNode = cy.getElementById(targetId);
        if (targetNode.length) {{
          cy.animate({{ center: {{ eles: targetNode }}, zoom: 2 }}, {{ duration: 400 }});
          setTimeout(() => targetNode.emit('tap'), 450);
        }}
      }});
    }});
  }}

  function closeSidebar() {{
    document.getElementById('sidebar').classList.remove('open');
  }}

  function escHtml(s) {{
    const div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML;
  }}

  // Close button
  document.getElementById('close-sidebar').addEventListener('click', function() {{
    closeSidebar();
    clearHighlights();
  }});

  // Zoom controls
  document.getElementById('zoom-in').addEventListener('click', function() {{
    cy.zoom({{ level: cy.zoom() * 1.3, renderedPosition: {{ x: cy.width()/2, y: cy.height()/2 }} }});
  }});
  document.getElementById('zoom-out').addEventListener('click', function() {{
    cy.zoom({{ level: cy.zoom() / 1.3, renderedPosition: {{ x: cy.width()/2, y: cy.height()/2 }} }});
  }});
  document.getElementById('fit').addEventListener('click', function() {{
    cy.fit(undefined, 40);
    clearHighlights();
  }});
  document.getElementById('relayout').addEventListener('click', function() {{
    cy.layout({{
      name: 'cose',
      nodeDimensionsIncludeLabels: true,
      animate: true,
      animationDuration: 1000,
      randomize: true,
      idealEdgeLength: function(edge) {{ return 50; }},
      nodeRepulsion: function(node) {{ return 8000; }},
      gravity: 1.0,
      numIter: 1500,
      fit: true
    }}).run();
  }});

  // Toggle geographic edges
  document.getElementById('toggle-geo').addEventListener('change', function() {{
    if (this.checked) {{
      cy.edges('.geo-edge').removeClass('hidden');
    }} else {{
      cy.edges('.geo-edge').addClass('hidden');
    }}
  }});

  // Search
  let searchTimeout;
  document.getElementById('search').addEventListener('input', function() {{
    clearTimeout(searchTimeout);
    const q = this.value.trim().toLowerCase();
    searchTimeout = setTimeout(function() {{
      if (!q) {{
        clearHighlights();
        return;
      }}
      cy.elements().addClass('faded');
      cy.nodes('.schema-node').removeClass('faded');

      // Search in table names, one-liners, and columns
      const matches = cy.nodes('.table-node').filter(function(n) {{
        const d = n.data();
        if (d.fullLabel.toLowerCase().includes(q)) return true;
        if (d.oneLiner && d.oneLiner.toLowerCase().includes(q)) return true;
        if (d.description && d.description.toLowerCase().includes(q)) return true;
        // Search columns
        const tableKey = d.schema + '.' + d.fullLabel;
        const cols = colLookup[tableKey] || [];
        return cols.some(c => c.name.toLowerCase().includes(q));
      }});

      matches.removeClass('faded').addClass('highlighted');
      if (matches.length > 0 && matches.length <= 10) {{
        cy.fit(matches, 80);
      }}
    }}, 300);
  }});

  // Escape key closes sidebar
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') {{
      closeSidebar();
      clearHighlights();
      document.getElementById('search').value = '';
    }}
  }});

}})();
</script>
</body>
</html>"""

    return html


def main():
    script_dir = Path(__file__).parent
    vendor_dir = script_dir / "vendor"
    output_path = script_dir / "the_library_explorer.html"

    if not vendor_dir.exists():
        print(f"ERROR: vendor directory not found at {vendor_dir}")
        print("Run: mkdir reports/vendor && download cytoscape.min.js + cytoscape-cose-bilkent.js")
        sys.exit(1)

    print("Connecting to Snowflake...")
    conn = get_connection()
    cur = conn.cursor()

    try:
        print("Fetching table metadata...")
        nodes = fetch_nodes(cur)
        print(f"  -> {len(nodes)} tables")

        print("Fetching relationships...")
        edges = fetch_edges(cur)
        print(f"  -> {len(edges)} edges")

        print("Fetching column data...")
        columns = fetch_columns(cur)
        print(f"  -> {len(columns)} columns")

        print("Building HTML...")
        html = build_html(nodes, edges, columns, vendor_dir)

        output_path.write_text(html, encoding="utf-8")
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\nDone! Written to: {output_path}")
        print(f"File size: {size_mb:.1f} MB")
        print(f"Open in browser: file:///{output_path.as_posix()}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
