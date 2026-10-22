# P0-D1 区域原生小数实验 — B082.109

Status: B082 USER_GAME_TEST_FAIL (harness/API/captions); B083 LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. P0-D1正式切换未完成。

## B083修正优先

[截图与修复](../../Status/Validation/Results/Specialization_B082_Failed_Probe_B083_Fix.md)：B082实际Gameplay没有Members、无城市槽位清理nil、四按钮缺字；精度未测得。B083改用P0-A已验证索引API、跳过nil城市集合、具名Caption+SetText；错误简明，变化后的OFF重置基线。以下B082本地证据不能升级成实机PASS；SQL/测试数值及正式writer不变。

## 用户授权增量

收益必须体现在区域。用户明确备用0.5/1指**最终收益步长**，不是把BASE转换系数从50%改100%。本轮先验证原值；没有采用量化、floor或改变正式Design参数。若最终需要量化，舍入方向仍需明确，不能偷改。原市级per-pop固定值方案不满足区域归属要求，不能作为本能力正式备用。

## 静态依据与限制

- 本机HD `UpdateDataBase/HD_Governors.sql:272,286–287`已有 `MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE` / Production Amount1。本机只读Gameplay DB确认它是 `COLLECTION_CITY_DISTRICTS / EFFECT_ADJUST_DISTRICT_YIELD_CHANGE`；原生/HD城邦亦有各区域整数yield实例。
- 同效果的浮点Amount能否保留，不能由SQLite或人口小数政策推断。已有[政策调查](../../Reports/Technical/HD_Policy_Fractional_PerPopulation_P0D1.md)的0.2/0.3/0.7是城市人口路径，不是区域路径。
- adjacency mirror已有 `YieldTypeToMirror/ToGrant` 先例，未找到有依据的50%参数；不能假定它读取纯BASE而非最终相邻。`Building_YieldDistrictCopies`无系数列。没有用这些路径偷换100%效果。
- 普通整数区域yield有明确先例；0.5仍需本实验验证。没有宣称任意小数已支持或已否定。

## 最小隔离实验

`DistrictPrecisionProbe.lua` + `Data/DistrictPrecisionProbe.sql`：三个内部City Center技术载体，各用上述City District效果限定Campus/直接特色替代，配置Science0.3/0.5/1。**学院仅为本次原生路径的实验对象，不在本轮冻结正式能力的目标区域选择。**不取代跨学科研究，不关闭8旧Research人口writer，不改P0-C/其它能力。

默认OFF；无trait自动附着、无自动ON、无Property。明确按钮设置同一档是幂等操作；先撤旧再加新，撤销失败不继续添加。OFF不要求学院仍存在；load一次扫描准确三ID撤销实验，不自动重试，不让旧实验存档静默继续。测试载体与正式能力截然区分；不要在实验开启时推进长局。

`DistrictPrecisionRead.lua`：仅显式读数时从UI读取学院GetYield、GetAdjacencyYield、Plot BASE及城市Science；一份城市baseline+最多4个阶段结果，换城市丢弃旧表，无逐事件字符串/文件日志。每个ACK最多一次原生读取；UI等待只看回复，不反复扫描。配置与原生测量分列；失败/stale为UNKNOWN，不伪造0。原生结果可能异步，写入后需另点读数。区域getter和城市总量交叉对照；若两个口径矛盾，先UNKNOWN而非按城市总量宣布成功。

四个实验按钮暂占原尤里卡/商业四/折扣/模板的四个位置；原处理入口保持，实验结束撤回临时展示，不扩张面板。旧半点实验ON时禁止叠加。B082显式子Label仍未显示；B083补齐具名Caption及Lua SetText，实机可见性仍待确认。

## 本地验证（非引擎验证）

- `test_district_precision_probe.py`：实际Lua ON/替换/OFF/重复10000/失败撤销阻止添加/创建失败/owner/未完成/掠夺/特色区域/load清理；实际UI10000 idle回调零额外send/read；原生mock读数与UNKNOWN。SQL在外部DB只读备份到内存后执行，Make_Hash仅stub；3隔离定义、正确集合/效果、manifest131文件、全Lua编译/XML唯一ID、其余writer/SQL与Design字节不变。
- `test_district_precision_regression.py`：P0-C/B2/B1/A及A–D2既有回归、D1纯模型与1785原有半点分解；只显式适配B082版本和新增实验文件白名单，不更改旧测试。D1旧测试的“全部Mod不变”历史阶段断言不适用实验包；独立新测试验证精确允许差异，8旧效果仍保留。
- 本地不模拟“引擎会保留小数”作为结论；0.3/0.5/1真实收益及显示仍USER_GAME_TEST_REQUIRED。

## 一次最小用户测试

用独立测试存档，选一座有已完成、未掠夺学院的己方测试城（无需科研III；优先没有其它动态效果的普通测试城）。保持同回合、人口/专家/政策不变。

1. 「区域读数 / 右键OFF」右键OFF，再左键读数记录基线。
2. 依次点「实验：区域科技+0.3」、读数；+0.5、读数；+1、读数。
3. 右键OFF，再读数。最后报告会合并本城四档差值，回传这一张即可；如果读数未刷新，稍后只重读，不必过回合。

判据：观察学院原生增量、城市增量（受倍率），且OFF恢复。+1为阳性对照：如果它也没变化，不能判小数被截断，先调查挂载/可见性。若区域变化但城市不符、原生读数UNKNOWN、其它收益变化，记录而不宣布PASS。可额外查看学院地块/区域Tooltip；精度显示不足时以诊断的非四舍五入到整数读数配合城市变化判断。

## 下一步

待实机证据选择区域正式承载；小数通过也不代表完整D1完成。量化备用已获用户授权但未启用；不改变50%系数，不启动P0-D2。旧runtime/完整B081保留恢复边界。
