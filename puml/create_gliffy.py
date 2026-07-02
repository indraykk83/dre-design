#!/usr/bin/env python3
"""
create_gliffy.py
Generates a Draw.io XML diagram (.drawio) showing the DRE 3D end-to-end
component flow on Databricks SaaS.

The .drawio file can be imported into Confluence via Gliffy:
  Insert > Gliffy Diagram > Import > select dre3d_platform_story.drawio
  (Gliffy shows "Draw.io Diagram - ALPHA (.drawio, .xml)" as a supported type)

Or open directly in https://app.diagrams.net  (free, no login needed).

Usage:
    python create_gliffy.py
    # Output: dre3d_platform_story.drawio  (same folder as this script)
"""
from __future__ import annotations
import xml.etree.ElementTree as ET
from pathlib import Path

# ─── ID counter ────────────────────────────────────────────────────────────────
_id = 1

def nid() -> str:
    global _id
    _id += 1
    return str(_id)


# ─── Style presets ─────────────────────────────────────────────────────────────
BASE_BOX = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=6;"
    "align=center;verticalAlign=middle;"
    "fontSize=11;fontFamily=Helvetica;"
)

def box_style(fill: str, stroke: str, font_color: str = "#1A1A1A",
              bold: bool = False) -> str:
    b = "1" if bold else "0"
    return (
        f"{BASE_BOX}"
        f"fillColor={fill};strokeColor={stroke};fontColor={font_color};"
        f"strokeWidth=2;bold={b};"
    )

def header_style(fill: str, stroke: str) -> str:
    return (
        f"{BASE_BOX}"
        f"fillColor={fill};strokeColor={stroke};fontColor={stroke};"
        f"strokeWidth=2;bold=1;fontSize=12;"
    )

def group_style(fill: str, stroke: str) -> str:
    return (
        f"rounded=1;whiteSpace=wrap;html=1;arcSize=4;"
        f"fillColor={fill};strokeColor={stroke};fontColor={stroke};"
        f"strokeWidth=2;dashed=0;opacity=30;"
        f"align=left;verticalAlign=top;fontSize=10;fontStyle=1;"
    )

def edge_style(color: str, dashed: bool = False,
               exit_x: float = 0.5, exit_y: float = 1.0,
               entry_x: float = 0.5, entry_y: float = 0.0) -> str:
    d = "dashed=1;dashPattern=8 4;" if dashed else "dashed=0;"
    return (
        f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;"
        f"jettySize=auto;{d}"
        f"exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;"
        f"entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;"
        f"strokeColor={color};strokeWidth=2;fontColor={color};"
        f"fontSize=9;fontFamily=Helvetica;fontStyle=2;"
        f"startArrow=none;endArrow=block;endFill=1;"
    )


# ─── Layer colours ──────────────────────────────────────────────────────────────
C = {
    "interact": ("#E8EAF6", "#3949AB"),   # indigo — User / Chatbot
    "orch":     ("#E3F2FD", "#0D47A1"),   # blue   — LangGraph
    "ai":       ("#FFF8E1", "#E65100"),   # amber  — AI Gateway / Model Serving
    "data":     ("#E8F5E9", "#1B5E20"),   # green  — Backend / Delta / UC
    "exec":     ("#F3E5F5", "#6A1B9A"),   # purple — Workflows / D1 / D2 / D3
    "ops":      ("#EFEBE9", "#4E342E"),   # brown  — Monitoring / Approval / Jobs
}


# ─── XML helpers ───────────────────────────────────────────────────────────────
def add_cell(parent: ET.Element, cell_id: str, value: str, style: str,
             x: float, y: float, w: float, h: float,
             vertex: bool = True) -> ET.Element:
    cell = ET.SubElement(parent, "mxCell",
                         id=cell_id, value=value, style=style,
                         vertex="1" if vertex else "0",
                         parent="1")
    ET.SubElement(cell, "mxGeometry",
                  x=str(x), y=str(y), width=str(w), height=str(h),
                  **{"as": "geometry"})
    return cell


def add_edge(parent: ET.Element, edge_id: str, label: str,
             source: str, target: str, style: str) -> ET.Element:
    cell = ET.SubElement(parent, "mxCell",
                         id=edge_id, value=label, style=style,
                         edge="1", source=source, target=target,
                         parent="1")
    ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    return cell


def html(title: str, svc: str, body: str) -> str:
    """Build HTML label for a box."""
    return (
        f"<b>{title}</b><br/>"
        f"<font color='{svc[1]}' style='font-size:9px'>{svc[0]}</font><br/>"
        f"<font style='font-size:9px'>{body}</font>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# BUILD XML TREE
# ══════════════════════════════════════════════════════════════════════════════
root = ET.Element("mxGraphModel",
                  dx="1422", dy="762",
                  grid="1", gridSize="10",
                  guides="1", tooltips="1",
                  connect="1", arrows="1",
                  fold="1", page="0",
                  pageScale="1",
                  pageWidth="1654", pageHeight="1169",
                  math="0", shadow="0")
xml_root = ET.SubElement(root, "root")
ET.SubElement(xml_root, "mxCell", id="0")
ET.SubElement(xml_root, "mxCell", id="1", parent="0")

p = xml_root   # shorthand

# ══════════════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════════════
add_cell(p, nid(),
         "<b><font style='font-size:16px'>DRE 3D — End-to-End Component Flow on Databricks SaaS</font></b>",
         (f"text;html=1;strokeColor=none;fillColor=#E8EAF6;"
          f"align=center;verticalAlign=middle;fontSize=16;"
          f"fontColor=#1A237E;fontStyle=1;"),
         10, 10, 1580, 44)

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 1 — INTERACTION  (User + DQ Chatbot App)
# ══════════════════════════════════════════════════════════════════════════════
# group background
add_cell(p, nid(), "INTERACTION",
         group_style("#E8EAF6", "#3949AB"),
         10, 66, 220, 370)

# User
u_id = nid()
add_cell(p, u_id,
         "<b>👤 User</b><br/><font style='font-size:9px'>Data Engineer / BA / PO</font>",
         box_style(*C["interact"], font_color=C["interact"][1], bold=True),
         30, 86, 180, 50)

# DQ Chatbot App
chat_id = nid()
add_cell(p, chat_id,
         html("DQ Chatbot App",
              ("📱 Databricks Apps (Serverless)", C["interact"][1]),
              "Streamlit UI · SSO / OAuth<br/>LangGraph runtime · Auto-scale"),
         box_style(*C["interact"], font_color=C["interact"][1]),
         30, 166, 180, 90)

# Session Memory
sm_id = nid()
add_cell(p, sm_id,
         html("Session Memory",
              ("📊 Delta Lake · agent_session_log", C["data"][1]),
              "Last 20 turns · cross-session context<br/>Compact after 10 turns → UC Volume"),
         box_style(*C["data"], font_color=C["data"][1]),
         30, 286, 180, 80)

add_edge(p, nid(), "NL query", u_id, chat_id,
         edge_style(C["interact"][1], exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))
add_edge(p, nid(), "response / confirmation", chat_id, u_id,
         edge_style(C["interact"][1], exit_x=0.1, exit_y=0.0, entry_x=0.1, entry_y=1.0))
add_edge(p, nid(), "read / write turns", chat_id, sm_id,
         edge_style(C["data"][1], dashed=True,
                    exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 2 — ORCHESTRATION  (LangGraph)
# ══════════════════════════════════════════════════════════════════════════════
add_cell(p, nid(), "ORCHESTRATION",
         group_style("#E3F2FD", "#0D47A1"),
         250, 66, 220, 260)

lg_id = nid()
add_cell(p, lg_id,
         html("LangGraph Orchestrator",
              ("📱 Databricks Apps runtime", C["orch"][1]),
              "Intent router · State graph<br/>Tool dispatcher · Memory manager<br/>Temperature controller"),
         box_style(*C["orch"], font_color=C["orch"][1], bold=True),
         270, 86, 180, 110)

# Rule Suggestion Cache
rc_id = nid()
add_cell(p, rc_id,
         html("Rule Suggestion Cache",
              ("📊 Delta · check_suggestions_cache", C["data"][1]),
              "hash(schema+check_type) → cache hit<br/>Skip LLM on repeat queries"),
         box_style(*C["data"], font_color=C["data"][1]),
         270, 236, 180, 70)

add_edge(p, nid(), "dispatch intent + session_id",
         chat_id, lg_id,
         edge_style(C["orch"][1], exit_x=1.0, exit_y=0.5, entry_x=0.0, entry_y=0.5))
add_edge(p, nid(), "cache hit → skip LLM",
         lg_id, rc_id,
         edge_style(C["data"][1], dashed=True,
                    exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 3 — AI / INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
add_cell(p, nid(), "AI / INTELLIGENCE",
         group_style("#FFF8E1", "#E65100"),
         490, 66, 220, 370)

agw_id = nid()
add_cell(p, agw_id,
         html("AI Gateway",
              ("🛡️ Databricks AI Gateway", C["ai"][1]),
              "Rate limits per team<br/>Token budgets · PII filter<br/>Cost caps ($)"),
         box_style(*C["ai"], font_color=C["ai"][1], bold=True),
         510, 86, 180, 80)

ms_id = nid()
add_cell(p, ms_id,
         html("Model Serving Endpoint",
              ("🤖 Databricks Model Serving", C["ai"][1]),
              "DBRX / BYOM self-hosted<br/>Autoscale → 0 · &lt;5s p95<br/>Temp 0.1 SQL / 0.7 NL"),
         box_style(*C["ai"], font_color=C["ai"][1]),
         510, 196, 180, 85)

vs_id = nid()
add_cell(p, vs_id,
         html("Vector Search",
              ("🔍 Databricks AI Search", C["ai"][1]),
              "BGE-M3 embeddings<br/>CRAG-gated retrieval (k=8)<br/>Confidence: HIGH/MED/LOW"),
         box_style(*C["ai"], font_color=C["ai"][1]),
         510, 311, 180, 80)

ucv_id = nid()
add_cell(p, ucv_id,
         html("UC Volume (RAG KB)",
              ("📁 Unity Catalog Volume", C["data"][1]),
              "data_contracts/<br/>sql_patterns/ · examples/<br/>domain_glossary/"),
         box_style(*C["data"], font_color=C["data"][1]),
         510, 411, 180, 70)

# LangGraph → AI Gateway → Model Serving (with return)
add_edge(p, nid(), "LLM inference request",
         lg_id, agw_id,
         edge_style(C["ai"][1], exit_x=1.0, exit_y=0.3, entry_x=0.0, entry_y=0.3))
add_edge(p, nid(), "rate-limited, cost-capped",
         agw_id, ms_id,
         edge_style(C["ai"][1], exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))
add_edge(p, nid(), "SQL / analysis response",
         ms_id, lg_id,
         edge_style(C["ai"][1], exit_x=0.0, exit_y=0.6, entry_x=1.0, entry_y=0.6))

# LangGraph → Vector Search → UC Volume
add_edge(p, nid(), "embed_and_search(query, k=8)",
         lg_id, vs_id,
         edge_style(C["ai"][1], exit_x=1.0, exit_y=0.7, entry_x=0.0, entry_y=0.5))
add_edge(p, nid(), "index backed by raw docs",
         vs_id, ucv_id,
         edge_style(C["data"][1], dashed=True,
                    exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))

# AI Gateway → Lakehouse Monitoring (added at end)

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 4 — STATE / DATA
# ══════════════════════════════════════════════════════════════════════════════
add_cell(p, nid(), "STATE / DATA",
         group_style("#E8F5E9", "#1B5E20"),
         730, 66, 220, 415)

dqb_id = nid()
add_cell(p, dqb_id,
         html("DQ Backend App",
              ("📱 Databricks Apps (REST)", C["data"][1]),
              "Rule validation · SQL security guard<br/>Duplicate detect · Trend scorer<br/>Approval gateway"),
         box_style(*C["data"], font_color=C["data"][1], bold=True),
         750, 86, 180, 90)

dl_id = nid()
add_cell(p, dl_id,
         html("Delta Lake",
              ("🔺 Databricks Delta Lake", C["data"][1]),
              "<b>Tables:</b> anomaly_check_config<br/>check_execution_log<br/>DIGITAL_DATA_ANOMALIES<br/>rule_audit_log · session_memory"),
         box_style(*C["data"], font_color=C["data"][1]),
         750, 206, 180, 110)

uc_id = nid()
add_cell(p, uc_id,
         html("Unity Catalog",
              ("🗂️ Databricks Unity Catalog", C["data"][1]),
              "Governance · Data lineage<br/>Row/col security<br/>All tables registered here"),
         box_style(*C["data"], font_color=C["data"][1]),
         750, 346, 180, 80)

add_edge(p, nid(), "tool_call: create_rule / validate_sql",
         lg_id, dqb_id,
         edge_style(C["data"][1], exit_x=1.0, exit_y=0.5, entry_x=0.0, entry_y=0.5))
add_edge(p, nid(), "INSERT anomaly_check_config",
         dqb_id, dl_id,
         edge_style(C["data"][1], exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))
add_edge(p, nid(), "governed by",
         dl_id, uc_id,
         edge_style(C["data"][1], dashed=True,
                    exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 5 — EXECUTION  (Workflows + D1 / D2 / D3)
# ══════════════════════════════════════════════════════════════════════════════
add_cell(p, nid(), "EXECUTION",
         group_style("#F3E5F5", "#6A1B9A"),
         970, 66, 220, 510)

wf_id = nid()
add_cell(p, wf_id,
         html("Databricks Workflows",
              ("📦 Databricks Workflows (Serverless)", C["exec"][1]),
              "Scheduled + event-triggered jobs<br/>DAG orchestration · Delta trigger<br/>Multi-task job pipelines"),
         box_style(*C["exec"], font_color=C["exec"][1], bold=True),
         990, 86, 180, 90)

d1_id = nid()
add_cell(p, d1_id,
         html("D1 — Detect Agent",
              ("📦 Workflows Job", C["exec"][1]),
              "5D anomaly checks<br/>Null/Outlier/Freshness/Volume/Schema<br/>EWMA baselines · SLA monitor<br/>P0 alert &lt; 5 min"),
         box_style(*C["exec"], font_color=C["exec"][1]),
         990, 216, 180, 100)

d2_id = nid()
add_cell(p, d2_id,
         html("D2 — Diagnose Agent",
              ("📦 Workflows Job", C["exec"][1]),
              "Drift classifier · Lineage tracer<br/>Segment slicer · Evidence retriever<br/>LLM root-cause playbook<br/>Confidence-scored output"),
         box_style(*C["exec"], font_color=C["exec"][1]),
         990, 346, 180, 100)

d3_id = nid()
add_cell(p, d3_id,
         html("D3 — Deflect Agent",
              ("📦 Workflows Job", C["exec"][1]),
              "State validator · Circuit breaker<br/>12 domain expert agents<br/>(adiClub/CRM/Payments…)<br/>LLM playbook execution"),
         box_style(*C["exec"], font_color=C["exec"][1]),
         990, 476, 180, 100)

# Delta → Workflows (trigger)
add_edge(p, nid(), "event trigger / schedule",
         dl_id, wf_id,
         edge_style(C["exec"][1], exit_x=1.0, exit_y=0.3, entry_x=0.0, entry_y=0.5))
# Workflows → D1 / D2 / D3
add_edge(p, nid(), "run detection job",
         wf_id, d1_id,
         edge_style(C["exec"][1], exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))
add_edge(p, nid(), "trigger on anomaly event",
         d1_id, d2_id,
         edge_style(C["exec"][1], exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))
add_edge(p, nid(), "trigger on diagnosis bundle",
         d2_id, d3_id,
         edge_style(C["exec"][1], exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0))

# D1 → Delta Lake (write anomalies)
add_edge(p, nid(), "WRITE anomaly events",
         d1_id, dl_id,
         edge_style(C["data"][1], exit_x=0.0, exit_y=0.4, entry_x=1.0, entry_y=0.7))
# D2 → Model Serving (root-cause reasoning)
add_edge(p, nid(), "LLM: root-cause reasoning",
         d2_id, ms_id,
         edge_style(C["ai"][1], dashed=True,
                    exit_x=0.0, exit_y=0.3, entry_x=1.0, entry_y=0.7))
# D2 → Vector Search (runbook retrieval)
add_edge(p, nid(), "retrieve runbook patterns",
         d2_id, vs_id,
         edge_style(C["ai"][1], dashed=True,
                    exit_x=0.0, exit_y=0.5, entry_x=1.0, entry_y=0.5))
# D2 → Delta Lake (write diagnosis bundle)
add_edge(p, nid(), "WRITE diagnosis bundle",
         d2_id, dl_id,
         edge_style(C["data"][1], exit_x=0.0, exit_y=0.6, entry_x=1.0, entry_y=0.8))
# D3 → Delta Lake (write audit)
add_edge(p, nid(), "WRITE deflection audit log",
         d3_id, dl_id,
         edge_style(C["data"][1], exit_x=0.0, exit_y=0.5, entry_x=1.0, entry_y=1.0))

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 6 — OPERATIONS  (Approval + Jobs API + Lakehouse Monitoring)
# ══════════════════════════════════════════════════════════════════════════════
add_cell(p, nid(), "OPERATIONS",
         group_style("#EFEBE9", "#4E342E"),
         1210, 66, 220, 510)

apr_id = nid()
add_cell(p, apr_id,
         html("Approval Gateway",
              ("👤 Human-in-loop", C["ops"][1]),
              "Auto-approve LOW severity<br/>P0/P1 → owner review<br/>SLA: 48 hr maximum"),
         box_style(*C["ops"], font_color=C["ops"][1]),
         1230, 86, 180, 80)

ja_id = nid()
add_cell(p, ja_id,
         html("Jobs API",
              ("⚙️ Databricks Jobs API", C["ops"][1]),
              "Pipeline restart<br/>Parameter override<br/>Trigger upstream rerun"),
         box_style(*C["ops"], font_color=C["ops"][1]),
         1230, 196, 180, 80)

lm_id = nid()
add_cell(p, lm_id,
         html("Lakehouse Monitoring",
              ("📊 Databricks Lakehouse Monitoring", C["ops"][1]),
              "EWMA cost baselines<br/>Token usage dashboards<br/>Spike alert &lt; 5 min<br/>Weekly domain cost report"),
         box_style(*C["ops"], font_color=C["ops"][1], bold=True),
         1230, 306, 180, 100)

# D3 → Approval + Jobs API
add_edge(p, nid(), "route by severity",
         d3_id, apr_id,
         edge_style(C["ops"][1], exit_x=1.0, exit_y=0.2, entry_x=0.0, entry_y=0.5))
add_edge(p, nid(), "pipeline restart / override",
         d3_id, ja_id,
         edge_style(C["ops"][1], exit_x=1.0, exit_y=0.5, entry_x=0.0, entry_y=0.5))
# D1/D2/D3 → Lakehouse Monitoring
add_edge(p, nid(), "metrics + EWMA",
         d1_id, lm_id,
         edge_style(C["ops"][1], dashed=True,
                    exit_x=1.0, exit_y=0.7, entry_x=0.0, entry_y=0.2))
add_edge(p, nid(), "metrics + cost",
         d2_id, lm_id,
         edge_style(C["ops"][1], dashed=True,
                    exit_x=1.0, exit_y=0.7, entry_x=0.0, entry_y=0.5))
add_edge(p, nid(), "metrics + audit",
         d3_id, lm_id,
         edge_style(C["ops"][1], dashed=True,
                    exit_x=1.0, exit_y=0.8, entry_x=0.0, entry_y=0.8))
# AI Gateway → Lakehouse Monitoring
add_edge(p, nid(), "token usage / cost",
         agw_id, lm_id,
         edge_style(C["ops"][1], dashed=True,
                    exit_x=1.0, exit_y=0.7, entry_x=0.0, entry_y=0.1))

# ══════════════════════════════════════════════════════════════════════════════
# WRITE .drawio FILE
# ══════════════════════════════════════════════════════════════════════════════
tree = ET.ElementTree(root)
ET.indent(tree, space="  ")

out = Path(__file__).parent / "dre3d_platform_story.drawio"
tree.write(str(out), encoding="utf-8", xml_declaration=True)

print(f"✅  Written: {out}")
print(f"   Objects : ~{_id} shapes + arrows")
print()
print("📋 Import into Confluence (Gliffy):")
print("   1. Edit a Confluence page")
print("   2. Insert > Gliffy Diagram")
print("   3. In Gliffy editor click 'Import a Diagram'")
print("   4. Select  dre3d_platform_story.drawio")
print("   5. Gliffy shows it under 'Draw.io Diagram - ALPHA'")
print("   6. Double-click any shape or arrow to edit")
print()
print("📋 Open directly in Draw.io (no login):")
print("   https://app.diagrams.net  → open file → select .drawio")
