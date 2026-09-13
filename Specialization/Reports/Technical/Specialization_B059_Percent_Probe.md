# B059.82 百分比探针

Document Owner: Codex

B059.81截图已显示Culture ACTIVE4、合格2件、creator D2、配置15%、后台IDLE；用户确认AUTO可读，初始化/配置链路在该存档USER_GAME_TEST_PASS。两图均AUTO、原生作品5C/20T、整城108.2656C、theme0，不能当OFF/AUTO对照或收益PASS。

B059.82按用户要求新增本城临时TEST +25/+50/+100按钮；互斥替换AUTO载体，不累加，仍Culture ACTIVE4及合格类型门控。OFF清除实验、AUTO恢复D0022公式，读档清理实验并恢复AUTO。D0022、正式SQL D档、后台事件机制不改。LOCAL_SIMULATION_PASS：14修正/测试档、125/150/200参数、真实请求、幂等/切档/资格撤销/读档清理及回归。实机百分比结算仍USER_GAME_TEST_REQUIRED。

下一用户批次见[大百分比对照](../../Status/Validation/Specialization_B059_Percent_User_Tests.md)：固定当前两著作及建筑，OFF→100→OFF先确认大差值；再25/50，每档读取一图。若100无变化只过一回合复读一次并停止；不继续盲测，需区分刷新/作用域/原生倍率合并。

SQL从正式D2逐项复制相同类型/分类作用域，仅ScalingFactor替换125/150/200，每档14项；无新Trait挂载。临时状态不持久，加载清理实验建筑。测试DevelopmentTests/test_b059_percent_probe.py。证据在外部W/Specialization/Status/Validation/Evidence/B059-81-Initialized，原件冻结。
