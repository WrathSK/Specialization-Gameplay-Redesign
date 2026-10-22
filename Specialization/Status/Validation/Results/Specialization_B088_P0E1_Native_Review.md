# B088.115 / P0-E1 原生观察 — 2026-09-20

## 结论与范围

三图逐张目视审阅并按SHA256原样归档，见[manifest](Specialization_B088_P0E1_Evidence.json)。用户明确：测试1/2用首都；首都无法转自由城，因此测试3用分城。两组不得拼成同一城市的读档→易主连续性链。

- **USER_GAME_TEST_PASS（本次用户实机范围）**：诊断正常显示；首都读档后仍可核对原Owner锚点；分城丢失token后正确返回UNKNOWN，不自动认领/迁移。
- **TECHNICAL_INVESTIGATION_REQUIRED**：E1永久城市连续性门禁未通过，E2/F继续关闭。不是诊断崩溃或模型误报；反而原生证据揭示不能依赖City Properties自动跨Owner保留。
- 未证明普通战争征服、夺回、转移后读档、夷平重建的所有行为；不认定存档损坏，不推断旧Game级总账已丢失，也不归因HD。

## 截图1/2：首都原范围保存/读档

| 文件时间 | 对象 | 可见结果 |
|---|---|---|
| 12:27:36 | Stirling (TEST)，T8，0/65536 @31,32 | LOCAL_CANDIDATE；DEV-B013-P0-1→同token；旧账本锚点0/65536 @31,32 |
| 12:28:51 | 同首都；用户说明按测试2读档后 | 相同引用/token/旧账本锚点，仍LOCAL_CANDIDATE |

两图TOKEN/JOURNAL/FLOW/INVEST均“原有→现有；一致”；TEMPLATES均“原无→现无；一致”。支持本例冷读档后仍可读取并验证原范围结构。每次重新记录后，“一致”比较的是**本次加载内**基线，不是跨load完整payload哈希。没有全部账本内容/历史最大值/收益继承的实机证明。首都身份不是永久技术标识，城市名只辅助定位。

## 截图3：分城转自由城市

对象Edinburgh (TEST)，T8；转换前引用来自该图内已保存的观察基线，不来自首都截图。

- 原：owner/cityID `0/131073`，位置`28,29`，token `DEV-B013-P0-2`。
- 现：`62/65536`，同位置`28,29`，token `nil`。
- TOKEN / JOURNAL / FLOW / INVEST / TEMPLATES：五项均**原有→现无**。
- 报告：无充分证据；缺少旧绑定凭据，不能认领历史；`UNKNOWN_TOKEN_MISSING`。

原样抄录事件（同T8，按面板顺序）：

```text
CityBuilt [62,65536,28,29]
CityRemovedFromMap [0,131073]
CityAddedToMap [62,65536,28,29]
CityInitialized [62,65536,28,29]
CityTransfered [62,65536,0,-738490196]
```

事件在一次转移中包含Built/Removed/Added/Initialized，不能单凭这些事件名判定“首次建城”或“真实夷平”。CityTransfered实际捕获四个标量；末参数`-738490196`语义**UNKNOWN**，不得当永久cityKey或旧CityID。原版教程只消费前两个参数的先例不是完整签名证明。

当前CityID 65536同时也是截图首都的ID（不同owner），直接说明不能用CityID单独作全局身份。owner:cityID跨此次转换也变化。坐标仅定位，不证明永久generation。

## 实现含义 / 后续最窄调查

旧City Properties在本次Cheat转自由城路径的新对象上未保留；仅靠旧City token冷读新对象无法恢复原记录。只读观察器保留的旧快照是session内证据，不能冒充save authority。

后续首先只读调查：能否从原Game级绑定账本和原生转移参数建立可验证的old→new映射；转移前何时还能可靠读取旧记录；如何区别转移与夷平/同地新建。已有CityTransfered参数必须查明确切语义，不解释未知末参数。若必须引入新的持久身份/转移日志或写入实验，先提出最小独立spike及保存边界，再授权；不恢复旧CityInheritance/InheritanceShadow writer、不实现E2。

用户本轮无需再重复测试或等待AI夺回。先解决证据来源与协议，之后才安排可控最小补测。Design/runtime/main/部署全部不改。
