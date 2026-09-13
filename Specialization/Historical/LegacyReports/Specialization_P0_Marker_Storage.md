> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

# 城市状态：Property 与隐藏建筑

## 已确认的范围

USER_GAME_TEST_PASS：用户在P0-A-003中Mark后正常，Read/Copy面板ACK city=65536 marker=P0-A-003:1:1；保存、返回后重新加载，未再Mark，读值一致。此结果验证该城市该字符串Property的普通存读档，不证明所有字段类型、城市易主、多人同步或Modifier动态刷新。

USER_GAME_TEST_FAIL：系统剪贴板无法粘贴。官方Base/Assets/UI/Popups/ChatPanel.lua:507及FrontEnd/Multiplayer/StagingRoom.lua:975同样使用UIManager:SetClipboardString(sText)。本地调用形式与官方一致，但没有系统剪贴板读取证据，不能断言是macOS、焦点或游戏实现的问题。P.Call/pcall成功只表示调用未抛Lua异常。已取消“Diagnostics copied”假阳性，输出屏幕ACK及有限console export；实际剪贴板交付未修复确认。

## 和而不同本机源码先例（STATIC_CONFIRMED）

根目录：/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070/

- SubMods/CityPolicies/CityPolicies.sql:1、73：赋予BUILDING_CITY_POLICY_EMPTY，注释明确以建筑表示城市政策，通过项目启停。空政策标记与具有效果的政策建筑分开。
- UpdateDataBase/DL_Wonders.sql:1046–1058：BUILDING_MEENAKSHI_DUMMY_INTERNAL_ONLY，Cost=0、InternalOnly=1，注册HD_DUMMY_BUILDINGS，并成为其他建筑的BuildingPrereqs。该段没有为标记本身添加产出；外围效果建筑另有产出定义。这里并未显式写DISTRICT_CITY_CENTER，不能把用户记忆中的具体市中心建筑和此例画等号。
- Gameplay/HD_Common.lua:83–95：提供CreateBuilding/RemoveBuilding封装；668起把HD_DUMMY_BUILDINGS加入虚拟建筑集合。
- DLCSupport/HD_SEJONG.sql:10等：批量建筑规则显式排除HD_DUMMY_BUILDINGS。这是需要兼容排除的实际源码证据，“没有产出”不等于“不会参与其他机制”。

这些是本机已安装版本的源码事实，未替用户实测隐藏建筑新实现，也没有修改和而不同文件。

## 取舍（架构判断）

| 方面 | City Property | 隐藏/虚拟建筑 |
|---|---|---|
| 状态表达 | 单独key存专业、等级、版本等；本次字符串已验证 | 每种建筑天然表达存在/不存在；多级通常需要多个定义及互斥切换 |
| 数据库接入 | 需验证相应Property Requirement及变化后的刷新 | 可利用BuildingModifiers、建筑存在条件、BuildingPrereqs，接入路径直观 |
| 对其他机制的影响 | 不增加实体建筑记录；仍需检查Property读写/要求刷新 | 需排除生产购买、建筑计数、免费建筑、政策、前置条件等；InternalOnly不保证所有第三方代码都忽略 |
| 城市易主/移除 | 需要测试迁移/清理策略 | 需要测试俘获、掠夺、移除与重建，不能假定比Property更稳定 |
| 复杂状态 | 容易添加字段，但应使用独立简单标量 | 网络集合、数量、版本记录等若用建筑编码，定义和同步负担增加 |
| 当前证据 | 单城marker普通存读档已用户通过 | 有本机源码先例，本Mod尚无隐藏建筑实机验证 |

建议保留Property为唯一权威状态。若某项数据库效果无法可靠读取Property，可增加隐藏建筑作为由状态派生的效果开关，幂等同步；不把两套数据同时作为权威。若未来证明Property存在实质持久化问题，再独立试验完整建筑备用方案。

若引入建筑：使用独立SPC命名空间、零产出/维护、明确禁造禁买与捕获策略；兼容HD_DUMMY_BUILDINGS必须条件化，避免把和而不同变成必需依赖。只在状态变化时增删，不每回合重建。先做新增/移除、存读档、城市易主和建筑统计排除的小批测试。当前仅记录方案，不安装新建筑、不迁移已有marker。
