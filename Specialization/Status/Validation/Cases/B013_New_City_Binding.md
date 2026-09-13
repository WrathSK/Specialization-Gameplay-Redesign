# B013 — 新城DEV绑定，两项实机测试

Document Owner: Codex
Build: P0-B-013 / modinfo20
Verification: USER_GAME_TEST_REQUIRED

USER_GAME_TEST_REQUIRED表示需要用户在Civ VI验证；本地模拟不能代替。只测专用DEV编号，不写专业/Potential，不消耗额外单位或赋予收益。B010继续延后，B011/B012不用重测。

## 准备与写入说明

加载现有测试文明存档，确认P0-B-013及Read binding按钮。可以用Cheat Panel获取Settler，再正常点击建城；不必重开游戏，也不要求建区域。首次首都在加载屏关闭前建立可能被忽略，因此本批按“加载完成后新建一座城”操作。

新增行为：加载完成后的测试文明CityBuilt事件自动写DEV标记；只读按钮不触发分配。新城正常过程是总账预留一次、城市token一次、总账确认一次，即Game=2 / City=1。计数是该玩家本次Gameplay加载的尝试次数，不是永久累计。只建一座新城方便直接比较。

专用Property：Game的SPC_DEV_BINDING_B013_P<playerID>，City的SPC_DEV_BINDING_B013_TOKEN。与B012合成表/旧marker/正式专业字段分开。当前最多记录32座测试新城，不回收编号。旧城不补写，读取/重载不修复部分数据。

## B013-1 — 旧城不写、新城绑定

1. 选现有旧城市→Read binding。预期UNTRACKED_NO_WRITE、city token=nil、ledger token=nil；本次加载Game=0 City=0；CityBuilt/Load均REGISTERED、阶段AFTER_LOAD_CLOSE。截图。
2. 建立一座新城市，选中它→Read binding。预期BOUND_MATCH，city token与ledger token相同，state=CONFIRMED，总账counter=1，Game=2 City=1，最近事件NEW_CITY_BOUND。截图。
3. 再点Read binding。预期上述编号、counter、Game/City计数完全不变。截图即可，无需抄ID。

PASS：旧城无写入，新城双方编号一致，重复Read不写。重复Read仅验证读取无副作用，不冒充重复CityBuilt事件实机验收；重复事件防重只有本地模拟证据。

如果本档已做过B013建城，counter可大于1，旧已绑定城也不会UNTRACKED；请说明该情况，不要清Property。首次按本批测试时应符合上面数值。

## B013-2 — 保存重载后只读恢复

1. 保存（可另存B013-test），退出主菜单，重新读同一存档；不要再建城。
2. 选刚才的新城→Read binding。预期BOUND_MATCH、双方token与读档前相同、CONFIRMED、counter不变；本次加载Game=0 City=0。截图。
3. 可再点一次Read binding，确认仍0/0；不要求额外截图。

PASS：持久数据匹配，读取前没有补写。加载自动检查也是只读，不重建缺失绑定。

## 失败回传

PARTIAL_NO_REPAIR / RESERVED_MATCH_NO_REPAIR / CONFLICT_NO_REPAIR / READ_ERROR / ERROR / hook ABSENT、REGISTER_ERROR均停止。新城UNTRACKED、计数异常或读档token改变也停止；不要继续建城尝试覆盖。

回传该屏与失败发生阶段。通常四张截图足够；有日志时附Lua.log的[SPC][B013][BINDING]，尤其ERROR或LOAD_AUDIT_ERROR。截图直接放Specialization/ScreenShots，保持默认文件名；助手判读后按B013归档。

本批不验证征服继承、毁城重建、城市引用跨所有权的永久性、首都初建、同时完成、专业事实、事务崩溃恢复或多人。正常通过也仅证明DEV绑定在本次场景可保持。
