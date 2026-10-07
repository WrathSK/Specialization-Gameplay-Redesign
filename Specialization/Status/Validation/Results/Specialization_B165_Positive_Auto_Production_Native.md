# B165.192 — 正旧AUTO共存与生产对照四图

Date: 2026-10-06 / America/Vancouver。Evidence: USER_GAME_TEST四张逐张读取原图；百分比来源另有HD代码／只读加载DB的STATIC_CONFIRMED。
State: POSITIVE_OLD_AUTO_SCOPED_PASS / CITY_PRODUCTION_DELTA_OBSERVED / EXACT_SETTLEMENT_ATTRIBUTION_OPEN。现有B165，不新增build／部署；不是新M或全城writerPASS。

## 逐图读数

同一Edinburgh文化ACTIVE4、W2／一座馆藏宿主、客运中心400成本，四图旧正常AUTO均+25%。

| 图／回合 | 状态 | 建筑进度 | 队列诊断读数 | 城市生产显示 | Meaning原生五项 |
|---|---|---:|---:|---:|---|
| 1／T63 | ①基线 | 0 | 100 | 100.3 | 0/0/0/0/0 |
| 2／T64 | ①基线 | 117 | 97 | 97.7 | 0/0/0/0/0 |
| 3／同T64 | ②追加中 | 117 | 110 | 110.7 | Science6/Production10/Gold18/Food6/Faith6 |
| 4／T65 | ②追加中 | 250 | 110 | 105.5 | Science6/Production10/Gold18/Food6/Faith6 |

图3每件预期3/5/9/3/3，W2本城6/10/18/6/6与原生绝对读数一致；旧AUTO保持+25%，没有将本项五项追加再乘1.25。图2与图3是同回合基线0→追加，正常+25%环境的五项原语共存按所测Writing范围PASS；不推广未启用的Culture追加、新M永久倍率或其它作品组合。

报告的“实测差值未确认”保护标记仍保留：不将跨回合UI基线失效改成自动PASS。这里以独立已读图2／图3的同回合绝对值核对，区别于界面自行验证。

## 百分比验算与10%来源

同T64城市生产力：110.7−97.7=13，与Meaning基础Production10×(1+20%+10%)一致。最后图的普通生产修正+20%与建筑／奇观+10%提供了可用解释，不能给已含修正的城市总数再重复乘30%。

图4基础项：9修正值＋2资源＋10巨作＋10区域＋14.2人口＋21建筑＋15开发地块＝81.2。81.2×(1+0.20+0.10)=105.56，与105.5显示精度相容。+20%显示的16.2也是81.2×20%的显示值；本次不继续追查其个别来源。

建筑／奇观+10%可归因于HD发电厂附着链：图4建筑明细明确“+5来自燃煤发电厂”；HD核心`UpdateDataBase/DL_Buildings.sql:280–284`为普通／燃煤／燃油发电厂挂`POWER_PLANT_BUILDING_PRODUCTION_PERCENTAGE_BOOST`，306行类型`MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION_MODIFIER`，361行Amount10。只读当前DebugGameplay DB确认该ID、Coal绑定、Amount10、Owner/Subject RequirementSet均NULL，无IsWonder=0过滤。与该城当前原生tooltip相吻合；不是Meaning另写一个建筑加速10%。原版CitySupport将Production提示直接取城市`GetYieldToolTip`。

## 实际结算：哪些已经知道、哪些不能硬算

实际基线增量=117−0=117；追加回合增量=250−117=133；两者差16。第二段不是132。

但城市背景读数在T63→T64由100.3→97.7，T64启用后110.7，下一回合又到105.5；队列getter和当前城市面板也不是始终相等。两次过回合并非已证明同一生产背景，因此不能把16全当作Meaning的独立结算贡献、再反推任意额外20%目标倍率。图4当前81.2不能当作此前每次结算的基值。

已知：Meaning提供了正确原生Production10，同回合城市实际生产显示增加13，真实建筑进度继续增加，并非仅馆藏tooltip。**精确队列结算归因仍开放，不判收益失效，也不凭数字相近判完整PASS。**本轮不再立即请求重复两回合、长测、冷加载或补旧截图。后续正式接入方案须明确如何处理该剩余门槛，可提出定域reader／结算整合验证方案供用户审核；本记录不自行放宽原cutover条件。

## 原图与停止点

四张原图原名原字节归档至ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B165_Positive_Auto_20261006_2002/`，manifest关联本记录，**4/4 SHA256 MATCH**；截图／manifest不入Git，收件箱目录及.DS_Store保留。此前B165五图、LOCAL记录、D0048暂行主题化及Balance边界不改。

B165补测资料已投递／审阅，正旧AUTO所测门槛关闭，不继续把这轮当作未做待办；剩余精确结算单独开放。Meaning仍手动单城七域五yield、Culture隔离；自动writer／全局旧GWA退役及M/N/UI等没有新实施授权。

用户需要决定：本轮无新Gameplay决定；后续正式接入／剩余门槛处置方案仍需审核授权。
用户需要测试：本轮不追加；不要重跑共享harness或把未知10%当故障。
Codex下一步：仅完成本次证据与当前状态同步、commit/push后停止，不改Mod／tests／GC／Design／runtime／main或部署；保留调查文件。
