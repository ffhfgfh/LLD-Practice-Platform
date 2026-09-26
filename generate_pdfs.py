import os
import re
import subprocess
import time
from pathlib import Path
import markdown
from pymdownx import superfences, highlight

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WORKSPACE = Path(r"c:\Users\N\Downloads\project2")

CSS_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

@page {
    size: A4 portrait;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {
        content: counter(page);
    }
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    font-size: 13.5px;
    line-height: 1.65;
    margin: 0;
    padding: 0;
}

/* Headings */
h1 {
    color: #0f172a;
    font-size: 26px;
    font-weight: 800;
    margin-top: 24px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
    letter-spacing: -0.02em;
}

h2 {
    color: #1e293b;
    font-size: 19px;
    font-weight: 700;
    margin-top: 22px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #f1f5f9;
    letter-spacing: -0.01em;
}

h3 {
    color: #334155;
    font-size: 15px;
    font-weight: 600;
    margin-top: 16px;
    margin-bottom: 8px;
}

h4, h5, h6 {
    color: #475569;
    font-size: 13.5px;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 6px;
}

p {
    margin-top: 0;
    margin-bottom: 10px;
    color: #334155;
}

a {
    color: #4f46e5;
    text-decoration: none;
    font-weight: 500;
}

/* Blockquotes / Callouts */
blockquote {
    margin: 14px 0;
    padding: 10px 16px;
    background: #f8fafc;
    border-left: 4px solid #6366f1;
    border-radius: 0 6px 6px 0;
    color: #334155;
    font-style: normal;
}

blockquote p:last-child {
    margin-bottom: 0;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 12px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    overflow: hidden;
    page-break-inside: avoid;
}

th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 8px 12px;
    border-bottom: 1.5px solid #cbd5e1;
    border-right: 1px solid #e2e8f0;
}

th:last-child {
    border-right: none;
}

td {
    padding: 7px 12px;
    border-bottom: 1px solid #f1f5f9;
    border-right: 1px solid #f1f5f9;
    color: #334155;
}

td:last-child {
    border-right: none;
}

tr:nth-child(even) {
    background: #fafafa;
}

tr:last-child td {
    border-bottom: none;
}

/* Code & Pre */
code {
    font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
    font-size: 11.5px;
    background: #f1f5f9;
    color: #db2777;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}

pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 12px 16px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    line-height: 1.5;
    margin: 12px 0;
    page-break-inside: avoid;
    border: 1px solid #1e293b;
}

pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
    font-size: inherit;
}

/* Lists */
ul, ol {
    margin-top: 4px;
    margin-bottom: 10px;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
    color: #334155;
}

li > ul, li > ol {
    margin-top: 2px;
    margin-bottom: 2px;
}

hr {
    border: none;
    height: 1px;
    background: #e2e8f0;
    margin: 20px 0;
}

/* Header Banner / Document Header */
.doc-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
    color: #ffffff;
    padding: 24px 28px;
    border-radius: 10px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.doc-header h1 {
    color: #ffffff;
    border: none;
    margin: 0 0 6px 0;
    padding: 0;
    font-size: 24px;
    font-weight: 800;
}

.doc-header p {
    color: #cbd5e1;
    margin: 0;
    font-size: 13px;
    line-height: 1.5;
}

.doc-meta {
    display: flex;
    gap: 16px;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    font-size: 11px;
    color: #94a3b8;
}

.doc-meta span {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* Mermaid Visual Container */
.mermaid {
    display: flex;
    justify-content: center;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px;
    margin: 14px 0;
    page-break-inside: avoid;
}

/* Page Break Helper */
.page-break {
    page-break-after: always;
}

/* Badge styling */
.badge {
    display: inline-block;
    padding: 2px 7px;
    font-size: 10.5px;
    font-weight: 600;
    border-radius: 9999px;
    margin-right: 4px;
}
.badge-easy { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.badge-med { background: #fef9c3; color: #a16207; border: 1px solid #fef08a; }
.badge-hard { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }

/* Print optimization */
@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .no-break {
        page-break-inside: avoid;
    }
}
"""

def markdown_to_html(md_content, title="Documentation", subtitle=""):
    # Convert Mermaid code blocks
    pattern = r'```mermaid\s*\n(.*?)```'
    def replace_mermaid(match):
        code = match.group(1).strip()
        return f'<div class="mermaid">\n{code}\n</div>'
    
    processed_md = re.sub(pattern, replace_mermaid, md_content, flags=re.DOTALL)
    
    extensions = [
        'extra',
        'tables',
        'fenced_code',
        'codehilite',
        'toc',
        'nl2br',
        'sane_lists',
        'pymdownx.superfences'
    ]
    
    html_body = markdown.markdown(processed_md, extensions=extensions)
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        {CSS_STYLES}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'neutral',
            flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }},
            sequence: {{ useMaxWidth: true, showSequenceNumbers: true }}
        }});
    </script>
</head>
<body>
    <div class="doc-header">
        <h1>{title}</h1>
        {f"<p>{subtitle}</p>" if subtitle else ""}
        <div class="doc-meta">
            <span>📅 Generated: September 2026</span>
            <span>🏛️ Project: LLD Practice Platform</span>
            <span>⚡ Status: Verified & Production Ready</span>
        </div>
    </div>
    <div class="doc-content">
        {html_body}
    </div>
</body>
</html>"""
    return full_html

def convert_html_to_pdf(html_path, pdf_path):
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=4000",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        str(html_path.resolve())
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error converting {html_path}: {result.stderr}")
    else:
        print(f"[OK] Generated PDF: {pdf_path}")

def main():
    docs_to_generate = [
        {
            "src": "RESEARCH.md",
            "html": "Research_Note.html",
            "pdf": "Research_Note.pdf",
            "title": "LLD Practice Platform — Research Note",
            "subtitle": "Comprehensive analysis of Low-Level Design learning gaps, deterministic verification vs AI reasoning, and product direction."
        },
        {
            "src": "DESIGN.md",
            "html": "Design_Note.html",
            "pdf": "Design_Note.pdf",
            "title": "LLD Practice Platform — Architecture & Design Note",
            "subtitle": "System architecture, clean domain model, dual-layer evaluator strategy, and service lifecycle specifications."
        },
        {
            "src": ["README.md", "AI_USAGE.md"],
            "html": "README_and_AI_USAGE.html",
            "pdf": "README_and_AI_USAGE.pdf",
            "title": "LLD Practice Platform — Specification & AI Usage Log",
            "subtitle": "Complete platform guide, 10 canonical challenges, quickstart setup, REST API reference, and architectural AI trade-offs."
        },
        {
            "src": "README.md",
            "html": "README.html",
            "pdf": "README.pdf",
            "title": "LLD Practice Platform — Platform Overview & Guide",
            "subtitle": "Interactive Low-Level Design Mastery & Interview Preparation Platform."
        },
        {
            "src": "AI_USAGE.md",
            "html": "AI_USAGE.html",
            "pdf": "AI_USAGE.pdf",
            "title": "LLD Practice Platform — AI Collaboration & Decision Log",
            "subtitle": "Architectural decisions contrasting AI suggestions against engineering rationale."
        }
    ]

    scratch_dir = WORKSPACE / "docs_pdf"
    scratch_dir.mkdir(exist_ok=True)

    for item in docs_to_generate:
        if isinstance(item["src"], list):
            content_parts = []
            for src_file in item["src"]:
                with open(WORKSPACE / src_file, "r", encoding="utf-8") as f:
                    content_parts.append(f.read())
            combined_md = "\n\n<div class='page-break'></div>\n\n".join(content_parts)
            html_content = markdown_to_html(combined_md, item["title"], item["subtitle"])
        else:
            with open(WORKSPACE / item["src"], "r", encoding="utf-8") as f:
                raw_md = f.read()
            html_content = markdown_to_html(raw_md, item["title"], item["subtitle"])
        
        html_file = scratch_dir / item["html"]
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        pdf_file = WORKSPACE / item["pdf"]
        convert_html_to_pdf(html_file, pdf_file)

if __name__ == "__main__":
    main()
