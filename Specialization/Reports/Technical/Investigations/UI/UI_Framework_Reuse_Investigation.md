# UI Framework / Reuse Investigation

> Publication note: machine-specific prefixes have been replaced with source labels; technical conclusions, evidence scope and historical observations are unchanged. `CIV_ASSETS` denotes the installed `Civ6.app/Contents/Assets`; `WORKSHOP_289070` denotes Civilization VI Workshop content, with each following numeric directory identifying its published item; `CIV6_USER_DATA` denotes the configured Civilization VI user-data root. Suffixes and line references preserve the original source location. These are source locators, not public links or shell variables.


Investigation / Non-authoritative / No design decision implied

Status: Stable
维护者: General Investigation Agent（主会话写报告；子调查只读取证）
范围: 用户列出的 UI 及复用路线；不实施、不操作游戏、不修改 AI logic／Gameplay。
依据: develop `cde8db61c4d7aed07d8f0586b058e1b9ecbfe412`；Authority D0048／Status CURRENT S0432。启动时 tracked／staged 无改动；Diplomacy 三个 untracked 文件保持原样。UI 主题此前不存在。

## Confirmed facts / 已确认事实

**已读界面以 Civ VI 原生 Lua／XML 实现。最值得复用的是列表／详情／树节点的组织方式、状态管理和选择／确认流程；业务脚本需要按新用途独立适配。**

本轮证据为 STATIC_CONFIRMED：已读 manifest、XML、Lua 调用和注册。没有运行游戏或测试；不新增 LOCAL_SIMULATION_PASS／USER_GAME_TEST。安装登记、组件注册、当前最终解析的脚本与用户实际看到的画面分别处理。

### 对象与结构总表

| 界面 | 本机源码版本／入口方式 | 主要组件与组织方式 | 复用价值与边界 |
|---|---|---|---|
| Better Trade Screen | manifest **4.2 / Beta**；ImportFiles 同名原版总览／chooser／support；Settings 独立 InGame context | 三 tab、筛选／分组／多字段排序、可折叠组、滚动行；选择目标后显示城市／收益详情，再按 Begin | 很适合列表管理与目标选择；TradeSupport 同时含保存和自动续商路，不能整份当纯 UI helper |
| Quick Deals | manifest **1**；独立 popup、按钮、三个 tab 与 offer automator contexts；显式 ReplaceUIScript 包装 DiplomacyActionView | 三 tab；出售页是库存／本方报价／AI报价三栏；共享 XML instances；异步报价／确认状态机 | 很适合独立窗口、组合页面、任务状态机与“先选再确认”；报价层会建立原生外交会话和工作交易，不是纯数据读取 |
| HD 间谍升级 | HD **2.2**；AddUserInterfaces 新 popup＋ImportFiles 配套 Lua／XML | 固定 **4层×5列**、三套节点／已解锁／连线实例；横向滚动、固定坐标／手工连线 | 可借节点状态与分层显示；不是通用自动树，绑定 Spy promotions、UNIT_SPY、原生 PROMOTE 和 SPYPROMOTION 桥接 |
| 原版总督列表／分配 | Expansion UI context；HD 导入同名 Panel／Details | 横向总督卡片；独立城市分配抽屉；owner＋cityID选择；旧／新总督对照；Confirm | 最适合“某实体分配到某城市”的确认流程；候选资格、忠诚 lens 与提交仍绑定 native Governor |
| 原版／HD 总督晋升 | 卡片内嵌 Details 子 context | 基础能力＋晋升节点；先待选后确认。Native固定3×3邻接绘线；HD读Prereqs，但仍限制相邻层／有限列差 | HD 更适合作为显式前置边的参考；两者都不是任意 DAG layout renderer |
| 右上间谍管理总览 | 原版 PartialScreenHooks 按钮；本机 BES **2.0 / Beta** 导入同名 Overview／Chooser／Support | Operatives／City Activity／Mission History 三 tab；间谍、城市、区域、俘虏、历史实例；BES加国家／区域筛选 | BES 是有源码证据的候选来源；没有独立按钮或新任务引擎，当前画面最终采用它仍 UNKNOWN |
| 间谍前往城市／任务选择 | Native Chooser＋Popup；BES重排 chooser | 目标列表、城市详情、任务预览、旅行时间、资格／失败理由；BES列表与任务并列 | 可借“目的地→任务→briefing→确认”视图流程；旅行、任务周期、概率与执行来自 native Spy operations |

### 公共组件是什么

| 层 | 已见具体组件 | 实际用途 |
|---|---|---|
| XML 布局 | Context／Container／Grid／Stack／ScrollPanel、Button／GridButton、Label／Image、PullDown、EditBox／CheckBox、AlphaAnim／SlideAnim | 定义层级、锚点、尺寸、滚动、输入、动画、实例模板；复用原版 Civ6 styles／图标／字体 |
| 重复元素 | XML `<Instance>`＋`InstanceManager:new(...)`、ResetInstances／GetInstance；局部 BuildInstanceForControl | 生成并复用列表行、节点、连线、图标；池化不等于可视区虚拟列表，也不证明大列表性能已通过 |
| Context／窗口 | ContextPtr 的 init／show／input／shutdown、LookUpControl、ChangeParent；UIManager QueuePopup／DequeuePopup | 窗口生命周期、输入焦点、层级、Esc、跨页面与原版 HUD 的协作 |
| 页签／弹窗辅助 | TabSupport、PopupDialog、ModalScreen_PlayerYieldsHelper、原版 Support／Icon helpers | 页签选择、确认对话框、顶部产出／背景与图标；需要保留其 Controls／include 依赖 |
| 数据与通知 | GameInfo／Players／PlayerConfigurations、TradeManager／DealManager／UnitManager／Governors；Events＋LuaEvents | 查询、资格、native 通知、Mod 内页面通信；发送请求与处理结果分别是两步 |
| 状态 | 本地选中项／tab／filter／dirty cache；GameDebug hotload cache；GameConfiguration／PlayerConfigurations；ExposedMembers | 这些是不同生命周期：热重载视图、用户设置、业务保存、跨 context 桥接，不能统称“存档系统” |

### 1. Better Trade Screen：列表管理和确认操作

结构是 **总览 → 目标选择器／起点选择器 → 独立确认操作**。总览三页分别查看自己的路线、到自己城市的路线及可用路线；城市组可展开／折叠，筛选、分组和多优先级排序分别处理。

总览用四类 InstanceManager 填同一 BodyStack；刷新先 ResetInstances，再按 tab 和数据源生成行，最后重算 ScrollPanel。选择器有当前选中城市、顶部城市／收益详情、候选城市列表及 BeginRouteButton；行点击主要修改选择，Begin 才做 CanStartOperation 和 MAKE_TRADE_ROUTE 请求。起点选择器另用 TELEPORT_TO_CITY，不是纯界面跳转。

可参考的不是“商路功能全包”，而是：**稳定记录键、数据适配、筛选／排序／分组、列表刷新、选中状态与详情、确认按钮**。源码也暴露了需保留的边界：

- Overview 会枚举起点×目的地；缓存和实例池不证明大地图耗时／内存已达标。
- 记录有 owner＋cityID；部分 selector 按城市名称比较，不宜作为新用途的稳定身份规则。
- TradeSupport 不只是 UI util：有 PlayerConfigurations 保存、路线 tracker、automater，最终可发 MAKE_TRADE_ROUTE。新界面不应随展示 helper 带入这些行为。
- 某个请求函数的 `return true` 位于 native 资格判断之外，不能拿它当操作完成 ACK。
- hotload 保存 visible／tab／filter／group，但排序条恢复仍有 TODO；不等于普通保存读档完整恢复。

HD 在 Expansion2＋BTS 条件下以 LoadOrder=15010 导入完整同名 TradeSupport／TradeRouteChooser；BTS 原包 ImportFiles 为 LoadOrder=11。HD 不是简单薄 wrapper，其差异包括可见地块刷新、目标校验、镜头／lens、world-input hook、yield／duration adapter。再次替换这些同名 context／helper 时必须先确定实际 owner。

### 2. Quick Deals：独立组合页面＋异步服务

这是本轮最清楚的“独立新屏幕”例子：AddUserInterfaces 注册主 popup、入口按钮、offer automator 和 Sale／Purchase／Exchange 三个子 tab；tab 打开时把自己的 context 重挂到主窗口 TabContentContainer，事件决定显示哪页。不是把三页都写进一个巨大的 Lua 函数。

主 XML 是固定1280×768的 modal 容器；出售页分库存、自己的待报价项目、对方报价三栏，每栏滚动，图标／报价行模板在 qd_instances.xml 共享。TabSupport 管页签，LeaderIcon和原版样式呈现对方与资源；Lua本地状态保存当前待报价项目，选择不等于成交。

入口按钮通过 LookUpControl 取得 `/InGame/LaunchBar/ButtonStack`，BuildInstanceForControl 插入 LaunchBarItem，并调整 backing／发送 resize。这是 **LaunchBar 的独立注入**；不是右上间谍按钮所在的 PartialScreenHooks。

关键业务边界：

- offer automator 有 FETCH／ACCEPT／EXCHANGE／MTGUPDATE 四类 job、pending job、awaiting response、close-request 标记。
- 报价并非一次 getter：会清／建立工作交易、RequestSession(MAKE_DEAL)，发送 INSPECT／EQUALIZE，然后等待 DiplomacyStatement，按 player／action 匹配响应再处理下一项。
- 接受操作先在UI核对工作交易，再进入 ACCEPT 状态；SendWorkingDeal(ACCEPTED) 与后续回应分别处理，不能把请求发出写成完成。
- 关闭时若仍等待外交回应，源码会等消费该回应后才完成 popup 关闭。状态机可借鉴，具体交易、会话和关闭约束不宜搬进无关用途。
- manifest 以 LoadOrder=99999 显式 ReplaceUIScript(DiplomacyActionView)。这份 Lua先include当前Expansion2／Expansion1／Base版本，保存BASE函数并包装 statement handler，处理 QD 查询期间的原生对话显示；不是独立popup就完全无覆盖风险。
- gameplay/qd_cachemanager 只是本地 Lua 表缓存，通过 ExposedMembers.QD.CacheManager 暴露给UI；已读代码不做 Game property 持久化，不应称完整存档机制。通知开关另用GameConfiguration；本轮未读取用户实际设置。

最可用的借鉴是 **独立context／共享instance模板／子页通信／请求与响应状态机／取消与收尾**。qd_offerautomator、diplomacy wrapper、金币换算／报价策略属于其业务服务，不是通用UI组件。

### 3. 原版总督：城市分配与晋升树

主列表是横向总督卡片，详情是内嵌子context，分配是独立侧栏。候选记录保存 **城市owner＋cityID**；上方显示选中城市、新总督与可能被替换的旧总督。点击行先改本地选择／镜头／忠诚 lens；Confirm遇到已有本玩家总督时再弹替换确认，最后请求 ASSIGN_GOVERNOR。

晋升也分为两阶段：节点点击修改 m_SelectedPromotion；Confirm才请求PROMOTE_GOVERNOR。节点视觉状态来自已获得、CanEarnPromotion、当前待选、read-only；资格getter和失败tooltip可以作为适配模式参考，不能把总督Hash或native operation类型直接用于新玩法。

树不是自动通用布局：Native按Level／Column固定三层三列，并以邻接矩阵绘线；HD按 GovernorPromotionPrereqs 显式边绘线，但只处理相邻层、列差0／±1／±2，仍有固定尺寸和offset。HD改动适合作为“前置关系数据→连线”的参考，复杂树需另做布局合同。

同样存在副作用与生命周期差异：关闭可能SetTitleConsidered(true)，选城改lens，相机与popup互相开关；主列表read-only是WorldCongress状态，不是通用权限系统。Details的hotload只保存visible／governorIndex，重新Open清待选晋升；Chooser保存总督＋选中城市owner／ID。部分脚本没有显式解绑全部事件，不能静态断言泄漏，但复用后必须验证hotload。

HD以ImportFiles／LoadOrder150000导入同名Panel／Details。XML却明确引用Expansion1 Details路径，而Expansion1／2 Details存在不同回调签名、取消及read-only处理；最终VFS解析版本 UNKNOWN。原版AddUserInterfaces在官方Expansion1 manifest注册Panel／AssignmentChooser；“InGame.xml没找到”不是“原版没有入口”。Native和HD还存在macOS先限制宽度还是先CalculateSize的差异，需要实际缩放核对。

### 4. 间谍管理、前往城市、任务选择、HD升级

**右上入口已经闭合为原版链：** PartialScreenHooks.xml 的右上ButtonStack同时包含WorldRankings入口；AddEspionageHook按解锁／capability加按钮，OnToggleEspionage发送 `PartialScreenHooks_OpenEspionage`。原版Overview和BESOverview都监听这个事件。因此本机BES是匹配该描述的候选，但不是仅凭位置就确认用户当下画面归属。

Overview是三个tab、五类实例：间谍、城市、区域、俘虏和任务历史；列表按tab重建，读取native units／off-map／captured／mission history。原版Chooser选中目的地后收起目的地列表并显示任务预览，briefing和完成结果交给独立EspionagePopup；BES将目的地列表与任务预览并排，加国家、城邦／国际及区域筛选。

这些结构仍调用native CanStartOperation、目标plots／失败原因、travel／establish时间、RequestOperation与SPY interface modes；BES没有另造mission engine。任务时长和概率不是纯Lua UI计时器。复制列表／preview可以，复制原生spy handler不能据此得到其它单位的任务生命周期。

HD升级是另一个窗口：独立AddUserInterfaces popup，固定4×5布局，三套IM显示已解锁节点、可选节点和连线；节点来自Spy promotion class／Level，坐标与连线手工安排。Show handler只接UNIT_SPY并dequeue原版promotion popup，点击发native PROMOTE，同时通过ExposedMembers.SPYPROMOTION存取其技能状态。桥接provider／底层存储未因UI任务扩展审计；这不是通用树或纯呈现脚本。

**实用兼容风险：** BES的区域筛选调用其EspionageSupport里的 `hasDistrict`，已读HD同名Support没有该helper；HD导入Support的LoadOrder为150000，BES未声明显式LoadOrder。若实际include解析HD版本且无其它provider，筛选可能缺helper。此处只报条件性冲突：最终解析和是否报错 UNKNOWN，不宣称当前游戏已经坏了。原版Expansion wrappers还会覆写目的地枚举，因此BES的城邦筛选实际覆盖不能单凭其base文件保证。

## 关键证据入口

行号为本轮读取版本；这些外部文件只有只读权限。

| 对象 | 直接入口／必要调用 |
|---|---|
| BTS | manifest (`WORKSHOP_289070/873246701/Better Trade Screen.modinfo:45`)；总览实例／刷新 (`WORKSHOP_289070/873246701/UI/TradeOverview.lua:70`)；选择器 (`WORKSHOP_289070/873246701/UI/Choosers/TradeRouteChooser.lua:363`)；确认操作 (`WORKSHOP_289070/873246701/UI/Choosers/TradeRouteChooser.lua:919`)；自动续订 (`WORKSHOP_289070/873246701/UI/TradeSupport.lua:473`) |
| HD BTS兼容 | 条件注册 (`WORKSHOP_289070/2465378070/DL.modinfo:1302`)；同名chooser目标处理 (`WORKSHOP_289070/2465378070/ModSupport/BetterTradeScreen/TradeRouteChooser.lua:860`) |
| Quick Deals | manifest (`WORKSHOP_289070/2460661464/QuickDeals.modinfo:31`)；popup与tab (`WORKSHOP_289070/2460661464/ui/qd_dealpopup.lua:29`)；共享模板 (`WORKSHOP_289070/2460661464/ui/qd_instances.xml:11`)；入口注入 (`WORKSHOP_289070/2460661464/ui/qd_launchbutton.lua:13`)；异步响应 (`WORKSHOP_289070/2460661464/ui/qd_offerautomator.lua:53`)；真正接受 (`WORKSHOP_289070/2460661464/ui/qd_offerautomator.lua:413`)；包装原生对话 (`WORKSHOP_289070/2460661464/ui/diplomacyactionview_qd.lua:1`)；桥接缓存 (`WORKSHOP_289070/2460661464/gameplay/qd_cachemanager.lua:1`) |
| 总督 | 官方注册 (`CIV_ASSETS/DLC/Expansion1/Expansion1.modinfo:229`)；城市候选／选择 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/GovernorAssignmentChooser.lua:153`)；分配确认 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/GovernorAssignmentChooser.lua:397`)；Native晋升节点 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/GovernorDetailsPanel.lua:150`)；HD前置边 (`WORKSHOP_289070/2465378070/UI/Replacement/GovernorDetailsPanel.lua:228`) |
| 右上间谍入口 | 右上按钮XML (`CIV_ASSETS/Base/Assets/UI/PartialScreenHooks.xml:12`)；开关事件 (`CIV_ASSETS/Base/Assets/UI/PartialScreenHooks.lua:93`)；能力入口 (`CIV_ASSETS/Base/Assets/UI/PartialScreenHooks.lua:238`) |
| BES／Native任务 | BES manifest (`WORKSHOP_289070/872296228/BetterEspionageScreen.modinfo:13`)；并列chooser (`WORKSHOP_289070/872296228/Base/Assets/UI/Choosers/EspionageChooser.lua:142`)；筛选helper (`WORKSHOP_289070/872296228/Base/Assets/UI/EspionageSupport.lua:228`)；native任务确认 (`CIV_ASSETS/Base/Assets/UI/Popups/EspionagePopup.lua:472`) |
| HD间谍树 | 独立popup注册 (`WORKSHOP_289070/2465378070/DL.modinfo:2209`)；三套节点实例 (`WORKSHOP_289070/2465378070/UI/Replacement/HD_PKSpyUnitPromotionPopup.lua:20`)；native命令／桥接 (`WORKSHOP_289070/2465378070/UI/Replacement/HD_PKSpyUnitPromotionPopup.lua:69`)；固定XML窗口 (`WORKSHOP_289070/2465378070/UI/Replacement/HD_PKSpyUnitPromotionPopup.xml:18`) |

## 可复用路线

### 推荐默认：独立新 context，借模式与小部件

如果目标是将来的专业／任务界面，默认选择**独立 AddUserInterfaces context**，XML声明布局和instances，Lua管理视图状态。按用途参考不同对象：

| 我们想做的界面 | 最合适参考 | 应独立替换的部分 |
|---|---|---|
| 城市／任务总览、筛选排序、列表＋详情 | BTS／BES | 数据record、稳定owner＋id、查询／资格适配、缓存失效规则；不要带入商路tracker或Spy原生state |
| 某实体分配到某城市 | GovernorAssignmentChooser | 候选资格、预览数据与实际 action；保留先选择后Confirm、取消和失败理由模式 |
| 多页库存／方案／报价式比较 | QD的主popup＋共享instances＋独立子tab | 页面model与异步service；不带入working deal／报价和外交会话逻辑 |
| 分层能力树 | HD Governor Details优先参考前置关系；HD Spy参考视觉状态 | 节点数据、坐标／边布局、资格、成本、确认／撤销；复杂DAG不能直接套固定3×3或4×5 |

最低必要分层是 **view → query/model adapter → action adapter**。先给只读数据、资格和选择状态，用户确认后由明确业务层发送请求；结果事件再重读与刷新。它不规定 Gameplay规则或保存合同。

```mermaid
flowchart LR
  Entry[独立入口与Context] --> View[XML布局与实例行/节点]
  Query[查询与资格适配] --> View
  View --> Select[本地选择/详情/待确认]
  Select --> Confirm[用户确认]
  Confirm --> Action[明确业务Action适配]
  Action --> Result[结果或失败/变化事件]
  Result --> Query
```

### 条件适用：给现有界面做小包装

需要保留原有业务入口时，可参考QD的 `include base →保存BASE函数→包装少数handler`，或者以LuaEvents对现有页面做窄接入。但先确认当前真正owner与回调签名；高LoadOrder不是自动兼容策略，也不能让两个完整替换同时成为主版本。

只有确实要求改原有商路／间谍界面时，才考虑完整同名替换。它会继承原版、Expansion、HD、其它UImod的上下文与helper依赖，维护成本最高。结构借鉴与逐段代码／资源移植分开；本轮没有核对发布／复制许可，不提供整包搬用结论。

## Inference / Unknown

- **高置信度推断**：独立context＋小范围结构借鉴比再次完整覆盖共享原版context更容易隔离依赖；是否采用由用户／Main Task后续review决定，不是本轮批准架构。
- **高置信度推断**：现成列表、节点模板、选择／确认流程可复用；native getters／operations、交易状态机、Spy身份、Governor资格、商路保存和自动化不是通用控件。
- **UNKNOWN**：本局当前最终加载的Overview／Chooser／Support／GovernorDetails版本；用户看到的右上间谍总览实际归属；BES／HD同名helper是否已经触发冲突；各复制组合的行为、布局、分辨率／缩放及性能。
- **UNKNOWN**：SPYPROMOTION provider／持久化合同、其它新玩法能否使用native Spy／Governor／Trade operation；本轮没有沿这些问题继续技术实施或其它主题调查。
- 安装登记和manifest版本是本次读到的源码信息；Native运行build未重新确认，未把前轮游戏版本当本轮实机证据。没有读取用户存档、备份、私人设置或二进制。

## Minimal native validation suggestions

本轮未运行。用户先决定要借鉴哪个结构与是否接入原有context；若以后授权实现，再按实际新增部分选择最小核对：

1. 当前原生按钮实际打开哪份界面、共享helper实际来源；先关闭“候选归属／覆盖顺序”未知。
2. 独立窗口开关、Esc／输入焦点、UI层级、取消／再次打开、热重载／本地玩家切换；确认没有重复订阅或残留popup／lens。
3. 列表过滤排序／折叠、owner＋id选中一致、目标消失／资格变化后刷新、确认请求与真正完成分别显示。
4. 能力树边与资格对应、固定布局的长文本／缩放；大城市列表响应／滚动性能。不要从IM池化或能打开窗口推导全场景PASS。

以上不是要求一次全测；新UI若只展示数据，就不加入交易、商路或Spy业务测试。

## Read Ledger

- Stage A：根／项目／调查区规则和导航、Git、Authority 必要元数据、Status CURRENT；当前 UI 用户任务及已有本机技术入口。此前用户全局技术来源补充保存在 Diplomacy README，本轮仅重核该来源／许可说明，没有读取其技术报告或扩展外交研究。未加载四专业实施 manifest／历史。
- 已执行来源定位：在用户已授权 `Firaxis Games/Sid Meier's Civilization VI/Mods.sqlite` 以 `mode=ro` 查询 Name 含 Trade Screen／Quick Deals／Espionage／Spy 的必要注册路径；未展开无关 Mod 或私人设置。HD manifest 的当前主题文件引用已查。
- C-UI1（计划，执行前记录）：未知是用户所述界面的控件／状态／操作层。拟在已授权原版 Assets 的 Base／Expansion1／Expansion2 UI 中按 Governor／Espionage／Spy／LaunchBar 的文件名定位，沿注册、include、XML instance／style、callback、Events／LuaEvents、UI／UnitManager／PlayerOperations 调用读取必要定义；HD 从 DL.modinfo 中对应 replacement／popup／BTS compatibility 文件沿同一链扩展。目标是给出 reusable UI layer 与 native operation 的边界；直接组件与生命周期足够或具体缺口即停止，不展开数据收益、AI planner、二进制或无关 UI。
- C-UI2（用户已明确确认，执行前记录）：登记路径为 Better Trade Screen `.../873246701/Better Trade Screen.modinfo`、Quick Deals `.../2460661464/QuickDeals.modinfo`、Better Espionage Screen `.../872296228/BetterEspionageScreen.modinfo`，均在 `WORKSHOP_289070/`。用户允许本次定域只读，确认后才读取各 manifest，沿 UI XML／Lua 和必要 include、entry／refresh／operation 调用研究组件，不通读整个 Mod；找到足够结构及风险或未知即止。确认前未读取这些目录，登记不等于读取许可。
- C-UI3（计划，执行前记录；已授权原版内）：原生总督 context 注册与右上间谍按钮尚未闭合。拟只查 `Base/Assets/UI/InGame.xml`／`DLC/Expansion2/UI/InGame.xml`（不存在即停）中的 GovernorPanel／Details／Chooser 引用，以及 Base／Expansion1／Expansion2 UI 内文件名含 PartialScreenHooks 的 Lua／XML，沿 Espionage／Victory 按钮与 `PartialScreenHooks_OpenEspionage` 映射读必要片段；目标是入口→context 证据，不从位置猜归属。另沿 GovernorPanel.xml 已明示的 `DLC/Expansion1/UI/Additions/GovernorDetailsPanel` 子 context 读取该 Lua／XML，与同名 Exp2／HD 定义对照；不扩大其它界面，取得注册／映射或明确缺口即止。
- 执行结果：三个新Mod目录均在用户确认后读取manifest及直接UI调用。BTS／HD覆盖、Quick Deals独立contexts与native会话状态机、HD固定Spy树、Native／HDGovernor卡片／分配／树已取得足够结构。C-UI3的Base InGame无Governor命中、Exp2 InGame不存在，停止猜路径；官方Expansion1 manifest的直接文件注册另确认Panel／Chooser入口，XML已明确引用的Exp1 Details实际读取并发现与Exp2签名差异。右上入口按PartialScreenHooks闭合到Overview；最终VFS／实机归属继续UNKNOWN。
- 关键扩展均沿include／XML context／回调／manifest：Quick Deals的qd_cachemanager桥接与diplomacy包装、GovernorDetails E1引用、BTS TradeSupport保存／automater、BES hasDistrict helper。没有借UI任务研究AI决策算法、Gameplay数值或桥接持久化全体系。
- 主会话独占本主题Markdown写入，子调查只读并已收口；Diplomacy既有三个untracked文件不修改。除已说明的来源许可入口外，未加载其它Investigation技术报告；未进入其它Mod、Historical、存档／备份、私人设置、二进制，不递归通读Assets或整个Mod，不执行源码中的操作。
- 收口：已核对本主题两个Markdown的链接目标、无占位／尾部空白；HEAD仍为启动时cde8db61，tracked／staged diff为空，已有Diplomacy三文件保留，仅新增UI两文件。文档核对不算LOCAL／native PASS；未写治理／hash／配置或Git。

## Handoff

**Stable checkpoint：本报告与同目录README已停写。** 用户需要决定：将来的具体界面用途，以及独立新context／窄包装／完整覆盖哪条路线；本轮没有实施授权。用户需要测试：本轮无。Codex下一步：等待用户讨论，不继续调查或实施，不自行更新正式Architecture或联系Main Task；是否接受指定checkpoint入库由用户决定，Git只读。
