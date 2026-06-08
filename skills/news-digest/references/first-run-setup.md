# First-run setup

Read and follow this only when the resolution step in SKILL.md finds no
`Claude/skill-config/news-digest.config.json` in the user's Drive (i.e. first run
or an explicit reconfigure). It is loaded on demand, not on every run.

The first time someone uses this skill, no `Claude/skill-config/news-digest.config.json`
exists in their Drive yet. Don't run a digest — interview the user and write their
config to Drive. The skill ships with a full set of example topics in
`config/topics.md`, so the fastest path is to offer those as-is; keep it light and
conversational, and tell them everything can be edited later.

Run it one short exchange at a time (multiple-choice prompts for the closed
questions; plain questions for free text like topic names — they don't fit buttons):

1. **Frame it.** "Looks like this is the first run — let me set up your topics. It
   ships with a set of example topics; you can use those as-is or set up your own.
   You can edit any of it later." Then offer the first choice:
2. **Topics — use examples or customize** (multiple choice): "Use the shipped example
   topics" or "Set up my own."
   - If they keep the examples, read the topic list out of the config so they can see
     what they're getting, and move on.
   - If they customize, **loop one topic at a time**: collect a short topic `name` and
     optional `keywords`/synonyms (free text). After each, ask "Add another topic?"
     and stop when done. Only the name is required; keywords just broaden the search.
3. **Sources** (multiple choice, multi-select): which of the open **web** and **email
   newsletters** to mine. Both on by default.
4. **Window** (multiple choice): keep the 2-week default, or change it (1 week / 1
   month / custom).
5. **Events to watch** (multiple choice): keep the shipped conference list, edit it,
   or skip event coverage. Default is fine for most.
6. **Noise to drop** (free text, optional): anything recurring they want suppressed
   (pure promos, generic funding news, etc.).

Then **write the config to the user's Drive** (never to the skill folder):

- Assemble the answers into a `news-digest.config.json` object whose keys mirror the
  fields in the `config/topics.md` template (e.g. `topics` as a list of
  `{name, keywords}`, `sources`, `window`, `events`, `noise`), plus `"configured": true`.
  A minimal shape:

  ```json
  {
    "configured": true,
    "window_days": 14,
    "sources": {"web": true, "email": true},
    "topics": [{"name": "On-device AI", "keywords": ["edge AI", "local AI"]}],
    "events_to_watch": ["Google I/O", "WWDC"],
    "noise": ["pure promos", "generic funding news"]
  }
  ```
- Store it at `Claude/skill-config/news-digest.config.json` in the user's Drive (create the
  `Claude/skill-config` folder if it doesn't exist). Load the Drive create/update tool via
  `tool_search`; if a file already exists there, update it rather than making a
  duplicate. **Because this writes to the user's Drive, confirm before creating it the
  first time, and tell the user whenever you update it.**
- If Drive isn't connected, save the JSON to `/mnt/user-data/outputs/news-digest.config.json`,
  share it with `present_files`, and tell the user to upload it to a `Claude/skill-config`
  folder in their Drive so future runs find it. Either way, show what was captured.

Finally, **explain editing later** in a sentence or two: the live config is the JSON in
their Drive at `Claude/skill-config/news-digest.config.json` — edit it there to change topics
or settings, and to re-run this guided setup just ask (or remove that file). The bundled
`config/topics.md` is only a read-only reference of defaults and field meanings; editing
it does not affect their runs. Then offer to run the first digest now.

