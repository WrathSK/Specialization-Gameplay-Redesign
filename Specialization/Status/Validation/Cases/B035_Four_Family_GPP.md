# B035 四类专业联合测试（B036 / modinfo45精简面板）

Document Owner: Codex
State: USER_GAME_TEST_REQUIRED
Supersedes current dispatch: B035_Lv2_GPP.md（原三案保留参考，不同时执行）

## 准备

沿用刚通过B036的存档，退出主菜单再读取即可，无需新局。本次只改面板，GPP和工业收益代码/SQL不变。标题应为SPC P0-B-036 | B035 GPP tests，只有底部三行9个功能按钮；看到版本B036是正常的，B035指测试项目。

四类城市：科研学院、文化剧院、工业工业区、商业商业中心。每城Potential至少2；使用2头衔且已建立的总督，使Read progression显示ACTIVE=2或更高。缺投资时可用现有移民与Prepare investment / Confirm investment；已有投资不重复做。尽量避开提供GPP倍率的总督晋升/政策；不要在比较前后同时修改其它城市工作人员。

Read Lv2 GPP：workers实际人数；expected/carrier仅本Mod每类新增基础点数，应为2×人数；other=0。UI EMPIRE GPP/turn为全国实际每回合点数。原有HD每名专家基础2点仍保留，所以无倍率时0→1人的全国变化应为+4，不是+2。UNKNOWN请回传，或提供原生伟人界面读数；不把UNKNOWN当0。

## 1. 四类0→1工作人员（核心）

依次选科研、文化、工业、商业城，在每城ACTIVE≥2时：
1. 移出该区域全部专家，Read Lv2 GPP记录全国基准；
2. 放入1名专家，再读报告；保持其他城市状态不变。

|专业|应该变化的全国每回合点数（无其它倍率）|新增基础报告|
|---|---|---|
|科研|Scientist +4|expected=carrier=2|
|文化|Writer、Artist、Musician各+4|每类expected=carrier=2|
|工业|Engineer +4|expected=carrier=2|
|商业|Merchant +4|expected=carrier=2|

PASS：四类对应点数都正确，文化三类同时生效，other=0，重复读取不增长。FAIL：carrier与人数不符、原生点数不增、串类或重复发放。有其它倍率时先回传前后原始数值和总督/政策，不要求人工计算或直接判失败。

## 2. 一个城市验证人数、调离和重载

选科研城（不必四城各做）。1→2名专家时新增基础2→4，全国Scientist再+4（无倍率）。保持2人调离总督，ACTIVE降为1，新增carrier归0，全国应减少本Mod4点，保留原有两专家合计4点。

再派回总督并等待建立，确认ACTIVE≥2、carrier4后保存读档；人数不变，carrier仍4、全国率不重复增加。PASS为正确撤销/恢复/重载；无需重测住房、投资或网络。

## 3. 文化百分比（同一文化城）

挂HD“文艺赞助人 / Art Patron”（人文主义；三类文化GPP+25%）。挂卡后重新以0名专家记录全国三类基准，再放入1名。

无其它倍率时三类各增加5=(原有2+本Mod2)×1.25；报告新增基础仍2。PASS：三个实际差值均5，不只作家。若是4.5、只有部分类型吃倍率或其它异常，请回传。原生界面若只显示四舍五入整数，不能仅凭显示5认定通过；优先报告UI EMPIRE数值。

## 回传

首案四城各0人与1人报告可各一张（共8张），或每城只交1人截图并口述0人基准；后两案正常可口述，异常再截图。不必每次读取都拍照。

失败请保留Read Lv2 GPP、原生伟人界面的前后读数，说明城市专业/总督/政策以及是否过回合才刷新；ERROR附Lua.log，数据库缺失再附Database.log/Modding.log。不要因DB错误反复投资。投递ScreenShots后照旧由Codex复核归档。
