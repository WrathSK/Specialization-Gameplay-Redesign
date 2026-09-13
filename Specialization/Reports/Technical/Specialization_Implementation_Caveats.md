# 实现限制与不要重复的调查

Document Owner: Codex
Role: technical evidence index; current task/validation only in Status

| 结论等级 | 经验与行动 | 证据 |
|---|---|---|
| 用户失败，限特定路径 | B029/30固定city YieldChange小数Amount未出现应有半点；不能重用整数载体假装精确20%或sqrt；也不能推出所有getter/Modifier只存整数 | Results/B029_Fractional与B030；[精度报告](Specialization_Fractional_PerPopulation_Evidence.md) |
| 用户通过，限测试场景 | per-population 0.5有效，B050人口3/4组合及B051工业4.5/科研半点有效；255人口仅数学/mock覆盖 | [B050结果](../../Status/Validation/Results/Specialization_B050_User_Result.md)、[B051.66](../../Status/Validation/Results/Specialization_B051_66_User_Result.md) |
| 用户观察，非全局精度定理 | Getter样本在1/256网格，宜居度影响最终差值；不能因此设全局floor/round或把.45判半点丢失 | [人口证据](Specialization_Fractional_PerPopulation_Evidence.md) |
| 用户失败/新局通过，初始化候选 | B029旧档Property和SQL存在却无效果，新局整数有效；只查GameInfo不足以证明实例挂载。不是所有新SQL都必须新局，后续旧档案例应个别验证 | [旧档](../../Status/Validation/Results/Specialization_B029_Old_Save_Failure.md)、[新局](../../Status/Validation/Results/Specialization_B029_New_Game_Result.md) |
| 原方案失败，修正成功 | 总督晋升只即时读可能早于事实更新；保留GovernorPromoted和发布后复核。不要借GPP可延迟理由删此修正 | [B037](Specialization_B037_Governor_Promotion_Fix.md)、[用户通过](../../Status/Validation/Results/Specialization_B037_Promotion_User_Pass.md) |
| 接受延迟，勿修/勿重测 | 住房载体撤销后UI可等下一回合/其它刷新；GPP carrier4→2而getter/UI18→下回合12。不能断言纯UI或实际结算层；已明确不修 | [住房](../../Status/Validation/Results/Specialization_B034_User_Result.md)、[GPP](../../Status/Validation/Results/Specialization_B035_GPP_Refresh_Note.md) |
| 有效替代接口已验证 | 城市总督依原生requirements驱动Property present/established/req2–4，不把全国已花头衔当本城等级；原Lua getter错误不必重试 | Data/GovernorProbe.sql、Probe.CityRoleFacts；历史Status确认 |
| 研究未找到，非绝对不存在 | Gameplay任务/计数不能给可靠当前端点全集；GetOperationParameter端点nil，符号/Modifier受限集合不构成全路线API | [第二轮审计](Specialization_Trade_Authority_Second_Audit.md) |
| 已接受实现方向 | City UI当前路线可后台读，无需窗口；BTS历史last-route不能当现在路线。游戏侧CountOutgoingRoutes是Count，不是GetOutgoingRoutesCount，也不是全集 | NetworkBridge/BackgroundRoutes；[计数修正](Specialization_B026_Trade_Count_Fix.md) |
| 用户失败后调度改进 | B051.65正式目标未知/配置0，UI候选有3；66加引擎事件+初始化fallback后用户回报正常。不能由此证明所有空context的SetUpdate永远无效 | [诊断](../../Status/Validation/Results/Specialization_B051_Copy_Diagnostic.md)、[修正](Specialization_B051_Background_Fix.md) |
| 设计已澄清，旧限制不要恢复 | D0014不按四专业/RequiresPopulation过滤Research IV；66的SCOPE_UNRESOLVED是旧限制，不是后台断线；67新范围待用户复验 | [D0014](Specialization_D0014_All_District_Copy.md) |
| 反例已证明，实际接口未完成 | 先采集再写/绝对覆盖仍可跨回合反馈；从有倍率总量减名义输入不等于纯本地。研究总量备选已获条件授权但未采用 | [Commerce IV](Specialization_CommerceIV_Basis_And_Cycles.md) |
| 稳定历史边界 | DONE/现有区域不能证明没漏通知；普通匹配存档可恢复，不凭旧缺失表猜首个区域。极端丢写暂后置，不能借此阻塞每个正常玩法 | [正常恢复](Specialization_B021_Normal_Load_Resume.md)、[反例](Specialization_Load_History_Ambiguity.md) |

只把Crew量化按D0012的共同函数处理；不要将其floor授权扩到其它收益。不要因读取所有区域的复制基数而实现Religion/Community等Future专业。

代码注释并不总是当前模块描述：BackgroundRoutes开头仍写无Gameplay请求，实际已加载NetworkSender；NetworkBridge无收益指本模块不发奖，消费者会用其来源发奖；Probe/DEV文件已有真实写入。这些注释本轮未改，Architecture已给真实调用关系。
