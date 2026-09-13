# B013 用户实机结果

Document Owner: Codex
Build: P0-B-013 / modinfo20
Verification: USER_GAME_TEST_PASS
Evidence: 用户操作顺序说明 + 五张原图逐张判读

USER_GAME_TEST_PASS表示用户在实际游戏中验证通过，只限本次新建城市与正常保存重载的DEV绑定。

| 图/时间 | 操作 | 城市ID | 状态 | Game/City写入 | counter |
|---|---|---:|---|---|---:|
| 1 / 18:20:56 | 旧城Read | 65536 | UNTRACKED_NO_WRITE | 0/0 | 0 |
| 2 / 18:21:41 | 新城Read | 327684 | BOUND_MATCH | 2/1 | 1 |
| 3 / 18:22:02 | 新城重复Read | 327684 | BOUND_MATCH | 2/1 | 1 |
| 4 / 18:23:10 | 保存重载后Read | 327684 | BOUND_MATCH | 0/0 | 1 |
| 5 / 18:23:13 | 重载后重复Read | 327684 | BOUND_MATCH | 0/0 | 1 |

图1两侧token/state均nil，最近事件NONE；图2–3两侧token均DEV-B013-P0-1，state=CONFIRMED，最近事件NEW_CITY_BOUND；图4–5同token与CONFIRMED保持，最近事件NONE。所有图为B013/ACK、AFTER_LOAD_CLOSE，CityBuilt和Load均REGISTERED，未见ERROR/PARTIAL/CONFLICT。

## 判定

- B013-1 USER_GAME_TEST_PASS：被选中的旧城没有补写，新城自动完成双方绑定；重复Read无额外写入。
- B013-2 USER_GAME_TEST_PASS：用户明确说明保存读档；图4先读即双方匹配且本次写0/0，图5重复读取仍0/0。不是读取时重新写入掩盖丢失。
- 不把重复Read等同重复CityBuilt事件，不把一个新城扩大为所有城市/征服/毁城复用通过。城市ID为当前引用，DEV token不因此直接升级为正式专业UID。

这组证据支持继续准备同一正常新城中的完成事实持久化。专业/Potential、正常首都初建、旧档补全、跨征服继承、多候选同时完成、崩溃原子性与多人仍不在验收范围。B010继续延后，没有新增测试要求。

## 归档与本轮范围

[五张原图](../Evidence/B013/)及manifest记录顺序、原名、大小和SHA256；已从ScreenShots移动，移动前后校验一致，未压缩/重命名/复制/删除原件。收件箱可继续投递。

本轮只登记结果、更新当前文档与归档已读截图，未修改运行源码、Tests、Design或游戏配置，未运行游戏。下一步先准备区域完成事实与已绑定新城的连接，仍不接正式收益。
