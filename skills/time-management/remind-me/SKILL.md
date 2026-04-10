---
name: remind-me
description: >
  Create reminders in the macOS Reminders app using natural language. Use when the user
  says "remind me to...", "set a reminder for...", "don't let me forget to...", or any
  variation of wanting to be reminded about something at a specific time or date.
  Handles relative times (tomorrow, next Monday, in 2 hours) and absolute times
  (at 3pm, on April 15th).
tools:
  - Agent
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

Before delegating, extract two things from the user's message:

1. **What** — the reminder text (what they need to be reminded about)
2. **When** — the date/time for the reminder

If either is missing, use AskUserQuestion to ask before delegating:

- Missing time: "When should I remind you? (e.g., tomorrow at 9am, next Monday, in 2 hours)"
- Missing what: "What should the reminder say?"

### Step 2: Delegate to Haiku Subagent

Once you have both **what** and **when**, spawn a Haiku subagent to do the work. This is a mechanical task (date math + AppleScript) that doesn't need a large model.

Use the Agent tool with these parameters:

- **model:** `haiku`
- **description:** "Create macOS reminder"
- **prompt:** Use the template below, filling in the user's request details and today's date/time.

#### Agent Prompt Template

Fill in {REMINDER_TEXT}, {TIME_EXPRESSION}, and {CURRENT_DATETIME} then pass as the agent prompt:

~~~
Create a reminder in the macOS Reminders app. You MUST actually run the commands using the Bash tool. Do NOT just describe what you would do — execute every step.

Reminder: {REMINDER_TEXT}
When: {TIME_EXPRESSION}
Current date/time: {CURRENT_DATETIME}

STEPS — run each one using Bash:

STEP 1: Resolve the date by running this python3 command (adapt the logic for the specific time expression):

python3 -c "
from datetime import datetime, timedelta
now = datetime.now()
# Adapt for the expression — examples:
# 'tomorrow morning' -> tomorrow at 9am
# 'next Monday' -> find next Monday at 9am
# 'in 2 hours' -> now + 2h
# 'at 3pm' -> today 3pm if future, else tomorrow 3pm
# 'this weekend' -> Saturday 10am
# 'EOD' -> today 5pm
target = now + timedelta(days=1)
target = target.replace(hour=9, minute=0, second=0, microsecond=0)
if target < now:
    print('PAST')
else:
    print(f'{target.year} {target.month} {target.day} {target.hour} {target.minute}')
    print(target.strftime('%A, %B %d, %Y at %I:%M %p'))
"

Time resolution rules:
- "tomorrow" / "tomorrow morning" -> tomorrow 9:00 AM
- "tomorrow afternoon" -> tomorrow 2:00 PM
- "tomorrow evening" -> tomorrow 6:00 PM
- "next Monday" (any weekday) -> next occurrence at 9:00 AM
- "in X hours/minutes" -> now + X
- "at 3pm" -> today if future, else tomorrow
- "on April 15" -> that date at 9:00 AM
- "on April 15 at 2pm" -> that date and time
- "end of day" / "EOD" -> today 5:00 PM
- "this weekend" -> Saturday 10:00 AM
- "next week" -> next Monday 9:00 AM
- "later today" -> 2 hours from now
- Date with no time -> 9:00 AM

If output is PAST, respond: ERROR: resolved date is in the past. Then stop.

STEP 2: Create the reminder by running this osascript command. Replace YEAR, MONTH_NUM, DAY, HOUR, MINUTE with the numeric values from step 1. Replace REMINDER_TEXT with the reminder text (escape any double quotes with backslash):

osascript -e '
set targetDate to current date
set year of targetDate to YEAR
set month of targetDate to MONTH_NUM
set day of targetDate to DAY
set hours of targetDate to HOUR
set minutes of targetDate to MINUTE
set seconds of targetDate to 0
tell application "Reminders"
    tell default list
        make new reminder with properties {name:"REMINDER_TEXT", due date:targetDate}
    end tell
end tell'

IMPORTANT: Do NOT use 'date "string"' in AppleScript — it is locale-dependent and breaks. Always construct dates with set year/month/day/hours/minutes as shown.

STEP 3: Report the result.

If osascript output contains "reminder id", respond EXACTLY:
RESULT: Reminder set: "REMINDER_TEXT" — HUMAN_READABLE_DATE

If osascript failed with permissions error, respond EXACTLY:
ERROR: Reminders permission needed. Grant access in System Settings > Privacy & Security > Reminders.

For any other error:
ERROR: description of what went wrong
~~~

### Step 3: Report Result

Relay the subagent's result to the user. If successful:

> Reminder set: **"[reminder text]"** — **Saturday, April 11 at 9:00 AM**

If it failed, relay the error and any suggested fix.

## Examples

**User:** "Remind me to review the deployment logs tomorrow morning"
**Agent prompt fills in:** Reminder: "Review the deployment logs", When: "tomorrow morning"
**Result:** Reminder set: "Review the deployment logs" — Saturday, April 11 at 9:00 AM

**User:** "Don't let me forget to email Sarah about the proposal on Friday at 3pm"
**Agent prompt fills in:** Reminder: "Email Sarah about the proposal", When: "Friday at 3pm"
**Result:** Reminder set: "Email Sarah about the proposal" — Friday, April 17 at 3:00 PM
