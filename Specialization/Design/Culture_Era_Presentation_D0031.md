# Culture Great Work Era Presentation — D0031

Document Owner: Codex
Design Authority: User
Requirement State: USER_CONFIRMED
UI Options State: INVESTIGATION_ONLY / NOT_APPROVED_IMPLEMENTATION_ARCHITECTURE
Gameplay Authority: Content/Culture_D0029.json (unchanged)

## Confirmed requirement
在巨作管理相关UI中，让选中Culture城市容易看到已有/缺失历史时代、合理空间内每时代数量、缺失时代在国内其它城市是否存在及可选城市来源；文明无该时代合格作品时明确说明。只整理信息，不自动搬作品、优化主题、交易或新增驻留/冷却/移动惩罚。Dialogue仍取本城当前馆藏，不改为全国时代数。多Culture考察、Standardization、工程实践、传统补旧奇观及专家/完善度机制不因外部Review改变。

合格作品及时代语义唯一引用Culture_D0029.contracts.work_pool；未知Mod作品仍排除。不用HD Tooltip的创作日期替代作品历史时代。缺失时代列表需要与受支持作品/时代数据一致，不硬编码8或把未来时代保证可收藏；无法解析的数据应标未确认，不伪报缺失/国内无作品。

## Static investigation
原版 Base/Assets/UI/GreatWorksOverview.lua 在城市实例中设置CityName，使用嵌套巨作实例、滚动区域，并监听GreatWorkMoved。HD DL.modinfo加载UI/Replacement/GreatWorksSupport.lua，修改作品Tooltip，读取TurnCreated与静态EraType；当前调查没有证明其它UI Mod都不替换Overview。城市实例/建筑行分组必须原型核对，不假定每城只有一行。已有Presentation Institution是presentation-only规划，不能当已实现入口。

## Options (recommendations only)
| Option | Location/main | Tooltip | New panel | Compatibility/density/1080p |
|---|---|---|---|---|
| A City summary | 城市标题附近短时代标签 | 数量及国内来源 | 否 | 同屏直观；完整时代标签拥挤，城市多行可能重复；缩放时需折行 |
| B Dialogue tooltip | 机构/Dialogue入口摘要 | 完整覆盖及来源 | 否 | 低常驻占用；机构UI未实现，整理作品时需切换界面，不宜唯一入口 |
| C Inline detail | Overview内选中城市的侧/底详情 | 补充说明 | 新增同层详情区 | 来源城市清晰；占槽位空间，1080p高缩放风险最高，需滚动与收起 |
| D Hybrid | 城市摘要显示覆盖数/短缺失提示 | 每时代数量、其它城市来源、文明缺失 | 否 | 推荐；少侵占空间，长来源需摘要或同层展开，不能无上限Tooltip |

## Recommended direction — awaiting user approval
D为主，B未来提供同源摘要。不要固定5/8；分母仅在可收藏时代全集可靠时显示，否则只显示已覆盖数量及缺失名单。Tooltip按时代列数量、国内来源；长城市列表截为摘要并可在同层详情展开（此展开也未授权实现）。不把城市标题既有镜头点击行为替换为新行为。

## Data/performance proposal — not implementation authorization
打开Overview取得一次已确认聚合快照：city reference/revision、era counts、empire era→city index；包含非Culture城市供国内查询。Gameplay与UI共享同一eligibility/era规则，UI不重算权威公式。hover零请求；移动事件更新来源/目的城市及全国索引，创建/交易/易主/读档需对应刷新。国内来源变化会影响其它城市的“国内可得”提示，但不改变其本城计数。暂不可用保留已确认信息并标记，不能显示为0。无每秒扫描，关闭释放临时实例；有限对账安全网。数据成本约O(合格作品数+城市×时代数)，无需逐hover遍历。

## Prototype unknowns
Overview与HD/其它UI替换加载兼容；城市/建筑分组；1080p/1440p/4K UI缩放下Tooltip边界；事件覆盖、稳定作品时代解析、读档与跨城移动缓存一致性。STATIC_CONFIRMED仅表示源码证据，不是实机PASS。本轮无UI实现、无测试需求。
