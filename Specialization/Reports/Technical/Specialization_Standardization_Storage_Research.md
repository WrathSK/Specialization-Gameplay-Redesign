# 工业标准化：永久记录与当前网络资格

Document Owner: Codex
Design authority: current Accepted Spec IND-NET-001..004 / PROG-004
Scope: research + offline contract, not runtime acquisition or purchase discount

## 建议记录方式

采用城市Property表保存“已掌握的建筑模板”，不以隐藏建筑作为永久原件，也不放在Player的全国永久buff表中。记录跟城市走；current owner只用于当下资格判断，不作为账本主键。城市自身模板在断网/总督调离后保留，征服后应随城市成果归新Owner；派生模板并集必须从新Owner当前有效网络重新计算。

建议键SPC_STANDARDIZATION_LEDGER_V1，字段：schema、稳定cityUID、catalogRevision、revision、learned。learned以具体BuildingType索引，保存首次有效获得时的district/tier、evidence、learnedTurn。最初证据不被重复事件覆盖，只有首次新模板增加revision。模板组按district+tier查询；保留具体建筑证据便于查错与数据库迁移，不把获得某Tier写成获得所有更低Tier。

为何不只放隐藏建筑：隐藏建筑适合可撤销的折扣标记，永久模板原件还需要版本、城市身份和首次获得证据；为每组建一个建筑反而依赖数据库定义及建筑移除生命周期。必要时可从Property派生临时内部建筑，以挂载Modifier，不能反过来从旧内部建筑推断永久掌握。

## 本机层级证据

HD UpdateDataBase/HD_BuildingTiers.sql构造HD_BuildingTiers(BuildingType,PrereqDistrict,Tier,ReplacesOther,Tag)，按BuildingPrereqs推导层级，市中心Tier0，排除HD dummy，另有宗教建筑例外。当前只读DB有167条；过滤InternalOnly/IsWonder，当前四类标准区域共有50个建筑，16个district+tier组。不能把所有Tier0市中心建筑自动视为同组。

| 区域 | Tier1/2/3/4建筑数量 |
|---|---|
| Campus | 2 / 4 / 4 / 3 |
| Commercial Hub | 2 / 3 / 4 / 3 |
| Industrial Zone | 2 / 2 / 3 / 5 |
| Theater | 3 / 2 / 5 / 3 |

这是本机分类调查，不是用户已经批准的新适用清单。其它区域、特色替代区域、未知/缺Tier应显式未分类；不能按成本猜Tier或仅用RequiresPopulation猜建筑组。保存分类版本，数据库更新后检测迁移，不静默把旧成果移到另一组。

## 与当前网络分离

每次读取当前有效Industry来源，分别取：永久模板并集、ACTIVE等级对应最大折扣、Lv4实际Production最大输出。不同模板提供者和最高折扣提供者合法：来源A拥有模板且ACTIVE1，B无该模板但ACTIVE4，接收城仍可对匹配建筑获得40%候选Gold折扣。A断网后资格消失，即使B仍在；A自己的账本不删。

DevelopmentTests/StandardizationLedger.lua仅实现离线契约：Record需要调用者明确authorized+completed+evidence，不擅自确定学习触发条件；ForRecipient仅接收当前有效source集合，拒绝缺失账本而不充空，Discount只返回候选Gold百分比。无事件注册、City Property写入或购买Modifier。实际稳定UID/跨owner继承仍是现有工程边界，不能用owner:cityID代替永久身份。

## 当前学习规则及剩余边界

IND-NET-004已由用户在D0013确认：合法获得/完成均记录，首次成为Industry一次补录，以后事件增量，不持续全城扫描。购买/免费获得与首次既有建筑补录不再DESIGN_DECISION_REQUIRED。未改下方离线Record契约，因此未来调用者仍须在当前引擎事实复核后提供authorized/completed/evidence；模型本身不注册事件。

DESIGN_DECISION_REQUIRED仅保留尚未明确的允许建筑目录/特殊分组，不能将上文50条统计自动当已授权适用清单。技术上需安排旧已Industry城市的新初始化标记迁移、事件覆盖与稳定UID支持范围，不以“补历史第一次完成”为理由否定用户已接受的一次既有建筑补录。

本报告原D0012时提出的学习时机问题已被D0013取代；原文备份在DevelopmentBackups/Specialization-before-fresh-agent-handoff。

## Gold-only限制

当前本机EFFECT_ADJUST_BUILDING_PURCHASE_COST实例只有Amount和BuildingType参数，未查到指定货币的用法。该事实既不能证明会影响Faith，也不能证明Gold-only。下一步需独立比较同一可双币购买建筑的Gold/Faith价格；不添加猜测YieldType参数，不采用退款，不改变购买资格。离线Discount只返回Gold不是原生Faith隔离已通过。

## 验证

STATIC_CONFIRMED：上述表结构/分类/参数查询，使用只读DB。LOCAL_SIMULATION_PASS：重复记录、同区域同Tier、跨区域不混、跨Tier不混、不同来源模板与折扣、来源撤销、城市成果换owner继续保留、旧owner拒绝、非授权不记录。真实征服继承、学习事件和购买价格尚未实机验证。本轮不为标准化派游戏测试。
