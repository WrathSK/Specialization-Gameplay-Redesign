# B022：Research Lv1原生专家收益（一个小批次）

Document Owner: Codex
Build: P0-B-022 / modinfo29
Verification: USER_GAME_TEST_REQUIRED
Scope: RES-001的原生收益载体实验；显式ON/OFF，不是自动完整专业系统。

## 准备

可先加载现有B021测试存档，选有RESEARCH/1记录的普通学院城市，点击Read Research support。如显示B022_DATABASE_MISSING，则必须新建测试局；旧档缺数据库不是本机制FAIL，不需要截图反复排查。若已有完整定义、有效记录，可直接沿用。

新局选择Scotland (Specialization Test)，保持HD与Cheat Panel组合。建立城市；如果首都Read city flow显示UNTRACKED，另建一城（不补写旧城）。用Cheat放置并完成该城第一个专业区域——普通学院，再完成图书馆/提供专家岗位的学院建筑；提高人口以便安排1名专家。确认Read city flow显示RESEARCH/1且stopped=false。此次不测试替代学院，也不需总督或Potential升级。

所有对比保持同一城市、同一回合、同一专家分配、建筑和政策；开关之间不要结束回合。面板会显示city与workers，不用手抄ID。面板Configured是预期配置，不能单独用于判定实际收益。

## B022-1：一名专家，开启/关闭与防重复

1. 市民管理手动固定1名学院专家。点击Research support OFF，记下学院专家岗位提示中的食物、生产力及其它产出；截图同时保留分配人数。
2. 点击Research support ON，关闭/重新打开市民界面刷新提示，保持同样1名专家，拍相同岗位提示与面板。再次点击ON确认收益不继续增加。
3. 点击OFF，刷新相同提示，收益应回到第一步。

PASS：每名岗位额外+3食物/+3生产力；其它岗位产出不被本开关改变；重复ON不叠加，OFF完全回到基准。不以城市总产出机械+3判定，因为城市百分比修正可能放大总量；优先比较岗位提示。若原生UI不显示可比较的专家明细，回传现有截图，不以Configured数值宣布通过，也不要求自行计算复杂倍率。

FAIL：实际无收益、加错区域/产出、额外岗位、重复累积、无法撤销，或出现ERROR。

## B022-2：没有工作的专家

把学院专家调成0并固定其它分配。分别OFF与ON，各记录城市食物/生产力明细（保持这次0专家分配不变）。

PASS：开关不改变实际食物/生产力产出；workers=0。不要拿有专家时与无专家时的城市总量比较，公民去其它地块本身会改变产出。此案直接检查是否误成固定建筑收益。

## B022-3：保存读档

恢复1名学院专家并ON，保存、回主菜单、重新加载。不要再点ON，直接Read Research support与查看岗位提示，拍图。然后重复ON一次。

PASS：读档后support=ON，Carrier changes this load=0，实际岗位收益保持；重复ON不额外增加。此案只验证正常保存恢复，不重复B021专业锁定测试。

## 回传

按顺序投递截图到Specialization/ScreenShots，不必改名。优先保留一人OFF/ON、零人OFF/ON、重载ON，共约5张；重复和关闭回到基准可文字确认。若失败，保留错误面板完整文字和发生步骤、岗位提示/城市产出明细；回传当前游戏生成的Lua.log及Database.log（常用位置Logs，若实际日志在嵌套游戏目录请以本次修改时间为准）。不用依赖剪贴板，不清理存档/Property。

不通过时关闭support；若OFF报错则保留测试存档与日志，不继续依靠该收益。所有操作由用户执行，Codex不启动游戏。
