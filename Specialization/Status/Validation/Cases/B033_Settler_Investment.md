# B033：一名移民提升永久Potential

Document Owner: Codex
State: USER_GAME_TEST_REQUIRED
Build: P0-B-033 / modinfo41

沿用已有测试文明存档，先另存测试副本；无需新局。选择已确认有Research/Culture/Commerce专业、Potential1的城市，最好没有已建立的高级总督，这样预期ACTIVE始终1。不需要额外建筑或商路；已有商路可保留。

1. 选择城市，Read progression应显示Potential1、Completed investments0，且没有UNKNOWN。用Cheat Panel获得一名移民并放在该城市中心，选中移民，点击Prepare investment。截图①：PREPARED、Potential1→2，移民仍存在。若城市没有跟踪记录或显示REJECTED，请先回传，不继续确认。
2. 点Confirm investment。截图②：INVESTED，移民消失，Potential2、Completed investments1、pending=false。没有已建立且满足2头衔的总督时ACTIVE1；有合格总督则ACTIVE2，但Lv2收益本批尚未实现。再点一次Confirm：应提示Prepare first或ALREADY_COMMITTED，不再升级/消耗；口头确认即可，不要求额外截图。
3. 保存、回主菜单、重新加载；选择同城，Read progression截图③。预期专业不变、Potential2、投资数1、pending=false，移民仍已消耗。顺便Read auto Lv1确认原carrier仍在；如原有商路，网络身份应保持，可口头确认，不重测商路变化。无需再创建新移民。

PASS：准备无消耗，确认恰好消耗1个移民并永久+1，重复不重复，重载保持，原Lv1/专业身份未丢失。FAIL：准备阶段已扣单位；确认消费但未正确增加；重复增加；重载重置；旧Lv1异常。REJECTED表示前提未满足，不自动判实际消耗失败；截图给Codex判断。

出现HELD/UNIT_DEBIT_UNCONFIRMED/其它错误时停止继续确认，不手动清账本，不为重试再献祭单位。截图需包含完整错误、当前Potential/投资数/pending及单位是否仍在；保留测试前后存档。若游戏生成Lua.log/Database.log/Modding.log，保留该次日志供失败排查。无需手抄内部ID。截图放ScreenShots，复核后归档。

本批不测2→4、征服或故障注入；cap与多级连续投资先由本地测试覆盖，不扩展实机PASS。
