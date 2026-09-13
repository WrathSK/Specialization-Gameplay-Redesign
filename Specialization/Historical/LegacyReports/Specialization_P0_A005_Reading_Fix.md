> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

# A004用户截图与A005修订

USER_GAME_TEST_FAIL：A004 Specialist读取。按文件时间第一张截图明确显示Probe.lua:340，function expected instead of nil，调用链为FocusProbe→Gameplay。对应源码为city:GetDistricts():Members()迭代。证明该路径不可用；还不能仅凭错误区分Members函数自身和返回迭代器的细节。

第二张显示回合2的DISPATCH_RETURNED。它只证明派发调用返回，不含Governor或Specialist返回值，也没有标明动作，不能据此分别判两个getter失败。用户报告过回合仍无信息；Governor语义保持USER_GAME_TEST_REQUIRED，A004结果展示可用性记录失败，不再让用户靠过回合尝试。

- 截图1：[系统原名](/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/DevelopmentReports/Screenshot 2026-09-10 at 9.49.24 PM.png)
- 截图2：[系统原名](/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/DevelopmentReports/Screenshot 2026-09-10 at 9.49.52 PM.png)

A005 STATIC_CONFIRMED：Specialist改用player:GetDistricts():Members()并通过district:GetCity()筛选选中城市（所有者和ID均匹配）；显式检查Members和返回iterator，上限512个玩家区域，显示上限6个专业区域。官方CitySupport.lua:360–361明确区分城市与玩家GetDistricts对象；和而不同UI/Additions/HD_GreatPeople_Common.lua:34及其后使用玩家Members和district:GetCity。Gameplay上下文是否完整仍需USER_GAME_TEST_REQUIRED。

UI单次点击Read后最多10秒观察ExposedMembers中的当前请求结果，显示ACK或READ FAILED（带Action及失败前阶段）。只读取已产生的诊断，不自动采样游戏、不发新请求；结束/超时/关闭脚本取消更新回调。超时不是API机制失败，Show仍可检查迟到结果。Show之前无请求则正常提示，不写PENDING_OR_ERROR吓人。剪贴板仍可选且未确认可用。

LOCAL_SIMULATION_PASS：原测试通过；新增城市GetDistricts抛错陷阱、玩家区域跨城过滤、nil迭代器、自动显示ACK/失败、10秒超时停止与迟到手动显示、首次Show友好提示。mock不能证明实际native iterator行为；没有启动游戏或视觉自动化。

备份DevelopmentBackups/SpecializationP0-P0-A-004/。修改Probe.lua、Gameplay.lua、UI/P0Panel.lua/xml、modinfo、DevelopmentTests/test_specialization_p0.py及报告。没有修改sqrt设计、SQL、文明或已有Property。

## 当前仅复测两次读取

用户下次手动重启后加载现有存档，确认P0-A-005；不必新建、过回合或等待总督建立。

1. 选已经派遣总督的城市，点Read governor一次；结果应自动显示assigned=true、established=false（若已建立则true）、计数和Req2/3/4，或明确READ FAILED及At阶段。截图即可。PASS只表示读取入口正常，有效等级/晋升语义仍按后续A3测试。
2. 同城点Read specialists一次；结果应自动显示区域人数。没有专业区域应显示NO_SPECIALTY_DISTRICT，这只是空城读取正常，不算专家人数测试通过。有区域则显示workers和complete；异常应给明确READ FAILED。截图即可。

任何ERROR、NO RESPONSE或卡住就停止该项、回传画面，暂不继续旧A3a/A3b/A4变化测试。不要为了这两次读取再过回合。截图放ScreenshotInbox即可，原名保留；已存在的两张截图未删除。
