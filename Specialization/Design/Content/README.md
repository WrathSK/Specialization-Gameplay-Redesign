# Specialization content schema v1

Document Owner: Codex
Design Authority: User

[Research D0026](Research_D0026.json)是Research Lv1–Lv4的唯一结构化内容正文，保存已冻结的机械合同、第一版中文Tooltip及领域映射。状态为 **DESIGN_FROZEN / implementation and balance validation pending**。Accepted Spec的RES节引用此表，不复制另一套新公式。仅Design冻结，不代表运行包实现。

[Industry D0027](Industry_D0027.json)沿同一结构扩展`parameters`（值与BALANCE_REQUIRED分离）、`contracts`（模板/历史/施工队范围）、`review_markers`（已确认但以后复审）、`superseded_old_rules`。Industry为DESIGN_FROZEN，候选命名和待平衡参数保留独立成熟度。

## 规范化表与本地化

- `institutions`：specialization、level、稳定institution_id、中文名、英文参考、RP简介、Potential门槛、状态及ability_ids。每个机构只记录一次。
- `abilities`：稳定ability_id→institution_id；名称、Tooltip、mechanical_contract、input_facts、output_effects、ACTIVE/Potential门槛、状态、notes_compatibility与待决引用。
- `base_effects`：无named ability的基础效果。Lv1不强造能力名称。
- `yield_mapping`：学以致用的统一领域→产出映射及价值换算；不从Tooltip反推映射，不把它隐式当其它能力的区域白名单。
- `district_qualification` / `decisions_resolved`：共同区域资格与本轮已关闭边界；未知类型按已确认默认排除并报告。

中文是正式语言目标，英文名仅reference；`null`表示TBD，不是空白发布文本。未来增加en_US Tooltip或语言键，不改变Mechanical Contract。内容ID不依赖显示名称，也不是游戏数据库Building Type。

本表目前仅设计数据，不加入modinfo、不作为运行输入。机构与能力一对多，命名能力数量0/1/2/3。每个Tooltip解释本阶段新增能力，永久机构存在与当前能力启用分开。技术载体不出现在玩家文案里。

## 单一权威与修订

本轮的公式、文案、映射以JSON为唯一编辑位置；[审阅记录](../Research_D0026_Review.md)引用ID，不复制第二套权威公式。Accepted Spec的RES条目已指向content；D0025历史原文冻结不倒改。Industry已加入；其余专业后续沿同schema分别维护，不强制命名能力数量。各专业JSON是自身内容权威，Spec引用，Review只作审阅记录。
