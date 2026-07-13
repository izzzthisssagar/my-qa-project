# Vault Operations Log

Append-only record of what Claude (or you) changed in the vault, one file per
day in `Logs/`. This file is just the pointer + template — entries never live
here.

## Entry format (`Logs/YYYY-MM-DD.md`)

```markdown
---
type: log
date: YYYY-MM-DD
ai-first: true
---

**HH:MM** - action | description
```

Latest: [[Logs/2026-07-13]]
