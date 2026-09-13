# 小数收益证据：原生每人口路径与平坦收益路径须分开

Document Owner: Codex

见[文化三图与精确计算](../../Status/Validation/Results/Specialization_B038_Culture_User_Result.md)。本次3人口、0/1/2专家，原生城市文化2.609375/6.66015625/10.7109375，等增量4.05078125。与每专家原有3+新增1.5，经截图宜居度-1对应的-10%后4.05吻合。支持0.5人口奖励保留并参与本局百分比，不是半点丢失。

本机数据库静态证据：HAPPINESS_DISPLEASED NonFoodYieldModifier=-10，范围-2..-1；原生per-population Modifier Amount0.5，Culture bit0的BuildingModifiers绑定存在。此路线与B029固定城市YieldChange小数失败不同，不归纳“所有Modifier支持/不支持小数”。

三个Getter值都在1/256网格上，差值1037/256；只记观察到的粒度，不确定引擎存储类型、全局精度或取整算法。0.00078125小误差不等于损失0.5。UI单小数显示及刷新滞后又是另一层，分析优先用原生Getter并核对当前人口/专家/倍率。

当前Design仍D0010的0.5。用户允许讨论1作为未来备选不构成立即变更；本轮不改任何收益值。文化本场景通过，未来复用优先采用经过对应路径验证的原生Modifier，不将结论迁移到Tourism/Great Work/其它精度未验证效果。
