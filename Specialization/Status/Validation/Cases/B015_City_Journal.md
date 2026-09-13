# B015 — 新城资格与实际记录提交

Document Owner: Codex
Build: P0-B-015 / modinfo22
Verification: USER_GAME_TEST_REQUIRED

USER_GAME_TEST_REQUIRED表示仍需用户实机确认；本地模拟不代表游戏通过。只写专用DEV城市表，不启用专业收益、Settler投资或正式征服继承。

## 准备

从主菜单重新加载现有测试文明存档，面板标题须为P0-B-015，使用新按钮 **Read city journal**。无需重新开局。必须在本版本加载后新建一座城：B013/B014旧城没有B015建城检查记录，不能代替本次资格测试；可以沿用原存档并用Cheat获得Settler建城。

本批不要同时创建其它城市，以使写入次数可直接比较。旧按钮无需复测。截图继续投递Specialization/ScreenShots，原名即可，读取后归档。

## B015-1：旧城不补写，新城自动建立记录

1. 选一座已有城市（之前B013/B014的纽约也可以），点Read city journal。预期UNTRACKED_NO_WRITE，本次加载写入=0；无需点任何Write/Mark。
2. 本版本中新建一座城市，不完成任何四类专业区域。选它点Read city journal。预期health=TRACKING、DEV specialization=NONE、potential=0、revision=0、本次加载写入=1、最近动作FOUNDATION_SAVED、stopped=false。
3. 再读一次，数字不变。可先放置学院但不完成，再读也应不变。

PASS：旧城不补写；新城自动写一份未定专业记录，重复读取/放置不锁定。旧城画面可文字回报，新城截图1张。Constructed=REGISTERED，AFTER_LOAD_CLOSE。

## B015-2：完成后一次锁定

在该新城完成学院（若无学院可换剧院/工业区/商业中心并说明），再点Read city journal。

预期：health=TRACKING、DEV specialization=RESEARCH（或对应类型）、potential=1、revision=1、本次加载写入=2；first显示正确区域，最近动作DEV_SPECIALIZATION_SAVED。再次读取所有数字保持。

PASS：从NONE/0变为正确专业候选/1，只有一次额外写入，城市/token未变，无STOP/GAP/READ_ERROR。截图1张。若使用Cheat完成，请顺手说明；本案不因此扩大为正常跨回合生产已验证。不要求为了测试再建第二种区域，后续不覆盖已在本地模拟。

## B015-3：保存重载只恢复

保存→退主菜单→加载同一存档，选同一新城，仅点Read city journal，不重新建城或完成区域。

预期：health=TRACKING、专业/potential/revision/first/token与保存前保持；本次加载写入=0，stopped=false，最近动作NONE。

PASS：记录保持，加载/读取不补写。截图1张。三张核心截图加旧城文字即可；也可加旧城截图共四张。

## 失败与回传

任一步出现STOP、GAP、READ_ERROR、stopped=true、写入计数不符合上表、类型不对或读档丢失，即停止本批，回传该屏和操作阶段。不要反复建城/完成区域试图修复。

有日志时回传Lua.log中 `[SPC][B015][JOURNAL]` 及相邻 `[SPC][B013][BINDING]` 行；只提供截图也可以。新城保持UNTRACKED时同时拍Read binding一次，有助区分绑定和新城扫描失败，无需重跑B013整批。

本批不测试征服、城市删除、Mod停用再启用或故意制造存储故障；这些没有完整方案，不要求用户尝试。B010继续延后。
