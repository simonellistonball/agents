# First-run setup

Read and follow this only when the resolution step in SKILL.md finds no
`Claude/skill-config/partner-status.config.json` in the user's Drive (i.e. first run
or an explicit reconfigure). It is loaded on demand, not on every run.

The first time someone uses this skill, no `Claude/skill-config/partner-status.config.json`
exists in their Drive yet. Don't run a scan — interview the user and write their config
to Drive. Keep it light and conversational: gather the essentials, let them skip
anything, and tell them everything can be enriched later by editing the Drive config.
The aim is a working config in a few minutes, not an exhaustive intake form.

Run it roughly like this, one short exchange at a time (use the multiple-choice
prompt for the closed questions, plain questions for the free-text ones — names
and domains don't fit buttons):

1. **Frame it.** "Looks like this is the first run — let me set up your partners
   first. A few quick questions, and you can edit any of it later." Then ask:
2. **Org domains** (free text): the email domains your company uses, so internal
   and external attendees can be told apart. Required — everything else leans on
   it.
3. **Sources** (multiple choice, multi-select): which of Email, Google Drive,
   Slack, Granola to mine. Calendar is always on.
4. **Window** (multiple choice): keep the 2-week report window and 90-day
   staleness lookback, or change them. Default is fine for most — offer it as the
   easy pick.
5. **Partners — loop one at a time.** For each partner, collect: name; email
   domain(s); any aliases/codenames; the account rep(s) as `Name <email>`; the
   expected cadence (offer weekly / biweekly / monthly / quarterly / custom as
   choices); and optionally a Drive folder, a Slack channel, and any linked
   projects (each with its own codename/folder/channel). Make clear that only the
   name plus a domain or rep is needed to be useful — the rest is optional and
   improves matching. After each, ask "Add another partner?" and stop when done.
   - If the user isn't sure who their partners are, offer to scan the last 90 days
     of calendar for recurring external domains and propose a starter list they
     can confirm — a faster start than typing from memory.
6. **Ledger** (multiple choice): keep a durable last-active record in their Drive
   (so partners quiet longer than 90 days still get flagged), or not. If yes, ask
   where it should live.
7. **Output format** (multiple choice): Markdown or Word for the report.

Then **write the config to the user's Drive** (never to the skill folder):

- Assemble the answers into a `partner-status.config.json` object whose keys mirror the
  fields documented in the `config/partners.md` template, plus `"configured": true`.
  A minimal shape:

  ```json
  {
    "configured": true,
    "org_domains": ["yourcompany.com"],
    "report_window_days": 14,
    "staleness_lookback_days": 90,
    "grace_factor": 1.5,
    "sources": {"email": true, "drive": true, "slack": true, "granola": true},
    "partners": [
      {"name": "Acme Corp", "domains": ["acme.com"], "aliases": [], "cadence": "weekly",
       "reps": ["Dana Lee <dana@yourcompany.com>"], "drive_folder": "Partners/Acme",
       "slack_channel": "#acme", "projects": []}
    ],
    "ledger": {"enabled": true, "location": "Claude/partner-activity-ledger.md"},
    "output_format": "markdown"
  }
  ```
- Store it at `Claude/skill-config/partner-status.config.json` in the user's Drive (create the
  `Claude/skill-config` folder if it doesn't exist). Load the Drive create/update tool via
  `tool_search`; if a file already exists there, update it rather than making a
  duplicate. **Because this writes to the user's Drive, confirm before creating it the
  first time, and tell the user whenever you update it.**
- If Drive isn't connected, save the JSON to
  `/mnt/user-data/outputs/partner-status.config.json`, share it with `present_files`,
  and tell the user to upload it to a `Claude/skill-config` folder in their Drive so future
  runs find it. Either way, show them what was captured.

Finally, **explain editing later** in a sentence or two: the live config is the JSON in
their Drive at `Claude/skill-config/partner-status.config.json` — to add a partner they add an
entry to `partners`, to change a cadence they edit that field, and to re-run this guided
setup they just ask (or remove that file). The bundled `config/partners.md` is only a
read-only field reference. Then offer to go ahead and run the first status report now.

