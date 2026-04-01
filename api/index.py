"""Vercel ASGI entrypoint — serves the landing page only.

Self-contained — no dependency on the engram package — so
Vercel only needs starlette in requirements.txt.
"""

from __future__ import annotations

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route


def _render_landing() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Engram — Shared memory for your AI agents</title>
  <meta name="description" content="Give your AI agents shared, persistent memory that detects contradictions. Works with Claude Code, Cursor, Windsurf, Kiro, and any MCP client.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  {_STYLE}
</head>
<body>

  <!-- Ambient background -->
  <div class="bg-glow bg-glow-1" aria-hidden="true"></div>
  <div class="bg-glow bg-glow-2" aria-hidden="true"></div>

  <!-- Nav -->
  <nav class="topnav">
    <div class="topnav-inner">
      <a href="/" class="logo" aria-label="Engram home">
        <svg width="26" height="26" viewBox="0 0 26 26" fill="none" aria-hidden="true">
          <circle cx="13" cy="13" r="11" stroke="url(#lg)" stroke-width="1.5" opacity="0.4"/>
          <circle cx="13" cy="13" r="5.5" fill="url(#lg)" opacity="0.9"/>
          <circle cx="13" cy="13" r="2.5" fill="#080c08"/>
          <defs><linearGradient id="lg" x1="0" y1="0" x2="26" y2="26">
            <stop stop-color="#6ee7b7"/><stop offset="1" stop-color="#059669"/>
          </linearGradient></defs>
        </svg>
        <span>engram</span>
      </a>
      <div class="topnav-links">
        <a href="https://github.com/Agentscreator/Engram" target="_blank" rel="noopener">GitHub</a>
        <a href="#how-it-works">How it works</a>
        <a href="#get-started" class="nav-cta">Get Started</a>
      </div>
    </div>
  </nav>

  <!-- ════════ HERO ════════ -->
  <section class="hero">
    <div class="hero-inner">
      <div class="hero-badge">Open source &middot; Apache 2.0</div>
      <h1>Shared memory for<br>your AI agents</h1>
      <p class="hero-sub">
        One knowledge base for every agent on your team.
        Detects contradictions automatically. Four MCP tools. Zero config.
      </p>

      <!-- Primary CTA — the install box -->
      <div class="hero-cta" id="get-started">
        <div class="terminal">
          <div class="terminal-dots" aria-hidden="true"><i></i><i></i><i></i></div>
          <div class="terminal-body">
            <div class="terminal-line">
              <span class="terminal-prompt">$</span>
              <code id="cmd-pip">pip install engram-mcp &amp;&amp; engram serve --http</code>
              <button class="copy-btn" onclick="copyCmd('cmd-pip')" aria-label="Copy install command">
                <svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 11V3a1 1 0 011-1h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                <span class="copy-feedback">Copy</span>
              </button>
            </div>
            <div class="terminal-divider"></div>
            <div class="terminal-alt">
              <span class="terminal-alt-label">or, no install needed:</span>
              <div class="terminal-line">
                <span class="terminal-prompt">$</span>
                <code id="cmd-uvx">uvx engram-mcp@latest serve --http</code>
                <button class="copy-btn" onclick="copyCmd('cmd-uvx')" aria-label="Copy uvx command">
                  <svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 11V3a1 1 0 011-1h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                  <span class="copy-feedback">Copy</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        <p class="hero-req">Python 3.11+ &middot; Runs on localhost:7474 &middot; No API keys</p>
      </div>
    </div>
  </section>

  <!-- ════════ 3 STEPS ════════ -->
  <section class="section" id="how-it-works">
    <div class="section-inner">
      <h2>Up and running in 3 steps</h2>
      <p class="section-sub">Like Claude Code — install, run, connect. That's it.</p>

      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <div class="step-body">
            <h3>Install</h3>
            <p>One pip install. No Docker, no database setup, no API keys.</p>
            <div class="step-code">
              <code id="s1-cmd">pip install engram-mcp</code>
              <button class="copy-btn copy-sm" onclick="copyCmd('s1-cmd')" aria-label="Copy">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 11V3a1 1 0 011-1h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                <span class="copy-feedback">Copy</span>
              </button>
            </div>
          </div>
        </div>

        <div class="step">
          <div class="step-num">2</div>
          <div class="step-body">
            <h3>Run</h3>
            <p>Start the server. Dashboard at localhost:7474.</p>
            <div class="step-code">
              <code id="s2-cmd">engram serve --http</code>
              <button class="copy-btn copy-sm" onclick="copyCmd('s2-cmd')" aria-label="Copy">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 11V3a1 1 0 011-1h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                <span class="copy-feedback">Copy</span>
              </button>
            </div>
          </div>
        </div>

        <div class="step">
          <div class="step-num">3</div>
          <div class="step-body">
            <h3>Connect</h3>
            <p>Add to your MCP client config. Pick your transport:</p>
            <div class="config-tabs" role="tablist">
              <button class="cfg-tab active" role="tab" aria-selected="true" onclick="cfgTab(event,'cfg-http')">HTTP</button>
              <button class="cfg-tab" role="tab" aria-selected="false" onclick="cfgTab(event,'cfg-stdio')">stdio</button>
            </div>
            <div class="cfg-panel active" id="cfg-http">
              <div class="step-code step-code-block">
                <pre id="cfg-http-code"><code>{{
  "mcpServers": {{
    "engram": {{
      "url": "http://localhost:7474/mcp"
    }}
  }}
}}</code></pre>
                <button class="copy-btn copy-sm copy-block-btn" onclick="copyBlock('cfg-http-code')" aria-label="Copy config">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 11V3a1 1 0 011-1h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                  <span class="copy-feedback">Copy</span>
                </button>
              </div>
            </div>
            <div class="cfg-panel" id="cfg-stdio">
              <div class="step-code step-code-block">
                <pre id="cfg-stdio-code"><code>{{
  "mcpServers": {{
    "engram": {{
      "command": "uvx",
      "args": ["engram-mcp@latest"]
    }}
  }}
}}</code></pre>
                <button class="copy-btn copy-sm copy-block-btn" onclick="copyBlock('cfg-stdio-code')" aria-label="Copy config">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 11V3a1 1 0 011-1h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                  <span class="copy-feedback">Copy</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ════════ TOOLS ════════ -->
  <section class="section section-alt">
    <div class="section-inner">
      <h2>Four tools. That's the entire API.</h2>
      <p class="section-sub">Your agents call them automatically through MCP.</p>
      <div class="tools-grid">
        <div class="tool-card">
          <div class="tool-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M16 16l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
          <h3>engram_query</h3>
          <p>Pull what your team's agents collectively know. Structured facts, ranked by relevance.</p>
        </div>
        <div class="tool-card">
          <div class="tool-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
          <h3>engram_commit</h3>
          <p>Persist a verified discovery. Append-only, timestamped, immediately shared.</p>
        </div>
        <div class="tool-card">
          <div class="tool-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 9v4M12 17h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <h3>engram_conflicts</h3>
          <p>Surface contradictions between facts. Reviewable, resolvable, auditable.</p>
        </div>
        <div class="tool-card">
          <div class="tool-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M9 12l2 2 4-4M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <h3>engram_resolve</h3>
          <p>Settle disagreements. Pick a winner, merge, or dismiss false positives.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ════════ COMPATIBLE CLIENTS ════════ -->
  <section class="section">
    <div class="section-inner">
      <h2>Works everywhere</h2>
      <p class="section-sub">Any MCP-compatible client. No vendor lock-in.</p>
      <div class="clients">
        <div class="client">Claude Code</div>
        <div class="client">Cursor</div>
        <div class="client">Windsurf</div>
        <div class="client">Kiro</div>
        <div class="client">VS Code</div>
        <div class="client">Any MCP Client</div>
      </div>
    </div>
  </section>

  <!-- ════════ FOOTER ════════ -->
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-left">
        <span class="footer-logo">engram</span>
        <span class="footer-tagline">The physical trace a memory leaves in the brain.</span>
      </div>
      <div class="footer-links">
        <a href="https://github.com/Agentscreator/Engram" target="_blank" rel="noopener">GitHub</a>
        <a href="https://github.com/Agentscreator/Engram/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">Contributing</a>
        <a href="https://github.com/Agentscreator/Engram/blob/main/LICENSE" target="_blank" rel="noopener">Apache 2.0</a>
      </div>
    </div>
  </footer>

  <script>
  function copyCmd(id) {{
    const el = document.getElementById(id);
    const text = el.textContent.replace(/&amp;/g, '&');
    navigator.clipboard.writeText(text).then(() => {{
      const fb = el.closest('.terminal-line, .step-code').querySelector('.copy-feedback');
      fb.textContent = 'Copied';
      setTimeout(() => fb.textContent = 'Copy', 2000);
    }});
  }}
  function copyBlock(id) {{
    const el = document.getElementById(id);
    navigator.clipboard.writeText(el.textContent).then(() => {{
      const fb = el.closest('.step-code-block').querySelector('.copy-feedback');
      fb.textContent = 'Copied';
      setTimeout(() => fb.textContent = 'Copy', 2000);
    }});
  }}
  function cfgTab(e, panelId) {{
    document.querySelectorAll('.cfg-tab').forEach(t => {{
      t.classList.remove('active');
      t.setAttribute('aria-selected', 'false');
    }});
    document.querySelectorAll('.cfg-panel').forEach(p => p.classList.remove('active'));
    e.currentTarget.classList.add('active');
    e.currentTarget.setAttribute('aria-selected', 'true');
    document.getElementById(panelId).classList.add('active');
  }}
  </script>
</body>
</html>"""


_STYLE = """
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }

  /* ── Palette ──
     bg:       #060a06  (near-black with green tint)
     surface:  #0c1410  (dark forest)
     border:   rgba(110,231,183,0.08)
     text:     #d4e7d4  (soft sage)
     muted:    #6b8f6b
     accent:   #34d399  (emerald-400)
     accent2:  #059669  (emerald-600)
     highlight:#a7f3d0  (emerald-200, for code)
  */

  body {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #060a06; color: #d4e7d4; line-height: 1.6;
    -webkit-font-smoothing: antialiased; overflow-x: hidden;
  }

  /* Ambient glows */
  .bg-glow {
    position: fixed; border-radius: 50%; pointer-events: none;
    filter: blur(120px); opacity: 0.12; z-index: 0;
  }
  .bg-glow-1 {
    width: 700px; height: 700px; top: -200px; left: -100px;
    background: radial-gradient(circle, #059669, transparent 70%);
  }
  .bg-glow-2 {
    width: 500px; height: 500px; bottom: -100px; right: -80px;
    background: radial-gradient(circle, #065f46, transparent 70%);
  }

  /* ── Nav ── */
  .topnav {
    position: sticky; top: 0; z-index: 100;
    background: rgba(6,10,6,0.85); backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(110,231,183,0.06);
  }
  .topnav-inner {
    max-width: 1060px; margin: 0 auto; padding: 0.7rem 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
  }
  .logo {
    display: flex; align-items: center; gap: 0.5rem;
    text-decoration: none; color: #d4e7d4; font-weight: 700; font-size: 1.05rem;
    letter-spacing: -0.01em;
  }
  .topnav-links { display: flex; align-items: center; gap: 1.5rem; }
  .topnav-links a {
    color: #6b8f6b; text-decoration: none; font-size: 0.85rem;
    font-weight: 500; transition: color 0.15s;
  }
  .topnav-links a:hover { color: #a7f3d0; }
  .nav-cta {
    background: rgba(5,150,105,0.12) !important; color: #34d399 !important;
    border: 1px solid rgba(52,211,153,0.2); border-radius: 8px;
    padding: 0.4rem 1rem; transition: all 0.15s;
  }
  .nav-cta:hover {
    background: rgba(5,150,105,0.22) !important;
    border-color: rgba(52,211,153,0.35);
  }

  /* ── Hero ── */
  .hero {
    position: relative; z-index: 1;
    padding: 5.5rem 1.5rem 3.5rem; text-align: center;
  }
  .hero-inner { max-width: 680px; margin: 0 auto; }
  .hero-badge {
    display: inline-block; padding: 0.25rem 0.85rem; border-radius: 100px;
    background: rgba(5,150,105,0.08); border: 1px solid rgba(52,211,153,0.15);
    color: #6ee7b7; font-size: 0.78rem; font-weight: 500; margin-bottom: 1.75rem;
    letter-spacing: 0.01em;
  }
  .hero h1 {
    font-size: clamp(2.4rem, 5.5vw, 3.6rem); font-weight: 700;
    line-height: 1.12; letter-spacing: -0.035em;
    background: linear-gradient(160deg, #f0fdf4 20%, #6ee7b7 50%, #059669 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .hero-sub {
    margin-top: 1.25rem; font-size: 1.1rem; color: #7da67d;
    max-width: 520px; margin-left: auto; margin-right: auto; line-height: 1.7;
  }

  /* ── Terminal CTA ── */
  .hero-cta { margin-top: 2.5rem; }
  .terminal {
    max-width: 580px; margin: 0 auto;
    background: #0c1410; border: 1px solid rgba(110,231,183,0.1);
    border-radius: 14px; overflow: hidden;
    box-shadow: 0 4px 40px rgba(5,150,105,0.06), 0 0 0 1px rgba(110,231,183,0.04);
  }
  .terminal-dots {
    display: flex; gap: 6px; padding: 0.7rem 1rem;
    border-bottom: 1px solid rgba(110,231,183,0.06);
  }
  .terminal-dots i {
    width: 10px; height: 10px; border-radius: 50%;
    background: rgba(110,231,183,0.12);
  }
  .terminal-dots i:first-child { background: rgba(239,68,68,0.25); }
  .terminal-dots i:nth-child(2) { background: rgba(250,204,21,0.25); }
  .terminal-dots i:last-child { background: rgba(52,211,153,0.25); }
  .terminal-body { padding: 1rem 1.25rem 1.15rem; }
  .terminal-line {
    display: flex; align-items: center; gap: 0.6rem;
  }
  .terminal-prompt {
    color: #34d399; font-family: 'JetBrains Mono', monospace;
    font-weight: 500; font-size: 0.9rem; flex-shrink: 0;
  }
  .terminal-line code {
    font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
    color: #a7f3d0; flex: 1; white-space: nowrap; overflow-x: auto;
  }
  .terminal-divider {
    height: 1px; background: rgba(110,231,183,0.06);
    margin: 0.85rem 0;
  }
  .terminal-alt-label {
    display: block; font-size: 0.72rem; color: #3d5c3d;
    margin-bottom: 0.45rem; letter-spacing: 0.01em;
  }

  .copy-btn {
    display: flex; align-items: center; gap: 0.3rem;
    background: none; border: 1px solid rgba(110,231,183,0.1);
    border-radius: 6px; padding: 0.25rem 0.55rem;
    color: #4a7a4a; cursor: pointer; font-size: 0.7rem;
    font-family: 'DM Sans', sans-serif; font-weight: 500;
    transition: all 0.15s; flex-shrink: 0;
  }
  .copy-btn:hover { color: #a7f3d0; border-color: rgba(110,231,183,0.25); }
  .copy-sm { padding: 0.2rem 0.45rem; font-size: 0.68rem; }

  .hero-req {
    margin-top: 1rem; font-size: 0.78rem; color: #3d5c3d;
    letter-spacing: 0.01em;
  }

  /* ── Sections ── */
  .section { position: relative; z-index: 1; padding: 5rem 1.5rem; }
  .section-alt { background: rgba(110,231,183,0.015); }
  .section-inner { max-width: 960px; margin: 0 auto; }
  .section h2 {
    font-size: 1.65rem; font-weight: 700; text-align: center;
    letter-spacing: -0.02em; color: #ecfdf5;
  }
  .section-sub {
    text-align: center; color: #6b8f6b; margin-top: 0.6rem;
    margin-bottom: 2.75rem; font-size: 0.95rem;
  }

  /* ── Steps ── */
  .steps {
    display: flex; flex-direction: column; gap: 2rem;
    max-width: 600px; margin: 0 auto;
  }
  .step {
    display: flex; gap: 1.25rem; align-items: flex-start;
  }
  .step-num {
    width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    background: rgba(5,150,105,0.1); border: 1px solid rgba(52,211,153,0.2);
    color: #34d399; font-weight: 700; font-size: 0.9rem;
    margin-top: 0.1rem;
  }
  .step-body { flex: 1; }
  .step-body h3 {
    font-size: 1.05rem; font-weight: 600; color: #ecfdf5;
    margin-bottom: 0.25rem;
  }
  .step-body p {
    font-size: 0.88rem; color: #6b8f6b; line-height: 1.6;
    margin-bottom: 0.65rem;
  }
  .step-code {
    display: flex; align-items: center; gap: 0.6rem;
    background: #0c1410; border: 1px solid rgba(110,231,183,0.08);
    border-radius: 10px; padding: 0.6rem 0.9rem;
  }
  .step-code code {
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
    color: #a7f3d0; flex: 1; white-space: nowrap; overflow-x: auto;
  }
  .step-code pre {
    margin: 0; flex: 1; overflow-x: auto;
  }
  .step-code pre code {
    white-space: pre; line-height: 1.6;
  }
  .step-code-block {
    position: relative; align-items: flex-start;
    padding: 0.75rem 0.9rem;
  }
  .copy-block-btn {
    position: absolute; top: 0.6rem; right: 0.6rem;
  }

  /* Config tabs */
  .config-tabs {
    display: flex; gap: 0.2rem; margin-bottom: 0.6rem;
    background: rgba(110,231,183,0.04); border-radius: 8px;
    padding: 0.2rem; width: fit-content;
  }
  .cfg-tab {
    background: none; border: none; color: #4a7a4a;
    padding: 0.35rem 0.9rem; border-radius: 6px; cursor: pointer;
    font-size: 0.8rem; font-weight: 500; transition: all 0.15s;
    font-family: 'DM Sans', sans-serif;
  }
  .cfg-tab.active { background: rgba(5,150,105,0.15); color: #34d399; }
  .cfg-tab:hover:not(.active) { color: #6ee7b7; }
  .cfg-panel { display: none; }
  .cfg-panel.active { display: block; }

  /* ── Tool cards ── */
  .tools-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 0.85rem;
  }
  .tool-card {
    background: rgba(110,231,183,0.02);
    border: 1px solid rgba(110,231,183,0.06);
    border-radius: 14px; padding: 1.4rem;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .tool-card:hover {
    border-color: rgba(52,211,153,0.2);
    box-shadow: 0 0 24px rgba(5,150,105,0.06);
  }
  .tool-icon { color: #34d399; margin-bottom: 0.65rem; }
  .tool-card h3 {
    font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
    color: #6ee7b7; margin-bottom: 0.4rem; font-weight: 500;
  }
  .tool-card p { font-size: 0.82rem; color: #6b8f6b; line-height: 1.6; }

  /* ── Clients ── */
  .clients { display: flex; flex-wrap: wrap; gap: 0.65rem; justify-content: center; }
  .client {
    padding: 0.55rem 1.15rem; border-radius: 10px;
    background: rgba(110,231,183,0.03); border: 1px solid rgba(110,231,183,0.07);
    font-size: 0.85rem; color: #6b8f6b; font-weight: 500;
    transition: border-color 0.15s, color 0.15s;
  }
  .client:hover { border-color: rgba(52,211,153,0.2); color: #a7f3d0; }

  /* ── Footer ── */
  .footer {
    position: relative; z-index: 1;
    border-top: 1px solid rgba(110,231,183,0.06); padding: 2rem 1.5rem;
  }
  .footer-inner {
    max-width: 1060px; margin: 0 auto; display: flex;
    justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 1rem;
  }
  .footer-left { display: flex; align-items: center; gap: 1rem; }
  .footer-logo { font-weight: 700; color: #3d5c3d; letter-spacing: -0.01em; }
  .footer-tagline { font-size: 0.78rem; color: #2a3f2a; font-style: italic; }
  .footer-links { display: flex; gap: 1.25rem; }
  .footer-links a {
    color: #3d5c3d; text-decoration: none; font-size: 0.8rem;
    font-weight: 500; transition: color 0.15s;
  }
  .footer-links a:hover { color: #6ee7b7; }

  /* ── Responsive ── */
  @media (max-width: 640px) {
    .hero { padding: 4rem 1rem 2.5rem; }
    .hero h1 { font-size: 2.1rem; }
    .hero-sub { font-size: 1rem; }
    .terminal-line code { font-size: 0.78rem; }
    .tools-grid { grid-template-columns: 1fr; }
    .topnav-links { gap: 0.75rem; }
    .topnav-links a:not(.nav-cta) { display: none; }
    .footer-inner { flex-direction: column; text-align: center; }
    .footer-left { flex-direction: column; gap: 0.4rem; }
    .step { flex-direction: column; gap: 0.75rem; }
    .step-num { width: 32px; height: 32px; font-size: 0.8rem; }
  }
</style>
"""


def _render_dashboard_placeholder() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dashboard — Engram</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #060a06; color: #d4e7d4; min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      -webkit-font-smoothing: antialiased;
    }
    .card {
      max-width: 480px; text-align: center; padding: 2.5rem 2rem;
      background: rgba(110,231,183,0.02); border: 1px solid rgba(110,231,183,0.08);
      border-radius: 16px;
    }
    h1 { font-size: 1.35rem; font-weight: 700; color: #ecfdf5; margin-bottom: 0.75rem; }
    p { color: #6b8f6b; line-height: 1.7; margin-bottom: 1.25rem; font-size: 0.92rem; }
    .code-box {
      background: #0c1410; border: 1px solid rgba(110,231,183,0.08);
      border-radius: 10px; padding: 1rem 1.25rem; text-align: left; margin-bottom: 1.5rem;
    }
    code { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #a7f3d0; }
    a { color: #34d399; text-decoration: none; font-weight: 500; transition: color 0.15s; }
    a:hover { color: #6ee7b7; }
    .back { margin-top: 0.5rem; font-size: 0.85rem; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Dashboard needs a running server</h1>
    <p>The live dashboard connects to your local Engram instance. Start it up:</p>
    <div class="code-box">
      <code>pip install engram-mcp<br>engram serve --http</code>
    </div>
    <p>Then visit <a href="http://localhost:7474/dashboard">localhost:7474/dashboard</a></p>
    <div class="back"><a href="/">&larr; Back to home</a></div>
  </div>
</body>
</html>"""


async def landing(request: Request) -> HTMLResponse:
    return HTMLResponse(_render_landing())


async def dashboard_placeholder(request: Request) -> HTMLResponse:
    return HTMLResponse(_render_dashboard_placeholder())


app = Starlette(
    routes=[
        Route("/", landing, methods=["GET"]),
        Route("/dashboard", dashboard_placeholder, methods=["GET"]),
        Route("/dashboard/{path:path}", dashboard_placeholder, methods=["GET"]),
    ],
)
