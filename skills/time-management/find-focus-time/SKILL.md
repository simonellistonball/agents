---
name: find-focus-time
description: >
  Find available time in the user's Google Calendar and book focus time for a task.
  Use when the user says "find time to...", "schedule focus time for...", "when can I
  work on...", "block time for...", "I need to find time to...", or any variation of
  needing to carve out calendar time for focused work. Estimates duration based on
  task complexity, finds free slots, and books the chosen one.
tools:
  - mcp__claude_ai_Google_Calendar__gcal_find_my_free_time
  - mcp__claude_ai_Google_Calendar__gcal_create_event
  - mcp__claude_ai_Google_Calendar__gcal_list_events
  - AskUserQuestion
---

# Find Focus Time

Find free time in the user's calendar and book a focus block for a task.

## When to Use This Skill

- User says "find time to..." or "when can I work on..."
- User says "block time for..." or "schedule focus time for..."
- User says "I need X hours to do Y, when am I free?"
- User wants to carve out dedicated time for a task on their calendar

## Process

### Step 1: Understand the Task

Extract from the user's message:

1. **What** — the task they need focus time for
2. **How long** — if they specified a duration, use it
3. **When** — any time constraints (e.g., "this week", "before Friday", "tomorrow")

If duration wasn't specified, estimate it based on the task type:

| Task Type | Suggested Duration |
|-----------|--------------------|
| Quick review (PR, doc, email draft) | 30 minutes |
| Code review, writing feedback | 45 minutes |
| Small feature, bug fix, short writing | 1 hour |
| Medium feature, design work, analysis | 1.5 hours |
| Large feature, deep research, strategy doc | 2 hours |
| Architecture planning, major refactor | 2.5-3 hours |

Present the estimate and ask for confirmation:

> For **"[task]"**, I'd suggest **[duration]** of focus time. Does that sound right, or would you prefer a different duration?
>
> And when should I look for time? (e.g., "this week", "tomorrow", "before Friday")
>
> Options:
> 1. [duration] sounds good, look this week
> 2. [duration] sounds good, look tomorrow
> 3. I'd prefer a different duration: ___
> 4. I'd prefer a specific timeframe: ___

### Step 2: Determine the Search Window

Resolve the time constraint into a concrete search range:

| User says | Search range |
|-----------|-------------|
| "today" | Now through end of today (6:00 PM) |
| "tomorrow" | Tomorrow 8:00 AM - 6:00 PM |
| "this week" | Now through Friday 6:00 PM |
| "next week" | Next Monday 8:00 AM - Friday 6:00 PM |
| "before Friday" | Now through Thursday 6:00 PM |
| No preference | Today through next 5 business days |

Use `date` via Bash to compute exact timestamps:

```bash
python3 -c "
from datetime import datetime, timedelta
now = datetime.now()
# Compute search window based on constraint
print(f'timeMin: {start.strftime(\"%Y-%m-%dT%H:%M:%S\")}')
print(f'timeMax: {end.strftime(\"%Y-%m-%dT%H:%M:%S\")}')
"
```

### Step 3: Find Free Time

Use `gcal_find_my_free_time` to find available slots:

- Set `calendarIds` to `["primary"]` (or ask the user if they have multiple calendars)
- Set `minDuration` to the task duration in minutes
- Use the user's timezone (detect via `date +%Z` or ask)

### Step 4: Present Options

Filter and rank the free slots:

**Ranking priorities:**
1. **Morning slots** (8-12) are best for deep/creative work — prefer these for coding, writing, strategy
2. **Early afternoon** (1-3 PM) is good for analytical work — reviews, planning, analysis
3. **Late afternoon** (3-6 PM) is best for lighter tasks — emails, reviews, admin
4. **Avoid splitting** — prefer a single contiguous block over two halves
5. **Sooner is better** — if the task is urgent, weight earlier slots higher

Present the top 3-5 options:

> I found these available slots for **[duration]** of focus time on **"[task]"**:
>
> 1. **Tomorrow (Wednesday)** 9:00 AM - 10:30 AM — great for deep work
> 2. **Tomorrow (Wednesday)** 1:30 PM - 3:00 PM — solid afternoon block
> 3. **Thursday** 10:00 AM - 11:30 AM — morning focus slot
> 4. **Friday** 8:00 AM - 9:30 AM — early start, uninterrupted
>
> Which slot works best? (Pick a number, or tell me a different preference)

If no slots are found in the window:

> I couldn't find a **[duration]** block in your calendar **[timeframe]**. Your options:
> 1. Look at a wider timeframe
> 2. Shorten the focus block to [shorter duration] — I see some [shorter] slots
> 3. Split into two shorter sessions

### Step 5: Book the Focus Time

Once the user picks a slot, create the calendar event:

- **Summary:** "Focus: [task description]" (prefixed with "Focus:" so it's identifiable)
- **Description:** Include the task details and any relevant context from the conversation
- **Color:** Use colorId "7" (Peacock/teal) to visually distinguish focus blocks from meetings
- **Reminders:** Set a 10-minute popup reminder before the block starts
- **No attendees** — this is solo focus time
- **sendUpdates:** "none" — no need to notify anyone

Example event creation:

```
summary: "Focus: Review PR #42 and deployment logs"
description: "Blocked focus time for reviewing PR #42. Check deployment logs and leave feedback."
start: { dateTime: "2026-04-11T09:00:00", timeZone: "Europe/London" }
end: { dateTime: "2026-04-11T10:30:00", timeZone: "Europe/London" }
colorId: "7"
reminders: { useDefault: false, overrides: [{ method: "popup", minutes: 10 }] }
```

### Step 6: Confirm

> Booked: **Focus: [task]**
> **[Day], [Date]** from **[start time]** to **[end time]** ([duration])
>
> You'll get a reminder 10 minutes before. Good luck with it!

## Handling Edge Cases

### User has a packed calendar
If the calendar is extremely full, suggest:
- Looking further ahead (next week, week after)
- Shorter focus blocks
- Early morning or late afternoon slots outside typical meeting hours
- Splitting the task across multiple shorter sessions

### User wants recurring focus time
If the user says "I need to do this regularly" or "block this every week":
- Book the first occurrence
- Ask if they want it recurring
- If yes, add a recurrence rule: `["RRULE:FREQ=WEEKLY;COUNT=4"]` (default 4 weeks, ask for preference)

### Multiple calendars
If the user mentions work/personal calendars, ask which calendar IDs to check. Use all relevant calendars for availability but book on the one they specify.

### Timezone
Detect the user's timezone with:
```bash
python3 -c "import time; import datetime; print(datetime.datetime.now().astimezone().tzinfo)"
```
Or use the system timezone. Always pass the timezone to the calendar API calls.

## Examples

**User:** "I need to find time to write the Q2 planning doc this week"
**Action:** Estimate 2 hours (strategy doc), search this week, present morning-weighted options, book chosen slot as "Focus: Write Q2 planning doc"

**User:** "Block 45 minutes tomorrow for code review"
**Action:** Use 45 min duration, search tomorrow, present options, book as "Focus: Code review"

**User:** "When can I work on the database migration? It'll probably take about 3 hours"
**Action:** Use 3 hours, search next 5 business days, present options, book as "Focus: Database migration"

**User:** "Find me some time to prep for Thursday's presentation"
**Action:** Estimate 1.5 hours (prep work), search today through Wednesday, present options, book as "Focus: Prep for Thursday presentation"
