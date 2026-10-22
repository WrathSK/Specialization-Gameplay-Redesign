# B168.195 — 巨作启迪原生实例诊断与末档退出修复

Date: 2026-10-06
State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED
Baseline: B167.194 source208ded2；八图反馈见[B167](Specialization_B167_Inspiration_Native_Feedback.md)。本批已获用户授权修复，完整自动L3未授权。

## 修复与接口范围

末档+1后再次NEXT正常执行同一module-owned撤销并结束，重复token不重启；任何阶段仍可用独立END。移除失败保持目标/档位及错误，禁止假报OFF。报告先显示档位、载体和下一操作，不再把末档完成显示成错误。

原生诊断只在右键READ、END或末档NEXT退出时调用。复用既有GameEffects GetModifiers/Definition/Owner/ObjectsPlayerId/ObjectType/ObjectString/Active/Subjects模式，精确匹配四个SPC_INSPIRE_PROBE定义ID；显示原生Amount与已校验定义Amount、class、Active、Owner与有限Subject原始证据。原生Object ID不能当CityID，本批不新增未经验证的格式解析；计数是本玩家/玩家未知范围，不冒充本城专属率。Active不证明入账，载体0不证明原生零残留。

倍率仅列当前DynamicModifiers明确为EFFECT_ADJUST_GREAT_PERSON_POINTS_PERCENT、Scientist或未限定class的原生候选；外国Owner如果Subject指向本玩家或Subject未知仍保留相应证据。无法读取Subject/Owner/定义/字段时INCOMPLETE，不把未知当无关。有效总倍率未确认，不求和候选或由+1→+2反推200%。本批没有发现可靠城市基础GPP/有效总倍率getter。

完整枚举上限32768，Subject64；测试与倍率各最多展开8实例、每项最多2Subject；文本字段192字符。保留一个token/reference/turn响应文本，重复ACK不重枚举；新明确请求/不同回合重读；原始实例/对象/数组不跨请求保留。无周期事件/每帧业务扫描、永久历史、Property写入或GC调整。API或全国率不可读仍明确UNKNOWN，不能假报零或假算差值。

## 本地检查

现有L3-A定向入口`DevelopmentTests/test_culture_inspiration_probe.py`：39方法PASS（原29＋本批10）。新增覆盖末档正常退出/重复token、移除失败保留与独立END重试、原生参数与配置不一致/多旧实例、请求缓存与reference、API/稀疏/未知字段、外国百分比来源/Subject未知、END后原生残留、输出有界。继承原本精确owned退出、UNKNOWN、保存/加载、其它城市与6项B166Meaning回归。

外部DebugGameplay.sqlite只读复制到内存；只重建内存中精确四测试定义以适配已部署B167缓存，无外部DB/旧断言修改。Lua语法、实际SQL/注册/XML、当前文档引用与context/hash、diff分别检查；不跑全历史回归/stress。不把本地模拟当原生精度、倍率或内存证据。

## 一次最小实机内容

一个现有Culture ACTIVE IV城、一个连续session：

1. 左键准备0档，右键读取基线与诊断。
2. 连续左键到整数+1档，中间不要求截图；右键读取。若未刷新，可按已观察的延迟过一个回合后再右键读取，保留回合。
3. 点独立“结束启迪测试”，或在+1档再左键一次；确认配置载体0，右键核对原生实例。若全国率延迟，再按实际刷新时机读取。

这三步分别回答整数入口/原生参数与倍率来源、旧实例替换/退出和实际读数。暂不要求重做0.1/0.3系列、保存ON/OFF/冷加载/重启；其它帝国来源变化仍限制全国率因果解释。

用户可能自行从不同存档在不同档位过回合提供补充信息；这不是本批测试步骤、门禁或强制工作量。反馈按加载来源、档位、操作和回合分别记录，不跨存档直接相减归因，也不要求补齐所有组合。

## 停止点

B167小数结果仍UNRESOLVED。修复不启用Floor、不发正式六class/D/W收益，不改Design、永久账本、HD、Meaning、GC、main或其它Culture批次。既有W0003门禁核对后可部署此原型；实际receipt/source/live查[Status](../../Specialization_P0_Status.md#current-authoritative-state)，本地完成不证明已部署或原生PASS。
