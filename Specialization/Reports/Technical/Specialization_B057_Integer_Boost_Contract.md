# B057：最终一次整数Boost量化与巨作设计同步

Document Owner: Codex
Design Revision: D0018
Build: P0-B-057.74 / modinfo74

## Contract

RawStrength=k×L×sqrt(N) → 所有合法浮点修正/未来Entertainment → FinalRawBoost → math.floor(FinalRawBoost+0.5) → AppliedBoost → 原生接口。非负且有限输入；不使用默认round；仅末端一次。2.5→3排除banker语义；以1.49×1.4→2对比先round1×1.4→1，明确区分早量化。k/L/N/max-source/topology均不改。

## 本轮实现边界

用户要求正式集成前先做最小原生测试。NetworkBoost.lua新增Quantize与隔离Test路径；Test以最终Raw输入，0/1.5/3.8分别选无载体/整数2/整数4，每种类型一个载体；按整数ID保持幂等，清除旧载体后再添加。测试同时替换Research/Culture而非与原网络相加。重载重新初始化清理实验载体，恢复B056默认自动路径。实验原始值仅运行时保存，不进入永久事实。

Data/BoostIntegerTest.sql只定义四栋隐藏载体及各自原生Boost、HD显示Property参数；Amount为明确整数2/4。Gameplay处理专用实验指令，P0面板增加4入口（共12工作按钮）。不会直接TriggerBoost或修改进度。旧存档缺新定义时报告并停止实验切换；用户可以先用原存档，不预先要求新局。

默认自动网络仍是B056的未量化float配置，作为验证期间明确过渡。不是“D0018正式网络已实现”。原生整数通过后，正式集成需要：生成器改为整数AppliedBoost载体目录；Plan保留RawStrength/FinalRawBoost/AppliedBoost分别报告；所有未来效率修正在同一末端前完成；Audit按最终整数ID替换/复用，清理旧B055行；边界上限不得静默clamp。现有生成式SQL参数不能靠改一项Lua数字热改游戏Modifier，未来效率范围需配套整数载体覆盖或另证实动态参数接口。当前不定义Entertainment任何数值。

## 巨作设计

D0018 GW-001改为本城拥有作品的分组最高基础值；文化类（著作/音乐/艺术/文物）一组、遗物另组，产品排除。原时代曲线/时代选择不再适用。基础值不得使用本Mod补贴后或城市/作品倍率后的最终值，防止自抬基数。不同yield谁最高存在冲突时的选择/遗物具体yield维度、旅游业/theming倍率及GW002遗物范围仍需后续细化。没有把这些不明确内容自动实现，也没有改旧GW手动对照的类别。

## 本地验证

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/city-gpp-test-runtime /Users/xutingzheng/.pyenv/versions/3.10.13/bin/python3 DevelopmentTests/test_b057_integer_boost.py`

STATIC_CONFIRMED：SQL整数参数/有效Modifier引用/manifest与按钮；LOCAL_SIMULATION_PASS：Quantize边界、无效输入、同整数3.6/3.9不叠加、2→4移除2、0清零、恢复自动、读档清理、缺表安全拒绝、非测试玩家拒绝，以及B055/B054/B052/B051已有回归。最初测试夹具继承旧读数测试的回合2，导致恢复网络被正确判stale；重置夹具到发布报文回合1后通过，未改运行安全逻辑。原生整数差值USER_GAME_TEST_REQUIRED，不能拿SQL/配置报告作为PASS。

## 关闭/保留

OPEN-06整数精度策略已确定，不再接受引擎自行floor；最终封顶仍未定。旧原生截断观察仍保留历史正确性。OPEN-08时代曲线被本城最高基准取代，产品/文化与遗物分组确定；其它明确列出的边界保留。D0017原文/hash冻结，D0018已按用户决定接受。当前技术限制：整数原生效果与旧存档新增载体加载须用户测试；动态效率修正不能擅自提前量化，正式整数目录覆盖需实现；基础Boost绝对偏差/封顶未由本测试解决。

## 部署校验

95文件，源/运行同hash：`6db4eb5d2e10bab6acccae8d0e968788939707e0b1a10b72d0849fdac1d086f6`。旧运行在外部SpecializationDeploymentBackups/.SpecializationP0-backup-qp9f8r9d；源码本轮前备份ignored local/before-b057-74。UUID不变、未启动游戏、未commit/push。
