# B162.189 — Meaning首次清理／OFF退出定域修复

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED。本结果不替代B161原生反证，不是完整L2 PASS。

## 已确认事实与根因范围

B161七图证明重启后session OFF但VALUE_5活动实例残留，旧GWA又已生效；未证明用户直接END是否执行，也未取得实际LoadScreenClose时序。源码可确认：首次清理依赖加载通知／玩家回合／ADVANCE，READ不初始化；空城市迭代会错误标ready；后台Dialogue／GWA可在Meaning首次清理前恢复；OFF END有仅确认token、不撤除残留的分支。前述机制缺口已定域修复，具体原生事件原因仍未唯一归因。

## 最小改动与责任

- `CultureMeaningProbe.lua`：一次startup/load exact37清理；至少可读取一个受支持玩家城市才可确认，资格不依赖Culture等级、总督或馆藏。空集合／支持身份暂不可读=PENDING；既有后台正向投影或本地玩家回合兜底，无新增轮询。逐城尝试撤销，不因一城失败漏清其它城。
- `Dialogue.lua`／`GreatWorkAdjacency.lua`：恢复旧正向收益前调用Meaning readiness gate；各模块自己清理自己的旧载体。已held的GWA零投影、full-reference Dialogue0%仍走既有当前资格／配对核验，不误阻断普通probe更新。Facts／sample intake／ACK照常。
- 真正撤销失败=FAILED，锁停普通sample/turn自动重试；残留城禁止旧正向混写，已清城可正常重算。同步busy阶段同样只读逐城exact37核验，不将其它城一起撤空。显式动作可恢复；不凭一城END宣称全局清理通过。
- OFF END执行本城exact37撤销，确认后旧writer依据当前事实重算；失败也由旧模块撤本城owned效果。整个同步recovery上下文覆盖撤销与恢复，结束即释放；重复token零写，新token才能重试失败动作。
- `BoostGreatWorkRead.lua`：session OFF、首次清理状态、实际载体／原生实例分别显示；READ仍零Gameplay写入，一explicit token最多一次全局原生Modifier枚举，Show／Copy不重扫。
- `Probe.lua`／modinfo：B162.189／189标识。SQL、37载体／259附件目录、Production公式、永久Property／账本、GC、Design及main不改。

## 本地证据

**108方法／96subTest PASS，0 failure／error／skip。** 复用真实Lua/request与read-only内层Firaxis DebugGameplay的内存副本，Lupa lua55；没有改外部数据库。旧README所示临时Python路径已不存在，本次复用现存兼容的Lupa安装并显式传入实际数据库，不修改配置或弱化条件。

| 选择范围 | 方法数 | 覆盖 |
|---|---:|---|
| 新startup/cleanup | 12 | 新session遗漏Load、0城早通知／身份未知、READ零写、两旧writer先清理、foreign exact37、真实失败锁停、ACK／其它城、OFF END／失败token恢复、同步全城Audit重入、ready快速路径／同回合ACTIVE变化 |
| 当前Production单值 | 24 | 0..10／逐域Floor／W、真实Shared建筑／掠夺／总督、UNKNOWN／reference／loss／load、写入失败与互斥、真实request／sample／Panel |
| 已有固定组合诊断 | 18 | 私有控制阶段／request／reader／退出及失败保护；不作为正式多片编码 |
| K Facts／Producer／LegacyIsolation | 23 | 采样、ACK、引用、移动、加载退出及旧系统隔离，直接受影响闭包 |
| selected原生reader fixture | 31 | 只读、准确owner／subject映射、signed字段、token／缓存／OFF残留与有界输出 |

首次新增测试在旧源码上失败（10方法、11 errors）；实现中定向回归抓出busy gate误阻断held0及同步重入隔离问题，已修代码并保持旧断言，最终上述范围全过。旧reader两个Panel字符串提取wrapper与版本184打包wrapper未选择；当前实际Panel由单值suite覆盖，独立syntax／modinfo检查另做。未跑旧five-yield全套、全历史或大规模stress；上述模拟不证明native收益／事件时序／真正载体撤销。

静态补检：5个变更Lua语法、modinfo189全部文件引用及27个当前导航链接／锚点PASS；context check/self-test PASS（182 runtime／432 guarded文件）。diff已复核，Design／SQL目录／工具未变。

## 性能、状态与退出

首次startup/load一次全局可读城市遍历，仅清本模块test载体，最多2048可读城市、仅37精确test IDs；临时城市集合只活在一次调用中。CONFIRMED后normal gate为常数判断，不新增正常全城扫描／诊断构造；FAILED无自动删除重试，PENDING只复用既有入口。唯一action receipt、scalar cleanup摘要和临时同步recovery无增长历史，永久成果不清。

B161原生Writing3→5／W2=10、signed映射继续沿用；其它作品、yield、精准recipient、倍率隔离、正常结算与完整Meaning／正式cutover仍各有门禁，不自动扩大。

## 一次最小实机核对

本批新增风险为首次清理与END，不重测已过收益。一个连续session即可：

1. 完全重启后加载已有B161测试存档，不先启用实验；选同一文化城，右键“意义延展·生产力”。预期session OFF、首次清理已确认、remainingOwned=0、无Meaning Writing活动实例。原生Production可包含恢复后的旧GWA，不能要求其总值为0。只读报告本身不清理；若PENDING／FAILED或Meaning残留即停止，提供这一份报告。
2. 第一项通过后，用同一城左键准备基线、再左键启用，然后点击现有“结束验证”入口；右键再读一次。只核对Meaning载体／活动实例归零，以及旧writer按当前事实恢复；不要求改变D／作品、保存启用态、退出重载或再次启用。

步骤1区分后台首次清理与OFF文本伪成功；步骤2验证新VALUE目录实际撤销与本次END修复。无需为harness单独再跑保存／默认OFF循环；用户无需新Gameplay决定。出现native撤销失败→NATIVE_LOAD_WITHDRAWAL_BOUNDARY或准确更细分类，保持失败证据，不自动其它yield／cutover／L3/M/N/U2。
