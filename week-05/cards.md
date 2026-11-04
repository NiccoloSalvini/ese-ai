---
marp: true
theme: default
paginate: false
title: "Week 5 — cards"
format:
  revealjs:
    theme: [default, ../slides.scss]
    slide-level: 0
    slide-number: false
    controls: true
    hash: true
    logo: ../images/ese-logo.svg
    footer: "AI for Business & FinTech · ESE Florence · Week 5"
    include-in-header: ../_fonts.html
---

<!-- card 1 -->

# The loop

```
 the model ──► asks, in an agreed shape ──► your code decides ──► runs the tool
     ▲                                                                 │
     └──────────── the result goes back in, as text ◄──────────────────┘
```

The model never touches anything. The gap in the middle is the only control point you have.

---

<!-- card 2 -->

# Three ways the loop breaks, one fix each

| what happens | why | the fix |
|---|---|---|
| it tries the same call forever | the result said *Error* and nothing else | a **contract**: what went wrong, what is valid |
| it does what a document told it | text from a tool looks like text from you | a **boundary**: tool text is never an instruction |
| the bill is 55× one question | every turn re-sends everything | a **ceiling**: steps, calls, money |

Never a better prompt.

---

<!-- card 3 -->

# What the harness adds — and whose decision it is

| it adds | the question for the PM |
|---|---|
| tools | which ones does *your* agent get? |
| permissions | what must always ask, what may never run? |
| project rules | who writes the file, who reviews it? |
| memory | what must it never remember? |
| context management | what is lost in the summary? |
| subagents | what does the parent never see? |
| MCP | which servers, and who audits them? |

---

<!-- card 4 -->

# Cheaper, cleaner, blind

A subagent reads forty files and returns two hundred words.
The parent pays for two hundred words, forever.
The parent cannot answer *"are you sure?"* about any of the forty.

The brief you give it is the only control you have.

---

<!-- card 5 -->

# Every tool is a door. Every door opens both ways.

A tool result is text in the context, next to your instructions.
The model cannot tell them apart structurally.

Air Canada's fare rule was one door. An MCP server is a hundred.

---

<!-- card 6 -->

# Engine and car

| | closed | open |
|---|---|---|
| **engine** | Claude · GPT · Gemini — rented by the token | DeepSeek · Qwen · Kimi · GLM — run anywhere |
| **car** | Claude Code · Cursor — a warranty, not a bonnet | OpenCode · Aider · Cline — a bonnet you can open; Codex CLI and Gemini CLI are open too, built for one engine |

Three questions: where does the context go · what does a turn cost · can you read the car.

---

<!-- card 7 -->

# Watch for four things

| you see | it is | you ask |
|---|---|---|
| steps before any code | the plan | is the test in it? |
| a prompt waiting for *y* | a permission | would you say yes unattended? |
| *"spawning an agent to…"* | a subagent | what will the parent not see? |
| a tool you did not hand it | an MCP server | who wrote it, what can it read? |

You cannot read the code. You can read all four.

---

<!-- card 8 -->

# What stays yours

The spec. The test. The permissions. The engine. The doors.

*"The agent did it"* will not work in a tribunal. *"The chatbot is a separate legal entity"* already did not.
