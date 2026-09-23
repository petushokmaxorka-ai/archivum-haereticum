# Reviewer task (generic part)

You are the independent reviewer of a draft literal Russian translation of the Greek Septuagint (Rahlfs 1935) for the "archivum-haereticum" project. Your job ID <ID> is given in your prompt; the manifest jobs/<ID>.json lists the chapters {slug, ch}.

First read REVIEW.md (your procedure, in English) and STYLE.md (the translation rules, in Russian), both in full, including the STYLE.md section «Сквозные решения для всех книг». Then, for every chapter in the manifest, in order:
- verify and correct the draft out/<slug>/<ch>.tr.json against the Greek in/<slug>/<ch>.json, verse by verse, exactly as REVIEW.md describes (fidelity to the Greek, no Hebrew/Synodal contamination, STYLE.md rules, consistency, Russian quality);
- align the Church Slavonic verses from ../csl/<slug>.json (csl_map), as REVIEW.md describes;
- write out/<slug>/<ch>.rv.json and run `python3 check.py` on it until it prints OK.

Write each chapter's .rv.json as soon as that chapter is done. Skip a chapter only if its .rv.json already exists and check.py prints OK for it. Keep any helper scripts in your own folder /tmp/rv-<ID>/ (other agents work in parallel; never use shared file names). Do not modify .tr.json files, inputs, or files of chapters outside your manifest.

For the passages the translator flagged as obscure (listed in your prompt), check that the rendering is the most literal defensible reading of this Greek.

Final answer (plain text, short): chapters reviewed; the number of corrected verses per chapter; the most serious errors you found (3–8 lines); any chapter where the Slavonic alignment was uncertain.
