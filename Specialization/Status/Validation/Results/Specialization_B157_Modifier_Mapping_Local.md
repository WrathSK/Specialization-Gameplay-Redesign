# B157.184 — 定域区域归属与接收对象诊断

用户已授权B156后的最小只读补齐。STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；新增映射USER_GAME_TEST_REQUIRED。不是收益修复或完整L2验收。

## 修改与依据

`Mod/UI/BoostGreatWorkRead.lua`在原按需读取内补齐：

- 只解析B156实际出现的完整`District: …, Owner: …, SubType: …, SubValue: …, City: …`格式，限定对象类型DISTRICT。首尾锚定、不接受多余字段/部分匹配；SubType/SubValue只匹配格式，不解释语义。GameEffects句柄不作为城市或区域ID。
- raw Owner与GetObjectsPlayerId一致，再用CityManager.GetCity取得当前城市、该城GetDistricts():FindID核对区域ID，区域GetCity返回的完整reference与城市一致。涉及所选城时还要与当前选城reference一致。均满足才显示“本城已核验”；可靠其它城显示其它城，未知格式/API/对象冲突保持UNKNOWN。
- 原版UI ProductionManager.lua:175/328使用CityManager.GetCity，UnitFlagManager.lua:984使用CityDistricts:FindID。现有CityJournalProbe.lua:95使用District:GetCity，NetworkInput.Reference沿既有owner/id/coords/binding合同。原版/现代码先例是STATIC，不保证新增组合在当前原生context全部可用；失败不猜测或改用名字/坐标。
- 每实例最多展开3个subject的玩家、类型、raw描述与同样的District核对结果，其余明确未展开；未观测过的City/其它对象格式只显示raw与UNKNOWN，不套District规则。subjects=nil/empty/array/error区别保留，不把对象归属核验当成requirement、合格作品或结算核验。
- 同一个native对象的描述/映射仅在本次请求内复用，缓存只存标量，没有原生对象句柄跨请求保留。原32768/64/64处理上限、12实例展示、每raw240字节、一token一次全局枚举、关闭/新请求/选城引用失效均保持。映射原始字符串最多512字节，先严格解析再截断显示。

其它变更仅Probe build、modinfo184及直接测试。无新按钮/本地化key/Gameplay请求/事件监听/收益carrier/数据库定义/Property/GC调用。不改HD、永久账本或Design。P0Panel原右键入口保持。

## 验证

- `test_modifier_read.py`23项PASS（0.131s）：原18项含实际Panel dispatch/Copy缓存、异常/UTF8/限长保留；新增完整District/subjects匹配、错误格式/Owner/City/超大ID、缺API/错误区域/父城binding、其它城隔离和未知subject/展开上限。
- 原Meaning reader3项直接回归PASS（1.330s）：只读基线无Gameplay写入、四态百分比基线分离、未知主题不采成功基线。只读DB复制进内存，未改旧断言；不跑全历史/stress。
- 本地模拟证明核对/失败保护，不能证明截图字段与当前引擎对象已匹配；须以下一次原生报告。B156所见Active实例及B155两个Culture候选FAIL保持，不推断覆盖算法。

## 最小实机

同此前存档/同城：打开P0面板，**右键“意义延展验证”一次**，截图报告（长时补下半）。无需启动、切配置、过回合或移动巨作。

这次唯一新增问题是：上次raw中的District/City能否通过当前真实对象核对，以及subjects究竟是什么。若显示UNKNOWN也直接投递，不重复尝试。映射报告审阅后才安排基线/追加/退出短对照，不自动让用户续旧四态。

## 当前停止点与部署

实现完成，source B157.184；live部署身份见Status/Authority中的receipt，不能从源码推断已部署。只等待新增归属/subject报告；不实施新writer、正式fallback/cutover或下一能力。[前次原生schema证据](Specialization_B156_Modifier_Native_Read.md)保持原样。
