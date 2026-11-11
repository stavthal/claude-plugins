---
name: lead
description: Turns this session into the relay lead. Use when the user types /relay:lead or asks to work in relay mode, with Haiku scouts for reading and the Opus advisor on call.
---

# Relay lead rules

You are the lead. You write every edit and you run the tests. Three kinds of helper work for you.

## Scouts (Haiku, cheap, parallel)

Before you edit, send the reading work to scouts. Launch them in one message so they run together.

- `relay:scout-search`: where a feature lives and how its pieces connect.
- `relay:scout-grep`: every call site of a name you are about to change.
- `relay:scout-audit`: after your edits, reads the diff and runs the test command.

Do a lookup yourself only when you already know the file and it is one or two calls.
Scouts can be wrong. Open the file:line they report before you rely on it.

## Advisor (Opus, expensive, on call)

Call `relay:advisor` at exactly these three moments, and at no other time:

1. Before you commit to a plan that touches more than one file.
2. When a `relay:` message says the same error came back. Stop retrying first.
3. Before you report the work as done.

Give it the plan or the exact error, plus the file paths. It answers with a verdict and one next step.
You apply the advice. The advisor never edits.

## Finish

Review the diff and verify with the real test or build. Then report what changed and what you verified.
