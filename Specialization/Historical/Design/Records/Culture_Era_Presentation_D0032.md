# Culture Great Work Era Presentation — D0032

Document Owner: Codex
Design Authority: User
Direction State: USER_CONFIRMED_PRESENTATION_DIRECTION
Prototype State: PROTOTYPE_REQUIRED / NOT_IMPLEMENTED
Gameplay Authority: Content/Culture_D0029.json — unchanged
Previous investigation: [D0031 frozen options](Culture_Era_Presentation_D0031.md)

## Hybrid D — approved

Great Works管理界面的Culture城市附近显示紧凑摘要：**已覆盖N个时代｜缺：X、Y、Z**。不强制N/Total；可靠可收藏时代全集以后可支持分母，但不是当前合同要求。

Hover缓存明细按每个受支持历史时代列：本城合格作品数、缺失时代、本文明其它城市是否有作品，最好列来源城；确实国内无作品时明确说明。未知/不可取得的信息不得伪装为缺失或国内没有。长名称、换行、完整清单布局由原型决定。

## Authority / no automation

唯一eligibility与作品历史时代规则来自Culture_D0029.contracts.work_pool。未知Mod作品排除；UI不另建可用作品定义，不用当前/取得时代替代。国内时代索引仅提供作品位置线索，Dialogue X仍是本城作品时代数。无自动移动、主题化、最优组合、向AI购买或自动准备Dialogue。

## Runtime contract

打开Great Works界面及相关已确认城市数据变化时更新聚合；创建、移动、交易、城市易主更新受影响城市和国内时代索引。Hover零Gameplay request，无每秒扫描；使用有版本/城市引用的已确认缓存，暂不可用不猜0。受影响国内来源提示可失效重绘，但不因此改变他城本地时代数。保留av2-runtime-b076.103性能基线。

## Prototype gates

HD hook及其它UI替换、城市/建筑行分组、layout、pixel size、icons、wrapping、UI scale、tooltip placement、cache invalidation、move/trade/ownership/load事件仍PROTOTYPE_REQUIRED。D0031的静态接口调查不等于实机布局通过。当前仅批准方向，无UI实现或用户测试。
