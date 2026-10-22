# B089.116 E1 experiment start — USER_GAME_TEST_FAIL

Two screenshots 2026-09-20 22:26:47/49, T8, reviewed and archived with hashes. User confirms owned noncapital selected; screenshot city panel shows Edinburgh and readonly report successfully resolves ref0/131073 @28,29 as LOCAL_CANDIDATE. Second screenshot shows 城市身份实验暂停：请在加载完成后选择己方分城, assertion stack.

Failure is the combined Begin precondition (`ready and IsTestPlayer and city and owner matches`), before any new experiment key write in this attempt. Not a failed transfer/save test, not evidence against Game Property persistence. Exact failed operand is not reported. UI owned-city validation plus successful preceding readonly check strongly point to `ready`, but no native flag/log evidence yet proves it.

Static finding: ready begins false and only becomes true in LoadScreenClose callback. Local simulation explicitly fires that callback, missing unavailable/missed callback scenario. Another defect: this recoverable precondition failure latches d.error for the load and exposes a truncated stack rather than an actionable reason. Do not ask user to reselect repeatedly.

Recommended narrow fix: initialize/read experimental saved state once on explicit validated request when needed, retain corruption/write-failure protection; report individual preconditions clearly and do not permanently latch ordinary readiness/selection refusal. No periodic retry, old-ledger writes, gameplay migration or E2/F. Not implemented in this evidence review. No deployment; B089 runtime unchanged. E1 gate remains HELD.
