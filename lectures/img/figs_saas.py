"""Diagrams for the companion deck 'Anatomy of a SaaS' (lectures/03b-anatomy-of-a-saas.qmd).
Pure box-and-arrow figures, same visual language as agent-loop.svg. Run: python figs_saas.py"""
from pathlib import Path

HERE = Path(__file__).parent
RED, GOLD, GOLDDK, NAVY, GREEN, INK, MUTED, RULE = (
    "#AF1F25", "#CDBA80", "#a8955a", "#2471a3", "#1e8449", "#363636", "#7a7f85", "#e6e2d8")
NAVY_BG, RED_BG, PAPER, PAPER_LN = "#eaf1f7", "#faeeee", "#fcfbf8", "#c9c4b8"
FONT = "font-family=\"'Source Sans 3','Source Sans Pro',-apple-system,Helvetica,Arial,sans-serif\""
MONO = "font-family=\"'JetBrains Mono',Menlo,monospace\""
DEFS = f'''  <defs>
    <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{GOLDDK}"/></marker>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker>
    <marker id="an" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker>
  </defs>'''


def svg(name, h, body, sub, w=960):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>',
         f'  <rect width="{w}" height="{h}" fill="#ffffff"/>', DEFS,
         f'  <text x="30" y="34" font-size="13" fill="{MUTED}">{sub}</text>'] + body + ['</svg>']
    (HERE / name).write_text("\n".join(s), encoding="utf-8")
    print("wrote", name)


def t(x, y, s, size=13, fill=INK, weight="400", anchor="middle", mono=False, ls=None):
    extra = (" " + MONO if mono else "") + (f' letter-spacing="{ls}"' if ls else "")
    return f'  <text x="{x:.0f}" y="{y:.0f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>{s}</text>'


def box(x, y, w, h, title, lines=(), kind="write", title_size=16):
    """kind: write (navy, you build it) · rent (paper, you rent it) · danger (red) · plain."""
    fill, stroke, col, sw = {"write": (NAVY_BG, NAVY, NAVY, 2), "rent": (PAPER, PAPER_LN, INK, 1),
                             "danger": (RED_BG, RED, RED, 2), "plain": ("#ffffff", PAPER_LN, INK, 1)}[kind]
    out = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    n = len(lines)
    ty = y + h / 2 - (n * 17) / 2 + 5
    if kind == "rent":
        out.append(t(x + w / 2, ty, title.upper(), 12, GOLDDK, "700", ls="1.1"))
    else:
        out.append(t(x + w / 2, ty, title, title_size, col, "700"))
    for i, ln in enumerate(lines):
        out.append(t(x + w / 2, ty + 20 + i * 17, ln, 12, col if kind != "rent" else INK))
    return out


def arrow(x1, y1, x2, y2, col="g", w=2, dash=None):
    c = {"g": GOLDDK, "r": RED, "n": NAVY}[col]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="url(#a{col})"{d}/>'


def path(d, col="g", w=2, dash=None, end=True):
    c = {"g": GOLDDK, "r": RED, "n": NAVY}[col]
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    me = f' marker-end="url(#a{col})"' if end else ""
    return f'  <path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{dd}{me}/>'


# ------------------------------------------------------------------ 1. the map
def anatomy(named=False):
    N = (lambda generic, name: name if named else generic)
    B = []
    B += [t(150, 72, "THE USER’S BROWSER", 11, MUTED, "700", ls="1.1"), t(480, 72, "YOUR SERVER", 11, MUTED, "700", ls="1.1"),
          t(810, 72, "YOUR DATA", 11, MUTED, "700", ls="1.1")]
    B += box(40, 84, 220, 96, "frontend", [N("what the user sees and clicks", "Next.js on Vercel"),
                                           N("pages, forms, buttons", "sign-up · watchlist · billing")])
    B += box(370, 84, 220, 96, "backend", [N("the logic and the secrets", "Python job in Docker, Cloud Run"),
                                          N("calls everything else", "+ API routes on Vercel")])
    B += box(700, 84, 220, 96, "database", [N("the ledger: who, what, when", "Postgres on Supabase"),
                                           N("tables of rows", "users · watchlists · alerts")])
    B += [arrow(262, 120, 366, 120), arrow(366, 146, 262, 146),
          t(314, 110, "requests", 12, INK), t(314, 166, "answers", 12, MUTED),
          arrow(592, 120, 696, 120), arrow(696, 146, 592, 146),
          t(644, 110, "queries", 12, INK), t(644, 166, "rows", 12, MUTED)]
    rent = [("auth", N("who are you?", "Supabase Auth")), ("payments", N("who has paid?", "Stripe")),
            ("email", N("send the alert", "Resend")), ("LLM provider", N("write the paragraph", "Claude API")),
            ("scheduler", N("every Monday, 7:00", "Supabase Cron"))]
    for i, (ttl, sub) in enumerate(rent):
        x = 40 + i * 180
        B += box(x, 280, 160, 70, ttl, [sub], "rent")
        B.append(path(f"M480 182 L480 225 L{x + 80} 225 L{x + 80} 274", "g", 1.5))
    B.append(path("M70 182 L70 274", "g", 1.5, "4 3"))
    B.append(t(30, 400, "Blue: you design it and it holds your logic. Grey: you rent it — someone else built it, runs it, and is better at it than you.", 14, INK, anchor="start"))
    B.append(t(30, 422, "The dashed line: signing in happens in the browser, against the auth service; the backend only checks the result.", 13, MUTED, anchor="start"))
    name = "saas-volalert.svg" if named else "saas-anatomy.svg"
    sub = "VolAlert, with a name on every box — one reasonable choice among many" if named else "every SaaS, from a to-do app to a bank, is these parts wired together"
    svg(name, 440, B, sub)


# ------------------------------------------------------------------ 2. two journeys
def journeys():
    B = []

    def lane(y, title, steps, col):
        out = [t(30, y - 14, title, 15, col, "700", anchor="start")]
        n = len(steps); w = (900 - (n - 1) * 26) / n
        for i, (a, b) in enumerate(steps):
            x = 30 + i * (w + 26)
            out += box(int(x), y, int(w), 74, a, [b], "plain", 14)
            if i < n - 1:
                out.append(arrow(int(x + w + 2), y + 37, int(x + w + 24), y + 37))
            out.append(t(x + 14, y + 16, str(i + 1), 11, GOLDDK, "700"))
        return out

    B += lane(80, "Daytime: Danila adds Solana to his watchlist", [
        ("browser", "he clicks “add SOL”"), ("frontend", "sends the request"), ("backend", "is the login valid?"),
        ("database", "insert one row"), ("frontend", "“SOL added” ✓")], NAVY)
    B += lane(250, "Monday 07:00: nobody clicks anything", [
        ("scheduler", "wakes the job"), ("backend", "fetch prices"), ("your model", "rule or forest"),
        ("LLM provider", "write two lines"), ("email", "send to 1,200 users")], RED)
    B.append(t(30, 380, "Most of a SaaS’s work happens with no user on the page: jobs, schedules, webhooks. Week 5’s agents live here too.", 14, INK, anchor="start"))
    svg("saas-journeys.svg", 400, B, "the same system, two moments")


# ------------------------------------------------------------------ 3. where the keys live
def secrets():
    B = [f'  <line x1="480" y1="60" x2="480" y2="330" stroke="{RED}" stroke-width="3"/>',
         t(480, 54, "the wall", 13, RED, "700"),
         t(255, 82, "THE BROWSER — PUBLIC", 12, MUTED, "700", ls="1.1"),
         t(705, 82, "THE SERVER — PRIVATE", 12, MUTED, "700", ls="1.1")]
    left = [("page code, labels, buttons", "anyone can read it: right-click ▸ Inspect"),
            ("the database’s public key", "public by design — safe only if every row is checked (RLS)"),
            ("the user’s login token", "proves who they are; expires")]
    right = [("the LLM key", "pays for every token"), ("the Stripe secret key", "can refund, can charge"),
             ("the database admin key", "bypasses every rule")]
    for i, (a, b) in enumerate(left):
        B += box(40, 100 + i * 74, 410, 62, a, [b], "plain", 14)
    for i, (a, b) in enumerate(right):
        B += box(510, 100 + i * 74, 410, 62, a, [b], "danger", 14)
    B += [t(30, 370, "The browser asks; the server calls with the key. A key in the frontend is a key on the internet —", 14, INK, anchor="start"),
          t(30, 392, "the same rule as this morning’s getpass box, and the first thing to check in any app an AI built for you.", 14, INK, anchor="start")]
    svg("saas-secrets.svg", 410, B, "what each side may hold")


# ------------------------------------------------------------------ 4. Supabase, opened
def supabase():
    B = [f'  <rect x="30" y="56" width="560" height="320" rx="3" fill="#ffffff" stroke="{GREEN}" stroke-width="2"/>',
         t(310, 80, "ONE SUPABASE PROJECT", 12, GREEN, "700", ls="1.1")]
    tiles = [("Postgres database", "your tables, plain SQL", "write"), ("Auth", "sign-up, login, Google, MFA", "rent"),
             ("Row-level security", "the database checks every row", "danger"), ("Storage", "files: PDFs, images", "rent"),
             ("Edge Functions", "small pieces of backend code", "write"), ("Cron + vectors", "schedules · embeddings for RAG", "rent")]
    for i, (a, b, k) in enumerate(tiles):
        x = 50 + (i % 2) * 270; y = 96 + (i // 2) * 92
        B += box(x, y, 250, 76, a, [b], k if k != "rent" else "plain", 15)
    alts = [("Postgres elsewhere", "Neon · AWS RDS · Google Cloud SQL"), ("Auth elsewhere", "Clerk · Auth0 · Firebase Auth"),
            ("Storage elsewhere", "AWS S3 · Cloudflare R2"), ("Functions elsewhere", "AWS Lambda · Cloud Run · Vercel"),
            ("All of it, from Google", "Firebase")]
    B.append(t(780, 80, "THE SAME, BOUGHT SEPARATELY", 12, MUTED, "700", ls="1.1"))
    for i, (a, b) in enumerate(alts):
        y = 96 + i * 56
        B += [t(630, y + 18, a, 14, INK, "700", anchor="start"), t(630, y + 36, b, 13, MUTED, anchor="start")]
    B += [t(30, 404, "A backend in a box: one bill, one dashboard, sensible defaults. The price is that your data model is now tied to it —", 14, INK, anchor="start"),
          t(30, 426, "plain Postgres underneath, so leaving is possible; easy, it is not.", 14, INK, anchor="start")]
    svg("saas-supabase.svg", 440, B, "why so many AI-built apps start here")


# ------------------------------------------------------------------ 5. Docker
def docker():
    def container(x, y, label):
        out = [f'  <rect x="{x}" y="{y}" width="260" height="190" rx="3" fill="{NAVY_BG}" stroke="{NAVY}" stroke-width="2"/>',
               t(x + 130, y + 24, "CONTAINER", 12, NAVY, "700", ls="1.1")]
        for i, (a, b) in enumerate([("your code", "volalert/job.py"), ("the language", "Python 3.12"),
                                    ("the libraries", "pandas · sklearn"), ("the settings", "PRICES_URL")]):
            yy = y + 40 + i * 36
            out += [f'  <rect x="{x+14}" y="{yy}" width="232" height="30" fill="#ffffff" stroke="{PAPER_LN}"/>',
                    t(x + 24, yy + 20, a, 13, INK, "700", anchor="start"), t(x + 236, yy + 20, b, 12, MUTED, anchor="end", mono=True)]
        out.append(t(x + 130, y + 214, label, 14, INK, "700"))
        return out
    B = []
    B += container(40, 70, "your laptop")
    B += container(660, 70, "a server in Frankfurt")
    B += [arrow(312, 140, 646, 140, "g", 2.5), t(479, 128, "the same box, byte for byte", 14, INK, "700"),
          t(479, 162, "docker build → push → run", 13, MUTED, mono=True)]
    B += box(360, 200, 240, 66, "image vs container", ["image: the frozen box", "container: a running copy"], "plain", 14)
    B += [t(30, 340, "“It works on my machine” — so ship the machine. Docker packs your code with everything it needs to run,", 14, INK, anchor="start"),
          t(30, 362, "and any cloud can run the box without knowing what is inside. Most platforms on the next slide take one.", 14, INK, anchor="start")]
    svg("saas-docker.svg", 380, B, "a shipping container for software")


# ------------------------------------------------------------------ 6. where it runs
def ladder():
    steps = [("a virtual machine", "you rent a computer", ["you manage: system, updates,", "security, scaling, backups"],
              "AWS EC2 · Google Compute Engine · Azure VMs · Hetzner"),
             ("a container platform", "you hand over a Docker image", ["it manages the machines;", "you manage the box"],
              "Google Cloud Run · Fly.io · Render · Railway · AWS ECS"),
             ("a serverless platform", "you hand over code", ["it builds, runs, scales to zero;", "you manage only the code"],
              "Vercel · Netlify · AWS Lambda · Supabase Edge Functions")]
    B = []
    for i, (a, b, c, ex) in enumerate(steps):
        x = 40 + i * 300; y = 210 - i * 60
        B += [f'  <rect x="{x}" y="{y}" width="280" height="{150 + i * 60}" rx="3" fill="{[PAPER, NAVY_BG, "#eef5ef"][i]}" stroke="{[PAPER_LN, NAVY, GREEN][i]}" stroke-width="{1 if i == 0 else 2}"/>',
              t(x + 140, y + 28, a, 17, [INK, NAVY, GREEN][i], "700"), t(x + 140, y + 50, b, 13, MUTED),
              t(x + 140, y + 80, c[0], 13, INK), t(x + 140, y + 97, c[1], 13, INK),
              t(x + 140, y + 128, ex.split(" · ")[0] + " · " + ex.split(" · ")[1], 12, MUTED),
              t(x + 140, y + 144, " · ".join(ex.split(" · ")[2:]), 12, MUTED)]
    B += [path("M40 382 L920 382", "g", 2), path("M920 382 L40 382", "g", 2),
          t(40, 404, "more control, more work", 13, INK, "700", anchor="start"), t(920, 404, "less work, less control", 13, INK, "700", anchor="end"),
          t(480, 432, "Underneath, almost all of them rent from the same three landlords: AWS, Google Cloud, Microsoft Azure.", 14, INK)]
    svg("saas-ladder.svg", 445, B, "three ways to rent somewhere for your code to run")


# ------------------------------------------------------------------ 7. deploy
def deploy():
    chips = [("commit", "you, or the agent, save a change"), ("git push", "to GitHub"), ("build", "the platform installs and compiles"),
             ("preview URL", "a live copy of this change only"), ("production", "merge → the real site, in seconds")]
    B = []
    for i, (a, b) in enumerate(chips):
        x = 30 + i * 186
        kind = "write" if i < 2 else ("rent" if i < 4 else "danger")
        B += box(x, 80, 166, 80, a, [b] if len(b) < 26 else [b[:b.rfind(" ", 0, 26)], b[b.rfind(" ", 0, 26) + 1:]], kind if kind != "rent" else "plain", 15)
        if i < 4:
            B.append(arrow(x + 168, 120, x + 184, 120))
    B += [f'  <rect x="30" y="200" width="900" height="96" rx="3" fill="{PAPER}" stroke="{PAPER_LN}"/>',
          t(50, 226, "ENVIRONMENT VARIABLES", 12, GOLDDK, "700", anchor="start", ls="1.1"),
          t(50, 250, "LLM_API_KEY · STRIPE_SECRET_KEY · DATABASE_URL", 13, INK, anchor="start", mono=True),
          t(50, 276, "typed once into the platform’s settings — never into the code, never into git. The code reads them by name.", 13, MUTED, anchor="start"),
          t(30, 336, "Every change gets its own address before it reaches users. Vercel, Netlify, Render and Cloud Run all work this way;", 14, INK, anchor="start"),
          t(30, 358, "it is also how you review what a coding agent did: open the preview, click through, then merge.", 14, INK, anchor="start")]
    svg("saas-deploy.svg", 375, B, "from a change on your laptop to the live site")


# ------------------------------------------------------------------ 8. model, harness, tools
def agent_stack():
    B = []
    B += box(40, 64, 560, 74, "the model", ["Claude · GPT · Gemini — reads text, writes text, nothing else"], "write", 17)
    B += [f'  <rect x="40" y="160" width="560" height="140" rx="3" fill="{RED_BG}" stroke="{RED}" stroke-width="2"/>',
          t(320, 186, "the harness", 17, RED, "700"),
          t(320, 206, "Claude Code · OpenAI Codex · Cursor · Gemini CLI · GitHub Copilot", 13, RED)]
    for i, (a, b) in enumerate([("tools", "read · edit · run"), ("permissions", "what needs your yes"),
                                ("context", "the project’s rules"), ("loop", "plan · act · check")]):
        x = 54 + i * 136
        B += box(x, 222, 126, 62, a, [b], "plain", 14)
    B += box(40, 322, 560, 60, "your world", ["the repo · the terminal · the tests · the cloud account"], "rent")
    B += [path("M604 101 C 690 101, 690 230, 604 230", "g", 2), path("M604 250 C 690 250, 690 352, 604 352", "g", 2),
          path("M604 370 C 880 370, 880 80, 606 86", "g", 1.5, "4 3"),
          t(676, 170, "it asks", 13, INK, "700", anchor="start"), t(676, 306, "it runs", 13, INK, "700", anchor="start"),
          t(830, 220, "the result", 13, MUTED, anchor="start"), t(830, 237, "goes back in", 13, MUTED, anchor="start"),
          t(30, 412, "The model is the engine; the harness is the car. Same engine, different car, different trip — which is why the same", 14, INK, anchor="start"),
          t(30, 434, "model feels different in a chat, in Claude Code and in Codex. It is week 5’s agent loop, pointed at a codebase.", 14, INK, anchor="start")]
    svg("saas-agent-stack.svg", 445, B, "what Claude Code and Codex actually are")


# ------------------------------------------------------------------ 9. the builders spectrum
def builders():
    zones = [("describe it, get an app", ["v0 (Vercel) · Lovable", "Bolt.new · Replit Agent", "Firebase Studio"], "rent"),
             ("start from a template", ["Supabase + Next.js starter", "Vercel templates", "a boilerplate on GitHub"], "plain"),
             ("an agent in your repo", ["Claude Code · Codex", "Cursor · Copilot agent", "you review every diff"], "write"),
             ("write it yourself", ["with an assistant", "for the part that", "is your edge"], "plain")]
    B = []
    for i, (a, lines, k) in enumerate(zones):
        x = 30 + i * 228
        B += box(x, 60, 212, 130, a, lines, k, 15)
    def bar(y, label, left, right, col):
        g = f'''  <defs><linearGradient id="g{y}" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity="0.08"/><stop offset="1" stop-color="{col}" stop-opacity="0.85"/></linearGradient></defs>'''
        return [g, f'  <rect x="30" y="{y}" width="900" height="26" fill="url(#g{y})"/>',
                t(30, y - 8, label, 13, INK, "700", anchor="start"),
                t(40, y + 18, left, 12, INK, anchor="start"), t(920, y + 18, right, 12, "#ffffff", "700", anchor="end")]
    B += bar(236, "time to the first demo", "minutes", "weeks", MUTED)
    B += bar(296, "what you can still change, test and explain", "little", "everything", NAVY)
    B += [t(30, 360, "Start on the left to see the idea; move right as soon as real users, real money or real data arrive.", 14, INK, anchor="start"),
          t(30, 382, "Most real products are mixed: a builder for the screens, an agent in the repo for the logic, a person for the decisions.", 14, INK, anchor="start")]
    svg("saas-builders.svg", 400, B, "from a sentence to a codebase — the tools sit on one line")


for f in (anatomy, lambda: anatomy(True), journeys, secrets, supabase, docker, ladder, deploy, agent_stack, builders):
    f()
