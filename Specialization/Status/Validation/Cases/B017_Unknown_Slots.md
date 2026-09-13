# B017：未知槽位明细（仅一案）

Document Owner: Codex
Build: P0-B-017 / modinfo24
Verification: USER_GAME_TEST_REQUIRED

1. 加载现有测试文明存档，进入地图后打开Specialization P0，确认B017。
2. 点击新增的 **Eligibility unknowns**，截图整个面板。无需选城市、过回合、保存再读档，也不必先点Read eligibility。
3. 预期本局未知8可在一页显示。若实际页数大于1，再点击同一按钮逐页截图，默认文件名投递ScreenShots即可。

显示验收PASS：能列出LOAD_CLOSE中的未知player编号和各自原因，页数/条数相符。无当前版本记录或报错则保留完整截图，不要重复旧B016两案。本案用于查原因，出现CIV_NOT_READY等并不自动证明“空槽位”，也不自动成为正式资格兼容PASS。

没有未知时也直接截图，数量变化本身是待分析信息。不需要复制或手抄ID。按钮只看现有缓存，不发Gameplay请求，不重新采样。B010继续延后。
