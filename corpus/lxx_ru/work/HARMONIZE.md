# Harmonisation pass: one book, one voice

A book was translated in parts by several translators and reviewed in parts by several reviewers. Your job is to make the **whole book consistent**. You are not re-translating it.

Read STYLE.md (Russian) in full first. It is the rulebook, including the name rules: one form per person/place (spelling variants unified, genuinely different names kept), traditional forms for the names listed there, otherwise the Greek form.

Inputs, for your book `<slug>`:
- the Greek text `in/<slug>/<ch>.json`
- the reviewed translation `out/<slug>/<ch>.rv.json`, one file per chapter; every chapter should have one
- the index tool: `python3 names.py <slug>` lists every capitalised Greek word (names, titles) with its occurrences. `python3 names.py <slug> --term <greek stem>` prints every verse containing that stem, with the Greek next to the current Russian. Use it to compare renderings.

## What to unify
1. **Names of persons, peoples and places.** Check every name that occurs in more than one chapter, and every name the reviewers' `changes` lists mention. Choose one form per STYLE.md and apply it everywhere, with correct case endings. Keep the rule for different names, e.g. Мемфивосфей vs Иевосфей.
2. **Recurring formulas**, for example:
   - the regnal formulas «и остальные слова … не вот ли они написаны в книге слов дней царей …»
   - «и почил … с отцами своими»
   - «сделал лукавое пред Господом»
   - «так говорит Господь», «и было слово Господне к …»
   - letter openings
   The same Greek formula gets the same Russian wording throughout the book. Choose the more literal of the variants in use.
3. **Key terms** that recur across chapters, where different parts of the book use different Russian words for the same Greek word in the same sense. Start from the glossary in STYLE.md; for anything not covered, take the majority rendering if it is correct.
4. **Divine names and pronoun capitalisation**, direct speech punctuation (colon, no quotation marks), and «вот» used only for ἰδού.

## What NOT to do
- Do not retranslate verses that are consistent and correct, and do not polish style for taste.
- Do not change the verse list, the `csl_map` or the `changes` history already in the files. Only edit the `r` strings. Append your own entries to `changes`, prefixed with «H:», e.g. «H: 9:19 Модеин → Модин».
- Never move the text toward the Hebrew or the Synodal Bible. When in doubt, the Greek decides.

## How to apply
Edit with a python3 script that loads each `.rv.json`, changes only the `r` strings of the verses concerned, and writes the file back (json.dump(..., ensure_ascii=False, indent=1)). Be careful with Russian case endings when replacing names: check every replaced verse by eye. Plain global string substitution is dangerous, because a short name can be part of another word.

Afterwards run `python3 check.py out/<slug>/*.rv.json` and make sure it prints OK.

Keep helper scripts in `/tmp/hz-<slug>/` only.

## Final answer
Plain text, short:
- the list of unified names, as «old forms → chosen form» with the number of verses changed
- the formulas and terms you unified
- the total number of verses touched
- anything you could not decide
