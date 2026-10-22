# B076.103 Architecture v2 Runtime Milestone — short idle validation

Document Owner: Codex
Runtime: B076.103 / modinfo103 / 6a84027edffa74ca27265e77f72bcd51b62638e0
Evidence level: USER_GAME_TEST_PASS for the observed short idle/no-expensive-work scope only (user actually ran the game). Not full gameplay regression or long-session memory certification.
Milestone tag: av2-runtime-b076.103

## 用户摘要

用户完成五组配对截图：起始零城、零城静置、单城、快速扩至四城、四城静置。观察窗内无异常卡顿/持续内存增长，静置时昂贵计数不再增长，接受为Architecture v2 Runtime milestone。无需立即重复测试；保留首回合桥接ACK未完成疑点，不能把它作为网络功能PASS或断言55GB根因已消除。无代码/Design/main/运行包改动。

## Observations

All five pairs show B076.103, turn1; Activity Monitor PID25326 throughout. Memory is Activity Monitor's displayed Memory, not command-line RSS. Times from screenshot filenames (local time). City counts from user sequence; fourth screenshot also visibly shows four cities. Exact enabled-mod list and continuous memory time series not provided in this batch.

| Group/time | State | Memory GB | Threads | Facts | City scans | District scans | Building checks | Property writes | Lv3 / Commerce / Copy audits |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
|1 20:52:24|0 cities baseline|9.28|32|0|0|0|0|0|4 / 16 / 2|
|2 20:54:05|0 cities idle|9.28|32|0|0|0|0|0|4 / 16 / 2|
|3 20:55:15|1 city|9.15|33|47|50|2|4182|7|9 / 32 / 3|
|4 20:56:01|4 cities after operations|9.24|32|478|520|59|40371|28|32 / 79 / 14|
|5 20:56:36|4 cities idle|9.24|34|478|520|59|40371|28|32 / 79 / 14|

Total window252s. Zero-city idle101s; four-city idle35s. Both show delta0 facts/city/district/building checks, actual Building Create/Remove, Property writes, full derives and displayed Audit counts. Memory unchanged at displayed precision in both idle windows; overall9.28→9.24GB (net−0.04GB), no monotonic increase across five points. Writes28 were recorded during city creation, not idle. Building Create/Remove=0 all groups. Route scans3/3/4/7/7; full derive0 throughout. Real city operations produce bounded observed work; this is not a scaling benchmark.

## Important unresolved bridge observation

All groups: routes0, revision0, inflight1/peak1, net_send1/net_receive0; discount_send2/ack0/retry0/timeout0; input_publication0, cache hits/misses0, audit_standard0. Therefore this session does NOT demonstrate successful verified Network initialization, Discount application, or advanced-network regression. The zero derives/checks cannot alone prove those functional paths healthy.

Repeated cheap guards still run: busy_skip481/6233/9985/12533/14287; send_inflight203/5955/9708/12285/14039; discount_attempt471/6223/9980/12566/14320; discount_pending469/6221/9978/12564/14318. `discount_pending` and `send_inflight` are suppression counts, not that many queued requests (source: UI/DiscountEligibility.lua and NetworkSender.lua). Idle deltas5752 and1754 remain cheap callback activity, with no extra actual sends/scans/writes. Distinguish this from 'all idle callbacks eliminated'. Pending/ACK status remains a follow-up correctness question; no diagnosis/fix or new test demanded this batch.

## Milestone scope and remaining evidence

Accept short idle performance validation, user-reported responsive city founding, and A–D2's already recorded local regression as a recoverable develop milestone. User judged abnormal performance resolved in this window; evidence supports the observed symptom improvement. Does not establish causality for prior native55GB growth, hours-long stability, all mechanics, or identical previous Mod composition. Original memory/crash evidence remains intact. Main remainsB069.96; no stable promotion, no BatchE. The annotated tag marks the documentation+validation commit with Mod identical to6a84027.

## Frozen evidence archive

External originals (not Git PNG assets):
/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B076.103-Runtime-Milestone-20260915

Ten screenshots read individually, moved from ScreenShots with unchanged basenames and SHA256 verified before/after. Manifest retained alongside originals; hash table below is portable audit metadata.

| File | Bytes | SHA256 |
|---|---:|---|
|Screenshot 2026-09-15 at 8.52.24 PM (2).png|1300907|`9216a28d9853843891fb82360a760b4e0c0948e111328e4e9e0982a20d70524c`|
|Screenshot 2026-09-15 at 8.52.24 PM.png|10053266|`dbb3bdcaa6740c8724265828027c6c31a4739abad67a407e2aee90b953d15809`|
|Screenshot 2026-09-15 at 8.54.05 PM (2).png|1293755|`2ec9a17917fa0a0e8787bf6788033a636f318363d38037548a5d9210b0b313f8`|
|Screenshot 2026-09-15 at 8.54.05 PM.png|10060330|`d448d0720021b4675d64d7c1abe75bf57007567e8fe3a64d0cc7c68b69ff04f4`|
|Screenshot 2026-09-15 at 8.55.15 PM (2).png|1292001|`c66dd9fa7dc137931c3ae053f4c0c74ca3e3781662d6320eacb68d4344abd0b4`|
|Screenshot 2026-09-15 at 8.55.15 PM.png|10946891|`41304c127b672b70cecbfb8a8fcc317a609bcc7b2eb40ebabab41028c04e3736`|
|Screenshot 2026-09-15 at 8.56.01 PM (2).png|1293194|`8c14bf77e26486ee41a95107f2c50c2359701d783a041588a6cfa44245a7095d`|
|Screenshot 2026-09-15 at 8.56.01 PM.png|11374577|`01c458123d7fc7d750caa32279414f9b0bafbc2d3abe64ace2e5e4891cdedd83`|
|Screenshot 2026-09-15 at 8.56.36 PM (2).png|1293717|`c6e9891b1ed1a010e8dfa4c12e10e65bc64030fce53e7422ad96023108e60a86`|
|Screenshot 2026-09-15 at 8.56.36 PM.png|11406196|`37dedc6d9762a4078257c8754d3f68f5dfe074369c86d66c7f531d2d4e96ea1e`|
