"""
make_profile_card.py

Generates profile-card.svg: the wide, two-column terminal-styled card
(header, impact strip, previously/education/languages on the left,
stack+tools/projects on the right, footer).

IMPORTANT: unlike make_info_card.py in the old design, this layout uses
hand-tuned pixel widths for the pill badges and column boundaries because
GitHub's SVG renderer doesn't have "Inter"/"Menlo" installed and falls back
to a substitute font (DejaVu Sans / DejaVu Sans Mono) with different
character widths. If you change any text below:
  1. Re-run this script
  2. Render it locally (rsvg-convert -b '#0d1117' profile-card.svg -o preview.png)
  3. Check nothing overflows its column before committing

Usage:
    python scripts/make_profile_card.py

Writes: profile-card.svg
"""

OUTPUT_SVG = "profile-card.svg"

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 730" width="1000" height="730">
  <rect x="1" y="1" width="998" height="728" rx="10" fill="#0a0e14" stroke="#1f2937" stroke-width="1"/>

  <!-- Terminal chrome -->
  <circle cx="28" cy="26" r="5.5" fill="#ff5f56"/>
  <circle cx="46" cy="26" r="5.5" fill="#ffbd2e"/>
  <circle cx="64" cy="26" r="5.5" fill="#27c93f"/>
  <text x="88" y="31" font-family="Menlo, Consolas, monospace" font-size="12.5" fill="#6e7681">lalithyaraochavala@github ~ $ whoami</text>
  <line x1="0" y1="46" x2="1000" y2="46" stroke="#1f2937"/>

  <!-- Name + tagline -->
  <text x="40" y="78" font-family="Menlo, Consolas, monospace" font-size="20" font-weight="700" fill="#e6edf3">Lalithya Rao Chavala</text>
  <text x="40" y="98" font-family="Menlo, Consolas, monospace" font-size="13" fill="#3fb950"># I help companies build better with AI.</text>

  <line x1="40" y1="120" x2="960" y2="120" stroke="#1f2937"/>

  <!-- Impact strip -->
  <text x="40" y="172" font-family="Menlo, Consolas, monospace" font-size="30" font-weight="700" fill="#3fb950">4M+</text>
  <text x="40" y="194" font-family="Menlo, Consolas, monospace" font-size="11" fill="#e6edf3">impressions</text>
  <text x="40" y="210" font-family="Menlo, Consolas, monospace" font-size="10.5" fill="#6e7681">8 markets · AEO/SEO</text>

  <line x1="360" y1="134" x2="360" y2="218" stroke="#1f2937"/>

  <text x="390" y="172" font-family="Menlo, Consolas, monospace" font-size="30" font-weight="700" fill="#3fb950">53K+</text>
  <text x="390" y="194" font-family="Menlo, Consolas, monospace" font-size="11" fill="#e6edf3">chatbot messages</text>
  <text x="390" y="210" font-family="Menlo, Consolas, monospace" font-size="10.5" fill="#6e7681">100% uptime SLO · RAG</text>

  <line x1="710" y1="134" x2="710" y2="218" stroke="#1f2937"/>

  <text x="740" y="172" font-family="Menlo, Consolas, monospace" font-size="30" font-weight="700" fill="#3fb950">10K+</text>
  <text x="740" y="194" font-family="Menlo, Consolas, monospace" font-size="11" fill="#e6edf3">KB articles migrated</text>
  <text x="740" y="210" font-family="Menlo, Consolas, monospace" font-size="10.5" fill="#6e7681">ITIL-governed rollout</text>

  <line x1="40" y1="238" x2="960" y2="238" stroke="#1f2937"/>

  <!-- Column divider -->
  <line x1="530" y1="250" x2="530" y2="600" stroke="#161b22"/>

  <!-- LEFT COLUMN -->
  <text x="40" y="268" font-family="Menlo, Consolas, monospace" font-size="10" font-weight="700" letter-spacing="1.2" fill="#3fb950">PREVIOUSLY</text>

  <text x="40" y="290" font-family="Menlo, Consolas, monospace" font-size="13" font-weight="700" fill="#e6edf3">Senior AI Analyst, Innovation &amp; AI Pod</text>
  <text x="40" y="306" font-family="Menlo, Consolas, monospace" font-size="12" fill="#6e7681">@ MPOWER Financing (2024–2026)</text>
  <text x="40" y="328" font-family="Menlo, Consolas, monospace" font-size="12" fill="#b6bec9">📰  500+ articles · 8 markets · 7 languages</text>
  <text x="40" y="348" font-family="Menlo, Consolas, monospace" font-size="12" fill="#b6bec9">🌐  3 live satellite websites — zero eng. dependency</text>
  <text x="40" y="368" font-family="Menlo, Consolas, monospace" font-size="12" fill="#b6bec9">📱  5 WhatsApp Business API channels — sole POC</text>
  <text x="40" y="388" font-family="Menlo, Consolas, monospace" font-size="12" fill="#b6bec9">🔄  GPT-4.0→4.1 model upgrade — zero-downtime</text>

  <text x="40" y="420" font-family="Menlo, Consolas, monospace" font-size="13" font-weight="700" fill="#e6edf3">Knowledge &amp; IT Analyst</text>
  <text x="40" y="436" font-family="Menlo, Consolas, monospace" font-size="12" fill="#6e7681">@ Morgan Stanley (2021–2023)</text>
  <text x="40" y="456" font-family="Menlo, Consolas, monospace" font-size="12" fill="#b6bec9">30% ticket reduction · 98% CSAT · 200+ agents trained</text>

  <text x="40" y="488" font-family="Menlo, Consolas, monospace" font-size="10" font-weight="700" letter-spacing="1.2" fill="#3fb950">EDUCATION</text>
  <text x="40" y="510" font-family="Menlo, Consolas, monospace" font-size="12" fill="#b6bec9">MBA, HR Management — Andhra University (First Class, 2024)</text>
  <text x="40" y="528" font-family="Menlo, Consolas, monospace" font-size="12" fill="#b6bec9">B.Tech, ECE — KL University (Silver Medalist · GPA 9.49/10, 2021)</text>

  <text x="40" y="560" font-family="Menlo, Consolas, monospace" font-size="10" font-weight="700" letter-spacing="1.2" fill="#3fb950">LANGUAGES</text>
  <text x="40" y="582" font-family="Menlo, Consolas, monospace" font-size="11.5" fill="#b6bec9">English, Hindi (fluent) · Telugu (native) · Tamil, Kannada (working)</text>

  <!-- RIGHT COLUMN -->
  <text x="560" y="268" font-family="Menlo, Consolas, monospace" font-size="10" font-weight="700" letter-spacing="1.2" fill="#3fb950">STACK &amp; TOOLS</text>

  <text x="560" y="292" font-family="Menlo, Consolas, monospace" font-size="9.5" font-weight="700" letter-spacing="0.8" fill="#3fb950">CORE</text>
  <g font-family="Menlo, Consolas, monospace" font-size="11" font-weight="600">
    <rect x="560" y="300" width="62" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="591" y="315" fill="#7ee2a8" text-anchor="middle">Python</text>
    <rect x="630" y="300" width="68" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="664" y="315" fill="#7ee2a8" text-anchor="middle">FastAPI</text>
    <rect x="706" y="300" width="68" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="740" y="315" fill="#7ee2a8" text-anchor="middle">Next.js</text>
    <rect x="782" y="300" width="88" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="826" y="315" fill="#7ee2a8" text-anchor="middle">TypeScript</text>

    <rect x="560" y="330" width="88" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="604" y="345" fill="#7ee2a8" text-anchor="middle">Claude API</text>
    <rect x="656" y="330" width="68" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="690" y="345" fill="#7ee2a8" text-anchor="middle">GPT-4.1</text>
    <rect x="732" y="330" width="42" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="753" y="345" fill="#7ee2a8" text-anchor="middle">RAG</text>
    <rect x="782" y="330" width="42" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="803" y="345" fill="#7ee2a8" text-anchor="middle">n8n</text>
    <rect x="832" y="330" width="82" height="22" rx="11" fill="#0d2818" stroke="#3fb950" stroke-width="1"/>
    <text x="873" y="345" fill="#7ee2a8" text-anchor="middle">Yellow.ai</text>
  </g>

  <text x="560" y="384" font-family="Menlo, Consolas, monospace" font-size="9.5" font-weight="700" letter-spacing="0.8" fill="#3fb950">TOOLS</text>
  <g font-family="Menlo, Consolas, monospace" font-size="11" font-weight="600">
    <rect x="560" y="392" width="49" height="22" rx="11" fill="#161b22" stroke="#3a4150" stroke-width="1"/>
    <text x="584" y="407" fill="#9aa4b5" text-anchor="middle">Jira</text>
    <rect x="617" y="392" width="88" height="22" rx="11" fill="#161b22" stroke="#3a4150" stroke-width="1"/>
    <text x="661" y="407" fill="#9aa4b5" text-anchor="middle">Confluence</text>
    <rect x="713" y="392" width="62" height="22" rx="11" fill="#161b22" stroke="#3a4150" stroke-width="1"/>
    <text x="744" y="407" fill="#9aa4b5" text-anchor="middle">Notion</text>
    <rect x="783" y="392" width="161" height="22" rx="11" fill="#161b22" stroke="#3a4150" stroke-width="1"/>
    <text x="863" y="407" fill="#9aa4b5" text-anchor="middle">Google Search Console</text>

    <rect x="560" y="422" width="62" height="22" rx="11" fill="#161b22" stroke="#3a4150" stroke-width="1"/>
    <text x="591" y="437" fill="#9aa4b5" text-anchor="middle">Ahrefs</text>
    <rect x="630" y="422" width="68" height="22" rx="11" fill="#161b22" stroke="#3a4150" stroke-width="1"/>
    <text x="664" y="437" fill="#9aa4b5" text-anchor="middle">SEMrush</text>
    <rect x="706" y="422" width="55" height="22" rx="11" fill="#161b22" stroke="#3a4150" stroke-width="1"/>
    <text x="733" y="437" fill="#9aa4b5" text-anchor="middle">Figma</text>
  </g>

  <text x="560" y="476" font-family="Menlo, Consolas, monospace" font-size="10" font-weight="700" letter-spacing="1.2" fill="#3fb950">PROJECTS</text>

  <text x="560" y="498" font-family="Menlo, Consolas, monospace" font-size="12" font-weight="700" fill="#e6edf3">🔧  aeo-product-ops-system</text>
  <text x="580" y="514" font-family="Menlo, Consolas, monospace" font-size="11" fill="#6e7681">5-agent AI system for AI-search visibility</text>

  <text x="560" y="536" font-family="Menlo, Consolas, monospace" font-size="12" font-weight="700" fill="#e6edf3">🗺  route-merge-optimizer</text>
  <text x="580" y="552" font-family="Menlo, Consolas, monospace" font-size="11" fill="#6e7681">logistics optimization, real Amazon geodata</text>

  <text x="560" y="574" font-family="Menlo, Consolas, monospace" font-size="12" font-weight="700" fill="#e6edf3">📊  dynamo-mvp</text>
  <text x="580" y="590" font-family="Menlo, Consolas, monospace" font-size="11" fill="#6e7681">weather-driven ad engine, live on Railway</text>

  <!-- Footer -->
  <line x1="40" y1="622" x2="960" y2="622" stroke="#1f2937"/>
  <text x="40" y="654" font-family="Menlo, Consolas, monospace" font-size="12.5" fill="#b6bec9">Bangalore, India · open to remote &amp; relocation (India) · immediate joiner</text>
  <text x="40" y="678" font-family="Menlo, Consolas, monospace" font-size="12.5" fill="#3fb950">LinkedIn: in/lalithyarao   ·   Portfolio: lalithyarao.vercel.app</text>
</svg>
'''


def main():
    with open(OUTPUT_SVG, "w") as f:
        f.write(SVG)
    print(f"Wrote {OUTPUT_SVG}")


if __name__ == "__main__":
    main()
