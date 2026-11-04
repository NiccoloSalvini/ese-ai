# Homework 5 — A harness in your own hands
**Due: Tuesday 10 November 2026, 23:59 · Drive ▸ `ese-ai-fintech/week-05/`**

## Goal
This morning you watched a coding agent build a service and you reviewed it without reading code: the plan, every permission, every subagent, every tool you had not handed it — against a test you wrote first. Now do the same with your own hands, on the smallest tool your capstone idea needs.

## Pick a harness (free)
One of these, installed on your laptop. Each has a free tier or runs on a free model; the setup guides are on their sites.

- **Gemini CLI** — Google's open-source harness, free with a Google account.
- **OpenCode** — open-source, any engine; the free models it lists are enough for this.
- **Claude Code** or **Codex** — if you already have a subscription.

Write down which one, and why, in one line.

## Deliverables
1. **`RULES.md`** (or the file your harness reads first: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) — five lines, written **before** you start: who uses the tool, what comes in, what comes out, the test by name, what it may never do.
2. **`test.csv`** — ten checks with the expected result found by hand, and the number that ships it. Written before the build.
3. **The tool** — the smallest thing from your capstone idea that reads one input and produces one output. A script, a page, a sheet with a formula the agent wrote: size does not matter; the test does.
4. **`log.md`** — every permission the harness asked for, in order, and what you answered. Every subagent it opened. Every tool it used that you did not hand it.
5. **`cost.md`** — tokens or turns for the session (the harness shows them), minutes of your time, and what you would have paid a developer for the same thing.
6. **`hw5.md`** — one page: what the test said (how many of ten), where it failed and which box failed (the brief, a permission, a tool, the model), and **what you would not let it do unattended** and why.

## Constraints
- The test is written before the first prompt. The harness never sees the expected answers.
- Say **no** to at least one permission and write down what the agent did with the refusal.
- No real keys, no real money, no customer data. If your capstone needs a key, use a free-tier one you created for this.

## Self-check
- Could someone else run your test on your tool and get the same number?
- Does `RULES.md` say what the tool may never do, in words a tribunal could read?
- Is there one line in `log.md` you would not have approved at 2 a.m.?

## How this feeds the capstone
The rules file, the test and the permission log are the first three pages of your capstone's risk and controls canvas (session 9). The tool is the first working piece of the portfolio (60%).
