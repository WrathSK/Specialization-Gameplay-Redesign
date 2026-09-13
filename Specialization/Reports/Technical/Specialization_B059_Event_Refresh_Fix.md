# B059.78：事件刷新与异步确认修复

Document Owner: Codex
Design: D0022 unchanged
Runtime: P0-B-059.78 / modinfo78

## 用户观察与可证明原因

用户尚未正式开启收益测试即察觉卡顿和连续刷新声音。77在SystemUpdateUI/Publish/Playback全部进入全收藏扫描，还每2秒重复；即使最终签名相同不发送，仍已经做完整扫描。另以Gameplay seq!=UI seq判定重发，没有等待异步确认，可能在引擎处理请求之前不断重发。之前mock同步执行Receive不能捕捉此类时序问题。本轮新增故意延迟ACK模拟，确认修复后不形成重发链。没有运行日志/游戏观测证明声音具体来源，故不宣称已在原生环境解决。

## 修复

DialogueRefresh无SetUpdate/定时循环。GreatWorkCreated/GreatWorkMoved触发dirty，城市增删/易主、总督状态、LoadScreenClose/PlayerTurnActivated提供资格与恢复信号；通用事件只drain ACK/dirty，不把普通UI更新本身视为需要扫描。多个事件合并，城市/作品排序避免顺序抖动。同回合单个请求未ACK不再次扫描或发送；采样期间新事件仍保留dirty。失败发送记录错误，等下次具体事件；丢ACK只在下一回合恢复尝试，不每帧重试。

移民投资和已有GPP资格更新直接Gameplay.Dialogue.Audit使用当前收藏缓存，不为资格刷新重复枚举巨作。普通读取不刷新collection。原生城市所有权变化/回合fallback沿用；未转变为历史事件累积表，仍在相关事件后读取当前真实集合。

参考：原版GreatWorksOverview.lua:1045/1125 GreatWorkMoved；DiplomacyRibbon.lua:823和CityPanelOverview.lua:1077 GreatWorkCreated。未修改这些文件。事件缺失覆盖仍由每回合核对兜底，不悄悄恢复周期扫描。

## 检查

新增DevelopmentTests/test_b059_event_refresh.py，以旧B059实际Lua/SQL回归为基础，只适配版本和替换已废弃的定时UI假设。空闲100轮×3通用事件零扫描/发送；多次同收藏Moved只一次扫描且不发送；ACK延迟200+事件零额外发送；期间多个变动合并到ACK后的单次新请求；下一回合恢复丢ACK；没有注册SetUpdate。其它收益与数据库回归通过。真实性能与声音USER_GAME_TEST_REQUIRED，公式/theming效果亦尚未实测。

修改：UI/DialogueRefresh.lua、UI/BoostGreatWorkRead.lua（诊断计数）、Gameplay.lua（资格直接reconcile）、Probe/manifest/P0Panel版本。新增测试/本报告，Architecture/Status同步。既有SQL和D0022不变；备份ignored local/before-b059-78；不启动游戏、不commit/push。

## 最小用户复验

主菜单重载原存档，确认B059.78。停留15秒，无操作不应连续响刷新音；前后Read Great Works中的事件后台扫描/发送计数保持稳定（加载最后一次dirty处理可发生一次）。然后移动一件巨作，D/配置应更新；不需要先开巨作UI才能初始化。若仍卡，回传两次报告计数、WAIT_ACK/ERROR状态，以及声音是否持续；不要求恢复完整收益测试直到性能正常。
