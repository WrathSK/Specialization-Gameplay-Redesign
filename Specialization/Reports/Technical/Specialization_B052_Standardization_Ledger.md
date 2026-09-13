# B052 标准化永久模板记录

Document Owner: Codex
Design: Accepted D0015, IND-NET-004 / IND-NET-005
Runtime: P0-B-052 / modinfo68
Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED

## 本批边界

只实现永久知识记录与只读面板。玩法范围以Design为准；不附加Gold/Faith Modifier、不解锁购买、不结算网络模板并集、不改变已有专业收益/投资/Crew。

## 数据与生命周期

- `Mod/StandardizationCatalog.lua`读取GameInfo.HD_BuildingTiers / HD_DUMMY_BUILDINGS，复核Buildings分类并排除内部/奇观/虚拟条目。当前外部数据库静态167条；运行不硬编码总数。保留具体BuildingType、HD district/tier，另附D0015启用与匹配组；原始PurchaseYield只用于调查，不作为购买许可。
- `Mod/Standardization.lua`城市Property `SPC_STANDARDIZATION_LEDGER_V1`：schema、uid、foundation、x/y、initialized、revision、learned[BuildingType]={district,tier,turn,evidence}。revision=1+模板数；账本中不保存当前折扣资格或网络输出。
- 初次Industry（含安装本功能前已有、且现有身份链有效的Industry）：后台遍历合格目录，复核本城实际拥有后，一次写入；空集合也标记初始化。每个建筑只有一份收据，建筑消失/当前未开放折扣不删除知识。
- 初始化发现遍历城市及已有收据校验；只有缺少账本的Industry扫描建筑。不是每回合全城扫描建筑列表。
- `GameEvents.BuildingConstructed` / 可用的`OnBuildingConstructed`：playerID, cityID, buildingID。HD `Gameplay/CivilizationTraits.lua`的QueenBibliotheque/Netherlands回调为前者的先例。
- `Events.BuildingAddedToMap`：x,y,buildingID,playerID；HD `Gameplay/RegionalYields.lua`使用此顺序。对该玩家每城只复核同一buildingID，以避免把plot坐标当cityID；无法凭事件直接赠送模板。
- 如果通知早于拥有状态，保留该建筑候选并在发布完成/回合检查，最多保留至通知后两回合；确切城市通知过期保留诊断警告。宽范围AddedToMap在其它城市不拥有属于正常情况，不报误错。重复信号合并，不延长首次通知寿命。候选是暂存队列，不伪装永久学习事实。
- Read templates / Next templates仅读取/分页；不会初始化、扫描建筑或写Property。显示模板数/revision/范围内与仅保留数、全玩家本次加载扫描/写入计数、当前城最后新增与错误。组相同的两个建筑仍是两份具体模板。

## 安全和未证实边界

旧Property损坏、位置冲突、HD分类变化或foundation改变停止相关写入，不重置已有记录。完整跨Owner/Conquest与缺失历史旧城身份仍是已有实现限制；本批未补齐，不声称已支持。没有捕获到任何兼容事件的获取方式仍可能漏记；需游戏实测正常生产/购买/Cheat，不能凭模拟宣布“所有Mod所有授予路径”通过。缓存候选不持久化，若在拥有事实成立但通知未完成时强行中断/存读档，尚无恢复证据；不以持续全表扫描掩盖。

## 本地证据

`test_b052_standardization.py`执行真实新Lua及只读DB目录：167条分类、特色/宗教/未启用记录、三市中心组、数字0/1字段、一次补录、两种事件参数、重复与延后拥有、读取/读档无新增、移除建筑保留、首次转Industry、空账本、缺HD表恢复、损坏/分类/身份冲突保护。故障日志为主动注入断言预期，测试退出0。

`test_b052_existing_effects.py`运行冻结B051回归，仅更新包装版本期望68，保持既有复制/半点/撤销等断言；运行通过。Lua语法、XML、modinfo导入/Files列表检查通过。测试使用Python3.10.13 + Lupa lua55；项目目录默认python3.14不能加载现有cp310扩展，须选匹配解释器。这不更改项目运行依赖或安装软件。

命令从仓库根执行，`PYTHONPATH`指向本机匹配Lupa目录，外部DB配置在忽略的local/config.json；不把外部DB或扩展复制进Git。

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/city-gpp-test-runtime /Users/xutingzheng/.pyenv/versions/3.10.13/bin/python3 DevelopmentTests/test_b052_standardization.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/city-gpp-test-runtime /Users/xutingzheng/.pyenv/versions/3.10.13/bin/python3 DevelopmentTests/test_b052_existing_effects.py
```

以上为本地模拟与静态证据，不等于CivVI游戏通过。当前用户测试仅由Status链接的新批次派发。
