#!/usr/bin/env python3
"""
Build comprehensive index.html for DRE 3D architecture diagrams.
Organizes diagrams in storytelling order with local PNG/SVG references.
"""

# Diagram catalog organized by narrative flow
diagrams = {
    "intro": {
        "title": "📖 The Story: From Problem to Solution",
        "description": "Start here to understand what DRE 3D is and why it exists",
        "diagrams": [
            {"file": "00_system_overview", "title": "System Overview", "desc": "The big picture: How DRE 3D fits into your data ecosystem"},
            {"file": "26_databricks_native_architecture", "title": "Databricks-Native Architecture", "desc": "Built 100% on Databricks: Apps, Workflows, Unity Catalog, Mosaic AI"},
        ]
    },
    "selfservice": {
        "title": "🤖 Self-Service Rule Portal: No Coding Required",
        "description": "The game-changer: Business analysts can create data quality rules via conversational chatbot",
        "diagrams": [
            {"file": "01_tech_rule_capture", "title": "Rule Capture (Technical View)", "desc": "How the chatbot translates natural language to SQL via LLM"},
            {"file": "24_rule_authoring_data_flow", "title": "Rule Authoring Data Flow", "desc": "End-to-end data flow: User input → LLM → Validation → Deployment"},
            {"file": "08_user_journey", "title": "User Journey", "desc": "Step-by-step: What users see when creating rules"},
            {"file": "09_rule_lifecycle", "title": "Rule Lifecycle", "desc": "From creation → approval → deployment → execution → retirement"},
            {"file": "37_chatbot_memory_session", "title": "Chatbot Memory & Session Management", "desc": "How the chatbot remembers context across conversations"},
        ]
    },
    "architecture": {
        "title": "🏗️ Architecture Deep Dive: The Three Layers",
        "description": "Frontend/Orchestration → RAG/Knowledge → Execution (D1/D2/D3)",
        "diagrams": [
            {"file": "27_frontend_orchestration_layer", "title": "Layer 1: Frontend & Orchestration", "desc": "Databricks Apps + LangGraph multi-agent orchestration"},
            {"file": "28_rag_knowledge_base_layer", "title": "Layer 2: RAG Knowledge Base", "desc": "UC Volumes → Delta chunks → AI Search with CRAG confidence gating"},
            {"file": "29_execution_d1_d2_d3_layer", "title": "Layer 3: Execution (D1/D2/D3)", "desc": "Detection → Diagnosis → Deflection workflows"},
            {"file": "20_multiagent_architecture", "title": "Multi-Agent Architecture", "desc": "How agents communicate via LangGraph shared state"},
            {"file": "18_domain_expert_agents", "title": "Domain Expert Agents", "desc": "Specialized agents: Schema Expert, Query Optimizer, PII Guardian, etc."},
        ]
    },
    "c4": {
        "title": "📐 C4 Model: System Structure",
        "description": "Standard C4 architecture views from Context → Container → Component → Code",
        "diagrams": [
            {"file": "04_c4_context", "title": "C4 Context", "desc": "External systems: Users, Jira, GitHub, Databricks, ITSM"},
            {"file": "05_c4_container", "title": "C4 Container", "desc": "Major containers: Frontend, Orchestration, RAG, Workflows"},
            {"file": "06_c4_component", "title": "C4 Component", "desc": "Internal components: Agents, Validators, Executors"},
            {"file": "07_c4_code", "title": "C4 Code", "desc": "Code-level structure: Classes and modules"},
        ]
    },
    "validation": {
        "title": "🛡️ Safety & Governance: 10-Stage Validation Pipeline",
        "description": "How we prevent SQL injection, PII leaks, and duplicate rules",
        "diagrams": [
            {"file": "30_rag_validation_pipeline", "title": "RAG Validation Pipeline (Sequence)", "desc": "10 stages: Query Optimization → CAG → CRAG → Security → Governance → Duplicate → SQL Validation → Approval"},
            {"file": "31_validation_layers_architecture", "title": "Validation Layers (Component View)", "desc": "How CAG, CRAG, and Rule-based validators work together"},
            {"file": "21_crag_retrieval_strategy", "title": "CRAG Retrieval Strategy", "desc": "Confidence-gated RAG: HIGH (≥0.72) → MEDIUM (0.50-0.72) → LOW (<0.50)"},
            {"file": "11_approval_workflow", "title": "Approval Workflow", "desc": "Rule routing: Low-risk → Data Steward, High-risk → Data Owner + Security"},
        ]
    },
    "flows": {
        "title": "🔄 User Journeys: Interactive & Async Flows",
        "description": "Real-world scenarios: How users interact with the system",
        "diagrams": [
            {"file": "33_interactive_flows_sequence", "title": "Interactive Flows", "desc": "Rule authoring + 'Why did my pipeline fail?' diagnosis queries"},
            {"file": "34_async_d1_d2_d3_flows", "title": "Async D1/D2/D3 Flows", "desc": "Scheduled detection → diagnosis → deflection loop"},
            {"file": "35_swimlane_component_responsibilities", "title": "Swimlane: Component Responsibilities", "desc": "Who does what? Clear separation of concerns"},
            {"file": "32_end_to_end_component_interaction", "title": "End-to-End Component Interaction", "desc": "Comprehensive view: All components working together"},
        ]
    },
    "3d": {
        "title": "🎯 The 3D Framework: Detect → Diagnose → Deflect",
        "description": "The core engine: How DRE 3D handles anomalies automatically",
        "diagrams": [
            {"file": "02_tech_rule_execution", "title": "Rule Execution (D1 Detection)", "desc": "How D1 Detection Agent runs user-defined rules on schedule"},
            {"file": "15_d2_diagnosis_flow", "title": "D2 Diagnosis Flow", "desc": "Root cause analysis: Logs + Deployments + Data Drift + Incident KB"},
            {"file": "16_d3_deflection_flow", "title": "D3 Deflection Flow", "desc": "Fix generation + Approval + Execution + Feedback loop"},
            {"file": "17_schema_change_handler", "title": "Schema Change Handler", "desc": "Special case: Handling schema evolution gracefully"},
        ]
    },
    "operations": {
        "title": "⚙️ Operations & Monitoring",
        "description": "How we ensure the system stays healthy in production",
        "diagrams": [
            {"file": "10_deployment", "title": "Deployment Architecture", "desc": "Infrastructure: Compute, storage, networking on Databricks"},
            {"file": "13_multi_env_promotion", "title": "Multi-Environment Promotion", "desc": "Dev → Staging → Prod pipeline for rule deployment"},
            {"file": "14_rule_health_monitoring", "title": "Rule Health Monitoring", "desc": "Tracking rule performance, false positives, execution time"},
            {"file": "12_notification_alerting", "title": "Notification & Alerting", "desc": "How users get notified: Email, Slack, Teams, PagerDuty"},
            {"file": "26_operating_excellence_framework", "title": "Operating Excellence Framework", "desc": "SLAs, SLOs, error budgets, incident management"},
        ]
    },
    "optimization": {
        "title": "💰 Cost & Performance Optimization",
        "description": "How we keep LLM costs low and response times fast",
        "diagrams": [
            {"file": "36_llm_cost_optimisation", "title": "LLM Cost Optimization", "desc": "Caching, batching, model selection, prompt engineering"},
        ]
    },
    "governance": {
        "title": "📋 Governance & Compliance",
        "description": "Architecture compliance and implementation roadmap",
        "diagrams": [
            {"file": "23_arch_compliance_strategy", "title": "Architecture Compliance Strategy", "desc": "How we keep PUML diagrams in sync with code"},
            {"file": "22_implementation_roadmap", "title": "Implementation Roadmap", "desc": "Phase 1 (Foundation) → Phase 2 (Intelligence) → Phase 3 (Autonomy)"},
        ]
    },
}

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DRE 3D - Complete Architecture Story</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }}
        
        header .tagline {{
            font-size: 1.4rem;
            opacity: 0.95;
            margin-bottom: 1rem;
        }}
        
        header .description {{
            font-size: 1rem;
            opacity: 0.85;
            max-width: 900px;
            margin: 0 auto;
        }}
        
        nav {{
            background: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        nav ul {{
            list-style: none;
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        nav a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
            font-size: 0.9rem;
        }}
        
        nav a:hover {{
            color: #764ba2;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .section {{
            margin-bottom: 4rem;
        }}
        
        .section-header {{
            background: white;
            padding: 2rem;
            border-left: 6px solid #667eea;
            margin-bottom: 2rem;
            border-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .section-header h2 {{
            font-size: 2rem;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .section-header p {{
            color: #555;
            font-size: 1.1rem;
        }}
        
        .diagram-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(550px, 1fr));
            gap: 2rem;
        }}
        
        .diagram-card {{
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .diagram-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .diagram-card h3 {{
            font-size: 1.3rem;
            color: #333;
            margin-bottom: 0.5rem;
        }}
        
        .diagram-card .desc {{
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 1rem;
            line-height: 1.5;
        }}
        
        .diagram-card img {{
            width: 100%;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            cursor: pointer;
            transition: opacity 0.3s;
        }}
        
        .diagram-card img:hover {{
            opacity: 0.9;
        }}
        
        .diagram-links {{
            margin-top: 1rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        
        .diagram-links a {{
            padding: 0.5rem 1rem;
            background: #667eea;
            color: white !important;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.85rem;
            transition: background 0.3s;
        }}
        
        .diagram-links a:hover {{
            background: #764ba2;
        }}
        
        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }}
        
        .modal-content {{
            margin: auto;
            display: block;
            width: 90%;
            max-width: 1400px;
            max-height: 90%;
            object-fit: contain;
        }}
        
        .close {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <header>
        <h1>🚀 DRE 3D Data Quality Framework</h1>
        <p class="tagline">Self-Service Data Reliability with AI-Powered Detection, Diagnosis & Deflection</p>
        <p class="description">
            Capture data quality rules via conversational chatbot (no coding!). 
            AI agents automatically detect anomalies, diagnose root causes, and deflect problems before they impact business.
            Built 100% on Databricks native components.
        </p>
    </header>
    
    <nav>
        <ul>
{nav_items}
        </ul>
    </nav>
    
    <div class="container">
{sections}
    </div>
    
    <footer>
        <p>&copy; 2026 DRE 3D Data Quality Framework | Architecture Documentation</p>
        <p><small>Built on Databricks | Powered by LangGraph + Mosaic AI</small></p>
        <p style="margin-top: 1rem;"><small>All diagrams available in PNG and SVG formats</small></p>
    </footer>
    
    <!-- Modal for full-size image view -->
    <div id="imageModal" class="modal">
        <span class="close">&times;</span>
        <img class="modal-content" id="modalImage">
    </div>
    
    <script>
        // Image modal
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImage');
        const close = document.getElementsByClassName('close')[0];
        
        document.querySelectorAll('.diagram-card img').forEach(img => {{
            img.addEventListener('click', function() {{
                modal.style.display = 'block';
                modalImg.src = this.src;
            }});
        }});
        
        close.onclick = function() {{
            modal.style.display = 'none';
        }}
        
        modal.onclick = function(e) {{
            if (e.target === modal) {{
                modal.style.display = 'none';
            }}
        }}
        
        // Smooth scroll
        document.querySelectorAll('nav a').forEach(anchor => {{
            anchor.addEventListener('click', function(e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});
    </script>
</body>
</html>
"""

def build_html():
    # Build navigation
    nav_items = []
    for section_id, section_data in diagrams.items():
        title = section_data["title"].split(":", 1)[-1].strip() if ":" in section_data["title"] else section_data["title"]
        nav_items.append(f'            <li><a href="#{section_id}">{title}</a></li>')
    
    # Build sections
    sections = []
    for section_id, section_data in diagrams.items():
        section_html = f'''        <section id="{section_id}" class="section">
            <div class="section-header">
                <h2>{section_data["title"]}</h2>
                <p>{section_data["description"]}</p>
            </div>
            
            <div class="diagram-grid">
'''
        
        for diagram in section_data["diagrams"]:
            file = diagram["file"]
            title = diagram["title"]
            desc = diagram["desc"]
            
            section_html += f'''                <div class="diagram-card">
                    <h3>{title}</h3>
                    <p class="desc">{desc}</p>
                    <img src="png/{file}.png" alt="{title}" loading="lazy">
                    <div class="diagram-links">
                        <a href="{file}.puml" target="_blank">📄 PUML Source</a>
                        <a href="png/{file}.png" target="_blank">🖼️ PNG</a>
                        <a href="svg/{file}.svg" target="_blank">📐 SVG</a>
                    </div>
                </div>
'''
        
        section_html += '''            </div>
        </section>
'''
        sections.append(section_html)
    
    # Assemble final HTML
    html = html_template.format(
        nav_items='\n'.join(nav_items),
        sections='\n'.join(sections)
    )
    
    return html

if __name__ == "__main__":
    html_content = build_html()
    output_path = "index.html"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {output_path}")
    print(f"Total sections: {len(diagrams)}")
    print(f"Total diagrams: {sum(len(s['diagrams']) for s in diagrams.values())}")
