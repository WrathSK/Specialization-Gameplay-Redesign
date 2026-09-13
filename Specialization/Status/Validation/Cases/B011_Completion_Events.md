# B011 — 完成事件最小实机批次

Document Owner: Codex
Build: P0-B-011 / modinfo18
Verification: USER_GAME_TEST_REQUIRED

USER_GAME_TEST_REQUIRED表示需要用户在Civ VI中验证，本地通过不能代替本批。只测试新增完成事件；B010仍延后。助手不启动游戏。

## 准备（两个案例共用）

由用户正常重新加载测试文明存档，让更新后的Gameplay脚本加载；不要求新开局。打开Specialization P0面板，确认标题为P0-B-011，点击Completion events。按钮只显示已经发生的自动记录，无需选城、无需剪贴板。Older completion events查看更早页；每页两条，最新在前。

先确认CityBuilt/Constructed/Added/Load均REGISTERED，阶段AFTER_LOAD_CLOSE。任一ABSENT、REGISTER_ERROR或版本仍B010：停止，回传这一屏；不要继续操作。REGISTERED只证明注册，不证明事件已触发。

计数含本次脚本加载以来所有测试文明城市事件；不只属于当前选城。每次重载计数重新开始，绝不累计上个存档会话。区域加入地图和完成通知是两种不同事件；加入时complete=true不能单独视为首次完成。

## B011-1 — 放置 → 正常完成

使用现有己方城市，选能建学院/剧院广场/工业区/商业中心之一且有区域容量的城市。尽量选生产力高、短期可完成的城市；期间避免其它城市同时完成区域，以便只比较一个变化。

1. 开工前点击Completion events，记住“完成通知”计数C0（截图即可）。
2. 放置选定区域，但尚未完成。点击Completion events截图。预期完成通知仍为C0；新增“区域加入地图”记录对应城市/区域，complete=false、NOT_COMPLETE。若暂时未显示对象就绪状态，不认PASS，保留错误行。
3. 正常生产直到这一个区域完成（不使用直接创建区域的Cheat命令）。再次点击Completion events截图；最新不是目标时用Older completion events翻页。

PASS：放置阶段不增加完成通知；完成阶段恰好增加1，记录为该城市/区域类型、对应专业family，complete=true、COMPLETE_OBSERVED，owner一致，无READ_ERROR/OBJECT_MISMATCH。若另外城市也完成，需凭记录逐条区分，不能直接按总数判定失败。

FAIL/需诊断：放置就收到完成通知；正常完成没有通知；同一目标重复通知；Type/family/实例不匹配；字段UNAVAILABLE或读取错误。停止追加测试并保存当前存档。事件异常不代表真实游戏建造失败，也不会锁错专业，因为本探针不写专业。

回传：放置后、完成后两屏；开工前C0若不为0也附基线屏。截图不用改名，按时间放入DevelopmentReports/ScreenshotInbox即可；已有Lua.log时可附[COMPLETION]行，没有日志不必配置。计数“错误=0”只表示没有抛出异常，仍需检查每条observation。

## B011-2 — 保存 → 重载，不做建造操作

B011-1通过后，在已完成区域存在的状态保存。退出到主菜单并重载同一存档；重载后先不要过回合、建城或开工，直接打开面板→Completion events。

PASS：版本B011、AFTER_LOAD_CLOSE、四hook REGISTERED；“建城=0、完成通知=0”。允许“区域加入”记录在加载时出现，即使其中complete=true，也不得混成完成通知。若没有任何事件记录，但hook/阶段正常，亦符合本案例预期。

FAIL/需诊断：重载后在没有建城/建造操作时出现建城或完成通知、计数明显沿用上次会话、hook缺失或错误。若发现事件重放，只说明需要做加载隔离/去重，不能把本批判PASS。

回传：重载后第一屏；若完成通知/建城非0，用Older completion events补充相关记录页。无需再点Mark，也不用Copy。必要时附存档名与是否过了回合的说明。

## 本批不覆盖

CityBuilt真实建城触发（本批只观察它是否在加载时重放）、修复/掠夺/征服/夷平、替代区域逐一实测、完整城市UID、正式Property保存、ACTIVE与Settler。不能因本批通过就宣称这些也通过。两案完成后停止，等待日志/截图分析。
