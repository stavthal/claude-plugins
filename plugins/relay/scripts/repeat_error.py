#!/usr/bin/env python3
"""Count repeated tool errors in a session. Every second repeat, tell the lead to call the advisor.

This is the part of relay that runs as plain code. No model decides it.
"""
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile

REPEATS_BEFORE_ADVICE = 2


def error_text(event):
    """The error a tool call ended with, or an empty string when it worked."""
    if event.get("error"):
        return str(event["error"])
    response = event.get("tool_response")
    if isinstance(response, dict) and response.get("is_error"):
        return json.dumps(response, sort_keys=True)
    return ""


def fingerprint(tool_name, text):
    """Same tool and same error give the same key, whatever the numbers in it."""
    normal = re.sub(r"\d+", "N", text.lower())
    normal = re.sub(r"\s+", " ", normal).strip()[:400]
    return hashlib.sha1(f"{tool_name}|{normal}".encode()).hexdigest()[:16]


def counts_path(session_id):
    safe_id = re.sub(r"[^A-Za-z0-9_-]", "", session_id) or "unknown"
    return os.path.join(tempfile.gettempdir(), f"relay-errors-{safe_id}.json")


def count_error(path, key):
    """Add one to the count for this error and return the new count.

    Parallel tool calls run this hook at the same moment, so the read and the
    write happen under one file lock.
    """
    with open(path, "a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        try:
            counts = json.load(handle)
        except ValueError:
            counts = {}
        counts[key] = counts.get(key, 0) + 1
        handle.seek(0)
        handle.truncate()
        json.dump(counts, handle)
        return counts[key]


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return

    text = error_text(event)
    if not text:
        return

    path = counts_path(str(event.get("session_id", "")))
    key = fingerprint(str(event.get("tool_name", "")), text)
    count = count_error(path, key)

    if count % REPEATS_BEFORE_ADVICE != 0:
        return

    advice = (
        f"relay: the same {event.get('tool_name', 'tool')} error has now come back "
        f"{count} times. Stop retrying. Call the relay:advisor agent with the "
        "exact error and the files involved, then apply its advice."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event.get("hook_event_name", "PostToolUse"),
            "additionalContext": advice,
        }
    }))


if __name__ == "__main__":
    main()
