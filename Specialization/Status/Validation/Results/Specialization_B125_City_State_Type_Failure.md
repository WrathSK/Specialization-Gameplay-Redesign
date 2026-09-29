# B125 — 商业入口通过；城邦类型读取失败

2026-09-29。用户明确确认原商业候选城可选择对应项目：入口限定USER_GAME_TEST_PASS（用户陈述，无商业新截图）；没有继续完成/双城/保存测试，不扩大PASS。

已逐张查看 `Screenshot 2026-09-29 at 4.19.45 AM.png`：B125.152，日内瓦征服消息，E2阶段“事件确认”，原因`ACQUISITION_SOURCE_KIND_UNKNOWN`；尚未登记，不是空候选。外部归档 `Specialization/Status/Validation/Evidence/B125_City_State_Type_Failure_20260929/`，manifest SHA256移动前后1/1一致。城邦取得USER_GAME_TEST_FAIL，PT013暂停。

## 定位与证据边界

CityProgressionStore当前在非Major分支调用`P.Call(old,'IsMinor')`，要求成功且布尔；本图证明此条件不成立，不能仅由错误码区分方法缺失、抛错或非布尔返回。

只读复核HD：`UI/Additions/HD_Utils.lua:200`定义PlayerIsMinor→Player:IsMinor；`Gameplay/Governors.lua`通过`ExposedMembers.DLHD.Utils`引用。因此HD使用证据是UI函数桥接，不是Gameplay直接接口证明。B125把它直接搬到Gameplay，本地fixture又提供IsMinor，遗漏了跨context接口差异。这是实现调查/测试不足，不是新Gameplay歧义。

只读外部DebugGameplay库确认Civilizations.StartingCivilizationLevelType分别为：GENEVA→CITY_STATE、FREE_CITIES→FREE_CITIES、BARBARIAN→TRIBE。候选修复：以原Owner配置的CivilizationType关联数据库明确类别，或采用有当前Owner依据的UI只读桥；先验证Gameplay配置接口及缺失/冲突分支。不能把“非Major”直接等同城邦，不按PlayerID区间或名字猜测，不放开Free/未知来源。此处仅方案，未实现。

下一窄修复应覆盖真实Gameplay缺IsMinor的fixture及明确城邦/自由城市/未知类型，保留现有征服链与一次snapshot。从征服日内瓦前档复测，商业入口无需再次单独验收；待两城准备好一起完成PT013。用户本轮要求等双城，不要求继续未完成步骤。本轮无runtime/Design/main修改或部署；等待接口修复授权。
