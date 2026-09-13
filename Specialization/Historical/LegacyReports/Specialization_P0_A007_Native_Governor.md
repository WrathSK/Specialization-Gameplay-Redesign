> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

# A007：改由原生Requirement判定总督

## 用户故障与范围

最新截图ScreenshotInbox/Screenshot 2026-09-10 at 10.11.31 PM显示P0-A-006，BEFORE_GetAssignedGovernor，GetAssignedGovernor:ABSENT。A005城市接口与A006玩家管理器接口均USER_GAME_TEST_FAIL。并不是引擎没有总督判定能力，而是两个UI先例在当前Gameplay对象上都未暴露。此前把原生Req属性展示放在查询之后，错误阻断了独立可用路径；A007已解除依赖。专家分支保持用户已确认的USER_GAME_TEST_PASS。

## 本机源码证据（STATIC_CONFIRMED）

和而不同根目录：/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070/

- 中书省：Texts/HD_Text_Buildings.sql:272将BUILDING_GOV_SPIES命名为中书省；UpdateDataBase/DL_Buildings.sql:877的GOV_SPIES_GOVERNOR_GOLD_MODIFIER使用CITY_HAS_GOVERNOR_REQUIREMENTS。其它建筑效果和本地化在Mod中存在覆盖，不能只看文字推断最后收益。
- 德川：DLCSupport/DL_SULEIMAN_ALT.sql:119–129使用HD_CITY_NOT_CAPITAL_NO_GOVERNOR、HD_CITY_CAPITAL_OR_GOVERNOR；DL_Requirements.sql:1399等把后者连接到REQUIRES_CITY_HAS_GOVERNOR。
- 善德：官方Expansion1/Data/Expansion1_Leaders_Major.xml:281–282绑定TRAIT_ADJUST_CITY_CULTURE_PER_GOVERNOR_TITLE_MODIFIER、TRAIT_ADJUST_CITY_SCIENCE_PER_GOVERNOR_TITLE_MODIFIER，是数据库原生按总督头衔效果，不需要此处尝试的Lua getter。当前和而不同又重做HWARANG，不能把官方数值当作当前组合最终效果。
- 原生存在条件：实际缓存Requirements中REQUIRES_CITY_WITH_ASSIGNED_GOVERNOR使用REQUIREMENT_CITY_HAS_GOVERNOR，Established=0。WITH_X_TITLES样本Amount=2且Established=1；和而不同DL_Requirements.sql:821–826、938–949定义1、3、4、5、6、7阈值及Established=1。
- 帕查库特：Gameplay/CivilizationTraits.lua:3452起监听GovernorEstablished；3470起PachacutiGovernorPromoted(playerId,governorId)读取玩家Property计数、加1，在旧值3时附加第四次升级效果。它是逐事件账本，不是即时查询既有总督等级。适用于维护自己的历史记录；既有未记录存档、免费晋升和额外Mod事件语义仍需明确。

## A007实现与限制

Data/GovernorProbe.sql保留已有Req2/3/4（X_TITLES且Established=1），新增独立SPC条件：PRESENT（HAS_GOVERNOR, Established=0）、ESTABLISHED（HAS_GOVERNOR, Established=1），以及无条件CONTROL。均通过原有MODIFIER_SPC_P0_GOV_PROPERTY/EFFECT_ADJUST_CITY_PROPERTY写调试城市Property，只绑定测试文明trait，不增加收益，不复制他人文明技能。

Read governor只读取六个城市属性：CONTROL_A007、PRESENT、ESTABLISHED、REQ_2/3/4。不调用任何Governor对象、不枚举晋升、不读取UI再反向写Gameplay。control=1证明无条件桥接效果在该城生效；它不证明其余条件刷新正确。缺少control时显示NOT_READY，不能把全部nil解释为无总督。

1表示该原生条件激活；nil/0暂作为未激活候选，必须通过前后状态对照验证撤销。阈值全部为1最多说明至少4个引擎头衔，不是恰好4个；没有精确总督名字/级别字段。后续专业Active Level可以取满足条件且不超过Potential的最高级，不必依赖任意Mod晋升树的精确计数。当前未实现正式专业激活。

SQL/内存SQLite/外键增量/绑定隔离测试通过；mock禁用所有Governor getter，读取属性正常，覆盖control缺失、到任、建立、阈值与0撤销的显式fixture。没有模拟引擎实际评估、建立计时或Property自动撤销，以上仍USER_GAME_TEST_REQUIRED。SQLite源只读，未修改缓存。

## 用户小批测试（最多三项；先看加载校验）

用户手动重启加载现有测试存档，标题应为P0-A-007。SQL也有增量，因此先选当前城点Read governor看control。

1. **加载/存在**：control应1。有已派遣总督时present应1；尚未建立时established应nil/0。截图即可。若control不是1，停止并回传；优先调查存档是否接受新增trait modifiers，不要求你立即重开一局。control缺失属于加载/桥接未准备，不能判定没有总督。如果总督已建立，直接按状态记录1，不要求撤回制造未建立状态。
2. **建立**：若当前正在到任，不改变晋升或城市，推进到游戏总督界面显示已建立，再Read。present保持1，established由nil/0变1。有至少两头衔时Req2应1；仅任命时Req2应nil/0。若已经建立可跳过此项，回报未测试转变。
3. **阈值或撤销（二选一，选现成条件）**：若已有建立且只任命的总督及1个可用头衔，增加一次普通晋升，预期Req2由nil/0变1，Req3/4不激活；或将总督调离，读取原城，present/established/Req2/3/4都应nil/0。不为这项强行开新局或获取多级晋升。

PASS按每个已执行子项记录，未执行的不外推。ERROR、control异常、状态不匹配应截图保留字段及总督界面，不反复尝试多回合。无条件校验成功却条件不变，需要继续调查原生条件或Modifier刷新，不能声称已经修复。

截图放ScreenshotInbox，默认文件名即可；不用重测专家。旧A3精确titleCandidate方案暂停，后续优先验证引擎阈值。

修改文件：Probe.lua、Data/GovernorProbe.sql、UI/P0Panel.xml、SpecializationP0.modinfo、DevelopmentTests/test_specialization_p0.py、test_specialization_identity.py及状态/架构/本记录。备份DevelopmentBackups/SpecializationP0-P0-A-006。未启动游戏。
