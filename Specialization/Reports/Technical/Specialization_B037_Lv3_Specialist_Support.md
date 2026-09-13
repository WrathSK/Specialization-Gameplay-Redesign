# B037 四类Lv3专家支持（部分Lv3能力）

Document Owner: Codex
Design: D0010 RES-003 / CUL-003 / COM-003 / IND-003 / SHARED-003
Build: P0-B-037 / modinfo46

本轮只落实四类专家支持档位，未实现Research/Culture的人口×专家Science/Culture、Commerce网络类型专家奖励、Lv4收益或Construction Crew。不得称为完整Lv3。

12个隐藏区域建筑/15条Building_CitizenYieldChanges提供Lv3相对Lv1的差额。Research/Culture/Commerce各+2F2P，与原Lv1的3F3P合计5F5P；Industry+2F、不额外加P，Gold权重2..256为基础相邻二进制位的两倍。保留原生区域/其它Mod专家收益，不声称UI总量就是5F5P。无额外槽位/住房/GPP。

Lv3Support独立读取EffectiveFacts，限标准四区域DEV锚点、Potential>=3且ACTIVE>=3；ACTIVE未知或下降、归属不符、锚点缺失时清除本模块载体，保留其它模块已有结果。先删除旧载体再增加当前载体，重复审计幂等。Industry复用已验证的后台基础相邻样本，通过IndustrySupport.ReadBase读取，不从专家总产出反推相邻，避免反馈。IndustryAudit后刷新Lv3；总督/回合/建成/移民确认及既有后台总督信号均重新核对。后台信号未修改GPP自身计数/显示/刷新逻辑。

Read auto Lv1沿用原读数并追加Lv3 top-up carrier。该行是补差量：常数三类2F2P；Industry2F0P和2×Base Gold。更低ACTIVE时补差均0。面板仍9个按钮，标题从当前版本生成。

STATIC_CONFIRMED：当前HD数据库只读复制至RAM，新SQL执行成功、12建筑15专家收益行、全Lua语法/manifest46。LOCAL_SIMULATION_PASS：真实Lv3模块四类门控、ACTIVE2/未知撤销、4保留、工业Base1→4→0/失败清除与恢复、归属/区域失效、重复刷新及重新初始化、只读诊断。旧Industry模块Lua/后台桥接回归通过；旧GPP测试以当前RAM已有SQL行、仅内存更新manifest断言回归通过。第一次照旧重复执行已装SQL触发唯一键冲突，是旧fixture不幂等，非运行失败；旧测试文件未改。

实机新能力仍USER_GAME_TEST_REQUIRED。既有B035通过及GPP延迟接受不回退、不追加验证。延迟备注见Specialization_B035_GPP_Refresh_Note.md（Status/Validation/Results）。
