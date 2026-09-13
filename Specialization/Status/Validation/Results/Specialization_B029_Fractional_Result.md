# B029：1.5配置实际仅+1，半点未体现

Document Owner: Codex
Date: 2026-09-12
Runtime: B029 / modinfo36
Verification: USER_GAME_TEST_FAIL（额外0.5未体现）；USER_GAME_TEST_PASS（OFF恢复；重复保持依用户回报）

用户称人工pass，并质疑重复测试。保留原话证据，但按截图的实际数值分项判读，不能把configured当实际收益。上一批三图配置为0→1→0，只有整数；本批两图为1.5→0，确实是不同档位，不再重发本组。

| 时间 | 配置 | Science total/delta | Culture total/delta | Production total/delta |
|---|---|---|---|---|
| 02:08:02 | 1.5 | 4.5 / 1 | 2.296875 / 1 | 7 / 1 |
| 02:08:04 | 0 | 3.5 / 0 | 1.296875 / 0 | 6 / 0 |

均为city65536。当前实际增量停留在整数档，额外0.5没有体现；这不是原生UI显示精度问题，Gameplay getter本身delta就是1.000000。OFF三项回零通过；重复不累加依用户明确人工pass回报，截图没有连续两个1.5状态，不能称两图独立证明重复过程。

STATIC_CONFIRMED：本轮只读查询当前缓存，三个HALF Amount仍为0.5文本：

[('SPC_B029_HALF_SCIENCE', '0.5'), ('SPC_B029_HALF_CULTURE', '0.5'), ('SPC_B029_HALF_PRODUCTION', '0.5')]

候选原因包含此Effect的Amount解析/精度或HALF实例/条件实际激活问题；未读取运行实例，尚不能断言所有Civ6 Modifier不支持小数，也不能从此两值推出任意数值的floor/round规则。整数新局已有效，旧档失败保留独立解释。

下一项先本地调查相同Effect的数值解析/替代承载与HALF激活证据，必要时设计能区分原因的新对照；本轮不再派同组测试，不自动接受整数化或量化fallback。新局已有OFF，无需再清理。商业IV精确收益承载仍未解决，非整个项目不可继续。

[原图与manifest](../Evidence/B029-Fraction/)已归档并核对SHA256。没有修改运行、Design或Tests，没有新模拟。
