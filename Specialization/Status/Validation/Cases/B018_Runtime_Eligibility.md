# B018：当前名单与内部诊断许可（两案）

Document Owner: Codex
Build: P0-B-018 / modinfo25
Verification: USER_GAME_TEST_REQUIRED

现有测试文明存档即可，无需选城/过回合/改资格，不用再点B016/B017按钮。

## B018-1

加载进入地图，打开Specialization P0，确认B018，点击 **Runtime eligibility**，截图整面板。

PASS：phase=LOAD_CLOSE、hook=REGISTERED、roster=COMPLETE_ROSTER；本玩家0诊断许可=true；诊断获准列表含0（当前只绑定测试文明时预期仅0）；内部撤销/重取检查=PASS。

当前名单、未知和54–61在名单内/外的结果按实际记录，不预设全部为空。数字区间如0-5表示0至5全部在列表内。本案不要求任何特定玩家总数。若存在其它未知，回传原图分析，不能把名单内未知默认为未启用。

FAIL或待排查：NO_RECORD/UNKNOWN、LOAD_CLOSE未到、当前玩家许可false、内部检查FAIL/NOT_PROVEN。直接截图，不靠过回合或其它按钮补读掩盖结果。

## B018-2

保存→返回主菜单→重新加载同存档；再打开Runtime eligibility截图。中间不改变局面。

PASS：上述字段仍满足，当前名单/诊断获准列表一致。验证的是新GetAliveIDs组合及许可重建，不重复旧Trait-only两案。

两图按顺序投递Specialization/ScreenShots即可，默认文件名保留。失败时保留面板及可用Lua.log，不需要手抄ID/复制文字。未生成Lua日志不用改配置。

内部PASS只代表只读诊断中的许可对象自检，绝不表示实际禁用玩家、征服或Modifier撤销通过。名单外也不证明从未参与。B010继续延后。
