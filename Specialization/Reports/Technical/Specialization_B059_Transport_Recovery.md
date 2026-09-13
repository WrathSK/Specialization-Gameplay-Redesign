# B059.80 收藏传输恢复

Document Owner: Codex
Design: D0022 unchanged
Status: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

截图2026-09-13 11.10.27 AM（B059.79）明确：Game ready=false ACK0 receivedNONE NO_PACKET；generation expected1 receivedNONE；UI scan1 send1 WAIT_ACK LOAD_SCREEN_CLOSE；作品2、5文化/20旅游、城市108.2656文化，themed0。只能证明接收函数未登记数据，不能证明具体引擎丢包原因，更不能归因建筑倍率。79初始化保护仍有效但不足以解决当前实机情况。

原发送把pcall无异常当作等待依据，却不区分RequestPlayerOperation返回false，且首包未到仅下一回合重试。80对pending包安装有限计时器，每两秒原包重发，最多两次（初始+重发共3次）；不扫描收藏，不增加seq，不永久重复。ACK、关闭、次数耗尽即清除。超时保留诊断；下回合按当前真实收藏新采样。重复包由Gameplay seq去重，迟到ACK清理pending；同步发布重入保护防止pending已被清除后继续访问。所有实机运输行为仍待测，未声称修复已游戏确认。

DevelopmentTests/test_b059_transport_recovery.py继承79实际Lua/SQL回归，新增首次false后恢复、同包双重发上限、扫描数不变、超时百次通用事件不发送、迟到确认、同步发布重入。不会启动游戏。

最小测试：主菜单重载原存档，确认80，约5秒后直接Read Great Works，不先AUTO。一张报告即可。若正常再按旧OFF/AUTO计划验算，不拆高阶建筑。若仍NO_PACKET，传输返回/超时字段用于继续定位；不建议盲目反复重载。

证据归档：外部W/Specialization/Status/Validation/Evidence/B059-79-No-Packet（PNG/hash manifest）；不导入Git。
