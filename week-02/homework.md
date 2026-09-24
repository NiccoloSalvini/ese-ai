# Homework 2 — Poke a real model
**Due: Tuesday 6 October 2026, 23:59 · folder `week-02/` in your shared Drive folder `ese-ai-fintech`**

## Goal
Make last week and today concrete on a real language model: read its knobs, watch temperature change its answers, and decode a model release on your own. Then take a first look at next week's data.

## Deliverables (in `week-02/`)
1. `gpt2.ipynb` — the session notebook, extended:
   - **three prompts of your own** (one from your work, one about markets, one about crypto): the top eight next tokens for each, with probabilities;
   - for one of them, **four generations**: one at T = 0, three at T = 1 — and one at T = 2 if you are curious;
   - under the generations, a markdown cell: which sentences contain a number or a name? Which of those are facts, and how did you check?
2. **The tokenizer** on one paragraph of your own, in English and in Russian: 30 merges each, symbols per word, and two sentences on what that means for the cost of a real project.
3. `release.md` — **another model release, decoded** (half a page to one page). Pick an open-weight release — Llama, Gemma, Qwen, Mistral or DeepSeek — and find its announcement or model card. For every technical term (parameters, context length, tokenizer, training stages, quantization, licence, anything else), one sentence in your words, linked to what we built in class (a weight, the training loop, the knobs, the box…). Mark the terms you could **not** explain: we start there next week.
4. **Next week's data, a first look.** Download the card-fraud dataset (284,807 real European card payments, 2013, anonymised): `https://www.openml.org/data/v1/get_csv/1673544/creditcard.csv`. In a notebook: how many rows and columns, what the columns are, and **what share of the payments are fraud**. Write that share down. We start from it.

## Constraints
- Use an assistant as much as you like; every line must be one you can explain.
- The explanations in `release.md` are in your words. An assistant may correct the English, not write the content.

## Scope
3–4 hours. If you are past 4 hours, stop, save what you have, and write where you got stuck.

## Self-check
- [ ] `Runtime ▸ Restart and run all` works (the GPT-2 download takes a minute the first time).
- [ ] Three prompts, each with its eight knobs.
- [ ] Every number in the generations is labelled fact / invented / cannot tell.
- [ ] `release.md` covers every technical term of the release, including the ones you could not explain.
- [ ] You know the fraud share of the dataset, as a percentage.

## How this feeds the course
The knobs and temperature are what you will set on every API call from week 4. The release decoding is the skill of reading a vendor's claims. The fraud share is the base rate — the number every model next week has to beat.
