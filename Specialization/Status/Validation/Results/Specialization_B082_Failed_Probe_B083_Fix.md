# B082实机未完成 / B083实验工具修复

Status: B082 USER_GAME_TEST_FAIL（实验工具失败，未测得小数能力）；B083 LOCAL_SIMULATION_PASS，待同一最小实机流程。

## 原始证据

用户两张截图已逐张查看，并按SHA256核验移入外部旧工作区 `Specialization/Status/Validation/Evidence/B082_District_Precision_Incomplete_20260920/`，保留原名，manifest同目录。原件不入源码包。

| 原名 | SHA256 | 内容 |
|---|---|---|
| Screenshot 2026-09-20 at 9.49.31 AM.png（原名含系统窄空格） | 13a084565d418ee3e076cb53c8886259584423dd689fccfdd95988bb6e5ccb59 | B082.109，OFF，学院科技/相邻/Plot BASE均2，城市43.187500；载入清理line65 nil容器；四新按钮无字。城市相对基线+13.593750且人口/回合改变，不是实验收益证据。 |
| Screenshot 2026-09-20 at 9.49.42 AM.png（原名含系统窄空格） | 64e8613cf4d9fd9f2863f4b677b492ce9460eeae5644242f33d622a946eb06f6 | line25 function expected instead of nil，发生在campus检查；用户报告三档按钮均此结果。尚未进入CreateBuilding。 |

## 原因与修复

1. B082错误地将UI的 `CityDistricts:Members()` 用在Gameplay；P0-A曾已确认Gameplay应使用 `GetNumDistricts/GetDistrictByIndex`。本次复用该已验证接口，不再扩展假设。
2. Load遍历所有玩家时某些 `GetCities()` 为nil；跳过合法无城市容器槽位，真实清理异常仍报告，不做高频重试。
3. B082只添加XML匿名Label，未采用现有面板Caption ID + Lua SetText规则。B083给四按钮各自具名Caption并初始化文字/Tooltip。视觉最终仍需用户确认，不能用mock冒称文字已实机PASS。
4. 错误报告只显示具体原因与短码；显式操作的完整错误留原日志，不向面板倾倒路径/堆栈。OFF读数若人口或回合已变化，重新建立基线，避免沿用无效城市增量。

## 测试质量纠正

B082 mock错误暴露Gameplay Members，且玩家全有城市容器，所以本地绿灯漏掉真实API差异。现在Gameplay fixture**没有Members**，UI fixture只有Members，并加入nil城市容器；先执行已发布B082源码，准确复现SET失败零写与load错误，再执行B083源码验证修复。不能将B082旧LOCAL PASS解释成真实API通过。

`test_district_precision_probe.py`：精确旧故障复现；新SET三档/重复10000/OFF/load/创建撤销失败/真实request dispatch/简明错误；具名按钮文字绑定；实际UI10000 idle零新增send/read；人口/回合改变重置基线；SQL只读外部DB备份到内存（缓存已含B082时仅移除实验定义后重放）；全Lua/XML/唯一ID/manifest110。三实验SQL与8旧正式writer完全不改。

`test_district_precision_regression.py`：P0-C/B2/B1/A、AV2 A–D2和D1纯模型通过。以上是LOCAL_SIMULATION_PASS，不是原生小数结算PASS，也不是本机GUI截图确认。

## Scope / 下一步

B083.110 / modinfo110仅修复实验入口/清理/报告，保持50%设计系数，未实施0.5/整数量化，未切换P0-D1 writer，不开始D2。原生区域0.3/0.5/1仍UNKNOWN。采用[原最小测试](../../../Architecture/v2/P0_D1_District_Precision_Probe.md)：同城同回合OFF读数，三档各读数，最后OFF读数，回传最终汇总即可。无需人为掠夺。
