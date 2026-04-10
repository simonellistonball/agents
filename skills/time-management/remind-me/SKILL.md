---
name: remind-me
description: >
  Create reminders in the macOS Reminders app using natural language. Use when the user
  says "remind me to...", "set a reminder for...", "don't let me forget to...", or any
  variation of wanting to be reminded about something at a specific time or date.
  Handles relative times (tomorrow, next Monday, in 2 hours) and absolute times
  (at 3pm, on April 15th).
tools:
  - Bash
  - AskUserQuestion
---

# Remind Me

Create reminders in the macOS Reminders app from natural language requests.

## When to Use This Skill

- User says "remind me to..." or "set a reminder..."
- User says "don't let me forget to..."
- User wants to be nudged about something at a future time
- User asks to schedule a reminder for a task

## Process

### Step 1: Extract What and When

Extract two things from the user's message:

1. **What** — the reminder text (what they need to be reminded about)
2. **When** — the date/time for the reminder

If either is missing, use AskUserQuestion to ask before proceeding:

- Missing time: "When should I remind you? (e.g., tomorrow at 9am, next Monday, in 2 hours)"
- Missing what: "What should the reminder say?"

### Step 2: Resolve the Date

Resolve the user's time expression into concrete numeric values: YEAR, MONTH, DAY, HOUR, MINUTE. Do this yourself — no tools needed, just arithmetic from the current date.

**Resolution rules (default time is 9:00 AM when not specified):**

| User says | Interpretation |
|-----------|---------------|
| "tomorrow" | Tomorrow at 9:00 AM |
| "tomorrow morning" | Tomorrow at 9:00 AM |
| "tomorrow afternoon" | Tomorrow at 2:00 PM |
| "tomorrow evening" | Tomorrow at 6:00 PM |
| "next Monday" (or any weekday) | The coming occurrence of that day at 9:00 AM |
| "in X hours/minutes" | Current time + X |
| "at 3pm" / "at 15:00" | Today if that time hasn't passed, otherwise tomorrow |
| "on April 15" / "on 4/15" | That date at 9:00 AM |
| "on April 15 at 2pm" | That specific date and time |
| "end of day" / "EOD" | Today at 5:00 PM |
| "this weekend" | Saturday at 10:00 AM |
| "next week" | Next Monday at 9:00 AM |
| "in a few days" | 3 days from now at 9:00 AM |
| "later today" | 2 hours from now |

If the resolved date is in the past, warn the user and ask if they meant a future date.

### Step 3: Create the Reminder

Run the `create-reminder.sh` script bundled alongside this SKILL.md. It takes the date components and reminder text as arguments — no inline scripting needed.

First, locate the script relative to this skill file. It is in the same directory as this SKILL.md. Use Glob to find it if needed:

```
skills/time-management/remind-me/create-reminder.sh
```

Then run it:

```bash
path/to/create-reminder.sh YEAR MONTH DAY HOUR MINUTE "REMINDER_TEXT"
```

**Arguments:**
- YEAR: 4-digit year (e.g., 2026)
- MONTH: month number 1-12 (e.g., 4 for April)
- DAY: day of month 1-31 (e.g., 11)
- HOUR: 24-hour format 0-23 (e.g., 14 for 2pm)
- MINUTE: 0-59 (e.g., 0)
- REMINDER_TEXT: the reminder text as a quoted string

**Example — "remind me to review the PR tomorrow at 2pm" (today is Friday April 10, 2026):**

```bash
skills/time-management/remind-me/create-reminder.sh 2026 4 11 14 0 "Review the PR"
```

If the output contains "reminder id", it succeeded.

### Step 4: Confirm to the User

After creating the reminder, confirm with a clear summary including the day of week:

> Reminder set: **"Review the PR"** — **Saturday, April 11 at 2:00 PM**

## Error Handling

- **Permissions error:** Tell the user to grant access in System Settings > Privacy & Security > Reminders.
- **Date in the past:** Warn and ask if they meant a future date.

## Examples

**User:** "Remind me to review the deployment logs tomorrow morning"
**Resolved:** 2026, 4, 11, 9, 0
**Result:** Reminder set: "Review the deployment logs" — Saturday, April 11 at 9:00 AM

**User:** "Don't let me forget to email Sarah about the proposal on Friday at 3pm"
**Resolved:** 2026, 4, 17, 15, 0
**Result:** Reminder set: "Email Sarah about the proposal" — Friday, April 17 at 3:00 PM

**User:** "Remind me in 2 hours to check the build"
**Resolved:** (current time + 2 hours)
**Result:** Reminder set: "Check the build" — Friday, April 10 at 3:38 PM
