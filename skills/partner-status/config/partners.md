# Partner status — configuration template (read-only)

This file is a **read-only template**: it documents the available fields and ships the
example placeholders the skill uses to show the shape of a config. It is **not** where
your live settings are stored. Your per-user config lives in your Google Drive at
`Claude/skill-config/partner-status.config.json` (written by the skill's guided setup); the
skill reads that file — not this one — at the start of every run. Editing this template
does not change your runs; edit the Drive config instead, or ask the skill to re-run
setup. Anything you say directly in a request (a single partner, a different window,
"skip Slack") overrides the config for that run.

## Your org domains

Used to tell *internal* attendees from *external* ones during auto-detection. An
event is a candidate partner meeting only if it has an attendee whose domain is
NOT in this list. Add every domain your company uses.

- org_domains: yourcompany.com, yourcompany.io

## Reporting window & staleness lookback

- report_window: 14 days        # the period the status writeup covers (default 2 weeks)
- staleness_lookback: 90 days   # how far back to search only to find each partner's
                                # most recent activity (for cadence flagging)
- grace_factor: 1.5             # a partner is "overdue" once idle time exceeds
                                # cadence × this; between cadence and that, it's "watch"

## Sources

Toggle which sources the skill mines. Calendar is always on (it's how meetings
are found). Turn one off if you don't use it or don't want it scanned.

- use_email: true
- use_drive: true
- use_slack: true
- use_granola: true

## Tracked partners

Each entry becomes one section in the report and one row in the cadence table.
Fields:

- `name` (required) — human-readable partner/account name.
- `domains` — email domain(s) used to match meetings and threads to this partner.
- `aliases` — other names this partner goes by in titles/notes (brand vs legal
  name, etc.). Helps match docs and Slack that don't carry the email domain.
- `cadence` — how often you *expect* to be actively working this account. Accepts
  `weekly` (7d), `biweekly` (14d), `monthly` (30d), `quarterly` (90d), or an
  explicit number of days like `21d`. This drives the quiet-account flag, so set
  it to the real expectation — a quarterly partner shouldn't be flagged for a
  normal three-week gap.
- `reps` — the internal people who own this account (account rep, lead, etc.),
  as `Name <email>`. These matter for two reasons: (1) an internal-only meeting
  (prep, debrief, deal review) counts as a partner meeting when a rep is on it and
  the partner/project is named, and (2) a rep's own mail/docs/Slack about the
  account count as activity even with no external party present. The rep is also
  the default owner of next steps and the person a "gone quiet" flag is routed to.
- `projects` — specific projects/workstreams tied to this partner. Each project
  can carry its own hints; activity on a project counts as activity on the partner.
  A project is `name` plus any of: `codename` (treated as an extra alias),
  `drive_folder`, `slack_channel`, `jira` (a project key/label — only used if you
  also enable a Jira source for the run).
- `drive_folder` (optional) — top-level Drive folder for this partner's docs.
- `slack_channel` (optional) — the main channel where this account is discussed.

Examples (replace with your real partners):

- name: Acme Corp
  domains: acme.com, acme.co.uk
  aliases: Acme Holdings
  cadence: weekly
  reps:
    - Dana Lee <dana@yourcompany.com>
  drive_folder: Partners/Acme
  slack_channel: #acme-partnership
  projects:
    - name: Checkout revamp
      codename: Roadrunner
      drive_folder: Partners/Acme/Roadrunner
      slack_channel: #proj-roadrunner
    - name: Data-share pilot
      codename: Coyote
      slack_channel: #proj-coyote

- name: Globex
  domains: globex.com
  aliases: Globex International
  cadence: biweekly
  reps:
    - Sam Ortiz <sam@yourcompany.com>
  drive_folder: Partners/Globex
  slack_channel: #globex
  projects:
    - name: Platform integration
      codename: Helios

- name: Initech
  domains: initech.com
  aliases: Initech Systems
  cadence: monthly
  reps:
    - Dana Lee <dana@yourcompany.com>
  slack_channel: #initech-deal

- name: Umbrella Health
  domains: umbrella-health.org
  aliases: Umbrella
  cadence: quarterly
  reps:
    - Priya Shah <priya@yourcompany.com>

# Add more partners below using the same shape. Only `name` is strictly required,
# but the more of domains / aliases / reps / projects you fill in, the more
# reliably the skill ties scattered activity back to the right partner. reps and
# projects are what let it catch internal work that never names the partner.

## Activity ledger (optional, durable last-active memory)

The skill can keep a small file in your Drive recording each partner's last
active-work date, so it can flag partners that have been silent LONGER than the
staleness lookback (which only sees ~90 days). Leave `ledger_enabled` false to
skip persistence entirely (staleness then relies only on the live lookback).

- ledger_enabled: true
- ledger_location: Claude/partner-activity-ledger.md
  # Path in the user's Drive. The skill confirms before creating it the first
  # time and tells you whenever it updates it. It only ever stores partner name,
  # last-active date, cadence, and owning rep — no message contents.

## Delivery

- output_format: markdown   # markdown | docx — the saveable status report
- ledger_only_with_consent: true  # never create/update the Drive ledger without
                                   # the user's explicit OK in the conversation
