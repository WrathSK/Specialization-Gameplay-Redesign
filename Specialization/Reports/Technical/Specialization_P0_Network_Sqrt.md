# Boost适配：sqrt与Modifier精度

Document Owner: Codex
Document Role: TECHNICAL_REFERENCE
Design Rule ID: NET-RC-001至005 / OPEN-06

Lua可计算浮点sqrt；数据库TEXT可存储不代表引擎接受小数或动态表达式。未来BoostAdapter需明确Amount精度、触发时序与溢出边界，整数取整不得默定。离线NetworkStrength.FromState已消费当前拓扑并完成多源max聚合；给定L与拓扑集成测试均已通过。仅限MOCK_ONLY，不代表动态Modifier可用；结果见Status。

WHAT、数值与作用范围仅引用[Accepted D0001](../../Design/Specialization_v0.1_Design_Spec.md)的上述Rule IDs；技术契约见[Architecture](../../Architecture/Specialization_v0.1_Architecture.md)，不在这里复制公式/档位表。
原始研究和当时限制保留在[冻结原件](../../Historical/LegacyReports/Specialization_P0_Network_Sqrt.md)；当前验证以[Status](../../Status/Specialization_P0_Status.md)为准。
