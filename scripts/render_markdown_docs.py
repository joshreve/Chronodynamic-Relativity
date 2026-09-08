r"""
Markdown to HTML Documentation Renderer with MathJax Support
============================================================
Compiles all core Markdown (.md) documents into fully responsive, MathJax-enabled
HTML files with:
  - Preserved LaTeX mathematical formulas ($...$ and $$...$$).
  - GitHub-style callouts/alerts (NOTE, IMPORTANT, WARNING, TIP).
  - Styled responsive tables and code blocks.
  - Universal top navigation return-to-index bar.
  - Automatic link re-mapping (.md -> .html).
"""

import os
import sys
import re
import markdown

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Chronodynamic Relativity Documentation</title>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true
            }},
            svg: {{ fontCache: 'global' }}
        }};
    </script>
    <script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <style>
        :root {{
            --primary: #0f172a;
            --primary-accent: #2563eb;
            --secondary: #0d9488;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --border: #e2e8f0;
            --text-main: #1e293b;
            --text-muted: #64748b;
        }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.7;
        }}
        .cr-top-nav-bar {{
            background: #0f172a;
            color: #ffffff;
            padding: 12px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            position: sticky;
            top: 0;
            z-index: 99999;
        }}
        .cr-nav-return-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #1e293b;
            color: #38bdf8;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9em;
            padding: 7px 16px;
            border-radius: 6px;
            border: 1px solid #334155;
            transition: all 0.2s ease;
        }}
        .cr-nav-return-btn:hover {{
            background: #334155;
            color: #ffffff;
            border-color: #38bdf8;
        }}
        .cr-nav-brand {{
            font-size: 0.95em;
            font-weight: 600;
            color: #94a3b8;
            letter-spacing: 0.5px;
        }}
        .container {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 40px 28px;
            box-sizing: border-box;
        }}
        .content-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 40px 48px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .doc-meta-banner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #f1f5f9;
            border-left: 4px solid var(--primary-accent);
            padding: 12px 18px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 30px;
            font-size: 0.9em;
            color: var(--text-muted);
        }}
        .raw-md-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
            color: var(--primary-accent);
            text-decoration: none;
            background: #ffffff;
            padding: 4px 10px;
            border-radius: 4px;
            border: 1px solid #cbd5e1;
        }}
        .raw-md-btn:hover {{
            background: #e2e8f0;
        }}
        h1 {{
            color: var(--primary);
            font-size: 2.3em;
            border-bottom: 2px solid var(--border);
            padding-bottom: 12px;
            margin-top: 0;
        }}
        h2 {{
            color: #1e3a8a;
            font-size: 1.65em;
            margin-top: 36px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
        }}
        h3 {{
            color: var(--secondary);
            font-size: 1.3em;
            margin-top: 26px;
        }}
        h4 {{
            color: #334155;
            font-size: 1.1em;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 24px 0;
            font-size: 0.92em;
        }}
        th, td {{
            border: 1px solid var(--border);
            padding: 12px 16px;
            text-align: left;
        }}
        th {{
            background-color: #0f172a;
            color: #ffffff;
            font-weight: 600;
        }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        tr:hover {{ background-color: #f1f5f9; }}
        pre {{
            background: #0f172a;
            color: #e2e8f0;
            padding: 16px 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: Consolas, Monaco, 'Courier New', Courier, monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        code {{
            background: #f1f5f9;
            color: #b91c1c;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: Consolas, Monaco, monospace;
            font-size: 0.9em;
        }}
        pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            margin: 20px 0;
            padding: 14px 20px;
            border-left: 4px solid var(--primary-accent);
            background: #f8fafc;
            color: #334155;
            border-radius: 0 8px 8px 0;
        }}
        /* Callout alert boxes */
        .alert {{
            padding: 16px 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 5px solid;
        }}
        .alert-note {{ background: #eff6ff; border-color: #3b82f6; color: #1e40af; }}
        .alert-important {{ background: #faf5ff; border-color: #8b5cf6; color: #5b21b6; }}
        .alert-warning {{ background: #fffbeb; border-color: #f59e0b; color: #92400e; }}
        .alert-tip {{ background: #f0fdf4; border-color: #22c55e; color: #166534; }}
        .footer {{
            text-align: center;
            padding: 30px;
            font-size: 0.85em;
            color: var(--text-muted);
            border-top: 1px solid var(--border);
            margin-top: 50px;
        }}
        @media (max-width: 768px) {{
            .content-card {{ padding: 24px 18px; }}
            .container {{ padding: 20px 12px; }}
        }}
    </style>
</head>
<body>

    <header class="cr-top-nav-bar">
        <a href="{prefix_to_index}index.html" class="cr-nav-return-btn">&larr; Return to Documentation Index</a>
        <span class="cr-nav-brand">Chronodynamic Relativity Research Suite</span>
    </header>

    <div class="container">
        <div class="content-card">
            <div class="doc-meta-banner">
                <div>Canonical Formal Markdown Document &bull; <b>{filename}</b></div>
                <a href="{raw_md_filename}" class="raw-md-btn">&darr; View Raw Markdown Source</a>
            </div>
            {body_html}
        </div>
    </div>

    <div class="footer">
        Chronodynamic Relativity Research Suite &bull; Rigorous Open-Source Theoretical Physics &bull; Rochester Institute of Technology Alumni Research Initiative
    </div>

</body>
</html>
"""

def render_markdown_file(md_path, html_path, prefix_to_index="./"):
    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        md_text = f.read()

    filename = os.path.basename(md_path)
    
    # 1. Extract first heading for title
    m_title = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = m_title.group(1).strip() if m_title else filename.replace('.md', '').replace('_', ' ').title()

    # 2. Protect LaTeX Math blocks from markdown parser mangling
    math_placeholders = []

    def replace_display_math(match):
        idx = len(math_placeholders)
        math_placeholders.append(match.group(0))
        return f"@@CR_MATH_BLOCK_{idx}@@"

    def replace_inline_math(match):
        idx = len(math_placeholders)
        math_placeholders.append(match.group(0))
        return f"@@CR_MATH_INLINE_{idx}@@"

    # Display math $$ ... $$
    protected_text = re.sub(r'\$\$(.*?)\$\$', replace_display_math, md_text, flags=re.DOTALL)
    # Inline math $ ... $ (negative lookbehind/ahead for $$)
    protected_text = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', replace_inline_math, protected_text)

    # 3. Handle GitHub-style blockquote alerts
    # > [!NOTE] ...
    def convert_alerts(text):
        lines = text.split('\n')
        out_lines = []
        in_alert = False
        alert_type = ""
        alert_content = []

        for line in lines:
            m_alert = re.match(r'^>\s*\[!(NOTE|IMPORTANT|WARNING|TIP|CAUTION)\]', line, re.I)
            if m_alert:
                if in_alert:
                    out_lines.append(f'<div class="alert alert-{alert_type.lower()}">' + " ".join(alert_content) + '</div>')
                    alert_content = []
                in_alert = True
                alert_type = m_alert.group(1).lower()
                continue
            elif in_alert and line.startswith('>'):
                alert_content.append(line.lstrip('>').strip())
            else:
                if in_alert:
                    out_lines.append(f'<div class="alert alert-{alert_type.lower()}">' + " ".join(alert_content) + '</div>')
                    in_alert = False
                    alert_type = ""
                    alert_content = []
                out_lines.append(line)

        if in_alert:
            out_lines.append(f'<div class="alert alert-{alert_type.lower()}">' + " ".join(alert_content) + '</div>')

        return '\n'.join(out_lines)

    processed_text = convert_alerts(protected_text)

    # 4. Convert markdown links to .html where appropriate
    # e.g. [Link](SOMETHING.md) -> [Link](SOMETHING.html)
    processed_text = re.sub(r'\]\(([^)]+)\.md\)', r'](\1.html)', processed_text)

    # 5. Compile with Python-Markdown
    md_compiler = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])
    body_html = md_compiler.convert(processed_text)

    # 6. Restore math blocks
    for idx, math_content in enumerate(math_placeholders):
        body_html = body_html.replace(f"@@CR_MATH_BLOCK_{idx}@@", math_content)
        body_html = body_html.replace(f"@@CR_MATH_INLINE_{idx}@@", math_content)

    # 7. Wrap into page template
    final_html = PAGE_TEMPLATE.format(
        title=title,
        filename=filename,
        raw_md_filename=filename,
        prefix_to_index=prefix_to_index,
        body_html=body_html
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"  + Rendered: {filename} -> {os.path.basename(html_path)}")

def render_all_docs_in_directory(docs_dir):
    print(f"\nRendering Markdown files in: {docs_dir}")
    md_files = [
        "MATHEMATICAL_FOUNDATIONS_AND_SYMBOLOGY.md",
        "PARAMETER_DEFINITIONS_AND_APPLICATIONS.md",
        "THEORETICAL_NICHE_AND_OBSERVATIONAL_METHODOLOGY.md",
        "REFERENCES.md",
        "HTML_DOCUMENTATION_REGISTRY.md"
    ]

    for md_name in md_files:
        md_path = os.path.join(docs_dir, md_name)
        if os.path.exists(md_path):
            html_name = md_name.replace('.md', '.html')
            html_path = os.path.join(docs_dir, html_name)
            render_markdown_file(md_path, html_path, prefix_to_index="./")

if __name__ == '__main__':
    targets = [
        os.path.abspath(os.path.join(REPO_ROOT, "official/docs")),
        os.path.abspath(os.path.join(REPO_ROOT, "development/docs")),
        os.path.abspath(os.path.join(REPO_ROOT, "../Chronodynamic-Relativity/docs"))
    ]
    for target in targets:
        if os.path.exists(target):
            render_all_docs_in_directory(target)
