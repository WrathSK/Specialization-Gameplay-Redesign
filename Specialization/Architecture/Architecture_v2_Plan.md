# Architecture v2 — investigation plan

Document Owner: Codex
Work branch: develop
State: AV2-I001 reviewed; Batch A input/publication contract implemented locally on develop; B–E not authorized
Stable runtime: B069.96 untouched

## Ordered deliverables

1. State Ownership Map + Persistence/Save Contract: persistent identity/progression/templates vs rebuildable routes, network and yields; save/load boundaries and isolated inheritance.
2. Runtime Dependency Graph + UI ↔ Gameplay Bridge Map: authoritative route source, validated snapshots, sender/ACK, consumers; preserve approved background UI/BTS contract.
3. Event/Trigger Map + Dirty Propagation Map: direct facts vs indirect notifications; old==new stopping conditions; redundant listeners and reentrant boundaries.
4. Cache/Revision Map + Performance Budget/Hot Path Map: shared revision keys, invalidation, bounded reconciliation; actual scans/writes and counter-based budgets before optimization. No fabricated numerical budget before measurement.
5. Carrier Building Inventory: `Specialization | Level | Carrier | Actual effect | District | Internal only? | Safe player-visible?`; inspect SQL and HD consumers. Bit/correction/negative/internal carriers stay hidden. Assess existing institutions before any extra 16 facade buildings.
6. External Mod Dependency/Adapter Map: HD tier/requirements/yields, BTS/native UI routes, other observed dependencies with exact source references. Future Core→Adapter→capabilities; no scattered HD/Vanilla branches or current dual-environment promise.

For EACH dynamic module record: authoritative facts; derived state; events directly changing facts; indirect events; duplicate listeners; dirty conditions; equality suppression; reconciliation frequency; global scans; incremental alternatives; cache owner/key/lifetime; write authority and save contract. Unknown API behavior is explicitly unverified, not assumed.

Principles: direct-event ownership, incremental dirty propagation, idempotent writes, shared derived-state caching, bounded reconciliation. Produce maps/reports and proposed order first; do not restructure stable Gameplay to draw the maps.

## Runtime performance audit backlog

High-frequency paths only update fixed-size integer counters. No per-event disk writes/payload history/string construction. Low-frequency per-turn summaries; bounded memory and rotated/session-bounded files; deduplicated anomalies; manual detailed snapshot. Investigate safe native I/O first, log failure bounded/no retry storm. Disabling logging must not change gameplay. Current B069 counters/manual report remain; automatic log is NOT implemented by this workflow task.

## Gate

Research identifies measurable batches and tests. Implement on develop only after scope is authorized; coherent local-verification commit and matching branch push even when user test pending. Live develop test needs explicit temporary-switch/restore agreement. No ownership reactivation, balance or speculative optimization in this infrastructure phase.

## 第一轮交付

[AV2-I001当前源码地图与候选批次](v2/README.md)覆盖上述1–3项。4仅记录当前revision/扫描证据以解释依赖；不构建缓存或预算实现。5/6未展开。

## Batch A implementation

[B070.97合同及本地验证](v2/Batch_A_Input_Contract.md)。只实施用户批准的事实版本/发布/撤销；不含shared cache或其它后续批次。未部署；等待用户审核。
