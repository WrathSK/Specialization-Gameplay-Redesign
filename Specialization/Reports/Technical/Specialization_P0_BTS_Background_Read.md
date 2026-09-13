# 后台读取与执行上下文

Document Owner: Codex
Document Role: TECHNICAL_REFERENCE
Design Rule ID: NET-004

BTS/原版UI调用当前Outgoing；不必打开可见贸易窗口，但仍是UI上下文。独立后台探针以当前全集重建，事件只作dirty；不能因HD文件位于Gameplay目录就断言是Gameplay执行。正式权威provider仍受Architecture约束。

WHAT、数值与作用范围仅引用[Accepted D0001](../../Design/Specialization_v0.1_Design_Spec.md)的上述Rule IDs；技术契约见[Architecture](../../Architecture/Specialization_v0.1_Architecture.md)，不在这里复制公式/档位表。
原始研究和当时限制保留在[冻结原件](../../Historical/LegacyReports/Specialization_P0_BTS_Background_Read.md)；当前验证以[Status](../../Status/Specialization_P0_Status.md)为准。
