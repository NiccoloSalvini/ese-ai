# ese-ai

## Moodle MCP

Server MCP `moodle` definito in `.mcp.json` (pacchetto [moodle-mcp](https://github.com/loyaniu/moodle-mcp), via `uvx`).

Setup quando avrai l'account Moodle:

1. Vai su `https://<moodle-host>/user/managetoken.php`, copia il token della riga **Moodle mobile web service**.
2. `cp .env.example .env` e compila `MOODLE_URL` e `MOODLE_TOKEN`.
3. Esporta le variabili nella shell prima di lanciare Claude Code (es. `set -a; source .env; set +a`), oppure sostituisci direttamente i valori in `.mcp.json` (non committarlo in quel caso).
4. `claude mcp list` deve mostrare `moodle ... Connected`.

Nota: `--with "mcp<2"` è necessario perché `moodle-mcp` 0.2.1 usa `FastMCP`, rimosso in `mcp` 2.x.

---

## Course materials
Course repository. One folder per teaching week.

```
week-NN/
  notes.md        session plan, objectives, script (questions, bets, hints), key concepts, tutor's notes
  cards.md        5–8 Marp cards used at concept moments (marp cards.md -o cards.pdf)
  session.ipynb   live Colab notebook for the session (Open in Colab → File ▸ Open notebook ▸ GitHub)
  homework.md     assignment, due the Sunday before the next session
  data/           small snapshots only; anything larger is fetched by code
  hw/             student's submission
```

Weekly rhythm: Monday 09:00–12:00 lesson · notes and homework published by Tuesday · homework due Sunday 23:59 · reviewed together at the start of the next Monday.

Rules: AI assistance is allowed and expected; every line submitted must be one you can explain. Nothing confidential goes into an AI tool. All market and crypto activities are educational simulations, not investment advice.

## Sessions
| # | Date | Theme |
|---|---|---|
| 1 | 21 Sep | How LLMs work, and how we will work |
| 2 | 28 Sep | Data analysis with AI as pair programmer |
| 3 | 5 Oct | Machine learning through one problem; from prediction to decision |
| 4 | 12 Oct | LLM applications I — API, structured output, RAG · EU AI Act |
| 5 | 19 Oct | LLM applications II — agents, tool use, evals · product lens |
| — | 26 Oct | Reading week — minor case brief (40%) |
| 6 | 2 Nov | Minor presentation · fintech landscape · capstone scoping |
| 7 | 9 Nov | Markets and backtesting done honestly · model risk |
| 8 | 16 Nov | Digital assets, on-chain data, DeFi · MiCA |
| 9 | 23 Nov | Responsible AI applied to the capstone · red-team |
| 10 | 30 Nov | Implementation and capstone studio · portfolio (60%) |
| Rev. | 7–13 Dec | Final presentation |
