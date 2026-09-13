# B011 用户实机结果 — 2026-09-11

Document Owner: Codex
Build: P0-B-011 / modinfo18
Evidence: 用户操作说明 + ScreenShots原始14张截图（逐张阅读）

## 用户摘要

已核对新城建立、学院放置、完成及保存重载的14张截图。学院放置未触发完成通知，实际完成后增加一次；重载未重放建城或完成通知，两项观察通过。建城时市中心也发送完成通知，且早于CityBuilt；它属于NON_V01，不能用于锁定专业。

这些证据支持后续区分放置、完成和加载，但不表示正式专业或Potential已写入。永久城市身份、旧档初始化及正式写入仍未接入；商路全集权威来源的既有阻塞未解除。用户现在无需操作；建议下一步设计新城初始化与完成事实的幂等写入边界，不重复本批。

## 判定与证据范围

USER_GAME_TEST_PASS表示用户已在实际游戏中验证通过，只覆盖下列明确场景。

| 项目 | 判定 | 范围 |
|---|---|---|
| B011-1 放置与完成区分 | USER_GAME_TEST_PASS | 本次新城学院：放置NOT_COMPLETE；完成后恰好一次COMPLETE_OBSERVED |
| B011-2 重载 | USER_GAME_TEST_PASS | 本次保存重载：建城0、完成通知0；只有加载期Added记录 |
| 附加CityBuilt观察 | USER_GAME_TEST_PASS | 本次新建城市触发CityBuilt且城市/owner可读；非征服、修复或所有建城路径验收 |

原案例要求正常生产完成；截图从放置到完成均为T1，用户未说明具体完成手段。因此B011-1的PASS限定为本次实际完成路径，不宣称已单独验证自然跨回合生产，也不推断使用了哪项Cheat命令。当前无需为此重复测试；将来正式写入验收可顺带覆盖正常生产路径。

## 时间序列

计数顺序为建城 / 完成通知 / 区域加入。所有截图错误=0、丢弃旧条目=0；四个hook均REGISTERED，面板当前阶段AFTER_LOAD_CLOSE。

| 截图 | 用户阶段 | 计数 | 关键读取 |
|---|---|---|---|
| 1–3 | 起始已有三城 | 0 / 0 / 6 | 三个市中心、三个商业中心均为加载期Added；没有完成通知 |
| 4–5 | 新建城市 | 1 / 1 / 7 | #7市中心完成，#8建城，#9市中心Added |
| 6–7 | 放置学院未完成 | 1 / 1 / 8 | #10 Campus Added，RESEARCH，complete=false / NOT_COMPLETE |
| 8–10 | 学院完成 | 1 / 2 / 8 | #11 Campus完成，RESEARCH，complete=true / COMPLETE_OBSERVED |
| 11–14 | 保存重载 | 0 / 0 / 8 | 八个Added均BEFORE_LOAD_CLOSE，包含已完成学院；未重放建城或完成通知 |

新城引用：owner=0，cityID=262147；市中心districtID=458758；学院districtID=524295。这里是引擎当前实例引用，不冒充永久城市UID。学院在放置、完成、读档三阶段引用一致。

建城顺序：#7 OnDistrictConstructed(CITY_CENTER/NON_V01) → #8 CityBuilt(CITY_OBSERVED) → #9 DistrictAddedToMap(CITY_CENTER)。新城建立后完成计数基线为1，所以学院完成1→2才是目标增量。CityBuilt行的district/family/complete=nil是不适用字段，不是读取失败。

重载后序列重新开始，#8是Campus Added，complete=true；完成通知总数仍为0。Added即使显示COMPLETE_OBSERVED，也只表示读取到了已完成对象，不能据此推断该区域刚完成，更不能从加载遍历顺序推断首次专业。

## 对后续实现的约束

- NON_V01市中心完成通知先过滤；不可消耗首个专业完成资格。
- 不能假定CityBuilt永远先于所有区域通知；初始化不能覆盖已合法提交的记录，重复调用必须幂等。
- 加载期Added只提供对象观察，不用于补写首次完成；缺失历史的旧城市仍按OPEN-04处理。
- 本批未验证Property专业写入、永久UID、同时完成排序、修复/征服、所有替代区域、正常跨回合完成及收益；不扩大PASS，也不重发B010。

## 截图原件索引

用户自行创建ScreenShots作为本批投递目录，原图原名保留；序号只在本报告中使用。SHA256用于以后识别证据，不复制图像。

| 序号 | 原件 | SHA256 |
|---|---|---|
| 1 | [Screenshot 2026-09-11 at 4.48.57 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.48.57 PM.png>) | `a723bb1356001662bff9dc2f68c899080a976cd3bdd63b68036f644d3be1cad8` |
| 2 | [Screenshot 2026-09-11 at 4.50.14 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.50.14 PM.png>) | `4fe41b52a134d19a5b68ff4081a5bec620935db014bc8e972d2f2f388950ea7d` |
| 3 | [Screenshot 2026-09-11 at 4.50.16 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.50.16 PM.png>) | `532e7b01e319822cefc6a4c97d8bc2e7fbc6e23df582b39002cbefff47cf8a3b` |
| 4 | [Screenshot 2026-09-11 at 4.52.06 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.52.06 PM.png>) | `f0dde0920ec4a2f696d0f6afa26be10c2c81ca54a22ab384d77a75c9352583c9` |
| 5 | [Screenshot 2026-09-11 at 4.52.26 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.52.26 PM.png>) | `ba3234a2461bb7e11716c3f2f5ed527b0545c1c557476bb02291a927d8eda79f` |
| 6 | [Screenshot 2026-09-11 at 4.52.59 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.52.59 PM.png>) | `c63af2651506dad33ba21a1ee932207c0e2c729b083b1412cab149ceec069d35` |
| 7 | [Screenshot 2026-09-11 at 4.53.01 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.53.01 PM.png>) | `a6eeb88c869ba06375d76dc1c408ed16771c4cb9e5b13ac00f0e4a7ff50c4b4b` |
| 8 | [Screenshot 2026-09-11 at 4.53.20 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.53.20 PM.png>) | `61a6d84d27cb59b79ebc298ae7a9787f502766ca5775af87592fb0ef62ec3cbf` |
| 9 | [Screenshot 2026-09-11 at 4.53.25 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.53.25 PM.png>) | `a4c24ae29423df9159991a1d785654d088dad814b420cfbf28a70fc4da8531e5` |
| 10 | [Screenshot 2026-09-11 at 4.53.27 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.53.27 PM.png>) | `367b9c51201bc1445af9bb249565246ff8c286682e3a7d75e38234381036234f` |
| 11 | [Screenshot 2026-09-11 at 4.56.57 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.56.57 PM.png>) | `3197815076fde4320e76d8c18dd9fa7b3a9159203e8d4a5cce9dc4a4a91e2611` |
| 12 | [Screenshot 2026-09-11 at 4.56.59 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.56.59 PM.png>) | `defb9d40c7b8dafd2376d6a943fd40ccfa79d4ece21f1785f342aac0ea7d0206` |
| 13 | [Screenshot 2026-09-11 at 4.57.01 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.57.01 PM.png>) | `c14f18b946aecc64fb812fe6c96540ca0a6fb70637e373ff0f0a07773156455b` |
| 14 | [Screenshot 2026-09-11 at 4.57.02 PM.png](<../../../ScreenShots/Screenshot 2026-09-11 at 4.57.02 PM.png>) | `2ec00415d38ad77b90b8d9a97c9b0f80d13cc6975fb2a67956f441a90e52043f` |

## 本轮文件范围

仅登记实机结果、更新Architecture/Status及入口文字；更新前四份文档另存新快照。当前Accepted D0002及冻结D0001、运行源码、DevelopmentTests、截图未改，没有运行游戏或写文件测试。

用户需要决定：无。
用户需要测试：无新增；B010继续延后。
Codex下一步：准备新城初始化和完成事实写入边界，保留未决生命周期规则，不直接接收益。

校验补记：当前Design为已接受D0002，SHA256与ChangeLog一致；本轮未改动Design。入口与架构标明D0002待技术同步，避免将旧D0001同步hash误认作当前Spec。
