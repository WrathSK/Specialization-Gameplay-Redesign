# P0-U1 提前实施计划 — 当前机构与技术载体隐藏

Status: PLANNED_NOT_AUTHORIZED。用户只授权先出计划。Baseline B086.113/modinfo113，P0-D3用户整体PASS；不扩大为逐项边界全部验证。
Authority: D0035 Shared；Research D0031、Industry D0032、Culture D0029、Commerce D0032；A0161；PAC-R0002累计、presentation-only原则。旧PAC的B076 carrier清单只作历史参考，实施时按当前SQL注册重新盘点。

## 1. 提前范围与依赖

本次建议实施U1的当前机构部分及本Mod技术carrier隐藏。四专业每个已达到Potential的等级独立展示：Current Identity + Potential决定1..P机构；ACTIVE只控制对应能力状态，不删除或降级机构。Research P4同时显示学者结社、研修院、学术联合会、学术总署。其它三专业名称/描述直接取各自当前canonical，不将旧候选名升级为新的命名决定。

U1历史机构部分保留在总计划，等待明确Historical State及保存合同；本批不从残留carrier或曾达到的ACTIVE猜历史，不新增存档字段。不等待所有专业玩法完成；但未实现能力不得显示为已生效。U2 Culture Hybrid D、U3 Commerce行动面板不进入本批。

## 2. 玩家界面与信息层次

优先在城市详情对应专业区域的普通建筑列表后增加独立“专业机构”小节。复用原生样式和现有图标，按Lv1→Lv4排列；无需新美术。条目不是GameInfo Building，不可生产、购买、出售或修复；不计普通建筑数、HD Tier、模板、基础设施深度。

每条Tooltip只包含机构简介、本阶段新增named abilities、当前状态。一级基础专家支持单独简述，不强造named ability；IV不重复塞入II/III全部能力。状态分别表达：已实现且当前生效、已实现但ACTIVE不足、本测试版尚未实现、数据暂不可确认。未实现条目可说明冻结设计，但不报虚假实际收益；旧Culture/Industry/Commerce效果不能直接改名冒充新设计。对已有临时floor实现明确实际取整口径，不修改Design。

ACTIVE不足用简短状态文字配合灰化，不只靠颜色。未知数据保留上次已确认内容并标待确认，不能显示为Potential0或删除机构。能力状态还须遵守各能力资格，不能只用等级阈值判“已生效”。动态收益只能读已确认输出，缺少安全读取时只显示规则和状态，不为Tooltip跑一次Audit。

## 3. Carrier隐藏边界

先建立当前Mod SQL/manifest产生的精确技术Building集合，覆盖支持、住房/GPP、Network、旧效果残留、bit/correction、Research C/D1/D2/D3等。只过滤本Mod明确internal对象，不笼统隐藏其它Mod建筑，不把普通基础设施误判为carrier。

| 界面 | 目标与验收 |
|---|---|
| 城市详情/区域建筑列表 | 不列技术建筑，普通建筑不变；机构另列 |
| 区域/地块建筑Tooltip | 不泄漏carrier名称；保留真实普通建筑/收益信息 |
| 生产/购买列表、百科 | 检查现有InternalOnly过滤是否已足够；已隐藏则不重复打补丁，存在泄漏才做最小局部过滤 |
| 开发诊断 | 仍可按需查看原始配置；普通机构Tooltip不展示技术ID |

隐藏是显示过滤，绝不RemoveBuilding、禁用Modifier或关闭writer。不要修改共享CitySupport数据使其它系统误以为载体不存在；在显示投影层过滤，显示数量与可见行一致但不改引擎建筑计数。旧效果即使Design已淘汰，未到对应cutover也不能借隐藏提前关闭。

## 4. 数据与UI合同

复用CurrentSpecializationFacts/EffectiveFacts只读权威及现有CITY_PRESENTATION_READ入口，扩展为确认的city reference、epoch、input revision、Identity/Potential/ACTIVE/validity及能力实现状态。UI仅保存有界的当前城市/已打开面板快照，不保存Gameplay权威。

静态现状：CityPotential.lua已有0.5秒SetUpdate轮询，dirty时才发送；现有Gameplay返回Potential等但没有完整ACTIVE/epoch合同。不能宣称当前已是零轮询，也不能再建第二套后台轮询。U1范围内整合旧badge与机构展示的同一只读快照；打开/选城/相关确认事实变化刷新，关闭界面不发请求；hover只读缓存。替换该presentation专属轮询，不顺手重构其它后台模块。

同一城市同一版本单flight，重复通知合并，旧epoch/旧城response拒绝；同输入不重建实例。只在面板打开时有界重试/必要回合兜底，不周期扫描全国。缓存和控件池有上限，关闭/切城释放，load清旧引用。读取请求不触发Network derive、Building/Property写或正式Audit。

## 5. 实施步骤及hook门禁

1. 当前carrier/能力实现状态盘点，冻结UI过滤清单和四专业stage映射；普通建筑反例纳入fixture。
2. 在实际启用的原版/HD CityPanelOverview与Tooltip加载链核实安全插入点。现有PAC静态证据表明不同surface各有过滤，InternalOnly不是通用隐藏保证。使用本Mod扩展保留原始函数链，不覆盖安装的HD/其它Mod文件，不建立大份原版UI副本。
3. 完成只读presentation快照、旧badge共用与累计机构render；再接精确隐藏过滤。入口位置、缩放、HD覆写均为PROTOTYPE_REQUIRED，尚未实机确认。
4. 回归/最小实机候选交付。若无法安全嵌入对应区域小节，报告具体限制和候选位置；不静默改成真实Building或大规模UI替换。

预计触及：Mod/UI/CityPotential.lua及必要XML、新机构read model/本ModUI扩展、Gameplay.lua只读dispatch、Localization、modinfo注册；必要事实变化通知仅发布变化，不改玩法。实际文件由hook门禁确定。无收益SQL、carrier增删、Design、永久state迁移。

## 6. 本地验收

- 四专业Potential0–4累计行数/名称/阶段映射；ACTIVE下降机构保留，能力状态改变；未实现和未激活严格区分。
- UNKNOWN、换城/旧response、load/epoch、城市引用失效、打开关闭不串城；不凭空造历史。
- 精确carrier集合全覆盖与普通/特色/其它Mod建筑反例；UI过滤前后Gameplay收益配置、普通目录/D/住房/GPP完全一致。
- 10000无关通知/hover/idle callback：无新增Gameplay请求、全国facts capture、Network derive或写入；重复同版本不重建控件。反复开关/切城后缓存和实例数有界。
- 字符串中英fallback完整，不显示空白按钮、LOC键、bit/Modifier ID；长Tooltip换行与两档缩放另由UI实机验收。
- P0-A/B1/B2/C/D1/D2/D3及Architecture v2受保护回归，Lua/XML/manifest、部署安全。STATIC/LOCAL_SIMULATION不能代替HD界面实测。

## 7. 最小用户测试与退出

实施通过后合并一次短测：已有Research IV城打开区域详情，确认四机构累计、普通学院建筑保留、carrier行消失；hover检查阶段能力及学术传统未实现标记；已有可控方式降低/恢复ACTIVE，机构不消失；切换另一专业城市再返回确认不串城。顺带看区域Tooltip与生产列表，不要求为此造新城市或掠夺。若容易切UI缩放再检查一次；否则记未测。静置与旧诊断对照无刷新声浪、无高频请求。无需当前开始测试。

完成条件：上述本地合同通过、现用HD入口可观测、实际隐藏surface列表明确、无收益/权威改变；commit/push。用户实机通过后只接受所测展示，不称全部未知UI组合兼容。
回滚边界：完整B086运行包和切换前另存；本批无新保存state，无carrier生命周期迁移。未来部署仍须W0003退出/备份/hash门禁；本轮不部署。

## 8. 当前结论

无新增Gameplay设计问题阻塞U1当前机构部分。技术门禁是HD/native hook及展示兼容，不是新玩法。历史机构未完成应明确保留，不能把本次称为U1所有历史能力完工。停止等待用户授权P0-U1当前机构/隐藏实施；不自动进入U2/U3、P0-D4或E。
