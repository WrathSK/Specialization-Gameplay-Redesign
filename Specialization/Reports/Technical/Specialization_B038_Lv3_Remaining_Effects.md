# B038：科研/文化人口收益与商业网络专家奖励

Document Owner: Codex
Design: D0010 RES-003 / CUL-003 / COM-003
Build: P0-B-038 / modinfo48

## 实现

Research/Culture：按实际对应区域工作专家0..255的二进制位，16个城中心隐藏建筑各绑定原生MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_PER_POPULATION，Amount=0.5×2^bit。游戏自行乘人口，合计0.5×Population×workers的基础Science/Culture，不用平坦YieldChange承载小数、不取整，也不是直接增加研究进度。先例HD UpdateDataBase/DL_Buildings.sql:737–751大学UNIVERSITY_ADD_POPULATION_SCIENCE Amount0.5；不同于既往B029固定城市收益失败路线。原生人口倍率/小数与城市百分比结合仍待实机，不能凭数据库值宣称成功。

Commerce：三个商业区隐藏专家建筑分别+2S/+2C/+2P。由当前贸易中心已接入来源类型去重，使用NetworkBridge.ConnectedKinds，在Gameplay核对本回合/signal/路线数/城市有效性并重新derive。不解析报告，不以source数量乘奖励。此接口取centers当前接入集合，不把仅接收但未接入本中心的远端来源当direct来源，也不启用Commerce IV汇聚。

19个新内部建筑无槽位、Housing或GPP。新Lv3Effects模块从EffectiveFacts验证标准专业锚点和ACTIVE>=3；未知/降级移除自身奖励，不删Lv1/Lv3支持/GPP。科研文化按工作人数增减系数；商业按类型增减载体。网络批次接收后、Rebuild后重新核对；TradeRouteProbe已有dirty事件提升signal后立即核对使旧网络奖励撤销，等待完整新批次恢复。既有专家/总督后台信号和投资确认触发该模块，报告仍只读。

Read auto Lv1附加configured人口基础额及商业类型载体。它是配置推导额，不是实际城市总产出，也不证明原生倍率。界面保持9按钮。原先GPP读数过回合延迟不修复。工业Lv3已在B037完成；至此四类Lv3设计组件均有实现，但本轮新增效果尚未实测，不能称全部Lv3通过。

## 本地证据

STATIC_CONFIRMED：新SQL在只读HD数据库的内存副本执行；16原生Modifier含0.5参数、3专家收益行；manifest48和全部Lua语法。LOCAL_SIMULATION_PASS：真实Lv3Effects与NetworkBridge模块，人数0/1/3、配置半点、ACTIVE降级、错误撤销/恢复、读档幂等、同类型多源去重、direct与仅接收区分、signal过期拒绝。测试test_lv3_effects.py；首轮测试SQL LIKE把下划线视作通配符误计既有COMMERCE支持行，已将测试查询修为GLOB并通过，运行SQL无需改动。

USER_GAME_TEST_REQUIRED：原生人口小数与百分比，网络类型专家收益真实发放/撤销。本轮无实机结果。依旧限定单人标准DEV适配，通用资格/Conquest、其它专业区域和Lv4不在范围。
