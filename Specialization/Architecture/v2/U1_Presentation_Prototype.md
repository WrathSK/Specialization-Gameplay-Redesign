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
