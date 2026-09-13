# B042：独立施工队250与共同单位动作
Document Owner: Codex
Architecture: A0096
Status: S0100
Build: B042 / modinfo55
Design: D0010 unchanged; user confirms partial builder presentation reuse

## 实现
新增UNIT_SPC_CREW_250，BuildCharges=1、陆地平民、2移动、不可常规训练、无购买yield，未赋CLASS_BUILDER/改良能力/替代关系。Cost280仅DB占位，不接城市项目、不使用这个值结算注入。仅DEV spawn显式生成，用完消失。五正式项目/其它四单位规格/速度与开放策略未落实；不能称完整Crew。
ArtDefs/Units.artdef只复制原版UNIT_BUILDER呈现entry并改name，Formation/Members引用原版Units.artdef既有资源。Specialization.dep采用HD Units依赖格式，清除其它不相关HD依赖，只依赖基础游戏art ID和Units/Unit/VFX/Light。原版/HD文件未修改。图标别名复用原builder icon/portrait，无新原创美术，战略视图外观尚未单独验证。
新增Data/Crew.sql在10001004加载，避免HD早期全表批处理复制改动；没有TypeTags，因此不会主动继承builder-specific abilities。但第三方普遍单位modifier影响不能仅靠无tag全部排除；执行要求实际GetBuildCharges()==1，否则拒绝并报告，不擅自多次施工。

## Gameplay
UnitActions从新UI收到动作后独立核对testplayer、unit/owner；UnitTargets freshly枚举并对unit当前plot匹配，不能凭高亮执行。
Crew Prepare验证真实1charge、未reserved、合法当前目标，保存turn/target/cost/progress。Confirm一次性取出计划并再次核对上述条件；player Property receipt INTENT、unit reservation、Destroy后确认unit不存在，再核对目标未变，记录GRANT_ATTEMPTED、调用AddProgress(min(250,remaining))一次，最后COMPLETED。
这是同请求顺序操作，不是引擎原子事务。异常若已开始写入/消耗则HELD，不自动重播。极端崩溃/消耗后引擎异常可能留下未完成receipt或消耗而未获得生产；不凭receipt尝试补发不确定grant，不宣称完备事务恢复。正常重复Confirm无计划/无单位即拒绝；单位移除事件清prepared计划，避免ID复用。unit removal后使用缓存unitID记录receipt，避免读取已销毁对象。
DEV Spawn只在显式按钮触发，拒绝市中心已有平民；记录请求token去重。UI token含build/turn/sequence，同回合同序号读档碰撞可拒绝一次而不会重复发放；后续正式项目不采用此DEV spawn机制。

## 投资与UI
新单位动作入口在Identity已完成区域执行投资，复用原InvestmentAction.Property事务；site参数由Gameplay新入口设置，不允许直接信任UI布尔。Prepare和Confirm及消费前复验均核对anchor区域位置；pending INTENT阶段不会因自身pending而错误拒绝位置。
旧P0市中心入口维持原语义，方便历史存档和测试；地块位置是用户要求探索后继续推进的运行测试入口，Accepted D0010文本未自动修订。
Unit actions / sites提供Spawn / Prepare / Confirm；单位被消费改变选择时仍显示匹配请求结果，不因单位消失丢ACK。真实Crew自动BUILD标记，普通工人仍只可显式位置预览，不能进入消费接口。
头像/动作当前通过独立自有面板，不宣称原生工人动作栏集成。

## 验证与边界
test_crew_unit_actions.py：
- 实际UnitActions：准备零消费、cap100/250、消耗一次、重复/换目标/过回合/劳动力非1拒绝、重启后无重复。
- 实际InvestmentAction/EffectiveFacts旧市中心完整suite，历史manifest41断言仅内存适配55；再加入区域投资并验证消费+Potential2。故障注入输出RECOVERY_HELD为预期断言案例，不是运行失败。
- 实际新UI生成/准备/确认分发与单位消失后ACK；所有Lua、modinfo文件/XML。
- live DebugGameplay.sqlite只读复制内存后执行新SQL，验证1charge、CanTrain0、PurchaseYieldNULL、无tags；art XML新unit entry唯一。LOCAL_SIMULATION_PASS / STATIC_CONFIRMED，不等于美术引擎或游戏操作PASS。
本轮新测试仅B042三案；B041奇观已用户通过关闭。备份DevelopmentBackups/Specialization-before-B042-crew-unit。UUID/配置/Accepted Design hash保持。
