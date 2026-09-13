# B014 — 已绑定城市的完成观察记录

Document Owner: Codex
Build: P0-B-014 / modinfo21
Verification: USER_GAME_TEST_REQUIRED

USER_GAME_TEST_REQUIRED表示需要用户实机确认，本地模拟不代表通过。这个批次只保存DEV首次观察记录，不授予专业/Potential/收益，不解决OPEN-04首次历史或同时完成规则。

## 准备

加载刚才B013测试存档，确认面板P0-B-014及Read completion record按钮。优先使用B013新建的纽约（上一批city=327684，DEV-B013-P0-1）；无需抄ID、重测Read binding或再建城。选中该城即可。

若该城已有学院，可改建另外一种四类专业区域（剧院广场/工业区/商业中心）；本批记录的不是历史首次，所以不会推断当前专业。尽量只让这座城完成一个目标区域，避免其它已绑定城同时完成影响本次写入总数。要是没有任何可建四类区域，再使用新建且B013绑定成功的测试城。

## B014-1：未完成 → 完成 → 只读

1. 目标区域未完成时点Read completion record，预期NO_OBSERVED_RECORD，记录写入=0。若尚未放置，可先放置但不要完成；仍应无记录。截图。
2. 完成该区域，再点Read completion record。预期OBSERVED_RECORD_MATCH，family/type与实际目标一致；token为该城B013编号，记录写入=1，最近事件OBSERVATION_SAVED。截图。尽量正常生产完成；若用Cheat加生产，请说明方式，避免把直接创建区域结果当正常跨回合生产证据。
3. 再点一次Read completion record，记录和写入次数应不变；无需额外截图。

成功判据：放置/未完成不创建记录，完成后保存正确城市/区域族及类型，重复读不写。Constructed和Load应均REGISTERED，阶段AFTER_LOAD_CLOSE。

## B014-2：保存重载

保存→退出主菜单→重新读同一存档，不再完成新区域。选相同城市→Read completion record。

预期OBSERVED_RECORD_MATCH，token/family/type/district/turn与读档前保持；本次加载记录写入=0。截图。重复读取仍0即可，不需额外截图。

成功判据：记录从存档恢复，不由加载事件重新写入。通常本批3张截图足够。

## 失败回传

READ_ERROR / ERROR / BINDING_NOT_READY、完成后无记录、记录错城/错类型、读档后丢失或写入非0均停止；回传该屏和发生阶段，不反复建区域。若有日志，附Lua.log的[SPC][B014][RECORD]及相关[SPC][B013][BINDING]行。只需截图时无需另行配置日志。

截图仍投递Specialization/ScreenShots，读完按B014归档。B010继续暂停，B011/B012/B013不用重测。

## 验收范围

FIRST_OBSERVED_COMPLETION不是历史FIRST_COMPLETION。它只按收到的首次有效通知保存观察，之后保留原记录；不决定同时完成多个候选的专业选择，不回填旧城市区域历史，不接CitySpecializationState正式写入。验证成功后仍需完成正式状态初始化/历史边界方案。
