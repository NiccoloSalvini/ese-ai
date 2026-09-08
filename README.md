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

Replace `OWNER` in the Colab links with the GitHub owner of this repository (`sed -i '' 's/OWNER/<owner>/g' README.md`). Colab opens private repositories after you authorise it once (File ▸ Open notebook ▸ GitHub ▸ tick *Include private repos*).

| # | Date | Theme | Open in Colab | Notes · Homework |
|---|---|---|---|---|
| 1 | 21 Sep | How LLMs work, and how we will work | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-01/session.ipynb) | [notes](week-01/notes.md) · [homework](week-01/homework.md) |
| 2 | 28 Sep | Data analysis with AI as pair programmer | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-02/session.ipynb) | [notes](week-02/notes.md) · [homework](week-02/homework.md) |
| 3 | 5 Oct | Machine learning through one problem | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-03/session.ipynb) | [notes](week-03/notes.md) · [homework](week-03/homework.md) |
| 4 | 12 Oct | LLM applications I — API, structured output, RAG · EU AI Act | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-04/session.ipynb) | [notes](week-04/notes.md) · [homework](week-04/homework.md) |
| 5 | 19 Oct | LLM applications II — agents, tool use, evals · product lens | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-05/session.ipynb) | [notes](week-05/notes.md) · [homework](week-05/homework.md) |
| — | 26 Oct | Reading week — minor case brief (40%) due Sun 1 Nov | | [brief](week-05/homework.md) |
| 6 | 2 Nov | Minor presentation · fintech landscape · capstone scoping | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-06/session.ipynb) | [notes](week-06/notes.md) · [homework](week-06/homework.md) |
| 7 | 9 Nov | Markets and backtesting done honestly · model risk | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-07/session.ipynb) | [notes](week-07/notes.md) · [homework](week-07/homework.md) |
| 8 | 16 Nov | Digital assets, on-chain data, DeFi · MiCA | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-08/session.ipynb) | [notes](week-08/notes.md) · [homework](week-08/homework.md) |
| 9 | 23 Nov | Responsible AI applied to the capstone · red-team | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-09/session.ipynb) | [notes](week-09/notes.md) · [homework](week-09/homework.md) |
| 10 | 30 Nov | Implementation and capstone studio · portfolio (60%) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/ese-ai/blob/main/week-10/session.ipynb) | [notes](week-10/notes.md) · [homework](week-10/homework.md) |
| Rev. | 7–13 Dec | Final presentation (proposed Mon 7 Dec 09:00) | | [portfolio brief](week-10/homework.md) |

Syllabus: [syllabus/ESE_AI_FinTech_Course_Design_v2.docx](syllabus/ESE_AI_FinTech_Course_Design_v2.docx)
