# B012 — DEV表存储，两项实机测试

Document Owner: Codex
Build: P0-B-012 / modinfo19
Verification: USER_GAME_TEST_REQUIRED

USER_GAME_TEST_REQUIRED：需要用户在实际Civ VI验证；本地模拟不代表实机通过。只测试Game Property中的合成数据，不测试城市身份或专业。B010继续延后，B011无需重复。

## 准备

重新加载现有Specialization测试文明存档即可，不要求新局、新城、选城或过回合。面板确认P0-B-012，看到Read storage和Write test table。保存时可另存为B012-test以便识别。

专用键为SPC_DEV_STORAGE_B012_P<playerID>，只含两个合成DEV记录，无真实城市ID。只有Write test table会在该键为空时尝试一次Game:SetProperty；Read storage只通过Gameplay读取，启动/读档不自动写入。不覆盖已有不一致数据。其它文明请求被拒绝。

## B012-1：首次写入与重复点击

1. 点击Read storage。首次测试应显示EMPTY、实际写入尝试=0。EMPTY只是未创建测试表，不是错误。
2. 点击Write test table。预期ACK正文为DEV表存储 MATCH，实际写入尝试=1；截图。
3. 再点一次Write test table。预期MATCH_NO_WRITE，实际写入尝试仍为1；截图。

PASS：完整表与预期一致，重复点击不增加写入次数。ACK仅表示收到回复，必须同时核对MATCH/MATCH_NO_WRITE。正文的revision=1 counter=2 records=2等行为预期值说明，只有MATCH才表示程序逐键核对通过。

如首次Read已经MATCH且尝试=0，说明本档已有同版DEV表；不要清除，可直接验证重复写入仍0并记录这是已有表场景，不把它当首次空表写入证据。

## B012-2：保存、退出、读档

1. B012-1完成后保存，退出主菜单，重新加载该存档。
2. 先只点Read storage，不点Write。预期MATCH、实际写入尝试=0、writeCall=NONE；截图。这表明读档后未靠重新写入补数据。
3. 再点Write test table。预期MATCH_NO_WRITE，实际写入尝试仍为0；截图。

PASS：重载前后完整内容一致，重载后重复按钮不写入。不要求人工计算内部ID，不要求选任何城市，不需过回合。

## FAIL/需诊断及回传

- READ_ERROR / READBACK_ERROR / WRITE_UNCONFIRMED / MISMATCH_NO_OVERWRITE，或重载后EMPTY：停止，保存当时截图，勿反复点Write。
- 重复点击使尝试次数增加，或读档前后值变化：停止，回传前后两屏。
- NO RESPONSE / DISPATCH_ERROR：记录截图；可点Show / Copy查看迟到ACK，但无需成功复制。若仍无回复，停止。
- 版本不是B012或按钮不存在：只回传版本截图，不做其它测试。

截图按系统原名放Specialization/ScreenShots即可。通常本批四张截图足够；失败时附Lua.log中的[SPC][B012][STORAGE]及[SPC][P0-B-012][GAMEPLAY]行（日志可获得时），并说明发生于写入前/后还是读档后。无需为日志配置额外工具。

本批通过也不证明崩溃原子性、多人同步、真实城市代际、征服继承、专业账本或单位消费事务。完成后等待结果分析。
