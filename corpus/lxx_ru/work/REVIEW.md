# Review stage: verify the draft translation and align the Slavonic text

You are the **independent second pair of eyes** on a draft Russian translation of the Greek Septuagint. Assume the draft contains mistakes until you have checked each verse yourself. The rules the translation must follow are in STYLE.md (Russian). Read STYLE.md in full first.

For every chapter in your job manifest (jobs/<ID>.json lists {slug, ch}):

## 1. Verify and correct the translation
Inputs: `in/<slug>/<ch>.json` (Greek, field `g`) and the draft `out/<slug>/<ch>.tr.json` (field `r`).

Go verse by verse, Greek next to Russian, and check:
- **Fidelity.** Every Greek word or phrase is rendered. Nothing is added, except minimal words in [square brackets]. Nothing is paraphrased away. Numbers, names, negations, tenses, persons, singular vs plural, and who does what to whom all match the Greek.
- **LXX, not Hebrew.** The draft must not have been "corrected" toward the Masoretic text or the Synodal Bible. Typical contamination looks like «филистимляне» for ἀλλόφυλοι, a Hebrew name form where the Greek has another, a Hebrew number or phrase the Greek lacks, or Synodal wording that does not match the Greek. Fix any you find.
- **STYLE.md rules.** «Господь» for κύριος; capitalised divine pronouns; direct speech after a colon with no quotes; glossary terms; traditional names where STYLE.md says so, otherwise the Greek form; source markers [a] [.1] preserved.
- **Consistency within the book.** The same Greek term and the same person get the same Russian rendering across the chapters of your job. Look at neighbouring chapters' files in out/<slug>/ if needed.
- **Russian quality.** Grammatical and readable, not archaic, punctuation correct.

Change only what is wrong. Do not rewrite correct verses for taste.

## 2. Align the Slavonic (1751) verses
The reader shows three columns per Greek verse: Greek, Church Slavonic 1751, and Russian. The Slavonic text is in `../csl/<slug>.json` as {"<ch>": {"<v>": text}}. It is itself a translation of the Greek, but its verse numbering sometimes differs.

- If the input's `csl_aligned_by_number` is **true**, glance at the first, middle and last verses of the chapter to confirm the Slavonic verse N really corresponds to Greek verse N. If it does, set `"csl_map": null`. If the numbering is shifted, build a map as below anyway.
- If it is **false** (or you found a shift), build `csl_map`. It maps each Greek verse number of this chapter to the list of Slavonic references `"ch:v"` that carry the same content, e.g. `{"1": ["1:1"], "2": ["1:2", "1:3"], "3": []}`.
  - Match by content: names, numbers, key words. Do not match by number.
  - Look in neighbouring Slavonic chapters too when chapter boundaries differ (the Slavonic may be one chapter ahead or behind, or in a different order, e.g. in Jeremiah, Proverbs, Sirach, 3 Kingdoms, 1 Esdras, 3 Maccabees).
  - Each Slavonic verse goes to **at most one** Greek verse.
  - A Slavonic verse with no Greek counterpart (e.g. an addition from the Latin): put it in the list of the nearest preceding Greek verse, so it still appears in reading order.
  - A Greek verse with no Slavonic counterpart gets `[]`.
  - Cover every Slavonic verse that belongs to this chapter's content. Slavonic verses that clearly belong to another Greek chapter are left to that chapter's reviewer.
- The Slavonic is **only** for alignment. Never change the Russian translation to follow the Slavonic. The translation follows the Greek only.

## 3. Write the result
Write `out/<slug>/<ch>.rv.json` as UTF-8 JSON via a python3 script (json.dump(..., ensure_ascii=False, indent=1)):
```json
{"slug": "...", "ch": "...", "verses": [{"v": "1", "r": "..."}, ...], "csl_map": null | {...},
 "changes": ["3: «филистимляне» → «иноплеменники» (ἀλλόφυλοι)", "7: added missing «и весь народ» (καὶ πᾶς ὁ λαός)"]}
```
- `verses`: the complete corrected chapter, with every verse in the input's order (not only the changed ones).
- `changes`: one short line per real correction. Use an empty list if the draft was already correct.

Then run `python3 check.py out/<slug>/<ch>.rv.json` and fix everything it reports until it prints OK. It also validates the `csl_map` references.

If the `.tr.json` draft for a chapter is missing, translate that chapter yourself from the Greek, following STYLE.md, and then review your own work the same way.

Do not modify `.tr.json` files, inputs, or any file of chapters not in your manifest.
