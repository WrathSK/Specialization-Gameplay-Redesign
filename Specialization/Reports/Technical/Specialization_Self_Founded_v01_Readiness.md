# 自建城市范围 v0.1 实现盘点与所有权模块暂停评估

Document Owner: Codex
Review date: 2026-09-13
Runtime reviewed: B066.92 / modinfo92
Design reviewed: D0025
Scope: 只用固定Specialization测试文明、从有效建城记录开始、自建城市不发生任何易主；不是正式删掉Accepted Design的征服规则。

## 结论

此限定范围内，四专业核心玩法主线基本实现，可以进入可玩测试版收尾，不需要先完成Conquest/Claim。不能把它称为完整D0025或所有组合均原生验证。用户以Cheat测试机制为主，无需以完整长局/极端故障矩阵阻塞此阶段。

| 能力 | 当前情况 |
|---|---|
| 首个合法区域完成锁专业；移民投资至Potential4；总督决定ACTIVE | 已运行，有此前用户正常路径证据 |
| 四专业Lv1–3，住房/GPP/人口与网络专家收益 | 已运行；此前用户按批次通过；已接受原生刷新延迟 |
| Research IV专家百分比/全非Campus区域Actual复制 | 已运行，扩展范围用户通过 |
| Industry IV输出、标准化永久模板及网络最高折扣/模板并集 | 已运行，用户对应批次通过 |
| Culture IV专家百分比/时代对话/巨作BASE相邻 | 已运行；GW相邻用户通过，逐件截断接受；D0025将系数改25%，用户免新实机测试，不标25%新版实测 |
| Commerce IV直接源最高20%最终floor | 已运行，Science/多源/撤销用户通过；Culture/Production单独实测由用户接受暂缓，不标实测 |
| 首都/商业贸易中心、源接入、全部网络分发、不递归转发 | 已运行，有用户正常路径证据 |
| Research/Culture Boost | 正式k1/max L/sqrt N/最终一次floor(x+0.5)已运行；接口实测已有，最终封顶仍OPEN-06 |
| 五档Crew、速度缩放整数、位置/预览/确认；移民单位按钮 | 已运行，用户按批次通过 |

## 此范围仍需收尾，而非新增整套专业能力

1. BindingProbe.lua现有DEV counter<=32，foundation要求counter<32；它是每玩家累计分配编号上限，不应误写成只有同时32城。正常铺城也会触及，需明确解除/替换此开发限制后才适合作为无限定建城版本。
2. P.IsTestPlayer当前硬编码CIVILIZATION_SPC_TEST+LEADER_SPC_TEST。满足当前固定载体测试，不等于ELIG通用opt-in已完成；如果首个可玩版本只开放测试文明，可后置泛化，但要明确发布范围。
3. 玩家说明、专业/网络可读入口、默认自动模式与诊断按钮收尾；目前存在P0名称/诊断工具，不把机制能运行当正式UI已完善。
4. 只补真正影响所选范围的整体验收；商路正常到期、取消/掠夺的全部组合并未由此前删城市或用户一般PASS覆盖。无需重做所有旧批次。城市完全不易主也不等于贸易路线永不变化。
5. Boost最终封顶等既有OPEN及各种承载目录限制如触及仍需如实报告；已接受的小数截断/住房GPP城市面板延迟不作为待修bug。

Future专业/Entertainment/Spaceport等不属于当前v0.1，不因“收尾”扩大实现。

## B066新回报与按钮说明

用户口述Read shadow / events显示“尚无该城市的已确认转移记录”。这是CityInheritance.Describe读取shadow.watch[pid]的UID后找不到对应转移登记的分支；不要求选中AI城市。用户可选任意己方城市开P0，观察目标在转出前由Select shadow city保留。

该分支未区分watch缺失与转移登记缺失，并提前返回，遮住了原shadow事件明细。属于诊断可读性缺口；当前不能仅凭提示确定事件没触发、签名不匹配还是观察UID未选定。原始备份可能仍存在，提示本身不说明投资已从Game账本丢失。

USER_GAME_TEST_FAIL只限B066本次无法提供预期确认转移状态；未得到APPLIED/恢复证据，不扩大为所有恢复均失败。B064备份/读档PASS、B065回调口述PASS不撤回。当前不追加操作要求，先由用户确定是否暂停此范围。

## 暂停开发与禁用运行不同

停止编写B066不会自动停用它。Mod/Gameplay.lua仍Start CityInheritance，BindingProbe.Resolve每次先查新Game转移登记（读/克隆表），InheritanceShadow仍加载时一次扫描和永久写入后同步备份，转移/建城事件监听仍活跃。研究代码已有正常路径回归，静态看不易主且无旧转移登记时新Restore不会执行，原Binding可回退原路径；但不能断言零成本/零回归风险。CityInheritance.Resolve读取错误也可能传播到现有严格读链。

建议若采用自建城市可玩版：可逆地停用自动转移恢复及其Binding override，保留源文件和冻结证据；备份观察可独立关闭或仅保留低频同步，不依赖它提供正常收益。保留B062商业四重做成果及D0025时代对话25%，不要粗暴整体回滚到B060。停用前检查存档是否已APPLIED/PROJECTING依赖继承绑定；对这类存档不能承诺直接删模块后正常，优先易主前自建城市存档。

本轮未禁用、未回滚、未部署、未改Design。源码/运行hash仍41d938283f8e57f623ab3172f2c50dab98f9057f0523ca265d3b47c88ccd23ce。下一步由用户确认自建城市发布边界后，单独处理隔离与收尾。
