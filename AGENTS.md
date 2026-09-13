# Specialization repository guidance

Document Owner: Codex

Read Specialization/README.md and Specialization/AGENTS.md, then accepted Design, current Architecture and Status. Their applicable governance rules are binding. This directory alone is the project boundary; Mod/ is the sole canonical editable source. External game runtime is a deployment copy, not another editing location. Old workspace guidance remains unchanged, but its old source routing is superseded for this project by this approved migration.

Never treat filesystem access as project ownership. Do not change other Mods, HD, Workshop, game assets/config, or launch Civilization VI. User performs game tests. Accepted Design intent is authoritative; technical limitations that change it require DESIGN_DECISION_REQUIRED and user decision, never silent fallback. Preserve accepted hashes and frozen evidence.

Codex maintains local files under user authorization; Design Chat proposes/reviews only. Architecture owns HOW, Status owns validation/queue, technical reports own research. Do not overwrite user/uncommitted/unapproved edits. Deployment defaults to check-only; inspect source/runtime hashes and use the bounded transaction tool only with authorization. Tests use repository fixtures and explicit read-only external DB configuration; never weaken assertions for portability.

Phase 1 authorizes filesystem migration and validation only. No .git, Git initialization, staging, commit, remote, GitHub authentication or push. Stop after reporting. No P0/P1 gameplay development this phase.
