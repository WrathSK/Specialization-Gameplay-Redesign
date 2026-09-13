# B037：Lv3专家支持小批次

Document Owner: Codex
State: USER_GAME_TEST_REQUIRED

先回主菜单重新加载现有存档，确认B037。新增隐藏建筑可能要求新局：若出现B037_DATABASE_MISSING或报告有载体但专家没有新增收益，请回传，优先判断旧档定义问题，不反复消耗移民。正常则继续沿用现有四专业测试城。

只测专家支持，不测本轮未实现的Lv3其它能力，也不重测GPP延迟。Read auto Lv1末两行显示Lv3 top-up（相对Lv1的补差）。

1. 科研/文化/商业分别ACTIVE>=3、各1名专家：top-up=2F2P0G。与ACTIVE1–2时比，每名专家多2F2P；本Mod合计5F5P，原有专家Science/Culture/Gold等仍保留。任选一城调离总督，top-up归0，额外支持回3F3P。另两城可口述正常，不要求逐步截图。
2. 工业ACTIVE>=3、1名专家：top-up=2F0P/(2×基础相邻)G。若Base仍6，本Mod支持为5F6P12G，加原有2P后典型专家总值5F8P12G；其它建筑收益另计。调离后回Lv1的3F6P，典型原生总值3F8P，Lv3金币撤销。若方便在ACTIVE3恢复后改变Base，Gold应随之变为2×新Base；不再专门重测翻倍政策。
3. 恢复其中一城ACTIVE>=3后保存读档：补差不丢、不叠加。人工说明即可。

PASS：上述差额/等级撤销/重载正确，无需总量恰等于本Mod新增量。FAIL：补差与ACTIVE不符、出现8F8P重复叠加、工业Production被错误加2、金币不是2×Base或ERROR。可过回合核对并说明刷新时机。

只需异常截图或每类代表报告；正常可人工回报。失败提供Read auto Lv1和专家提示、ACTIVE、是否旧档；ERROR时Lua.log，数据库缺失时Database.log。B035无需额外测试。
