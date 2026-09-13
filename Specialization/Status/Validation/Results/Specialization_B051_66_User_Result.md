# B051.66：自动收益通过范围与区域限制失败

Document Owner: Codex
Observed build: P0-B-051 / modinfo66

USER_GAME_TEST_PASS（用户明确实机回报）限以下范围：工业IV网络实际给予生产力，4.5P可由每人口分量与整数补偿正确组成；科研IV工业区/剧院区域50%实际转科技，0.5尾数正确。未附这些成功步骤的图，以口述为依据，不扩大到全部来源撤销/人口切换/存读档三案。

USER_GAME_TEST_FAIL：加入军营/圣地/政府等类型后整项科研复制停止。用户同时明确设计应涵盖所有非学院区域，包括社区/娱乐等不属于当前四专业的区域，通过行业等取得产出时也复制50%。这是范围澄清，不是批准改变50%或精度。

已读截图city65536、人口7、ACTIVE4，后台SAMPLED、请求14/接收14、有效回合25；错误COPY_DISTRICT_SCOPE_UNRESOLVED，SCIENCE未知/配置0。工业区Production8，下方旧小计8/半值4。Science13.12109375，Production27.5234375。说明后台链路已工作，旧四类范围检查导致停止；不能当作新后台失效，也不能拿旧小计当全区域总额。该城未接工业网络、Production本项0正常。

截图原名归档../Evidence/B051-scope/，SHA256见manifest.json。D0014及modinfo67移除窄范围限制，扩展类型原生结果仍待用户验证。
