import subprocess
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PANDOC_BIN = r"C:\Program Files\Pandoc\pandoc.exe"
EDGE_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

ACADEMIC_CSS = """
@page {
    size: letter;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 10pt;
    }
}

body {
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #111;
    background: #fff;
    max-width: 100%;
    margin: 0;
    padding: 0;
    text-align: justify;
    text-justify: inter-word;
}

h1:first-of-type {
    text-align: center;
    font-size: 18pt;
    font-weight: bold;
    margin-bottom: 8px;
    line-height: 1.25;
}

p:has(strong:only-child) {
    text-align: center;
}

h1, h2, h3, h4 {
    font-family: "Times New Roman", Times, serif;
    color: #000;
    font-weight: bold;
}

h2 {
    font-size: 13pt;
    border-bottom: 1px solid #333;
    padding-bottom: 3px;
    margin-top: 22px;
    margin-bottom: 10px;
}

h3 {
    font-size: 11.5pt;
    margin-top: 14px;
    margin-bottom: 6px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 9.5pt;
}

table, th, td {
    border: none;
}

thead tr {
    border-top: 2px solid #000;
    border-bottom: 1.5px solid #000;
}

tbody tr:last-child {
    border-bottom: 2px solid #000;
}

th, td {
    padding: 5px 8px;
    text-align: left;
}

th {
    font-weight: bold;
}

code, pre {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 9pt;
}

pre {
    background-color: #f7f7f9;
    border: 1px solid #e1e1e8;
    border-radius: 3px;
    padding: 10px 14px;
    overflow-x: auto;
    line-height: 1.4;
    white-space: pre-wrap;
    word-break: break-all;
}

p code {
    background-color: #f3f3f5;
    padding: 1px 4px;
    border-radius: 2px;
    border: 1px solid #e5e5e8;
}

blockquote {
    border-left: 3px solid #888;
    margin: 12px 0;
    padding-left: 14px;
    font-style: italic;
    color: #333;
}

hr {
    border: none;
    border-top: 1px solid #bbb;
    margin: 20px 0;
}

.katex {
    font-size: 1.05em !important;
}
"""

def generate():
    paper_md = BASE_DIR / "PAPER.md"
    temp_html = BASE_DIR / "temp_preprint.html"
    output_pdf = BASE_DIR / "cloud_sort_paper.pdf"

    # Step 1: Run Pandoc to generate KaTeX HTML
    cmd_pandoc = [
        PANDOC_BIN,
        str(paper_md),
        "-s",
        "--katex",
        "--metadata", "title=Cloud Sort: An Overhead Caller-Buffer Merge Paradigm",
        "-o", str(temp_html)
    ]
    subprocess.run(cmd_pandoc, check=True)

    # Step 2: Inject Academic CSS
    html_content = temp_html.read_text(encoding="utf-8")
    injected_html = html_content.replace(
        "</head>",
        f"<style>{ACADEMIC_CSS}</style>\n</head>"
    )
    temp_html.write_text(injected_html, encoding="utf-8")

    # Step 3: Run Edge Headless to render PDF
    file_url = temp_html.as_uri()
    cmd_edge = [
        EDGE_BIN,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf}",
        file_url
    ]
    subprocess.run(cmd_edge, check=True)

    # Cleanup temp HTML
    if temp_html.exists():
        temp_html.unlink()

    print(f"SUCCESS: Generated {output_pdf} ({output_pdf.stat().st_size} bytes)")

if __name__ == "__main__":
    generate()
