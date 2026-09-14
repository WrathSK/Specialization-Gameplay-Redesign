# B062 商业四重新实现与问题复现

Document Owner: Codex

用户重新授权从已提交/推送3382d7d B060.85基线审查并重做商业四。B062.88（modinfo88）为新独立CommerceConvergence.lua，D0024保持不变；B061.86/87隔离目录不覆盖，不恢复旧重试和跨回合扫描。

问题审查：用户B061.86 OFF图source28.4219→floor5、实际S6；AUTO6→7只有口述，没有AUTO载体证据，仍不能解释实际+1。B061.87共用网络报BATCH_LIMIT_OR_SHAPE、0/5路线。真实3382d7d接收代码在Count/Data缺失的零路线模拟中同样失败；说明存在先于87的空值协议脆弱性，不是已经证明游戏原生如何序列化。B062发送WireCount=count+1、空数据EMPTY，接收严格decode/count冲突/实际路线数校验；旧非空协议仍兼容。不把UNKNOWN冒充有效空集合。

STATIC_CONFIRMED：BackgroundRoutes.lua与3382d7d逐字节相同；NetworkSender只改明确空包字段，没有87重试；NetworkBridge只改解码及商业模块新快照后通知，旧主体由精确diff回归。沿用此前48个整数载体的定义/ID便于清除旧档残留，并非恢复旧Commerce Lua。

LOCAL_SIMULATION_PASS（非游戏）：真实sender/receiver经过丢弃Count0/空Data边界fixture，非空→空清除网络和商业收益、重复空包/错误count/非空缺数据拒绝；直接源按对应总yield最高，不按等级、不求和、不通过distribution继承，最终floor；100次相同计划无额外写入；OFF/固定TEST5/AUTO共享apply，1+4载体核对、ACTIVE降级/重载清理及前批回归。全部来源计划先算完再写city层。只读报告分别显示预期、最后配置、实际载体组成、原生城市读数/OFF基线差值，不用配置冒充实测。

USER_GAME_TEST_REQUIRED：B062最小批次见Validation/Specialization_B062_User_Tests.md。完整退出再启动加载原档；先零商路验证共用网络空集合，再原商业4城OFF→TEST+5（不需要商路）检验同一承载层，再恢复AUTO接一条科研直连验证20%与跨回合。任何前项失败即停止。不要求重新做全部高级收益/多源矩阵。无新commit/push。

技术边界：缺当前网络时撤销本项而非沿用旧来源；城市UI/实际收益刷新时点、+5原生效果及第三方间接回路未实机确认。技术目录0..65535不clamp；报告错误。TEST5只作用选中Commerce4城，本玩家其它汇聚暂清除；OFF关闭本玩家汇聚且记录选中城读数；AUTO恢复所有合格城市，读档默认AUTO。控制均不改变Potential/身份/永久账本。
