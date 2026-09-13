> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

> 用户已明确确认：本次加载A007之前的旧存档。新增效果未回填仍是待验证解释，下一项仅需A007临时新局control对照。

# A007截图结果：旧阈值响应、新增效果未就绪

## 可直接确认的证据

五张截图均为A007、city=65536，control/present/established始终nil。结果包含NOT_READY。

| 文件时间 | 游戏回合 | 用户操作说明 | Req2/3/4 |
|---|---|---|---|
| 22:22:12 | 1 | 无总督 | nil/nil/nil |
| 22:22:57 | 2 | 用户说明已派遣、初始未升级 | nil/nil/nil |
| 22:23:09 | 3 | 用户说明过回合后 | nil/nil/nil |
| 22:23:28 | 3 | 用户说明升级一次后 | 1/nil/nil |
| 22:23:44 | 3 | 用户说明再次升级后 | 1/1/nil |

USER_GAME_TEST_PASS（有限子项）：用户升级总督后，同城Req2和Req3先后变为1的响应已观察到。不能据此宣布完整Governor机制通过：未验证建立前阻断、迁移撤销、城市隔离和Req4；“>=2/3阈值”也不是精确总督等级。

USER_GAME_TEST_FAIL：A007新增无条件control在本次测试局未返回1。present/established在校验未就绪时无法判定语义，保持USER_GAME_TEST_REQUIRED，不把nil当作false。完整激活机制仍未验收。

STATIC_CONFIRMED：只读当前DebugGameplay.sqlite，存在全部6个SPC Governor Modifiers以及6条测试trait绑定，包括CONTROL/PRESENT/ESTABLISHED。说明数据库定义已入缓存；不能证明当前存档已实例化相应Modifier。

较强待核假设：原存档已包含A002起的Req2/3/4，A007新增三个trait效果未回填到存档。无条件control也为空支持加载/实例化问题，而不是某个总督条件本身为假。已向用户确认是否加载旧存档，不擅自认定。另一种情况是新局也失败，届时需调查Modifier实例化及属性桥接，不能继续归因旧存档。

## 对印加方案的判断

不能直接采用它的现成业务逻辑。和而不同PachacutiGovernorPromoted用玩家Property按governorId记录累计升级，达到四次时给首都附加效果；并未维护“某个城市当前驻扎的总督是否达到条件”及调离撤销。

若改造成我们的备用方案，至少需要每总督头衔账本＋当前城市映射＋建立/到任状态＋迁移/移除/易主时撤销＋旧存档初始化/免费晋升语义。这不是全国四级总督计数能替代的，也不能将旧存档未知历史设0。

首选仍是本城原生阈值：每个城市作为Requirement subject，由引擎判断驻城总督且Established=1与Amount门槛。正式设计：满足Potential及本城条件的最高等级；无合格已建立总督只激活Lv1。不使用全国高阶总督数决定任何城市Active Level，不授予未驻扎城市同样能力。

## 下一项仅验证效果装载，不再升级总督

本轮不发新版本，不改SQL/运行Lua，不用SetProperty人为补control=1，也不盲目Attach已绑定Modifier，以免重复计数。

若用户确认是旧存档：保留现有存档，用同一A007和同样Mod组合仅新建一个临时测试局，建立首都、无需任命/升级总督，只Read governor一次。预期control=1，present/established/Req2/3/4为nil或0。control=1支持旧存档新增效果未回填；新局也nil则推翻该解释并回传该截图及Database/Modding日志。此新局有必要仅因本次测试变量就是“新建实例与旧存档”，不是要求重做其它已通过项目。

若本来就是A007新局：不要求再新建相同测试，回传确认即可，进一步检查加载链。当前不要继续过回合或升级试探，不要求重测专家。

本轮只更新报告、状态、架构，没有修改用户存档或启动游戏。
