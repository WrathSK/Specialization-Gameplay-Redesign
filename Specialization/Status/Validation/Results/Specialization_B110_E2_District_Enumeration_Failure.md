# B110 E2 — 首次AI征服快照区域枚举失败

日期：2026-09-27。包：B110.137 / modinfo137。证据：两张用户实机截图逐张读取；不是本地模拟结果。

## 实机观察

两图分别选中尼德罗斯、希恩，回合21，均显示“城市取得待确认／等待确认，旧流程未写入”，错误为 `CityProgressionStore.lua:852: function expected instead of nil`，调用栈进入 `admit`。消息列表可见征服。两城快照验收为 **USER_GAME_TEST_FAIL**；未证明候选集合、空集后首次完成或冷加载成功。不能从这两图推断两城分别应有哪些候选。

用户中止测试，并明确持有征服这两城之前的存档。保留该存档，修复后从此处复测；当前不要求重建测试局或继续投资/迁移。B109既有三城及冷加载验收不被扩大或撤销。

## 直接原因与证据边界

STATIC_CONFIRMED：源码852行在 `c:GetDistricts()` 后调用 `districts:Members()`。当前Gameplay城市区域读取已有 `DistrictCompleteness.lua` 的 `GetNumDistricts()` + `GetDistrictByIndex(i)` 路径。新征服快照错误沿用了不兼容的遍历方式；`test_b110_conquest_snapshot.py` 的fixture人为提供Members，掩盖此接口差异。本地模拟曾通过不等于此原生路径通过。

错误发生在候选收集阶段，早于该次admit的index/token/record写入；这是源码路径结论，不宣称截图证明整个存档没有任何其他写入。到达852行说明本次执行已越过前面的事件顺序与AI资格断言，不等于所有生命周期均验证通过。无需因此变更城市identity、候选玩法或保存模型。

## 最小修复建议（待授权）

1. 沿用已存在的Gameplay indexed district读取，验证数量/条目及原有owner/reference/完成性，保留失败关闭与一次快照语义。
2. 修正fixture为零起始indexed API，不提供Members；覆盖空/单/多区域、未完成区域和读取失败，保留直接B109回归。不扩大为全历史stress。
3. 将玩家报告收窄为城市、读取阶段和简短原因，避免整段Lua堆栈遮挡结果；不隐藏UNKNOWN或失败。
4. 获授权修复并通过定向检查后，依部署门禁另行部署；从用户征服前存档重走原两城流程及一次完整重启。不得用当前失败后城市补扫来假造征服时快照。

本轮只归档与诊断，没有修改源码、测试、Design或部署。Claim/F仍未授权。

## 原始证据

外部原件目录：`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B110_E2_District_Enumeration_Failure_20260927`。保留默认文件名，移动前后SHA256一致；manifest与原图不进入Git。

- `Screenshot 2026-09-27 at 5.29.38 PM.png`：尼德罗斯；SHA256 `a6e0133f4dba0e8ecbbf59668b0cc19b4a71482957f942cd746d3533a695e2f7`。
- `Screenshot 2026-09-27 at 5.29.43 PM.png`：希恩；SHA256 `111dbd3d20773dcefe7587e1317100d9fec98d328ad5351f901767fc379d89c4`。
