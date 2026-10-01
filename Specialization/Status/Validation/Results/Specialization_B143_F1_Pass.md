# B143.170 P0-F1 限定实机验收

日期：2026-10-01（America/Vancouver）。依据运行截图B143.170及既有部署记录source fa9fcd4 / receipt B143.170-fa9fcd4-playtest.json。本轮不重新检查外部运行包、不部署。

## 观察与结论

逐张读取两张原图：

| 截图 | 可见事实 |
|---|---|
| Screenshot 2026-09-30 at 11.54.03 PM.png（原名PM前为空窄间隔） | 游戏T47；报告首次P4=T47、age0、累计中；Potential4 / ACTIVE1；预期+5%，下阶段10回合、还需10；明确未施加科技收益 |
| Screenshot 2026-09-30 at 11.56.04 PM.png（原名PM前为空窄间隔） | 游戏T49；首次P4仍T47、age2、累计中；Potential4 / ACTIVE1；预期+5%，下阶段10回合、还需8；仍为影子 |

用户明确确认“验证通过……冷重启后保持”。冷重启保持按用户实机陈述记录；不从两张截图时间顺序推断重启发生位置，也不声称画面证明同回合重复读取零写入。

**USER_GAME_TEST_PASS（用户实机已测范围）**：本城首次科研P4起点、ACTIVE1时跨两个回合累计、影子5%与下一阶段显示、用户确认的冷重启保持。F1最小门禁关闭，无需重复本测试。

未外推：实际科技收益尚未接入；10/20/30/40与其它速度仍是本地模型证据；未测试转专业动作、跨Owner传统归属、旧P4起点补录或所有异常保存场景。F1原实现/模拟依据见[当前F计划](../../../Architecture/v2/P0_F_Research_Tradition.md#b143170--f1-implementation-and-validation)。

## 原图归档

外部W/Specialization/Status/Validation/Evidence/B143_F1_Pass_20261001/ 保存两原图及manifest。2/2移动前后SHA256一致，收件箱保留，原图不进Git：

- 11.54.03：`1de1fb0cf612d1986fbbbc8fc9d4e4fda04cb8a47d0bff7903e46c7e414964c8`
- 11.56.04：`16ac624747d42e35a3c18074509a7552a5efcd2ba62b3929a032974cb458a46b`

下一步仅提出F2实际科技收益计划，等待明确实施授权。Design、runtime、main与GC策略不变。
