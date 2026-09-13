# B056：正式Boost恢复与巨作标准研究

Document Owner: Codex
Implementation Build: P0-B-056.73 / modinfo73
Design Reference: Accepted D0017 NET-RC-005、GW-001/002/003

## 已实施

恢复正式等级权重1/2/3/4；k_R、k_C独立为1。生成器同时生成SQL与Lua配置，1032组合完整保留浮点Amount。稳定载体ID沿用B055，以便既有清理/撤销逻辑继续识别；不新建一套残留效果。Native小数舍去按用户结果接受，没有Lua floor/round/补偿。更新版本和面板说明，GW仍为手动接口实验。

变更：tools/generate_boost.py、Mod/BoostConfig.lua、Mod/Data/NetworkBoost.sql、Mod/NetworkBoost.lua、Mod/Probe.lua、Mod/SpecializationP0.modinfo、Mod/UI/P0Panel.xml；新增DevelopmentTests/test_b056_formal_boost.py；Architecture/Status同步。

## 验证

STATIC_CONFIRMED：SQL引用/1032组合、manifest/UUID、accepted Design SHA保持。LOCAL_SIMULATION_PASS：独立全表L√N检查＋B055真实Lua状态测试及B054/B052/B051回归。B055旧测试冻结，新入口只适配明确列出的profile/version期望，不修改native读数的小数测试。

运行命令（仓库根）：
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/city-gpp-test-runtime /Users/xutingzheng/.pyenv/versions/3.10.13/bin/python3 DevelopmentTests/test_b056_formal_boost.py`

测试中的失效端点/owner/分类失败输出为故障注入断言，不是本次实机错误。SQLite外部数据库只读连接，复制至内存运行SQL。未启动Civ VI；正式权重效果及旧存档配置更新未另获USER_GAME_TEST_PASS。不重发已通过B055小数测试；旧存档仅新报告变更不证明保存的原生实例参数更新。

## Great Work实际研究（尚未决定玩法）

外部HD只读源码：Workshop 2465378070/UpdateDataBase/DL_GreatWorks_YieldChanges.sql:1–76；本机DebugGameplay只读查询交叉确认。HD_GREATWORK_YIELDCHANGES以类型、时代、YieldType为键，含文化基数和Tourism。42行，6类各7时代。

| 类别 | 古典 | 中世纪 | 文艺复兴 | 工业 | 现代 | 原子 | 信息 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 著作 | 2 | 3 | 6 | 9 | 12 | 15 | 18 |
| 音乐 | 4 | 6 | 6 | 9 | 12 | 15 | 18 |
| 雕塑/肖像/风景/宗教艺术 | 2 | 3 | 4 | 6 | 8 | 10 | 12 |

表内Culture与Tourism基数相同；这不是承诺补贴自动享有相同倍率。文物在表外独立设18文化/18旅游业。遗物、产品不在时代表。古代、未来也无表行。实际GreatWork_YieldChanges中有特殊著作额外/不同产出，故不从当前作品最大值猜曲线。

## DESIGN_DECISION_REQUIRED

GW-001已明确“补足当代基准”，但时代口径与缺失标准处理待决。可直接读取HD表作为实现数据源，避免硬编码复制整个HD。已提出候选：玩家当前时代，表中缺失暂不补贴。这会使未来时代没有标准；如希望未来继续保留信息时代标准，需要明确选择“沿用最近已定义时代”，不能自行视为已批准。文物无曲线不等于排除它的GW002资格。

还需区分补贴Culture与Tourism、theming及作品专属加成。现有用户实验只验证单件著作+2Culture的城市/作品两后端及撤销，不能推导旅游或主题化。GW002仍须明确适用类型/专业区域清单与城市倍率处理；不因本次时代研究静默实现整个Great Work系统。建议先确定上述WHAT，再实现可替换的城市补贴计算与后台作品状态读取，按作品移动/时代变化/ACTIVE失效准备小批次。

## 部署

版本73，94运行文件。源/运行hash：`d13b986f93d6b219c24a802525b29f1ddd8c96c446b710c3e4af58d0454c4a89`。
部署前72基线hash：`e021d6a4bbed39c9eefd1d8c3a1537a18f3e3ed5c77db175b5d6567271eefb1d`。
旧运行备份在外部SpecializationDeploymentBackups/.SpecializationP0-backup-j8mtgdnc，不进入Mods扫描或Git。源码本轮前备份在ignored local/before-b056-73。无commit/push。
