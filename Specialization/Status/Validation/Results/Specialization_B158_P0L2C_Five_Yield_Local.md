# B158.185 — 意义延展七域五产出单城门禁

用户在P0-L2C具体计划后明确“授权实施”。D0043保持不变。本次为默认关闭、单城可逆实验，STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；五产出新增原生范围及本次冷加载仍为USER_GAME_TEST_REQUIRED，完整L2 NOT_PASSED。

## 实际范围与旧效果

- `CultureMeaningModel.lua`只在本能力排除市政／外交，读取Campus／Industry／Commercial／Harbor／Encampment／Holy Site／Neighborhood。Shared普通建筑目录、D、其它consumer不改。K=0.5；**每领域先Floor，再按同yield相加，最后乘合格作品W**。金币份额3，其余1，不先合并同yield原始值。
- 复用S/G编码与已测整数primitive；`CultureMeaningProbe.sql`增加Production4、Food3、Faith3个整数片，共10项。原16项定义／112附件字节保持，含已延期Culture候选。合计26精确owned IDs／182附件，每片限定原7类作品，非Relic/Product/Tourism。单件合法最大S/Food/Faith=5、P=10、G=30；越界失败，不clamp或补差。当前writer不产生Culture或切换旧候选。
- `CultureMeaningProbe.lua`流程改为OFF→BASELINE→ACTIVE→END/OFF，不再要求正Culture或进入100%四态。只hold本城旧GWA精确156项及旧Dialogue0%；确认新owned撤除后，旧模块按当前事实恢复。旧GWA仍维护其它城市；没有正式全城cutover。
- 保留K当前引用／两receiver配对、same-reference UNKNOWN暂留最近确认配置、明确失效及reference退出、module-owned loss、一次有界load清理。load默认OFF，不持久化实验／读数，不写永久Property／E2账本、不改GC。
- `BoostGreatWorkRead.lua`按需显示五yield每件／本城预期、真实native绝对值及有效同回合基线差值。回合／人口／资格／D／位置／主题变化或未知会废弃比较，不伪造0。读数不是结算PASS。当前ACTIVE未知不借旧值显示为当前。
- `P0Panel.lua`同一ACK的Show／写日志复用一份字符串；新请求刷新，reference／回合过期拒绝旧比较；close／load／shutdown释放读数。正常右键不枚举全局Modifier；旧实例诊断helper及反证保留未来使用。复用现有本地化keys，原“切换验证配置”变为“结束验证”，左右键均END；无新按钮／XML／icon。

## 本地验证与证据范围

47项定向检查PASS（7.968s），不是引擎测试或性能／结算认证：

| 检查 | 已验证范围 |
|---|---|
| 新L2C套件27项 | 七域映射；D0/1/3/6/10×W0/1/2；Shared cap前14→10及最高单区；逐域Floor反例；五yield全部合法编码；26项／182附件SQL |
| writer／生命周期 | 零Culture三步流程、重复token零写、同回合建筑／掠夺修复／W／ACTIVE变化、两城隔离、UNKNOWN、引用退出；实际seed全部26项后loss／cold-load精确清理；普通建筑／binding不改 |
| 失败／bridge | 原旧退出失败阻止新写；新创建前／后失败和退出失败保留holds直到精确清理；同步自身事件有界；K实际请求／配对／重复／新回合恢复5项继承回归 |
| reader／UI | 五yield实际差值及故意偏差不自动PASS；nil/NaN/inf／count/definition/theme/slot/ref错误；人口／D／资格／turn比较失效；下回合pair未就绪不是0；OFF／clear／load无旧基线重放；同ACK/Copy不重复native读取或Gameplay写入 |
| 保留诊断20项 | 原Modifier allowlist、未知schema／owner／subject、严格District对象映射、其它城、错误／有界报告及token缓存等直接回归 |

`DevelopmentTests/test_culture_meaning_l2c.py`是本批测试入口，复用原L2/K/L1 fixture。原`test_culture_meaning_probe.py`只更新内存DB精确重建名单26项；**没有改旧断言**。新套件选择8项仍有效旧直接回归；未运行旧四态／Culture候选套件。旧`test_modifier_read.py`保留原件，20项适用断言直接运行；旧Panel路由/Copy两项及modinfo184固定断言不适用于本次已批准变更，分别由新UI测试和实际modinfo185静态检查覆盖，不通过删断言制造全历史PASS。

五个修改Lua经Lua5.5 load语法检查；modinfo185的181个列出文件唯一且存在，实际package182个文件（含modinfo本身）；Text SQL及复用keys检查PASS。外部当前配置HD数据库仅mode=ro读取并复制进内存应用源SQL，实际包含2649建筑、旧Meaning16项；没有改真实DB。原26项测试首次reader turn fixture缺当前Dialogue pair：分开验证pending失败与pair就绪后过期比较，未弱化生产保护。

本轮W0004 L2＋触及load/loss/ref的相关L3，未跑历史full／stress／内存长测。B157的S/G及实例进入／退出原生证据仅沿原范围；新P/F/Faith、全作品精准recipient、主题化／Dialogue独立及正常结算不因模拟通过而升级。

## 一个最小用户流程

使用已启用本Mod的Culture ACTIVE IV存档副本，选一城已有确认、支持的作品（建议非主题Writing）；未支持／有额外Modifier作品时实验会拒绝，不为了测试改Design。

1. **准备输入。** 确保本城五yield预期非0。可用既有Cheat补已登记建筑：学院图书馆＋大学、工业水磨坊＋工作坊、商业集市＋市场、圣地祠堂＋寺庙、社区食品市场，且相关区域／建筑已完成、未掠夺。这些在本机现HD目录分别可形成D3；无需建设全部7域。若城市已有不同深度，以Shared“区域完善度／科研影子”按需组成和本次报告为准，不扩目录。若某yield无非0输入，标未测，不能算通过。
2. **同回合基线与追加。** 选该城，P0面板左键“意义延展验证”一次，等报告明确①基线及“同回合基线已记录”；再左键一次启用②，右键刷新报告。保持其它政策／作品／建筑／资格不变，比较五行“本城预期”和“实测差值”，投递这一份。若只有W1且上述五域D3、Harbor/Encampment无额外D，示意每件／本城为S1/P1/G4/Food1/Faith1，**示意非实测**。延迟可新右键刷新，不能用配置当实测。
3. **同回合变化。** 移走一件作品，等确认馆藏变化，右键一次，核对W和本城预期同步变化；位置／W变化会使旧差值“未确认”，这是正确失效，不是0或自动PASS。报告仍给当前native绝对值。可将作品移回，不需旧四态或长测。
4. **退出与加载。** 实验仍启用时存独立副本，再点击“结束验证”，确认未开启／旧路径按当前事实恢复；必要时用现有“巨作相邻”只读六yield核对正常旧路径，不把结束后旧收益恢复误当新追加残留。完全退出游戏后，冷加载刚才**启用时保存**的副本：右键意义延展应显示未开启；旧收益按当前事实恢复，新实验不自动继续。投递变化、结束／冷加载的少量报告；不逐回合截图。

第一项native差值／退出／引用错误停止对应路径并投递，不自动尝试其它primitive。实际结算、精确recipient及倍率等未覆盖门禁保持；这次不是正式L2验收。

## 当前交付与停止

本地完成B158.185／modinfo185，部署动作与source commit／receipt以[Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)为准；本记录创建时外部仍B157，尚未替换。普通Git提交不等于部署。

当前只等待本单城原生门禁。通过后才提出正式Meaning接入／旧GWA cutover下一计划，不自动实施。市政／外交Culture技术档案、旧候选FAIL及三阶段实例证据保持未来参考；不作为v0.1五yield前置，不改永久状态、Design、main或下一能力。
