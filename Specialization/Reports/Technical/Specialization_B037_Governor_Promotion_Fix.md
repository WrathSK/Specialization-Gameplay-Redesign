# B037 总督晋升刷新补充（modinfo47）

Document Owner: Codex

Lv3Support加入Gameplay GovernorPromoted监听；UI/GPPRefresh加入同名dirty信号，沿用发布完成后的请求以应对立即回调中事实尚未更新的时序。Gameplay原有LV2_GPP_DIRTY分支已调用Lv3Support.Audit，无需更改。没有新轮询、没有改收益值、投资规则或GPP原生率刷新。重复刷新幂等。

STATIC_CONFIRMED：HD Gameplay/RegionalYields.lua:274–275以GovernorPromoted标记待刷新；自身旧监听缺失。LOCAL_SIMULATION_PASS：实际Lv3模块晋升事件使文化/商业开启，重复事件不写；即时读到旧ACTIVE时，真实后台模块在publish后再次请求并正确开启。测试test_lv3_governor_promotion.py。

修正部署B037/modinfo47，Design D0010未变。旧modinfo46“先投资再晋升”失败记录保留；新修正为USER_GAME_TEST_REQUIRED，不能标新PASS。既有GPP过回合延迟仍按用户要求不改。

最小后续确认（可并入下次使用，不重做整批）：现有文化或商业城Potential2/已建立2头衔总督，先投资到3，再同回合晋升总督到3；不动专家、不投资别城、不结束回合，读auto Lv1并看专家。top-up应2F2P且实际支持多2F2P。若仍0，回传该报告与Read progression即可，不扩展其它动作组合。无需重建局（无SQL更改）。
