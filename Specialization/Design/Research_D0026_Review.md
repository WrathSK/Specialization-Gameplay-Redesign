# Research D0026 — 冻结审阅记录

Document Owner: Codex
Design Authority: User
Design Revision: D0026
Document State: ACCEPTED
Freeze Status: DESIGN_FROZEN
Implementation / Balance Validation: PENDING

## 当前结论

[canonical content](Content/Research_D0026.json)为唯一新Research规则与首版Tooltip正文；[schema](Content/README.md)定义机构/能力/基础支持/映射的规范化结构。四机构永久累计、命名能力0→1→2→3。用户明确关闭本轮五组问题，Research没有剩余冻结阻塞。

## 已确认边界（原RES-OPEN-01至05关闭）

1. Lv3使用映射领域；特色替代归一，未完成/被掠夺不计入；未知类型排除并提示，不阻塞。需要提示的未映射类型例如航空港、保护区、娱乐中心/水上乐园，不自行赋yield；本轮不新增数据库调查或兼容实现。
2. 不同类型映射同yield时分别贡献并相加。
3. Infrastructure Value逐建筑计值，学术主持亦逐建筑；同Tier重复不是强行忽略项。四建筑五专家的50/20是示例，不额外新增全局上限。
4. 传统阶段按游戏速度同比缩放，各绝对阈值独立floor；不先取整速度或把取整后的10T连乘。传统持续年龄与当前ACTIVE分开。
5. Research所有等级保持额外3F3P，取消旧三级5F5P提升；其它专业不变。

## Tooltip comprehension自审

输入/输出：三级BASE→Science；其它领域→专家mapped yield；四级Tier→专家Science、专家→建筑Science。BASE不是Actual。X去重TYPE、同yield相加。机构不是普通建筑，技术载体不进入玩家文案。传统25%封顶，永久Potential起算且按速度缩放，ACTIVE只控制启用。主持Science不反馈Infrastructure。英文参考/TBD与社区Food默认候选均按用户要求不阻塞。

## 内容例子检查

- 工业区+军营：X=2，每名专家各得2P，相加4P。
- 工业区+商业中心：X=2，每名专家2P+6G。
- 1/2/3/4各一普通学院建筑：V=10；5专家提供50基础Science；主持另加20。
- 若多一座Tier2：V=12，5专家提供60；主持5建筑×5=25；无相互递归。
- 标准速度传统阈值10/20/30/40；0.67速度阈值6/13/20/26，分别直接floor原阈值乘速度。

## 修订与实现边界

旧RES-003人口科研与5F5P、旧RES-004专家百分比/全非Campus Actual复制退出新Research Design，不与新能力叠加。Research Network及其它专业不变。D0025原文冻结，Architecture尚未sync D0026；运行B076.103未改变。设计检查不等于技术可行性或游戏验证。旧存档传统起算迁移与实际API承载属于后续架构审查，不能捏造历史时间。

本轮无Gameplay/UI修改，无部署、无游戏启动、无Batch E。只提交Design内容，等待用户审阅后续Implementation授权。
