# U1 前置展示原型 — B087.114 / modinfo114

最新：用户技术验收PASS；[四图/证据边界](../../Status/Validation/Results/Specialization_B087_U1_User_Pass.md)。排版与文字润色后置，完整U1未完成。下方待实机为原交付时状态。

Status: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED。用户授权的是技术/显示原型，不是完整U1。Design D0035及四专业authority不改；D3整体用户PASS保留。

## 实际范围与显示

只有Research当前Identity/Potential1–4：四机构累计，分阶段能力名称/权威中文说明；ACTIVE不足不撤机构。学术传统明确“本测试版尚未实现”；D1汇总floor、D2每专家floor注明当前测试版口径，Shared显示术语使用基础设施深度。只说明条件，不伪造动态实际收益。

城市详情建筑/区域页的BreakdownStack追加“学院 · 专业机构（展示原型）”独立小节，固定四行+hover。不是嵌入学院BuildingInstance，不是实际Building。这是先确认位置与排版的最小原型；普通建筑与专业机构分组，用户尚未确认实际渲染/缩放效果。其它专业/历史机构/U2/U3未实现。

## 静态接入证据（STATIC_CONFIRMED）

本机HD workshop 2465378070：DL.modinfo对CityPanelOverview ReplaceUIScript load150000，DL_CityPanelOverview包含CityPolicies/Suk/Expansion链；CityPolicies以显示副本过滤CITY_CENTER，并发LuaEvent；其Instances独立UI通过ChangeParent挂到BreakdownStack。原版ViewPanelBreakdown使用BuildingsAndDistricts显示数据。

本Mod ReplaceUIScript load2000003先include实际HD DL_CityPanelOverview，再包装ViewPanelBreakdown，保留HD原函数链。原型依赖当前HD已安装脚本，不声明任意UI overhaul兼容；其它Mod若更晚替换同context仍可能覆盖，需实机观察。没有复制原版大UI文件、没有编辑HD。

## 改动与隔离

- InstitutionPresentation.lua：四阶段纯显示内容/tooltip及显示副本过滤。
- UI/InstitutionOverview.lua：包装现用HD入口。一次初始化从GameInfo建立BUILDING_SPC_且InternalOnly的精确ID集合；只在已确认Research城过滤当前页面的carrier行，普通/特色/其它Mod/internal反例保留。原CitySupport表不变，不改变引擎计数、Building实例、Modifier、D或模板。
- UI/Institutions.lua/xml：四个固定控件，无控件历史；重复相同状态不重建，卸载移除事件及重挂容器。
- Gameplay.lua：仅CITY_PRESENTATION_READ已有响应增加ACTIVE/status及城市坐标；无新request action、writer或持久状态。
- UI/CityPotential.lua：已有token匹配的响应完成后发送UI内LuaEvent；不增加实际Gameplay请求。原badge0.5秒dirty检查保持，不宣称已删除全局轮询；本原型没有新SetUpdate。
- Probe/modinfo/RuntimeAudit：B087.114版本与文件注册，runtime log版本一致。

cache只保留一个展示城及一份verified引用。暂时不可用保留机构、ACTIVE标待确认；确认其它Identity撤展示；换城按owner/id/x/y隔离，load重新初始化。沿用badge token抑制旧响应，不实施完整新epoch协议。页面刷新来自原界面事件或已有有效响应；相同显示signature不重跑原View。hover不读取Gameplay。关闭页不通过新路径请求/扫描。

隐藏只覆盖本次城市详情列表，且需要科研身份确认；区域地图Tooltip、生产列表、百科均没有新补丁或全面PASS声明。开发诊断保留原始载体信息。新build没有新SQL/carrier/收益/保存字段，没有关闭旧writer。

## 验证

LOCAL_SIMULATION_PASS（Lua/UI mock与静态检查，不是Civ VI实机）：

- 实际Lua：Potential1–4/ACTIVE0–4、临时UNKNOWN保留、确认非Research撤出、city reference不匹配排除。
- display过滤仅去本Mod internal，普通/其它Mod/internal对象保留，原数据不变。
- 10000次重复通知/Tooltip读取无新request/Gameplay写，wrapper相同signature不重绘；10000次render通知控件仍固定4，重复状态不重复parent/size。
- 所有Lua编译、XML/147文件manifest114；受保护runtime及Design与b1b997f逐文件对照。Gameplay改动仅只读响应。
- D3 210配置及D2/D1/C/B2/B1/A、AV2 A/B/C1/D1/C2/D2受保护链通过。适配器只扩版本、允许新增UI文件及旧mock可调用LuaEvent，不改收益断言；旧测试输出中的build文字为冻结标签，不是当前build。
- deployment安全测试通过。没有启动游戏；不宣称55GB内存问题或显示效果已经验证。

## 最小用户短测

在现有Research IV城打开“城市详情→建筑/区域”页，必要时向下滚动：确认四机构名称、分阶段hover可读、学术传统标未实现；普通学院建筑仍在，原先SPC技术建筑行隐藏。用现有收益/诊断确认D3等效果仍保留；有方便的总督操作时再看ACTIVE下降机构不消失，不强制制造掠夺。

只需反馈：小节是否出现、位置/文字是否清楚、carrier是否仍泄漏。若未出现，提供该页面截图和Lua.log；不要求先跑长局。本批不自动扩展到完整U1。

## 发布

coherent develop implementation；main/Design/收益SQL不变。W0003仍授权退出/备份/hash事务部署；最终部署状态见Status。保留完整B086运行包，不启动游戏。完成后停止等显示验收。


## B145.172 — 专业机构大类置顶

2026-10-01用户已授权显示修订；本地完成，原生布局待验。本节更新B087末尾小分类的位置/标题，不扩展完整U1或其它专业。

机构容器仍在城市详情BreakdownStack，置于城市概况之前；使用与原版奇观及HD城市政策一致的24高DivHeader、渐变与CityPanelSubPanelTitle，标题“专业机构”。固定四机构、Potential/ACTIVE、Tooltip及隐藏carrier语义保持；仅去掉已过时“学术传统尚未实现”标记，不改能力文字含义。

原生CityStates等使用GetChildren/SortChildren；此处建立一次局部顺序表，机构排0，其余兄弟保持原相对顺序。已置顶时不重复排序；不复制/替换HD完整面板，不移动其它节点到新容器。大小变化只重算当前显示stack及PanelStack。沿已有事件/单城展示缓存，无新Gameplay请求、轮询或永久字段；关闭卸载移除自身控件和订阅。

L1 STATIC_CONFIRMED / LOCAL_SIMULATION_PASS：原生/HD标题定义及排序用例；临时Lua mock执行实际Institutions.lua验证置顶、其它分类顺序、重复不排序、P4→P2换城、ACTIVE状态、隐藏/恢复、shutdown；XML及modinfo引用检查通过。未跑历史全套、stress或玩法回归。原生排序视觉/滚动仍USER_GAME_TEST_REQUIRED。

最小一次验收：打开科研城详情，专业机构在城市概况之前且标题与奇观同级；切换另一城后条目/阶段不串；向下滚动仍可正常访问建筑、奇观、城市政策。无需重复收益或年龄测试。B144/F2验收保持，下一Gameplay批次未授权。

部署：source77f9561，B145.172 / modinfo172，receipt B145.172-77f9561-playtest.json DEVELOP_ACTIVE；174/174 MATCH，游戏退出、B144/stable恢复点及无pending事务已核验。用户红框参考图已读取并归档外部Evidence/B145_UI_Layout_Reference_20261001，1/1 hash一致；这是布局需求证据，不是B145实机验收。


## B146.173 — 单行机构与阶段层级

用户授权仅UI表现：B145置顶/同级标题已在本轮截图显示，用户确认机构正常出现；这不是完整U1或其它专业验收。B146替代旧四个48高双行控件，使用原生InstanceManager管理32高单行实例；数据新增presentation-only level，行数按机构记录枚举，不按1–4索引写死。同阶段多个sibling可分别成行，当前仍只填既有科研机构；未实施Harbor。

左24宽罗马数字Ⅰ–Ⅳ；名称从38开始，随父宽缩放，右侧独立64宽状态栏，边缘8、名称与状态之间6间距。名称/状态使用原生TruncateWidth，名称完整内容保留在整行Tooltip。复用CityPanelText/Small，不新增图标。最高已知且有效阶段显示“当前”并保持完整alpha；此前已启用行名称alpha .9、阶段 .8、状态 .65（仍可读、不禁用）。Potential已建立而ACTIVE不足的行显示“未激活”并保留名称；UNKNOWN显示“待确认”，不猜阶段。例P4/ACTIVE1：Ⅰ当前，Ⅱ–Ⅳ未激活；同一最高阶段的siblings均可强调。

本地化新增现有TestText.sql中zh_Hans_CN/en_US五key：LOC_SPC_INSTITUTIONS_HEADER（专业机构/Institutions）、LOC_SPC_INSTITUTION_CURRENT（当前/Current）、ENABLED（启用/Active）、INACTIVE（未激活/Inactive）、UNKNOWN（待确认/Pending）；后四key共享LOC_SPC_INSTITUTION_前缀。机构名称与能力文字来源不变。

依赖仍是InstitutionOverview现有confirmed city view→本地render。相同显示signature不重建；变化时ResetInstances复用池，隐藏清活动实例，shutdown销毁池并解除订阅。只重新计算本地stack，不增加Gameplay请求、hover请求、轮询、保存字段或收益writer。无新专业/ACTIVE逻辑；B145分类置顶与精确carrier显示过滤不变。

L1 STATIC_CONFIRMED / LOCAL_SIMULATION_PASS：实际Lua临时mock覆盖P1/P2/P4、ACTIVE4→1、UNKNOWN、重复通知不重绘、隐藏/恢复/卸载、模拟同阶段sibling和对应Tooltip；Lua编译、XML模板、现有SQL本地化执行/10行校验通过。未跑玩法回归或stress。原生InstanceManager与父宽truncation有静态用例依据；真实罗马字体、缩放/滚动及截断仍USER_GAME_TEST_REQUIRED，不以mock代替视觉验收。

最小一次验收：现有科研P4城查看四个单行、罗马对齐、状态右对齐与最高ACTIVE突出；切换P1/P2城；调离总督后检查保留机构/未激活并切回；用一个可用的另一UI缩放或分辨率检查名称不覆盖状态及滚动，悬停读完整名称。若字体不支持罗马数字，报告后处理，不自行改图标。无需重做收益、投资或年龄测试。本批完成后停止，未授权文化/完整U1。

参考截图已逐张读取，外部Evidence/B146_UI_Row_Reference_20261001归档1/1 SHA256一致；仅证明旧双行显示与本轮修改需求，不作为B146验收。
