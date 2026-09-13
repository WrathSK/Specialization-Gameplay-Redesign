# Phase 1 独立项目迁移验证报告

Document Owner: Codex
Result: READY_WITH_NOTED_GAPS
Date: 2026-09-12

## 用户摘要

已按copy + validate建立独立项目。Mod/现在是唯一可编辑源码；旧游戏目录保留原包作为部署目标。没有初始化Git、连接GitHub、提交、推送、启动游戏或开发玩法。B051.67原实机待测项保持不变。

本地回归与部署模拟通过，源码及D0014没有变化。边界是游戏数据库/Lupa仍外部提供，历史链接按原证据保留而非全部改写，部署异常退出需要依据事务标记人工处理。用户本轮无需新测试；审核后决定是否授权Git Phase 2。

## A–C 建立与来源

目标：`/Users/xutingzheng/Projects/Specialization-Gameplay-Redesign`。

- 旧W嵌套Mods/SpecializationP0 → Mod/，77个文件逐字节一致。
- 旧W/Specialization → Specialization/，保留Design/Architecture/Status/Cases/Results/Reports/Historical嵌套；排除PNG、Evidence、日志和大机器manifest。
- 旧W/DevelopmentTests → DevelopmentTests/，排除3个CityGPPProbe脚本及缓存；历史脚本保留原断言并在Test_Catalog.json标注，不能全部当当前入口。
- B051前RuntimeSnapshot中7个基准 → DevelopmentTests/Fixtures/B051-before-copy/，源/hash见Fixtures/manifest.json。
- 新建root README/AGENTS/.gitignore、local配置模板、tools部署工具/说明、部署测试与本次报告。

目录计数：{"Mod": 77, "Specialization/Design": 15, "Specialization/Architecture": 1, "Specialization/Status": 135, "Specialization/Reports": 91, "Specialization/Historical": 104, "DevelopmentTests": 126, "tools": 2}。

## D 外部保留

旧runtime、整个DevelopmentBackups、截图Inbox/PNG Evidence、原始日志、数据库/缓存/存档、HD/Workshop/base assets和无关测试均未移入。`.dep`、ArtDefs保留项目自有引用定义，未复制引用的外部资源。local/config.json仅机器路径且被.gitignore忽略。详见Phase1_External_Materials.md。

## E / G 完整性

D0014 SHA256：`759365dd68c3b4a166b0f05e250b72f14e33dcc145c3889f6afefa16f999005c`。

所有Design文件、既有Historical/Results与7个fixtures逐字节对照来源一致；没有重解释FUTURE/DEFERRED。运行77文件完整，Mod manifest版本67、UUID `df9efdad-dd48-40a7-b868-87f0617bc16d` 保持。

对旧工作区原先记录的5126个文件重新hash，无变化。范围包括旧runtime、文档、Tests、Backups、Evidence/截图、DevelopmentReports和W/AGENTS.md。外部整个Steam/HD/base-game树未作全量hash；本轮没有执行对它们的写操作，DB由测试以mode=ro读入内存。不要把未扫描范围称为全量hash通过。

## F 本地检查

- test_b051_all_districts.py：PASS。真实Lua模块/背景事件模拟、255人口半点计划、范围/撤销/重建/幂等、80载体SQL、Lua/XML/modinfo及7基准。
- test_deployment.py：PASS。临时目录无变化部署、hash冲突拒绝、整包替换、注入故障回退、备份保留、未知文件/挂起事务/符号链接/错误UUID拒绝、无关Mod未动。
- test_convergence_plan.py：PASS，离线模型未改；不代表Commerce IV已实现。
- tools/deploy.py：只读PASS，source/runtime摘要hash相同，未apply。
- Python语法解析PASS；当前入口Markdown链接无未解析项；按已复制范围和凭据模式扫描无污染命中。模式扫描不是绝对安全证明。

STATIC_CONFIRMED=静态文件/结构证据；LOCAL_SIMULATION_PASS=本地模拟通过；两者均不等于Civ VI实机通过。B051.67仍USER_GAME_TEST_REQUIRED（待用户实机验证）。

## H 部署

默认`python3 tools/deploy.py`只读核对。显式--apply须提供刚审核的source/runtime完整树hash。仅允许项目UUID和SpecializationP0目标，不覆盖未知runtime-only文件或未审核改变；拒绝symlink/重叠路径。新整包stage验证后两次rename，旧整包备份保留；可捕获错误会回退。进程/机器硬中断可能短暂没有目标目录，但事务标记记录stage/backup并阻止重试；须按tools/README.md审核恢复。没有宣称跨崩溃单操作原子性。本轮live runtime没有覆盖。

## I–J 保留依赖与风险

- Python3 + Lupa lua55后端；当前测试使用既有临时安装，目录指示2.8但distribution metadata不完整。requirements-test.txt记录预期2.8；未重新安装/下载验证干净环境，不宣称完整依赖锁。
- SQL集成需要本机Civ VI/HD生成的DebugGameplay.sqlite，显式环境变量或local配置，只读；不随repo提供。纯模型/部署测试不需要DB。
- 1289个历史相对链接未解析，全部位于冻结Historical/Design Revisions；119个截图/备份等链接指向明确的本地外部材料。当前入口无未解析链接。Phase1_Link_Audit.json列出；旧证据不改字节、不制造stub。新Phase1前文档快照也是历史，只保存原文。
- 部分历史报告/旧脚本保留个人绝对路径作为出处；它们不是当前执行入口。隐私细节在Phase2 staging审核时仍需检查，尤其历史JSON；无凭据模式命中。
- 旧W/AGENTS.md与旧副本未改动；未来工作必须打开新repo，避免从旧入口继续编辑。旧目录保留用于回退，并非第二套可编辑source。
- 仅6个既有文件的迁移副本有预期改动：两份入口、Architecture A0112、Status S0117、测试README、当前base test的路径/import。运行、玩法、旧文件不变。测试逆向还原路径后与原文一致，断言未削弱。

## K 停止点

READY_WITH_NOTED_GAPS。独立边界已建立，下一阶段可由用户审核决定；本轮没有.git且未执行任何Git/GitHub操作。不继续P0/P1。

用户需要决定：审核本Phase 1结果后是否批准Phase 2。
用户需要测试：无新增；保留Status现有B051.67待测。
Codex下一步：停止，等待用户确认。
