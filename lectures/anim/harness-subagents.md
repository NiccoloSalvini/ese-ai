```{=html}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 440" width="95%" style="max-height:520px;display:block;margin:0 auto" font-family="'Source Sans 3','Source Sans Pro',-apple-system,Helvetica,Arial,sans-serif">
  <rect width="960" height="440" fill="#ffffff"/>
  <text x="30" y="34" font-size="13" fill="#7a7f85">one conversation becomes several &#8212; each with its own window, and only a summary comes back</text>
  <defs>
    <marker id="sa-ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#a8955a"/></marker>
  </defs>

  <!-- orchestrator: always visible -->
  <rect x="40" y="70" width="250" height="280" rx="3" fill="#eaf1f7" stroke="#2471a3" stroke-width="2"/>
  <text x="165" y="104" font-size="17" font-weight="700" fill="#2471a3" text-anchor="middle">the orchestrator</text>
  <text x="165" y="124" font-size="12" fill="#2471a3" text-anchor="middle">the agent you are talking to</text>
  <rect x="60" y="150" width="210" height="100" rx="3" fill="#fcfbf8" stroke="#c9c4b8"/>
  <text x="165" y="176" font-size="13" font-weight="700" fill="#363636" text-anchor="middle">its context window</text>
  <text x="165" y="200" font-size="12" fill="#363636" text-anchor="middle" font-family="'JetBrains Mono',Menlo,monospace">your request</text>
  <text x="165" y="218" font-size="12" fill="#363636" text-anchor="middle" font-family="'JetBrains Mono',Menlo,monospace">the plan</text>
  <text x="165" y="290" font-size="12" fill="#7a7f85" text-anchor="middle">small, and it stays small</text>
  <text x="165" y="308" font-size="12" fill="#7a7f85" text-anchor="middle">it reads only what comes back</text>

  <!-- 1: brief 1 + subagent 1 -->
  <g class="fragment" data-fragment-index="1">
    <path d="M294 150 L604 90" fill="none" stroke="#a8955a" stroke-width="2" marker-end="url(#sa-ag)"/>
    <rect x="400" y="96" width="104" height="18" fill="#ffffff"/>
    <text x="452" y="109" font-size="12" font-weight="700" fill="#363636" text-anchor="middle">a brief &#8594;</text>
    <rect x="610" y="60" width="300" height="88" rx="3" fill="#faeeee" stroke="#AF1F25" stroke-width="2"/>
    <text x="624" y="82" font-size="14" font-weight="700" fill="#AF1F25">subagent 1 &#8212; read the codebase</text>
    <rect x="624" y="92" width="272" height="44" rx="3" fill="#fcfbf8" stroke="#c9c4b8"/>
    <text x="634" y="109" font-size="11" font-weight="700" fill="#363636">own context window</text>
    <text x="634" y="126" font-size="11" fill="#363636" font-family="'JetBrains Mono',Menlo,monospace">brief &#183; 40 files read &#183; 2,000 lines out</text>
  </g>

  <!-- 2: summary 1 -->
  <g class="fragment" data-fragment-index="2">
    <path d="M604 130 L294 172" fill="none" stroke="#a8955a" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#sa-ag)"/>
    <rect x="384" y="146" width="140" height="18" fill="#ffffff"/>
    <text x="454" y="159" font-size="12" fill="#7a7f85" text-anchor="middle">&#8592; a summary (200 words)</text>
  </g>

  <!-- 3: brief 2 + subagent 2 -->
  <g class="fragment" data-fragment-index="3">
    <path d="M294 200 L604 196" fill="none" stroke="#a8955a" stroke-width="2" marker-end="url(#sa-ag)"/>
    <rect x="400" y="180" width="104" height="18" fill="#ffffff"/>
    <text x="452" y="193" font-size="12" font-weight="700" fill="#363636" text-anchor="middle">a brief &#8594;</text>
    <rect x="610" y="166" width="300" height="88" rx="3" fill="#faeeee" stroke="#AF1F25" stroke-width="2"/>
    <text x="624" y="188" font-size="14" font-weight="700" fill="#AF1F25">subagent 2 &#8212; write the tests</text>
    <rect x="624" y="198" width="272" height="44" rx="3" fill="#fcfbf8" stroke="#c9c4b8"/>
    <text x="634" y="215" font-size="11" font-weight="700" fill="#363636">own context window</text>
    <text x="634" y="232" font-size="11" fill="#363636" font-family="'JetBrains Mono',Menlo,monospace">brief &#183; 12 files written &#183; 30 test runs</text>
  </g>

  <!-- 4: summary 2 -->
  <g class="fragment" data-fragment-index="4">
    <path d="M604 226 L294 222" fill="none" stroke="#a8955a" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#sa-ag)"/>
    <rect x="384" y="214" width="140" height="18" fill="#ffffff"/>
    <text x="454" y="227" font-size="12" fill="#7a7f85" text-anchor="middle">&#8592; a summary (200 words)</text>
  </g>

  <!-- 5: brief 3 + subagent 3 -->
  <g class="fragment" data-fragment-index="5">
    <path d="M294 250 L604 302" fill="none" stroke="#a8955a" stroke-width="2" marker-end="url(#sa-ag)"/>
    <rect x="400" y="264" width="104" height="18" fill="#ffffff"/>
    <text x="452" y="277" font-size="12" font-weight="700" fill="#363636" text-anchor="middle">a brief &#8594;</text>
    <rect x="610" y="272" width="300" height="88" rx="3" fill="#faeeee" stroke="#AF1F25" stroke-width="2"/>
    <text x="624" y="294" font-size="14" font-weight="700" fill="#AF1F25">subagent 3 &#8212; check the deploy</text>
    <rect x="624" y="304" width="272" height="44" rx="3" fill="#fcfbf8" stroke="#c9c4b8"/>
    <text x="634" y="321" font-size="11" font-weight="700" fill="#363636">own context window</text>
    <text x="634" y="338" font-size="11" fill="#363636" font-family="'JetBrains Mono',Menlo,monospace">brief &#183; 300 log lines &#183; 1 failure found</text>
  </g>

  <!-- 6: summary 3 + "3 summaries" lands in the parent's window -->
  <g class="fragment" data-fragment-index="6">
    <path d="M604 342 L294 272" fill="none" stroke="#a8955a" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#sa-ag)"/>
    <rect x="384" y="300" width="140" height="18" fill="#ffffff"/>
    <text x="454" y="313" font-size="12" fill="#7a7f85" text-anchor="middle">&#8592; a summary (200 words)</text>
    <text x="165" y="236" font-size="12" fill="#363636" text-anchor="middle" font-family="'JetBrains Mono',Menlo,monospace">3 summaries</text>
  </g>

  <!-- 7: the point -->
  <g class="fragment" data-fragment-index="7">
    <line x1="40" y1="382" x2="910" y2="382" stroke="#e6e2d8"/>
    <text x="40" y="408" font-size="14" font-weight="700" fill="#AF1F25">the parent never sees the 40 files &#8212; that is the point, and the risk</text>
    <text x="40" y="428" font-size="13" fill="#7a7f85">cheaper and cleaner context for the parent; whatever the subagent missed, nobody saw</text>
  </g>
</svg>
```
