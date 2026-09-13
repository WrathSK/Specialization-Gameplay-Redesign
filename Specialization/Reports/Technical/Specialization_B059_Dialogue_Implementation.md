# B059：时代对话自动百分比实现

Document Owner: Codex
Design: D0022
Build: P0-B-059.77 / modinfo77

## 实现

新增DialogueModel.lua（纯当前收藏计划）、Dialogue.lua（游戏侧资格/状态/载体）、UI/DialogueRefresh.lua/xml（无需打开UI的采集）、Data/Dialogue.sql（依据加载Eras总数自动生成D2至EraCount档位）。每档七类×文化/旅游共14项修正；ScalingFactor=100+15×(D−1)，Culture设置YieldType=YIELD_CULTURE，Tourism使用原生ADJUST_TOURISM，均限定GreatWorkObjectType。无per-work setter、无城市固定yield、无D7 cap。

普通作品从GreatWorks关联GreatPersonIndividuals.EraType，文物自身EraType明确例外；相同时代合并一次，Product/Relic/未知类型排除，缺失关联/时代拒绝该城计算而非猜时代。Collect记录全部当前city/slot/work type，游戏侧重新查DB解析D。UI是作品集合采样来源，不要求玩家开巨作界面；Gameplay不假装有独立原生作品全集枚举。

完整样本携带city空标记，校验当前城市覆盖、owner、唯一work ID、work type、turn/seq；拒绝过期/重复/不完整输入，撤销无可靠样本的效果，不保留历史最大D。100000字节仅传输保护，不作玩法上限，超出报错不裁剪。每城最多一个当前档位，移除旧档后加新，重复不写。ACTIVE4且Culture才应用；OFF是测试玩家临时全部暂停，AUTO恢复，读档回自动。

后台在加载/原生事件/两秒后备刷新中采集，签名相同且已确认seq不重复发送；签名包含当前专业/ACTIVE，避免只升总督却无作品变化时不刷新。Gameplay同时挂总督/回合/转移事件。读档初始化清理当前派生载体和旧B055手动巨作carrier；没有存成永久事实。当前支持测试文明本地玩家后台，完整多玩家同步/异常征服仍沿用项目边界，不外推所有场景。

旧GreatWorkBasis文件留作历史探针，但已不被当前报告调用。面板隐藏旧+2C和整数Boost实验按钮，保留Read Great Works、Dialogue OFF/AUTO及少量其它入口；实际产出读数增加IsBuildingThemedCorrectly计数。没有对theme做模拟或补偿。

## 验证

DevelopmentTests/test_b059_dialogue.py：只读外部DB复制内存执行SQL，时代目录/14项/ScalingFactor/原生Modifier类型/排除类别/manifest；真实Lua验证创作者Era与作品Era不同、文物例外、D9=120%、空集合、重复、后台无面板自动启动/签名幂等、总督门槛、作品移动、OFF/AUTO、重载清理、过期/缺失样本。B058/B055/B054/B052/B051回归通过。测试首次遗漏SPCP0全局，补齐实际Probe导出夹具后通过，未降低断言。

STATIC_CONFIRMED和LOCAL_SIMULATION_PASS不代表原生Culture/Tourism/theming已通过。实际ScalingFactor115在当前其它Modifier叠加下的结果必须由用户回传。缺失原生theming读取只报告unknown，不阻止收益；未开游戏、无commit/push。D0022hash未改。

## 文件

新增Mod/DialogueModel.lua、Mod/Dialogue.lua、Mod/UI/DialogueRefresh.lua/xml、Mod/Data/Dialogue.sql、DevelopmentTests/test_b059_dialogue.py、用户测试与本报告。修改Gameplay、Probe、manifest、P0Panel Lua/XML、BoostGreatWorkRead，Architecture/Status/Technical索引同步。旧测试冻结，源前备份ignored local/before-b059-77。

## 部署

B059.77 / modinfo77，103文件，source/runtime同hash `569dfb1ba6b6846be7eee5511dfef08b9c0f782b16d225e2b5b5dd97b51fa5f2`。旧运行留在外部SpecializationDeploymentBackups/.SpecializationP0-backup-wattw1tc；不在Mods扫描范围。
