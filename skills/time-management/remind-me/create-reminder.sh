#!/bin/bash
# Creates a reminder in macOS Reminders.app
# Usage: create-reminder.sh <year> <month> <day> <hour> <minute> <reminder text>
# Example: create-reminder.sh 2026 4 11 14 0 "Review the PR"

set -euo pipefail

if [ $# -lt 6 ]; then
    echo "ERROR: Usage: create-reminder.sh <year> <month> <day> <hour> <minute> <reminder text>" >&2
    exit 1
fi

YEAR="$1"
MONTH="$2"
DAY="$3"
HOUR="$4"
MINUTE="$5"
shift 5
REMINDER_TEXT="$*"

# Validate numeric arguments
for val in "$YEAR" "$MONTH" "$DAY" "$HOUR" "$MINUTE"; do
    if ! [[ "$val" =~ ^[0-9]+$ ]]; then
        echo "ERROR: All date components must be numeric. Got: $val" >&2
        exit 1
    fi
done

osascript <<APPLESCRIPT
set targetDate to current date
set year of targetDate to $YEAR
set month of targetDate to $MONTH
set day of targetDate to $DAY
set hours of targetDate to $HOUR
set minutes of targetDate to $MINUTE
set seconds of targetDate to 0
tell application "Reminders"
    tell default list
        make new reminder with properties {name:"$REMINDER_TEXT", due date:targetDate}
    end tell
end tell
APPLESCRIPT
