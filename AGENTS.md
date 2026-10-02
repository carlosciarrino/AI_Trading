
## session-engram

This project has a session memory system at .engram/.

Rules:
- At the start of every session, read .engram/index.md to understand the project's session history, active work, and available experiences
- When working on a task that may relate to past sessions, check .engram/index.md for relevant context
- If .engram/experience/ contains entries related to your current task, read them — they contain reusable solutions and lessons learned
- If index.md shows a freshness warning ("Index stale"), run `sengram index` immediately before proceeding
- After completing a session, run `sengram index` to update the memory index
- When reading an experience file, increment its `uses` counter in front matter if it helped solve the current problem
