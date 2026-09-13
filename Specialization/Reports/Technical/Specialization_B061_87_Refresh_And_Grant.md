# B061.87 商路刷新与实际载体诊断

> HISTORICAL / WITHDRAWN：用户要求回滚，B061代码已隔离；当前为B060.85，不执行下列旧测试。


Document Owner: Codex

B061.86首批USER_GAME_TEST_FAIL：用户AUTO城市Science6→7、OFF6；截图只有OFF，source28.4219→20%5.6844→floor5，不能据此确认AUTO实际配置曾为5。第二图turn22 NETWORK_REFRESH_PENDING。未标商业四收益PASS。数据库已确认48载体定义存在，SCIENCE Amount为1/2/4等正确整数，不归因为旧组件缺失。

B061.87修复两项静态缺口：NetworkSender原先只按API调用成功去重，没有按Gameplay接收确认重试；BackgroundRoutes增加独立当前回合观察，漏回合事件时在已有UI脉冲中仅标记一次重采样。发送只对同包最多重试两次，不放宽当回合/来源有效性要求、不用旧网络继续发收益。收益报告增加每类实际存在载体总数值及bit组成，网络未就绪用简短状态/前后回合/发送状态代替长堆栈（完整日志保留）。

LOCAL_SIMULATION_PASS（不等于实机）：真实sender首次丢包恢复/最多两次/空闲零请求/新批恢复、真实turn observer一次触发，以及既有商业择优/撤销/SQL和旧批回归。实际只加1原因仍未确定；不猜测是倍率/刷新或成功。Design D0024、SQL/20%/floor/结算规则不变。

USER_GAME_TEST_REQUIRED：读原存档B061.87，原商业四城OFF后读一次，AUTO后Read Commerce IV截图，报告若目标5应显示配置5/载体5[1+4]；过一回合再Read截图。若仍未就绪，报告包含后台回合/发送信息，立即停止不重复。此次无新增组件，重载即可；若版本未刷新则完全退出重启。结果回来前暂缓多源/分发测试。

证据：外部W/Specialization/Status/Validation/Evidence/B061-86-First-Failure/manifest.json。
