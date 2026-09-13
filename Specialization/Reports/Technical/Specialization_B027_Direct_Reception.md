# B027：D0009直接接收适配与Commerce IV初步调查

Document Owner: Codex
Design Spec: D0009 / ACCEPTED
Architecture Revision: A0060
Implementation Build: P0-B-027 / modinfo34

## 已实现与验证

NetworkBridge.lua在完整重建direct source集合（含首都天然自接入）后，将中心自身并入各类recipient，再合并distribution。仍按城市去重，recipient不会反馈为direct source；重复重建全量替换，无新Property/Modifier/网络收益。现有DEV Lv1身份范围不扩大到通用ACTIVE/资格或Commerce IV。

LOCAL_SIMULATION_PASS（本地模拟，不等于游戏通过）：test_d0009_network_runtime.py加载真实运行模块，覆盖无路线科研首都自接收、直接接入中心、同城多路线去重、接收中心不递归、direct/distribution重叠与撤销后保留、最后来源移除、空集合重建、污染缓存跨新加载重建、旧序号/部分批次拒绝；检查全部Lua语法、XML及UUID/modinfo文件引用。

test_background_network_sender.py回归通过：后台采样自动提交、不依赖可见贸易UI。两组输出见备份verification.json。不扩大为实际游戏证明。

旧DevelopmentTests/NetworkState.lua及其D0005/旧multisource fixture仍是旧语义离线原型，本轮未接入运行，也未声称符合D0009。后续离线统一适配仍在待办；原test_network_bridge.py与B026计数wrapper的旧N/版本断言由本次新运行测试替代，不能直接用于当前包验收。

## Commerce IV：读取先例与缺口

STATIC_CONFIRMED（本机源码证据）：

- HD `2465378070/UI/Replacement/CitySupport.lua:316–332` 使用city:GetYield与GetYieldToolTip展示总产出，没有在这里排除Specialization输入；展示值还截断至一位小数，不能作为精确basis。
- 同文件UpdateCityYieldToolTip（约787–835行）调用CityYield.GetYield按来源拆分tooltip的modifier行，是文字展示，不是引擎本地自产分解API。
- HD `2465378070/Gameplay/CityYield.lua:42–64` 的GetYield读取城市Property中按sourceType记录的追加值；它只知道使用该账本写入的项目，不能当成城市所有输入的完整账本。
- 同文件ChangeYield与GetModifierList（约67–131行）按差值AttachModifierByID，记录名义输入；`UpdateDataBase/DL_City_Yield.sql`使用MODIFIER_SINGLE_CITY_ADJUST_YIELD_CHANGE。生成modifier名称的方式要求实际数据库存在对应amount；不能由Lua小数能计算就断言所有小数可应用。

准确结论：有按来源记账的本地先例；目前检查到的路径没有提供COM-006要求的现成精确basis。尚未证明该设计不可实现，不选择fallback，也不依赖tooltip解析。

下一研究应追踪本Mod未来跨城输入承载的百分比作用层：若最终yield为(local+input)×倍率，仅减input会残留input的倍率部分。用示例100 local、20 input、+50%时最终180，减20得160而纯local应150；这是数学反例，不声称游戏所有yield统一按该顺序结算。需要分别调查S/C/P的原生分解及承载影响，才能选择等价的输入扣除方式。不得为采样临时拆装收益，也不能用区域Actual替代city local basis。现阶段不注册汇聚收益或改动HD代码。

## 用户测试与待办

[B027一个最小测试](../../Status/Validation/Cases/B027_Direct_Reception.md)仅核对D0009新接收语义。旧可读性/断路实机批次依用户要求继续延后；B010不重发。商业IV basis研究不阻塞此项直接接收验证。原八图/Design/SQL/自动Lv1收益实现保持不变。
