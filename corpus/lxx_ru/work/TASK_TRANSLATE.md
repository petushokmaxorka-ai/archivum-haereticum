# Translator task (generic part)

You are translating the Greek Septuagint (Rahlfs 1935) into Russian for the "archivum-haereticum" project: a precise, literal (дословный) translation from the Greek, NOT from the Hebrew/Masoretic text and NOT the Synodal translation. Your job ID <ID> is given in your prompt; the manifest jobs/<ID>.json lists the chapters {slug, ch} in order.

1. Read STYLE.md (in Russian) in full before starting, including the section «Сквозные решения для всех книг», and follow every rule. Key points: translate only the given Greek; keep Greek-specific readings; κύριος → «Господь»; capitalised pronouns for God; direct speech after a colon, no quotation marks, capital letter; words added for grammar in [square brackets]; keep source markers like [a] or [.1] in place; one output verse per input verse; no commentary; one form per name within a book.
2. For each chapter of the manifest, in order:
   a. If out/<slug>/<ch>.tr.json already exists and `python3 check.py out/<slug>/<ch>.tr.json` prints OK, skip it.
   b. Read in/<slug>/<ch>.json (fields: book, ch, verses[{v, g}]; ignore csl_* fields).
   c. Translate every verse from the Greek into Russian per STYLE.md, carefully, verse by verse. The Greek has no punctuation; add Russian punctuation by sense. Keep names and terms consistent with chapters of the same book already in out/<slug>/ (yours or other translators').
   d. Immediately write out/<slug>/<ch>.tr.json (mkdir -p out/<slug>) as UTF-8 JSON {"slug": "<slug>", "ch": "<ch>", "verses": [{"v": "<v>", "r": "<russian>"}, ...]}, same verse numbers and order as the input, with a python3 script (json.dump(..., ensure_ascii=False, indent=1)). Write each chapter as soon as it is done.
   e. Run `python3 check.py out/<slug>/<ch>.tr.json`; fix every problem until it prints OK (look at length-ratio warnings; fix real omissions/padding).
   f. Re-read your Russian against the Greek once more, side by side, for omissions, additions and mistranslations.
3. Keep ALL helper scripts and drafts in your own folder /tmp/tr-<ID>/; many agents run in parallel, never use shared file names in shared folders. Only write inside out/ for your manifest's chapters.

Final answer (plain text, short): chapters completed with verse counts; any unfinished chapter; genuinely obscure/corrupt Greek passages (slug ch:v, one line each).
