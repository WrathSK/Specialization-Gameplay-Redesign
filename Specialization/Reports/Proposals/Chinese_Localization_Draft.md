# 简体中文文案候选稿

基线为 B489.516（develop `932f875fdb39`）。本稿供项目负责人审阅，文本键和源码位置均以基线定位。

本轮核对 10 份文本文件中的 685 个项目自带简体中文键，以及界面路径中找到的 169 处 Lua、XML 和模组元数据直写文字。下文收录 72 条文本键改写和 61 处直写候选。原版百科段落、内部日志和断言属于原有游戏资源或诊断范围。

## 审阅要点

- 16 座机构各用一句话介绍自身定位，接下来按能力写收益和条件。食物、生产力、科技值、住房、伟人点数等使用游戏现有图标。
- 项目和合同先说明完成后会发生什么，并交代计时、消耗、退还和结束条件。机构的详细换算与例外可在后续百科展开，报价和合同风险由各自面板提供。
- 派遣和任务窗口改用考察团的实际状态。任务结束与任务成功各有含义，首次见闻按来源城、目标文明和任务类型计算。

文案段落中的换行对应游戏的 `[NEWLINE]`，图标和动态参数使用原生格式。

## 专业机构

### 科研

#### 学者结社（1级）

`LOC_SPC_RESEARCH_INSTITUTION_1_HELP` · [TestText.sql:387](../../../Mod/Text/TestText.sql#L387)

```text
学者在此结社研习，为城市的科研事业奠定基础。

基础专家支持：
每名在岗科研专家额外提供 +3 [ICON_Food] 食物和 +3 [ICON_Production] 生产力。
```

<details>
<summary>现行文字</summary>

```text
学者在此结成稳定的研究共同体，构成城市科研专业化的基础。

基础专家支持：
[ICON_BULLET] 每名正在工作的科研专家额外提供：+3 [ICON_Food]食物、+3 [ICON_Production]生产力。
```

</details>

#### 研修院（2级）

`LOC_SPC_RESEARCH_INSTITUTION_2_HELP` · [TestText.sql:391](../../../Mod/Text/TestText.sql#L391)

```text
系统的研修与人才培养，让科研成为城市的长期事业。

人才培养：
[ICON_BULLET] 每名在岗科研专家额外提供 +2 基础 [ICON_GreatScientist] 大科学家点数。
[ICON_BULLET] 本城学院及其每一级合格建筑各 +1 [ICON_Housing] 住房。
```

<details>
<summary>现行文字</summary>

```text
系统的研修与人才培养，使科研从个人志业成为城市的长期事业。

人才培养：
[ICON_BULLET] 每名正在工作的科研专家额外提供2点基础[ICON_GreatScientist]大科学家点数，可受伟人点数百分比加成影响。
[ICON_BULLET] 本城学院区域及其每一级合格建筑各提供+1 [ICON_Housing]住房。
```

</details>

#### 学术联合会（3级）

`LOC_SPC_RESEARCH_INSTITUTION_3_HELP` · [TestText.sql:395](../../../Mod/Text/TestText.sql#L395)

```text
不同领域在此交流，让研究成果与城市实践相互促进。

跨学科研究：
[ICON_BULLET] 本城学院以外已建成且未遭掠夺的合格专业区域，其基础相邻产出总和的 50% 转化为 [ICON_Science] 科技值。

学以致用：
[ICON_BULLET] 每名在岗科研专家从本城其他合格专业领域获得额外产出，数量取决于各领域的基础设施深度。
```

<details>
<summary>现行文字</summary>

```text
不同专业领域在此交流，使研究成果与城市实践相互促进。

跨学科研究：
[ICON_BULLET] 将本城除学院外的合格专业区域的基础相邻产出总和，按50%转化为[ICON_Science]科技值；汇总后向下取整。
[ICON_BULLET] 仅计入已建成且未被掠夺的区域；不计政策等相邻加成倍率及非相邻产出。适用区域见专业领域表。

学以致用：
[ICON_BULLET] 每名正在工作的科研专家，从本城每个其它合格专业领域获得对应产出。
[ICON_BULLET] 每1点基础设施深度提供0.5份产出：[ICON_Gold]金币每份3点，其它产出每份1点。
[ICON_BULLET] 同一领域取最高单区域深度；提供同种产出的不同领域分别计算后相加。
[ICON_BULLET] 每名专家的各项收益先向下取整，再按专家人数结算。
```

</details>

#### 学术总署（4级）

`LOC_SPC_RESEARCH_INSTITUTION_4_HELP` · [TestText.sql:399](../../../Mod/Text/TestText.sql#L399)

```text
完备的学院设施让学者得以深入研究，学术传统也随岁月积累。

科研基础设施：
[ICON_BULLET] 本城学院每 1 点基础设施深度，使每名在岗科研专家额外提供 +1 基础 [ICON_Science] 科技值，最高 +10。

学术主持：
[ICON_BULLET] 每名在岗科研专家使本城每座完好的普通学院一至四级建筑 +1 基础 [ICON_Science] 科技值。

学术传统：
[ICON_BULLET] 科研潜力达到四级后开始积累。四级启用时，本城初始 +5% [ICON_Science] 科技值。
[ICON_BULLET] 保有科研身份时持续积累，即使暂未启用四级。转出科研后暂停，转回后继续积累。标准速度下，每累计 10 回合再提高 5 个百分点，最高 +25%。
```

<details>
<summary>现行文字</summary>

```text
完善的科研设施、学术组织与长期传统，共同支撑深入研究。

科研基础设施：
[ICON_BULLET] 本城学院每1点基础设施深度，使每名正在工作的科研专家额外提供+1基础[ICON_Science]科技值。
[ICON_BULLET] 深度上限10点；达到上限时，5名专家共提供+50基础[ICON_Science]科技值。

学术主持：
[ICON_BULLET] 每名正在工作的科研专家，使本城每座未遭掠夺的普通学院一至四级建筑额外提供+1基础[ICON_Science]科技值。
[ICON_BULLET] 被掠夺的建筑不计入且不享受收益；额外科技值不提高基础设施深度。

学术传统：
[ICON_BULLET] 首次达到科研潜力四级后开始积累。启用四级时，初始提供+5%[ICON_Science]科技值。
[ICON_BULLET] 标准速度下，累计10、20、30、40回合，依次提高至10%、15%、20%、25%，上限25%。其它速度按比例缩放阶段回合数并向下取整。
[ICON_BULLET] 保有科研身份时持续积累；暂未启用四级不影响积累。转出科研后暂停并保留进度，转回后继续，不补算离开期间的回合。
```

</details>

### 文化

#### 文艺同好会（1级）

`LOC_SPC_CULTURE_INSTITUTION_1_HELP` · [TestText.sql:229](../../../Mod/Text/TestText.sql#L229)

```text
创作者与爱好者聚在一起，让城市的文化生活扎根成长。

基础专家支持：
[ICON_BULLET] 每名在岗文化专家额外提供 +3 [ICON_Food] 食物和 +3 [ICON_Production] 生产力。
```

<details>
<summary>现行文字</summary>

```text
创作者与爱好者因共同的艺文兴趣形成稳定社群，构成城市文化专业化的基础。

基础专家支持：
[ICON_BULLET] 每名正在工作的文化专家额外提供：+3 [ICON_Food]食物、+3 [ICON_Production]生产力。
[ICON_BULLET] 与原生专家收益叠加；更高等级继续沿用此基础支持。
```

</details>

#### 赞助人行会（2级）

`LOC_SPC_CULTURE_INSTITUTION_2_HELP` · [TestText.sql:231](../../../Mod/Text/TestText.sql#L231)

```text
稳定的资助与委托，让文学、艺术与音乐在城中长久兴盛。

文艺赞助：
[ICON_BULLET] 本城剧院广场 +1 [ICON_Housing] 住房。每个已有合格普通建筑的等级再 +1，同级只计一次。
[ICON_BULLET] 每名在岗文化专家额外提供 +2 [ICON_GreatWriter] 大作家、+2 [ICON_GreatArtist] 大艺术家、+2 [ICON_GreatMusician] 大音乐家基础点数。
```

<details>
<summary>现行文字</summary>

```text
稳定的资助、委托与社会支持，使文学、艺术与音乐创作成为持续的城市事业。

文艺赞助：
[ICON_BULLET] 本城剧院广场提供+1 [ICON_Housing]住房；每有一个包含合格普通建筑的建筑等级，再提供+1 [ICON_Housing]住房，同级不重复。
[ICON_BULLET] 每名正在工作的文化专家额外提供：2点基础[ICON_GreatWriter]大作家点数、2点基础[ICON_GreatArtist]大艺术家点数、2点基础[ICON_GreatMusician]大音乐家点数。
[ICON_BULLET] 上述点数可受伟人点数百分比加成影响。
```

</details>

#### 人文联合会（3级）

`LOC_SPC_CULTURE_INSTITUTION_3_HELP` · [TestText.sql:233](../../../Mod/Text/TestText.sql#L233)

```text
不同时代的巨作在此汇聚，旧作有了新的诠释，艺术也渐渐融入城市生活。

时代对话：
[ICON_BULLET] 项目需 1 个完整生产回合。每城每个游戏时代限完成一次，按开工时的时代计。
[ICON_BULLET] 完成时，合格馆藏每涵盖一个作品时代，巨作本身的 [ICON_Tourism] 旅游业绩倍率永久累积 5 个百分点。文化启用等级达到三级时生效。

风雅熏陶：
[ICON_BULLET] 本城合格馆藏每涵盖一个作品时代，每座完好的合格普通建筑 +1 [ICON_Tourism] 旅游业绩。
```

<details>
<summary>现行文字</summary>

```text
作品不再只属于创作当下；历史不断赋予新的理解，艺术也逐渐塑造整座城市的审美。

时代对话：
[ICON_BULLET] 开展同名城市项目，占用1个完整生产回合；按启动时的游戏时代计算，每城每时代最多成功一次。
[ICON_BULLET] 完成时，合格馆藏每覆盖一个不同的作品时代，永久累加5个百分点的巨作原生[ICON_Tourism]旅游业绩倍率。
[ICON_BULLET] 不放大“意义延展”的追加产出。项目中断不消耗本时代成功次数。
[ICON_BULLET] 文化启用等级低于三级或转出文化身份时暂停加成，保留累计记录。

风雅熏陶：
[ICON_BULLET] 本城合格巨作每覆盖一个不同的作品时代，每座未遭掠夺的合格普通建筑额外提供+1 [ICON_Tourism]旅游业绩。
[ICON_BULLET] 按本城当前馆藏的时代覆盖数动态计算。
```

</details>

#### 博雅总院（4级）

`LOC_SPC_CULTURE_INSTITUTION_4_HELP` · [TestText.sql:235](../../../Mod/Text/TestText.sql#L235)

```text
学者借各领域的见解重读巨作，也把目光投向异国的风土与艺术。

意义延展：
[ICON_BULLET] 每件合格巨作从本城符合条件的专业领域获得额外产出。基础设施深度决定收益。可受主题化加成影响，不受「时代对话」放大。目前不计市政广场与外交区的文化追加。

巨作启迪：
[ICON_BULLET] 本城合格馆藏每涵盖一个作品时代，已有基础产出的 [ICON_GreatPerson] 伟人点数 +3%，最高 +24%。

人文考察团：
[ICON_BULLET] 可训练人文考察团，全国同时最多 1 支。派往已遇见的外国主要文明。每个来源城市对每个目标文明的每类任务首次成功时，取得 1 份文化见闻。
[ICON_BULLET] 有效见闻提高来源城市的 [ICON_Tourism] 旅游业绩，同一来源城市集齐同一文明的三类见闻后，可通过商路为合格的在岗专家提供 [ICON_Culture] 文化值。
```

<details>
<summary>现行文字</summary>

```text
成熟的人文体系从社会各领域理解文化，让巨作启发未来人才，并主动走向其它文明拓展自身视野。

意义延展：
[ICON_BULLET] 每件合格巨作，从本城各合格专业领域获得代表产出：每1点基础设施深度提供0.5份产出。
[ICON_BULLET] [ICON_Gold]金币每份3点，其它产出每份1点；同一领域取最高单区域深度。
[ICON_BULLET] 各领域收益分别向下取整后相加，再按合格巨作件数结算。
[ICON_BULLET] 可受原生主题化加成影响，不受“时代对话”放大。当前不计入市政广场与外交区的[ICON_Culture]文化追加。

巨作启迪：
[ICON_BULLET] 本城合格巨作每覆盖一个不同的作品时代，所有已有基础产出的伟人点数提高3%；最多8个时代，最高+24%。
[ICON_BULLET] 没有基础点数的伟人类别不会因此获得点数。

人文考察团：
[ICON_BULLET] 可训练人文考察团，全国同时最多拥有1支；采用间谍生产成本公式，训练次数独立累计。
[ICON_BULLET] 派遣至已遇见的外国主要文明，执行风土考察、艺文采撷、奇观巡礼；标准速度下均为2回合。
[ICON_BULLET] 每个来源城市对每个目标文明的每类任务，首次成功获得1份文化见闻并归档保留。
[ICON_BULLET] 当前有效见闻提供本城[ICON_Tourism]旅游业绩与文化网络加成。
```

</details>

### 工业

#### 匠作坊（1级）

`LOC_SPC_INDUSTRY_INSTITUTION_1_HELP` · [TestText.sql:248](../../../Mod/Text/TestText.sql#L248)

```text
工匠与劳动者在此聚集，将生产条件化为熟练的技艺。

基础专家支持：
[ICON_BULLET] 每名在岗工业专家额外提供 +3 [ICON_Food] 食物，并获得等同于本城工业区基础相邻加成的 [ICON_Production] 生产力，不计政策等倍率。
```

<details>
<summary>现行文字</summary>

```text
工匠与生产人口在此聚集，将区域的生产条件转化为熟练劳动。

基础专家支持：
[ICON_BULLET] 每名正在工作的工业专家额外提供+3 [ICON_Food]食物。
[ICON_BULLET] 额外[ICON_Production]生产力等于本城工业区基础相邻生产力加成，按1:1转化，不计政策等相邻加成倍率。
[ICON_BULLET] 与原生专家收益叠加；各专业等级均沿用此公式。
```

</details>

#### 百工会馆（2级）

`LOC_SPC_INDUSTRY_INSTITUTION_2_HELP` · [TestText.sql:252](../../../Mod/Text/TestText.sql#L252)

```text
不同工种分工合作，共同培养城市的工程人才。

专业分工：
[ICON_BULLET] 本城工业区 +1 [ICON_Housing] 住房。每个已有合格普通建筑的等级再 +1，同级只计一次。
[ICON_BULLET] 每名在岗工业专家额外提供 +2 基础 [ICON_GreatEngineer] 大工程师点数。
```

<details>
<summary>现行文字</summary>

```text
不同工种与技术职业形成稳定分工，共同培养城市的工程人才。

专业分工：
[ICON_BULLET] 本城工业区提供+1 [ICON_Housing]住房；每有一个包含合格普通建筑的建筑等级，再提供+1 [ICON_Housing]住房，同级不重复。
[ICON_BULLET] 每名正在工作的工业专家额外提供2点基础[ICON_GreatEngineer]大工程师点数，可受伟人点数百分比加成影响。
```

</details>

#### 工程局（3级）

`LOC_SPC_INDUSTRY_INSTITUTION_3_HELP` · [TestText.sql:256](../../../Mod/Text/TestText.sql#L256)

```text
工程师将建造经验编成规范，并组织施工队支援新的建设。

标准化：
[ICON_BULLET] 建造符合模板的区域和建筑时，+10% [ICON_Production] 生产力。模板可沿商路共享，同一目标只取最高加成。

施工队：
[ICON_BULLET] 解锁一级至三级施工队组建项目，工业启用三级时，组建成本为基础施工力的 150%。每个来源城市同时最多支持 2 支。
[ICON_BULLET] 消耗施工队，为当前在建奇观投入 [ICON_Production] 生产力。超出所需的部分不结转。
```

<details>
<summary>现行文字</summary>

```text
工程规范、资源统筹与施工组织，使生产经验能够重复，施工力量能够部署。

标准化：
[ICON_BULLET] 已完成的建设经验记录为可靠模板；建造符合模板的区域与建筑时，获得+10%[ICON_Production]生产力。
[ICON_BULLET] 三级不提供[ICON_Gold]金币购买折扣。贸易路线相连的城市按专业网络规则共享模板。
[ICON_BULLET] 同一目标有多个可用来源时，仅取最高加成，不叠加。

施工队：
[ICON_BULLET] 解锁一级至三级施工队组建项目，组建成本为基础施工力的150%。
[ICON_BULLET] 对于当前所有者，每个来源城市最多同时支持2支现存施工队。
[ICON_BULLET] 仅能向正在建造的奇观一次性投入基础[ICON_Production]施工力，可受适用生产力加成影响；超出剩余所需的部分不溢出结转。
```

</details>

#### 土木工程总局（4级）

`LOC_SPC_INDUSTRY_INSTITUTION_4_HELP` · [TestText.sql:260](../../../Mod/Text/TestText.sql#L260)

```text
工程师研习历代奇观的建造经验，把过去的巧思用到今天的大工程上。

工程传统：
[ICON_BULLET] 按本文明亲建奇观的所属时代计算。每涵盖一个时代，本城可研习一次。每次占用 1 个完整生产回合，完成后积累 1 层。
[ICON_BULLET] 四级启用时，每层成果使「标准化」的 [ICON_Production] 建造加成和合格建筑的购买折扣各提高 2 个百分点。

工程实践：
[ICON_BULLET] 解锁四级、五级施工队组建项目。本城累计建成 1、3、6 座奇观后，组建成本依次降至基础施工力的 140%、130%、120%。

巨构工程学：
[ICON_BULLET] 建造比本文明当前时代早 1、2 或至少 3 个时代的奇观时，分别获得 +10%、+20% 或 +30% [ICON_Production] 生产力。施工队的投入也享受此加成。
```

<details>
<summary>现行文字</summary>

```text
成熟的工程体系组织大型建设，并将实践经验与历史积累转化为更深厚的工程能力。

工程传统：
[ICON_BULLET] 本文明亲自建成的奇观，每覆盖一个不同的奇观时代，提供一份可供本城研习的经验。
[ICON_BULLET] 每次“工程传统研习”占用1个完整生产回合，永久积累1层成果。
[ICON_BULLET] 四级启用时，每层使“标准化”的[ICON_Production]建造加成与合格建筑的[ICON_Gold]购买折扣各提高2个百分点。
[ICON_BULLET] 已完成成果按城市历史保留，恢复四级启用后重新生效；购买折扣不包含区域本体。

工程实践：
[ICON_BULLET] 解锁四级、五级施工队组建项目。
[ICON_BULLET] 本城累计建成1、3、6座奇观时，组建成本由基础施工力的150%，依次降至140%、130%、120%。
[ICON_BULLET] 每支施工队的组建成本在开工时锁定。

巨构工程学：
[ICON_BULLET] 建造早于本文明当前时代的奇观时，按时代差获得[ICON_Production]建造生产力加成：
[ICON_BULLET] 落后1个时代：+10%；落后2个时代：+20%；落后3个及以上时代：+30%。
[ICON_BULLET] 符合条件时，此加成同样作用于施工队投入的基础施工力。
```

</details>

### 商业

#### 商贾聚落（1级）

`LOC_SPC_COMMERCE_INSTITUTION_1_HELP` · [Restructuring.sql:23](../../../Mod/Text/Restructuring.sql#L23)

```text
商人与经营活动逐渐汇聚，形成城市最初的商业共同体。

基础专家支持：
[ICON_BULLET] 每名在岗商业专家额外提供 +3 [ICON_Food] 食物和 +3 [ICON_Production] 生产力。
```

<details>
<summary>现行文字</summary>

```text
零散商人与经营活动在此稳定聚集，形成自发的商业共同体。

基础专家支持：
[ICON_BULLET] 每名正在工作的商业专家额外提供：+3 [ICON_Food]食物、+3 [ICON_Production]生产力。
```

</details>

#### 同业公会（2级）

`LOC_SPC_COMMERCE_INSTITUTION_2_HELP` · [Restructuring.sql:25](../../../Mod/Text/Restructuring.sql#L25)

```text
同业者建立稳定的组织，培养城市的商业人才。

同业制度：
[ICON_BULLET] 每名在岗商业专家额外提供 +2 基础 [ICON_GreatMerchant] 大商人点数。
[ICON_BULLET] 本城商业中心及其每一级合格建筑各 +1 [ICON_Housing] 住房。
```

<details>
<summary>现行文字</summary>

```text
同业制度形成稳定职业共同体与商业人才体系。

同业制度：
[ICON_BULLET] 每名正在工作的商业专家额外提供2点基础[ICON_GreatMerchant]大商人点数，可受伟人点数百分比加成影响。
[ICON_BULLET] 本城商业中心区域及其每一级合格建筑各提供+1 [ICON_Housing]住房。
```

</details>

#### 交易所（3级）

`LOC_SPC_COMMERCE_INSTITUTION_3_HELP` · [Restructuring.sql:27](../../../Mod/Text/Restructuring.sql#L27)

```text
商人发现各领域的价值，也在投资中权衡时间与风险。

商业化：
[ICON_BULLET] 每名在岗商业专家可经营一个本城拥有对应区域的领域。取本城或直接国内商路相连的己方对应专业城市的最高产出，转化为额外 [ICON_Gold] 金币，不扣除来源产出。
[ICON_BULLET] 本城无需对应专业身份。相连城市须有对应身份，但无需启用。港口领域按总 [ICON_Food] 食物产出计算。

资本投资：
[ICON_BULLET] 可投资科研、文化或工业。本金为签约时国库的 25%，标准速度下 10 回合到期，每城每领域限一份未结合同。
[ICON_BULLET] 稳健投资返还本金与利润。风险投资成功时利润为稳健的 3 倍，失败返还 50% 本金，商业信誉可提高返还比例。
```

<details>
<summary>现行文字</summary>

```text
商业组织发现不同领域的价值，并经营资本的时间与风险。

商业化：
[ICON_BULLET] 每名在岗商业专家允许同时商业化1个不同领域；本城须有对应区域。
[ICON_BULLET] 取本城及直接国内商路相连、持有对应专业身份的己方城市中，最高的对应城市总产出；来源专业无需当前启用。
[ICON_BULLET] 学院、剧院广场、工业区、圣地、港口分别读取[ICON_Science]科技、[ICON_Culture]文化、[ICON_Production]生产力、[ICON_Faith]信仰、[ICON_Food]总粮食。
[ICON_BULLET] 每领域[ICON_Gold]金币＝0.05×本城对应基础设施深度×最高来源产出×商业信誉倍率。
[ICON_BULLET] 各领域分别向下取整后相加；转化为本城额外金币，不扣除来源产出。

资本投资：
[ICON_BULLET] 可投资科研、文化或工业。本金为签约时国库[ICON_Gold]余额的25%；标准速度下10回合到期，每城每领域限1份未结合同。
[ICON_BULLET] 稳健投资返还本金与核定利润；风险投资成功时利润为稳健的3倍，失败返还50%本金，可由商业信誉提高。
[ICON_BULLET] 利润取决于本城对应基础设施、专业网络内对应专业启用等级及该领域商业化；具体报价见“资本投资”，签约后锁定。
```

</details>

#### 资本信托（4级）

`LOC_SPC_COMMERCE_INSTITUTION_4_HELP` · [Restructuring.sql:29](../../../Mod/Text/Restructuring.sql#L29)

```text
资金沿商路投向新的建设，旧产业有了新的出路，信誉也在经营中逐渐积累。

发展投资：
[ICON_BULLET] 向本城发出的直接国内商路所连接的城市投资 [ICON_Gold] 金币。目标区域建造合格建筑时，+50% [ICON_Production] 生产力。下一座合格建筑完成后，合同结束。

资产重组：
[ICON_BULLET] 重组团队可在潜力至少二级的己方专业城市清算资产，永久扣除 1 级潜力。重组期间，非食物产出和用于人口增长的 [ICON_Food] 余粮减少 75%。
[ICON_BULLET] 计满 5 个完整回合后，须在同城另一合格专业区域手动配置资产，消耗团队并转换专业。

商业信誉：
[ICON_BULLET] 建立四级机构后，保有商业身份时每完整回合积累 1 点信誉，上限 40（标准速度）。转出商业后信誉清零。
[ICON_BULLET] 四级启用时，每点信誉使商业化收益 +0.5%，风险投资失败的本金返还比例提高 0.5 个百分点。最高分别为 +20% 和返还 70%。
```

<details>
<summary>现行文字</summary>

```text
成熟商业组织配置发展资本、重组既有资产，以长期稳定经营积累信誉。

发展投资：
[ICON_BULLET] 沿本城出发的直接国内贸易路线，投资目标城市的合格区域。
[ICON_BULLET] 支付其可建下一阶建筑中最低理论[ICON_Gold]金币购买价的15%，使该区域建筑获得+50%[ICON_Production]建造生产力，与标准化加算。
[ICON_BULLET] 该区域下一座合格建筑完成后结束，不绑定报价建筑。
[ICON_BULLET] 每名在岗商业专家提供1个签约名额；每座目标城市同时限1份合同。已签合同不因商路、专家或启用等级变化而取消。

资产重组：
[ICON_BULLET] 标准速度下，以500 [ICON_Production]生产力训练重组团队。
[ICON_BULLET] 在潜力至少二级的己方专业城市清算资产，永久扣除1级潜力；重组期间非食物产出及盈余[ICON_Food]食物增长降低75%。
[ICON_BULLET] 至少5个完整回合后，在同城另一个合格专业区域配置资产，消耗团队并转换专业；不会自动结束重组。

商业信誉：
[ICON_BULLET] 首次建立四级机构后，保有商业身份时每完整回合累计1点，上限40，以上为标准速度。
[ICON_BULLET] 四级启用时，每点使商业化收益提高0.5%，风险投资失败的本金返还比例提高0.5个百分点；最高分别为+20%与返还70%。
[ICON_BULLET] 暂时失去启用等级保留信誉；退出商业身份清零。
```

</details>

## 面板、项目与单位文案

### 机构、施工队与城市详情

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_SPC_CREW_BASE_CONFIRM](../../../Mod/Text/TestText.sql#L303) | 消耗此施工队，为当前正在建造的奇观投入 {1_Input} 点基础生产力（实际转化量可享受适用生产力加成）。<br>此操作一旦确认无法撤销。 | 消耗此施工队，为当前在建奇观投入 {1_Input} 点基础 [ICON_Production] 生产力。适用的建造加成可提高实际投入。<br>确认后无法撤销。 |
| [LOC_SPC_INST_ENGINEERING_VALUE](../../../Mod/Text/TestText.sql#L350) | 已完成研习：{1} 层。<br>四级启用时：[ICON_Production]标准化建造加成与合格建筑[ICON_Gold]金币折扣各增强 {2} 个百分点。 | 已完成研习：{1} 层。<br>四级启用时：[ICON_Production] 标准化建造加成与合格建筑购买折扣各提高 {2} 个百分点。 |
| [LOC_SPC_INST_STANDARDIZATION_VALUE](../../../Mod/Text/TestText.sql#L354) | 本城当前提供：[ICON_Production]生产力 +{1}%，合格建筑[ICON_Gold]金币购买折扣 {2}%。<br>不含区域购买折扣。 | 本城当前提供：[ICON_Production] 生产力 +{1}%，合格建筑购买折扣 {2}%。<br>不含区域购买折扣。 |

### 商业机构与资产重组

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_SPC_REST_PREVIEW](../../../Mod/Text/Restructuring.sql#L8) | 目标城市：{1_City}<br>清算后保留潜力：{2_Potential} 级<br>执行「资产清算」将永久扣除该城 1 级专业潜力；资产重组期间，该城所有非食物产出及盈余食物增长均降低 75%。持续至少 5 个完整回合后，须将该团队移动至同城内另一个合格的专业区域，手动执行「资产配置」以完成重组。 | 目标城市：{1_City}<br>清算后保留潜力：{2_Potential} 级<br><br>清算永久扣除该城 1 级专业潜力。重组期间，非食物产出和用于增长的盈余食物降低 75%。<br>至少 5 个完整回合后，须在同城另一个合格专业区域手动执行「资产配置」，消耗团队并完成重组。 |
| [LOC_SPC_REST_TEAM_HELP](../../../Mod/Text/Restructuring.sql#L3) | 本城商业启用等级达到 4 级时可训练（仅能使用生产力组建）。可前往专业潜力至少为 2 级的己方城市，在其当前专业对应的区域执行「资产清算」（永久扣除该城 1 级专业潜力）；经过至少 5 个完整回合后，须在同一城市内另一个合格的专业区域执行「资产配置」并消耗本团队，完成专业转换（原专业的历史记录按各自规则保留）。此单位遭遇敌军时将自动撤退，不会被敌方俘获。 | 本城商业启用等级达到四级时可训练，只能使用生产力。<br><br>在专业潜力至少二级的己方城市当前专业区域执行「资产清算」，永久扣除该城 1 级潜力。至少 5 个完整回合后，在同城另一合格专业区域执行「资产配置」，消耗团队并转换专业。原专业历史按各自规则保留。<br>遭遇敌军时自动撤退，不会被俘获。 |
| [LOC_SPC_REST_WAIT](../../../Mod/Text/Restructuring.sql#L9) | 绑定城市：{1_City}<br>当前保留潜力：{2_Potential} 级<br>距离可执行「资产配置」还需等待 {3_Turns} 个完整回合（回合数届满后不会自动结束重组，须手动完成配置）。 | 绑定城市：{1_City}<br>当前保留潜力：{2_Potential} 级<br>还需等待 {3_Turns} 个完整回合才能配置资产。届时须手动配置，重组不会自动结束。 |

### 商业化与资本投资

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_SPC_CAPITAL_BELOW_SAFE](../../../Mod/Text/Commerce.sql#L102) | 提示：本次风险投资的预期净收益低于稳健投资。 | 本次风险投资的预期净收益低于稳健投资。 |
| [LOC_SPC_CAPITAL_CONTRACT](../../../Mod/Text/Commerce.sql#L104) | 生效合同：{1}<br>投入本金：{2}<br>第 {3} 回合到期 | 合同状态：{1}<br>投入本金：{2}<br>第 {3} 回合到期 |
| [LOC_SPC_CAPITAL_HELP](../../../Mod/Text/Commerce.sql#L111) | 每座商业城市的每个经营领域最多可同时存在 1 笔未结算合同；每次签约后将按剩余国库重新计算后续报价。<br>合同确认后，各项参数与风险判定结果即行锁定；若本商业城市或锁定的实力(S)来源城市在合同期内易主，合同将立即终止且不退还本金。 | 每座商业城市每个领域同时最多有 1 份未结合同。每次签约后，后续报价按剩余国库重新计算。<br>确认后锁定合同参数与风险结果。商业城市或锁定的实力来源城市在合同期内易主时，合同立即终止，本金不予返还。 |
| [LOC_SPC_CAPITAL_NEGATIVE_EV](../../../Mod/Text/Commerce.sql#L101) | 注意：本次风险投资的预期净收益为负（预期亏损），你仍可自行决定是否投入。 | 本次风险投资的预期净收益为负。仍可确认投资。 |
| [LOC_SPC_CAPITAL_OPEN_HELP](../../../Mod/Text/Commerce.sql#L87) | 打开资本投资面板，进行稳健投资或风险投资（此操作不占用城市生产队列）。 | 打开资本投资面板，选择稳健投资或风险投资。不占用城市生产队列。 |
| [LOC_SPC_CAPITAL_TERMINATED](../../../Mod/Text/Commerce.sql#L107) | 合同涉及的关键城市已易主，合同强制终止，所投本金不予返还。 | 合同已终止。若已扣款，本金不予返还。 |
| [LOC_SPC_COMMERCE_FORMULA](../../../Mod/Text/Commerce.sql#L8) | 单领域收益：向下取整 [ 0.05 × 本城基础设施深度(D) × 最高合格来源城总产出(X) × (1 + 0.005 × 有效信誉R) ]，各生效领域分别取整后相加。合格来源为本城或与本城有直接贸易路线相连的对应专业城市（港口领域取城市总食物产出，而非盈余食物）。最终金币收益受游戏原生结算加成影响。 | 每个领域的基础 [ICON_Gold] 金币为：0.05 × 本城基础设施深度 × 最高合格来源城市总产出 × (1 + 0.005 × 有效信誉 R)，分别向下取整后相加。<br>来源可为本城，或以直接国内商路相连、拥有对应专业身份的己方城市。港口按总食物产出计算。最终收益受游戏原生金币倍率影响。 |
| [LOC_SPC_COMMERCE_INACTIVE](../../../Mod/Text/Commerce.sql#L27) | 当前 ACTIVE 不足三级 | 商业启用等级未达到三级 |
| [LOC_SPC_COMMERCE_LIFO_HELP](../../../Mod/Text/Commerce.sql#L24) | 当商业专家名额减少时，较晚开启的经营领域将优先暂停；名额恢复后按原顺序重新生效。只有手动关闭才会移除已选配置；若本城脱离商业专业身份或城市易主，将清空所有已选配置。 | 商业专家名额减少时，较晚开启的领域优先暂停。名额恢复后按原顺序生效。手动关闭才会移除配置。本城脱离商业专业或易主时，所有已选配置清空。 |
| [LOC_SPC_COMMERCE_OPEN_HELP](../../../Mod/Text/Commerce.sql#L5) | 打开商业化面板，选择本城已拥有对应区域的经营领域（此操作不消耗生产回合，也不会改变城市生产队列）。每名正在工作的商业专家可提供 1 个经营领域名额。 | 打开商业化面板，选择本城拥有对应区域的经营领域。每名在岗商业专家提供 1 个名额。不占用生产队列。 |
| [LOC_SPC_COMMERCE_WAITING](../../../Mod/Text/Commerce.sql#L22) | 等待当前事实 | 等待收益确认 |

### 发展投资

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_SPC_DEVELOPMENT_HELP](../../../Mod/Text/DevelopmentInvestment.sql#L13) | 发起签约需满足：本城商业启用等级达到 4 级、拥有从本城出发前往目标城市的直接国内贸易路线，且本城有空余的在岗商业专家名额。<br><br>签约生效后，贸易路线变动或本城启用等级下降均不会取消合同；但若签约双方任一城市易主，合同将立即终止且不退还已投金币。 | 签约需要本城商业启用等级达到四级、从本城出发通往目标城市的直接国内商路，以及空余的在岗商业专家名额。<br><br>商路变化、专家减少或启用等级下降不会取消已签合同。签约双方任一城市易主时，合同立即终止且不退还金币。 |
| [LOC_SPC_DEVELOPMENT_NO_OUTGOING](../../../Mod/Text/DevelopmentInvestment.sql#L18) | 当前没有从本城出发的直接国内贸易路线目标城市 | 本城暂无直达其他己方城市的国内商路。 |
| [LOC_SPC_DEVELOPMENT_OPEN_HELP](../../../Mod/Text/DevelopmentInvestment.sql#L3) | 打开发展投资面板：依托从本城出发的国内贸易路线，为目标城市的指定区域建筑提供 +50% 建造生产力加成。 | 打开发展投资面板，沿本城发出的直接国内商路投资目标区域，使其合格建筑 +50% [ICON_Production] 建造生产力。 |
| [LOC_SPC_DEVELOPMENT_STALE](../../../Mod/Text/DevelopmentInvestment.sql#L21) | 签约条件或建筑报价已发生变动，请刷新面板后重新核对 | 签约条件或建筑报价已变化，请刷新面板后重新核对。 |
| [LOC_SPC_DEVELOPMENT_TERMS](../../../Mod/Text/DevelopmentInvestment.sql#L11) | 合同效果：目标区域的合格建筑获得 +50% 建造生产力加成（与工业「标准化」加成相加计算）。<br><br>结束条件：该区域完成下一座合格建筑后合同即告结束（不强制绑定报价时的基准建筑）。<br><br>补充说明：中途改建其它目标不会取消合同；若通过金币购买或其它方式直接完成该区域建筑，合同同样随之结束。 | 目标区域的合格建筑获得 +50% [ICON_Production] 建造生产力，与「标准化」加成相加。<br><br>该区域下一座合格建筑完成时合同结束，包括金币购买或其他方式直接完成。所建建筑可以与报价时不同。<br>切换建造目标不会取消合同。 |

### 人文考察团

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_SPC_EXPEDITION_GATE_NO_TARGET](../../../Mod/Text/ExpeditionGate.sql#L13) | 暂无可读目标（已遇见且已揭示的外国首都） | 当前没有可用的目的地。 |
| [LOC_SPC_EXPEDITION_SPY_ACTION_UNAVAILABLE](../../../Mod/Text/ExpeditionGate.sql#L441) | 当前不可用。抵达后可开始一次验证任务；完成后请从 P0「人文考察·验证」结束验证团。 | 当前无法执行此操作，请确认考察团状态与所选目标。 |
| [LOC_SPC_EXPEDITION_SPY_ACTIVITY_BLOCKED](../../../Mod/Text/ExpeditionGate.sql#L350) | 任务活动异常，已暂停；请保留报告，可结束并移除验证团。 | 任务状态异常，操作已暂停。请保留报告。 |
| [LOC_SPC_EXPEDITION_SPY_ACTIVITY_START_DECLINED](../../../Mod/Text/ExpeditionGate.sql#L710) | 任务未开始：引擎当前不允许休眠，未发出休眠指令，也未计时或发放见闻。本次启动锁定已解除；拒绝信息已记录，请保留日志，不必反复尝试。 | 任务未开始：游戏当前不允许进入任务状态，未开始计时或发放见闻。请保留日志，不必反复尝试。 |
| [LOC_SPC_EXPEDITION_SPY_ACTIVITY_START_EXPIRED](../../../Mod/Text/ExpeditionGate.sql#L709) | 任务未能确认启动，已撤销此次准备；未消耗名额或发放文化见闻。可以重新选择任务。 | 任务启动未获确认，本次准备已取消。未消耗任务次数或发放文化见闻。可重新选择任务。 |
| [LOC_SPC_EXPEDITION_SPY_ACTIVITY_WAIT](../../../Mod/Text/ExpeditionGate.sql#L354) | 任务进行中或正在释放活动占用；目前只能查看管理报告或结束验证团。 | 任务进行中或正在结束，请等待当前活动完成。 |
| [LOC_SPC_EXPEDITION_SPY_BOUND_REQUIRED](../../../Mod/Text/ExpeditionGate.sql#L215) | 请先创建本次绑定验证团；暂停/未绑定团只能读取或结束。 | 考察团尚未确认绑定来源城市或已暂停，当前无法派遣。 |
| [LOC_SPC_EXPEDITION_SPY_DESCRIPTION](../../../Mod/Text/ExpeditionGate.sql#L167) | 绑定来源城市且拥有独立名额的特殊文化单位（当前暂占用 1 个原生间谍名额）。可派遣至已遇见的外国主要文明执行专属计时考察任务，首次完成可为来源城市赢得「文化见闻」；不可执行原生间谍任务。 | 人文考察团绑定来源城市，可前往已遇见的外国主要文明执行考察，为来源城市取得文化见闻。不能执行普通间谍任务。当前占用 1 个原生间谍名额。 |
| [LOC_SPC_EXPEDITION_SPY_MISSION_FACTS_UNKNOWN](../../../Mod/Text/ExpeditionGate.sql#L643) | 任务目标事实暂时无法确认；本次检查未判定失效，也未发放见闻。 | 目标条件暂时无法确认。本次检查未判定失效，也未发放文化见闻。 |
| [LOC_SPC_EXPEDITION_SPY_MISSION_PEOPLE_TOOLTIP](../../../Mod/Text/ExpeditionGate.sql#L624) | 深入考察该文明的社会生活、风俗习惯、典章制度与城市文化。首次成功完成可获得 1 份文化见闻。<br>目标条件：该文明实际控制的现任首都（每个来源城市对该文明仅能成功完成一次此类考察）。 | 考察该文明的社会生活与风俗。首次成功为来源城市取得 1 份文化见闻。<br>目标须为该文明实际控制的现任首都。每个来源城市对该文明仅可成功一次。 |
| [LOC_SPC_EXPEDITION_SPY_MISSION_PLACES_TOOLTIP](../../../Mod/Text/ExpeditionGate.sql#L628) | 巡礼该文明的宏伟建筑与物质遗产，体悟其中的审美意趣、工程技艺与文明象征。首次成功完成可获得 1 份文化见闻。<br>目标条件：该文明旗下拥有至少 1 座已建成奇观的城市（每个来源城市对该文明仅能成功完成一次此类考察）。 | 巡礼该文明的奇观与物质遗产。首次成功为来源城市取得 1 份文化见闻。<br>目标须为该文明拥有的城市，且至少有 1 座已建成奇观。每个来源城市对该文明仅可成功一次。 |
| [LOC_SPC_EXPEDITION_SPY_MISSION_WORKS_TOOLTIP](../../../Mod/Text/ExpeditionGate.sql#L626) | 接触并品鉴该文明的艺文硕果，从中汲取文化经验。首次成功完成可获得 1 份文化见闻（不会移动、复制、窃取或消耗对方的巨作）。<br>目标条件：该文明旗下拥有至少 1 件合格巨作的城市（每个来源城市对该文明仅能成功完成一次此类考察）。 | 品鉴该文明的艺文成果。首次成功为来源城市取得 1 份文化见闻，不移动、复制、窃取或消耗对方巨作。<br>目标须为该文明拥有的城市，且至少有 1 件合格巨作。每个来源城市对该文明仅可成功一次。 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_CREATION](../../../Mod/Text/ExpeditionGate.sql#L513) | 创建准备期间普通间谍状态发生变化或无法读取，验证团已暂停。请从 P0 结束本团后重新创建；准备完成后可正常操作普通间谍。 | 准备考察团时普通间谍状态发生变化或无法读取，本团已暂停。请查看 P0「人文考察·验证」报告。结束本团后可重新训练。 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_NATIVE](../../../Mod/Text/ExpeditionGate.sql#L517) | 原生引擎未确认或拒绝本次派遣。请查看 P0「人文考察·验证」详细报告，不要连续重复提交。 | 游戏未确认或拒绝派遣。请查看 P0「人文考察·验证」报告，不要连续重复提交。 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_TARGET](../../../Mod/Text/ExpeditionGate.sql#L515) | 目标城市已变化或无法确认，本次不能派遣。请重新打开目的地列表；详细原因见 P0 报告。 | 目标城市已变化或无法确认，无法派遣。请重新打开目的地列表。详细原因见 P0 报告。 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_UNKNOWN](../../../Mod/Text/ExpeditionGate.sql#L519) | 考察团已暂停或操作失败。请查看 P0「人文考察·验证」详细报告，保留其中的具体错误。 | 考察团已暂停或操作失败。请保留 P0「人文考察·验证」报告中的错误信息。 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_ONE_SHOT](../../../Mod/Text/ExpeditionGate.sql#L463) | 本次任务已结束，考察团已返回该城市中心。你可在此城继续执行其它未完成的考察任务，或点击「派遣到新城市」前往新的目的地。 | 任务已结束。考察团恢复待命后，可在此城执行其他未完成的考察，或派遣至新城市。 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_ENDED](../../../Mod/Text/ExpeditionGate.sql#L481) | 状态：验证团已结束 | 状态：考察团已结束 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_TASK_COMPLETE](../../../Mod/Text/ExpeditionGate.sql#L475) | 状态：考察任务已完成 | 状态：考察任务已结束 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_PREFLIGHT_UNKNOWN](../../../Mod/Text/ExpeditionGate.sql#L511) | 尚未确认当前考察团或目标的派遣条件，本次未发送派遣请求。请重新打开；若仍失败，查看 P0「人文考察·验证」详细报告。 | 考察团或目标的派遣条件尚未确认，未发送派遣请求。请重新打开。若仍失败，请查看 P0「人文考察·验证」报告。 |
| [LOC_SPC_EXPEDITION_SPY_NORMAL_SELECTION_CHANGED](../../../Mod/Text/ExpeditionGate.sql#L451) | 正在核对所选考察团；若已切换单位，请关闭窗口后从该团的按钮重新打开。 | 所选考察团正在核对。若已切换单位，请关闭窗口，从该团的按钮重新打开。 |
| [LOC_SPC_EXPEDITION_SPY_TASK_NATIVE_NOT_IDLE](../../../Mod/Text/ExpeditionGate.sql#L248) | 未确认原生任务为空；本次不启动。刷新报告后保留异常信息。 | 无法确认考察团当前空闲，任务未启动。请刷新报告并保留异常信息。 |
| [LOC_SPC_EXPEDITION_SPY_TASK_REQUIRES_ARRIVAL](../../../Mod/Text/ExpeditionGate.sql#L246) | 需先抵达且身份/来源绑定核对成功。每支验证团只做一次任务。 | 考察团须先抵达目标城市并确认来源绑定，才能开始任务。 |
| [LOC_SPC_EXPEDITION_TRAINING_HELP](../../../Mod/Text/ExpeditionGate.sql#L560) | 本城文化启用等级达到 4 级时可训练。全国同时最多拥有 1 支（生产队列中的项目亦占用名额）。生产成本沿用间谍公式，并独立累计考察团的训练次数。训练完成后将自动绑定来源城市；请通过「派遣到新城市」或「任务」按钮进行操作。 | 本城文化启用等级达到四级时可训练，全国同时最多 1 支，生产队列中的项目也占用名额。成本沿用间谍公式，考察团训练次数独立累计。<br>训练完成后绑定来源城市。通过「派遣到新城市」或「任务」操作。 |

### 专业认定项目

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_PROJECT_SPC_CLAIM_COMMERCE_DESCRIPTION](../../../Mod/Text/ClaimProjects.sql#L7) | 开启后将作为唯一当前生产目标，连续占用 1 个完整回合。项目完成后，本城将确立「商业」专业身份并获得 1 级专业潜力（其它专业认定项目将随之移除）。项目开启前未分配的生产力及项目期间产生的生产力均不会结转至后续目标；中途保存或读档会继续正常计时，但若在队列中改选其它项目，再次开启时需重新计时。 | 完成后，本城确立「商业」专业身份，获得 1 级专业潜力，其他专业认定项目随之移除。<br><br>项目须作为唯一生产目标持续 1 个完整回合。未分配及项目期间产生的生产力不会结转。保存或读档后继续计时，改选其他项目则须重新开始。 |
| [LOC_PROJECT_SPC_CLAIM_CULTURE_DESCRIPTION](../../../Mod/Text/ClaimProjects.sql#L3) | 开启后将作为唯一当前生产目标，连续占用 1 个完整回合。项目完成后，本城将确立「文化」专业身份并获得 1 级专业潜力（其它专业认定项目将随之移除）。项目开启前未分配的生产力及项目期间产生的生产力均不会结转至后续目标；中途保存或读档会继续正常计时，但若在队列中改选其它项目，再次开启时需重新计时。 | 完成后，本城确立「文化」专业身份，获得 1 级专业潜力，其他专业认定项目随之移除。<br><br>项目须作为唯一生产目标持续 1 个完整回合。未分配及项目期间产生的生产力不会结转。保存或读档后继续计时，改选其他项目则须重新开始。 |
| [LOC_PROJECT_SPC_CLAIM_INDUSTRY_DESCRIPTION](../../../Mod/Text/ClaimProjects.sql#L5) | 开启后将作为唯一当前生产目标，连续占用 1 个完整回合。项目完成后，本城将确立「工业」专业身份并获得 1 级专业潜力（其它专业认定项目将随之移除）。项目开启前未分配的生产力及项目期间产生的生产力均不会结转至后续目标；中途保存或读档会继续正常计时，但若在队列中改选其它项目，再次开启时需重新计时。 | 完成后，本城确立「工业」专业身份，获得 1 级专业潜力，其他专业认定项目随之移除。<br><br>项目须作为唯一生产目标持续 1 个完整回合。未分配及项目期间产生的生产力不会结转。保存或读档后继续计时，改选其他项目则须重新开始。 |
| [LOC_PROJECT_SPC_CLAIM_RESEARCH_DESCRIPTION](../../../Mod/Text/ClaimProjects.sql#L1) | 开启后将作为唯一当前生产目标，连续占用 1 个完整回合。项目完成后，本城将确立「科研」专业身份并获得 1 级专业潜力（其它专业认定项目将随之移除）。项目开启前未分配的生产力及项目期间产生的生产力均不会结转至后续目标；中途保存或读档会继续正常计时，但若在队列中改选其它项目，再次开启时需重新计时。 | 完成后，本城确立「科研」专业身份，获得 1 级专业潜力，其他专业认定项目随之移除。<br><br>项目须作为唯一生产目标持续 1 个完整回合。未分配及项目期间产生的生产力不会结转。保存或读档后继续计时，改选其他项目则须重新开始。 |

### 时代对话项目

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_PROJECT_SPC_ERA_DIALOGUE_DESCRIPTION](../../../Mod/Text/DialogueProjects.sql#L4) | 需本城具备文化专业身份且启用等级达到 3 级。开启后将作为唯一当前生产目标，连续占用完整的 1 个回合（每城按项目启动时的游戏时代计算，每个时代最多成功完成一次）。完成时，本城合格馆藏每覆盖一个不同的作品时代，便为巨作原生旅游业绩倍率永久累加 5 个百分点（不放大「意义延展」的追加产出）。若中途打断将取消本轮项目，但不会消耗该时代的成功次数；项目开启前未分配的生产力及项目期间产生的生产力均不会结转至后续目标。 | 完成后，本城合格馆藏每涵盖一个不同的作品时代，巨作原生 [ICON_Tourism] 旅游业绩倍率永久累积 5 个百分点。文化启用等级达到三级时生效。<br><br>需要文化专业及三级启用。项目须作为唯一当前生产目标持续 1 个完整回合。每城按启动时的游戏时代计算，每时代最多成功一次。中断不消耗次数，未分配及项目期间产生的生产力不会结转。 |

### 工程传统研习项目

#### LOC_PROJECT_SPC_ENGINEERING_STUDY_DESCRIPTION

`LOC_PROJECT_SPC_ENGINEERING_STUDY_DESCRIPTION` · [EngineeringStudy.sql:5](../../../Mod/Text/EngineeringStudy.sql#L5)

```text
需要本城工业启用等级达到四级，且研习层数少于本文明亲建奇观所覆盖的时代数。

项目占用 1 个完整生产回合，每次完成后累计 1 层。四级启用时，每层使匹配模板的建造加成及原本可购买的合格建筑购买折扣各提高 2 个百分点。

中断、城市易主或启用等级下降会取消未完成的研习，已积累层数保留。未分配及项目期间产生的生产力不会结转。
```

<details>
<summary>现行文字</summary>

```text
需本城工业启用等级达到 4 级，且本城已完成的研习层数（L）少于本文明奇观历史覆盖的时代数（E）。开启后将连续占用 1 个完整的生产回合，完成后本城研习层数（L）永久 +1。当工业启用等级为 4 级时，每层研习成果使本城持有可靠模板的建造生产力加成与合格建筑金币购买折扣各提高 2 个百分点（当前版本暂未实装目标区域的逐模板购买折扣）。若中途打断、城市易主或启用等级下降，将取消未完成的当前轮次，但已积累的历史层数不会清零。项目将吸收开启前未分配的生产力及项目期间产生的生产力，不会结转至后续目标。
```

</details>

### 测试文明与文明百科简介

| 文本键 | 现行文字 | 候选文字 |
|---|---|---|
| [LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_CAPSULE_BODY](../../../Mod/Text/TestAmerica.sql#L35) | 罗斯福（进步党）的专业测试版本。 | 罗斯福（进步党）的城市专业化测试版本。 |
| [LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_DETAILED_BODY](../../../Mod/Text/TestAmerica.sql#L36) | 本领袖不拥有美国或罗斯福的特色能力、特色单位和特色建筑。可通过城市专业化使用科研、文化、商业和工业专业系统。 | 此测试领袖不拥有美国或罗斯福的特色能力、特色单位和特色建筑。城市可使用科研、文化、商业和工业专业系统。 |
| [LOC_SPC_ABILITY_DESCRIPTION](../../../Mod/Text/TestAmerica.sql#L14) | 可使用科研、文化、商业和工业专业系统。各专业的机构、投资与网络能力按专业规则启用。 | 城市可使用科研、文化、商业和工业专业系统。各专业的机构、投资与网络能力按专业规则启用。 |
| [LOC_SPC_SYSTEM_DESCRIPTION](../../../Mod/Text/TestAmerica.sql#L10) | 可使用科研、文化、商业和工业专业系统。各专业的机构、投资与网络能力按专业规则启用。 | 城市可使用科研、文化、商业和工业专业系统。各专业的机构、投资与网络能力按专业规则启用。 |

## 界面内直写文字

源位置的行列用于找到拼接片段。引号内保留动态值前后的空格与换行标记。标作「仅显示」的候选供将来在呈现层映射，状态、存档或恢复判断继续使用原始原因。时代对话的「生产未确认」由生产队列恢复逻辑读取，定位见 [TimedProjectQueueIntent.lua:144](../../../Mod/UI/TimedProjectQueueIntent.lua#L144)。

### 专业认领

| 来源 | 现行文字 | 候选文字 |
|---|---|---|
| [ClaimProjects.lua:54:110](../../../Mod/ClaimProjects.lua#L54)（仅显示） | `"专业已认领，Potential 1"` | `"专业已确立，起始潜力为 1 级"` |
| [ClaimProjects.lua:58:42](../../../Mod/ClaimProjects.lua#L58)（仅显示） | `"已改选目标；重新选择须完整占用一回合"` | `"生产目标已更改。重新选择后须持续 1 个完整回合"` |
| [ClaimProjects.lua:59:82](../../../Mod/ClaimProjects.lua#L59)（仅显示） | `"当前队列未确认；不完成项目"` | `"生产队列待确认，项目不会完成"` |
| [ClaimProjects.lua:63:121](../../../Mod/ClaimProjects.lua#L63)（仅显示） | `"当前队列未确认；等待相关事件，不完成项目"` | `"生产队列待确认。等待队列更新，项目不会完成"` |
| [ClaimProjects.lua:67:59](../../../Mod/ClaimProjects.lua#L67)（仅显示） | `"当前项目没有计时；请先改选普通目标，再重选认领项目，重新占用完整一回合"` | `"项目尚未计时。请先改选普通生产目标，再重新选择认定项目，持续 1 个完整回合"` |
| [ClaimProjects.lua:71:117](../../../Mod/ClaimProjects.lua#L71)（仅显示） | `"选择一个候选项目，完成后认领专业"` | `"选择一个认定项目，完成后确立专业"` |
| [ClaimProjects.lua:131:23](../../../Mod/ClaimProjects.lua#L131)（仅显示） | `"找不到对应已完成区域；暂停认领"` | `"未找到对应的已完成区域。认定已暂停"` |
| [ClaimProjectUI.lua:23:29](../../../Mod/UI/ClaimProjectUI.lua#L23) | `"等待Gameplay确认；若持续如此请查看当前项目提示"` | `"等待项目状态确认。若持续如此，请查看当前项目提示。"` |
| [ClaimProjectUI.lua:25:13](../../../Mod/UI/ClaimProjectUI.lua#L25) | `"认领需完整一回合；完成才建立专业。已有未分配生产与项目期间生产不留给后续目标。"` | `"项目须持续 1 个完整回合，完成后才确立专业。未分配及项目期间产生的生产力不会结转。"` |
| [ClaimProjectUI.lua:46:58](../../../Mod/UI/ClaimProjectUI.lua#L46) | `"认领项目不能排在队列后面；请选为唯一当前目标"` | `"认定项目不能排在队列后面。请选择为唯一当前目标。"` |
| [ClaimProjectUI.lua:49:40](../../../Mod/UI/ClaimProjectUI.lua#L49) | `"等待原生选择确认"` | `"等待生产选择确认"` |

### 时代对话

| 来源 | 现行文字 | 候选文字 |
|---|---|---|
| [DialogueProjects.lua:121:114](../../../Mod/DialogueProjects.lua#L121)（仅显示） | `"需要文化身份及ACTIVE III"` | `"需要文化专业身份及三级启用等级"` |
| [DialogueProjects.lua:122:41](../../../Mod/DialogueProjects.lua#L122)（仅显示） | `"当前资格尚不可确认；未清除历史，也不完成项目"` | `"专业资格待确认。历史保留，项目不会完成"` |
| [DialogueProjects.lua:124:84](../../../Mod/DialogueProjects.lua#L124)（仅显示） | `"当前资格或生产未确认；等待相关事件，不完成项目"` | `"资格或生产状态待确认。等待相关更新，项目不会完成"` |
| [DialogueProjects.lua:174:30](../../../Mod/DialogueProjects.lua#L174)（仅显示） | `"需要已确认的文化ACTIVE III"` | `"需要确认文化启用等级达到三级"` |
| [DialogueProjectUI.lua:21:13](../../../Mod/UI/DialogueProjectUI.lua#L21) | `"时代对话：需连续占用完整的 1 个回合；完成后按本城合格馆藏覆盖的作品时代数，永久累计巨作原生旅游业绩倍率。"` | `"时代对话需持续 1 个完整生产回合。完成时，本城合格馆藏每涵盖一个作品时代，巨作的 [ICON_Tourism] 旅游业绩加成永久累积 5 个百分点。加成在文化启用等级达到三级时生效。"` |
| [DialogueProjectUI.lua:31:35](../../../Mod/UI/DialogueProjectUI.lua#L31) | `"此项目须独占生产队列并连续占用完整的 1 个回合；计时等待Gameplay确认，未确认时不会完成项目。"` | `"此项目须独占生产队列并持续 1 个完整回合。计时待确认，确认前不会完成项目。"` |

### 模组列表

| 来源 | 现行文字 | 候选文字 |
|---|---|---|
| [SpecializationP0.modinfo:5:5](../../../Mod/SpecializationP0.modinfo#L5) | `"B443.470：恢复专业项目生产面板接入。"` | `"城市专业化玩法测试：体验机构、投资与专业网络。"` |

### 资本投资

| 来源 | 现行文字 | 候选文字 |
|---|---|---|
| [CapitalInvestmentPanel.lua:20:80](../../../Mod/UI/CapitalInvestmentPanel.lua#L20) | `"签约需要商业 ACTIVE III"` | `"签约需要商业启用等级达到三级"` |
| [CapitalInvestmentPanel.lua:21:73](../../../Mod/UI/CapitalInvestmentPanel.lua#L21) | `"同级来源缺少可靠机构建立时间"` | `"同级来源的机构建立时间暂不可确认"` |
| [CapitalInvestmentPanel.lua:23:29](../../../Mod/UI/CapitalInvestmentPanel.lua#L23) | `"金币实际变化与请求不符，已停止重复操作；请交回日志"` | `"本次金币变动尚未确认。请保留日志，暂勿再次确认。"` |
| [CapitalInvestmentPanel.lua:24:34](../../../Mod/UI/CapitalInvestmentPanel.lua#L24) | `"金币回执尚未确认；合同已暂停"` | `"金币回执待确认。合同已暂停"` |
| [CapitalInvestmentPanel.lua:25:26](../../../Mod/UI/CapitalInvestmentPanel.lua#L25) | `"专业来源暂不可确认"` | `"专业实力来源待确认"` |
| [CapitalInvestmentPanel.lua:25:68](../../../Mod/UI/CapitalInvestmentPanel.lua#L25) | `"城市归属暂不可确认"` | `"城市归属待确认"` |
| [CapitalInvestmentPanel.lua:26:32](../../../Mod/UI/CapitalInvestmentPanel.lua#L26) | `"国库暂不可读取"` | `"国库余额暂不可读取"` |
| [CapitalInvestmentPanel.lua:26:69](../../../Mod/UI/CapitalInvestmentPanel.lua#L26) | `"信誉暂不可确认；风险投资暂停，稳健投资仍按独立资格判断"` | `"商业信誉待确认。风险投资暂停，稳健投资仍按自身条件判断"` |
| [CapitalInvestmentPanel.lua:35:54](../../../Mod/UI/CapitalInvestmentPanel.lua#L35) | `"信誉记录异常；本次按无信誉加成政策计价（R=0），原记录保留。"` | `"信誉记录异常。本次按无信誉加成计价（R=0），原记录保留。"` |
| [CapitalInvestmentPanel.lua:108:66](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | `"需核对回执"` | `"回执待确认"` |
| [CapitalInvestmentPanel.lua:108:107](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | `"需核对扣款"` | `"扣款待确认"` |
| [CapitalInvestmentPanel.lua:108:152](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | `"需核对返还"` | `"返还待确认"` |

### 工程传统研习

| 来源 | 现行文字 | 候选文字 |
|---|---|---|
| [EngineeringStudyUI.lua:13:44](../../../Mod/UI/EngineeringStudyUI.lua#L13) | `"工程传统研习：完整一回合后，本城历史层数 +1。"` | `"工程传统研习：完成 1 个完整生产回合后，本城永久积累 1 层成果。"` |
| [EngineeringStudyUI.lua:16:63](../../../Mod/UI/EngineeringStudyUI.lua#L16) | `"工程传统研习必须独占生产队列；移除其他项后自动核对计时。"` | `"工程传统研习须独占生产队列。移除其他项目后自动核对计时。"` |
| [EngineeringStudyUI.lua:22:35](../../../Mod/UI/EngineeringStudyUI.lua#L22) | `"请选择为唯一当前项目；中断后需要重新选择。"` | `"请选择为唯一当前项目。中断后须重新选择。"` |
| [EngineeringStudyUI.lua:23:13](../../../Mod/UI/EngineeringStudyUI.lua#L23) | `"需要工业 ACTIVE IV 且本城 L 小于全国 E；中断取消本轮。"` | `"需要工业启用等级达到四级，且本城研习层数少于本文明亲建奇观覆盖的时代数。中断会取消本轮。"` |

### 生产队列

| 来源 | 现行文字 | 候选文字 |
|---|---|---|
| [TimedProjectQueueIntent.lua:86:39](../../../Mod/UI/TimedProjectQueueIntent.lua#L86) | `"已达到当前可研习知识；若队列中仍有项目，请移除。"` | `"本城已完成所有可研习的经验。若队列中仍有项目，请移除。"` |
| [TimedProjectQueueIntent.lua:86:68](../../../Mod/UI/TimedProjectQueueIntent.lua#L86) | `"本游戏时代的时代对话机会已使用；若队列中仍有项目，请移除。"` | `"本游戏时代的时代对话已完成。若队列中仍有项目，请移除。"` |
| [TimedProjectQueueIntent.lua:88:10](../../../Mod/UI/TimedProjectQueueIntent.lua#L88) | `"当前专业资格不满足；不会计时或发放奖励。"` | `"当前专业资格不满足，项目不会计时或产生收益。"` |
| [TimedProjectQueueIntent.lua:94:36](../../../Mod/UI/TimedProjectQueueIntent.lua#L94) | `"入队请求尚未确认，不重复加入；等待相关队列变化。"` | `"入队请求待确认，不会重复加入。请等待队列更新。"` |
| [TimedProjectQueueIntent.lua:100:25](../../../Mod/UI/TimedProjectQueueIntent.lua#L100) | `"待核实"` | `"待确认"` |
| [TimedProjectQueueIntent.lua:100:31](../../../Mod/UI/TimedProjectQueueIntent.lua#L100) | `"生产队列暂不可确认，请稍后重新选择；不会重复加入项目。"` | `"生产队列待确认，请稍后重新选择。不会重复加入项目。"` |
| [TimedProjectQueueIntent.lua:103:76](../../../Mod/UI/TimedProjectQueueIntent.lua#L103) | `"队列内存在重复项目，请只保留一项；不会重复发放。"` | `"队列中有重复项目，请只保留一项。不会重复发放收益。"` |
| [TimedProjectQueueIntent.lua:103:105](../../../Mod/UI/TimedProjectQueueIntent.lua#L103) | `"此项目已在队列中，不会重复加入；成为唯一当前项目后才计时。"` | `"项目已在队列中，不会重复加入。成为唯一当前项目后才开始计时。"` |
| [TimedProjectQueueIntent.lua:153:20](../../../Mod/UI/TimedProjectQueueIntent.lua#L153) | `"本回合已有完成记录，无法确认此队列项是否为新一轮；请重新选择项目。"` | `"本回合已有完成记录，无法确认此队列项是否为新一轮。请重新选择项目。"` |
| [TimedProjectQueueIntent.lua:174:25](../../../Mod/UI/TimedProjectQueueIntent.lua#L174) | `"待核实"` | `"待确认"` |
| [TimedProjectQueueIntent.lua:174:31](../../../Mod/UI/TimedProjectQueueIntent.lua#L174) | `"生产队列尚不可确认，等待相关变化；不会完成项目。"` | `"生产队列待确认。请等待相关状态更新，项目暂不结算。"` |
| [TimedProjectQueueIntent.lua:180:34](../../../Mod/UI/TimedProjectQueueIntent.lua#L180) | `"队列内存在重复项目，请只保留一项；不会重复发放。"` | `"队列中有重复项目，请只保留一项。不会重复发放收益。"` |
| [TimedProjectQueueIntent.lua:184:55](../../../Mod/UI/TimedProjectQueueIntent.lua#L184) | `"项目必须独占生产队列；移除其他项后自动核对计时。"` | `"项目须独占生产队列。移除其他项目后自动核对计时。"` |
| [TimedProjectQueueIntent.lua:184:84](../../../Mod/UI/TimedProjectQueueIntent.lua#L184) | `"尚未成为唯一当前项目，不计时；轮到后自动核对。"` | `"项目尚未成为唯一当前目标，不会计时。轮到时自动核对。"` |
| [TimedProjectQueueIntent.lua:191:35](../../../Mod/UI/TimedProjectQueueIntent.lua#L191) | `"本地回合已结束，等待下一个可靠回合起点开始完整计时。"` | `"本回合已结束。须等到下一回合确认可开始后才计时。"` |
| [TimedProjectQueueIntent.lua:196:71](../../../Mod/UI/TimedProjectQueueIntent.lua#L196) | `"等待本地回合可操作状态确认；不补计排队时间。"` | `"等待本地回合可操作状态确认。排队时间不计入项目。"` |
| [TimedProjectQueueIntent.lua:201:16](../../../Mod/UI/TimedProjectQueueIntent.lua#L201) | `"正在确认完整一回合计时；不会重复提交同一轮。"` | `"正在确认完整回合计时。不会重复提交本轮。"` |
| [TimedProjectQueueIntent.lua:204:60](../../../Mod/UI/TimedProjectQueueIntent.lua#L204) | `"启动请求结果未知；不会盲目重发，请保留日志。"` | `"启动请求结果待确认。状态没有变化时，系统会等待确认。请保留日志。"` |

### 施工队和移民

| 来源 | 现行文字 | 候选文字 |
|---|---|---|
| [UnitPanelActions.lua:128:9](../../../Mod/UI/UnitPanelActions.lua#L128) | `"施工[NEWLINE]将施工队移动至正在建造奇观的单元格，即可进行施工。"` | `"施工[NEWLINE]将施工队移动至正在建造奇观的单元格，即可预览施工。"` |
| [UnitPanelActions.lua:135:6](../../../Mod/UI/UnitPanelActions.lua#L135) | `"[NEWLINE]本次消耗：1 名移民[NEWLINE][NEWLINE]提示：更高阶的专业能力仍需满足对应的总督就职与晋升条件方可启用。"` | `"[NEWLINE]本次消耗：1 名移民[NEWLINE][NEWLINE]更高等级的专业能力仍需满足相应的总督就职与晋升条件。"` |
| [UnitPanelActions.lua:136:4](../../../Mod/UI/UnitPanelActions.lua#L136) | `"确认专业投资[NEWLINE]消耗此移民，使本城的专业潜力永久提升至 "` | `"确认专业投资[NEWLINE]消耗此移民，将本城专业潜力永久提升至 "` |
| [UnitPanelActions.lua:136:60](../../../Mod/UI/UnitPanelActions.lua#L136) | `" 级。[NEWLINE]此操作一旦确认无法撤销。"` | `" 级。[NEWLINE]确认后无法撤销。"` |
| [UnitPanelActions.lua:138:31](../../../Mod/UI/UnitPanelActions.lua#L138) | `"投资专业化[NEWLINE]消耗 1 名移民，使本城的专业潜力永久提升 1 级。"` | `"投资专业化[NEWLINE]消耗 1 名移民，使本城专业潜力永久提升 1 级。"` |
| [UnitPanelActions.lua:139:62](../../../Mod/UI/UnitPanelActions.lua#L139) | `" 级[NEWLINE]点击以预览投资结果并进行最终确认。"` | `" 级[NEWLINE]点击查看投资预览，再确认投资。"` |
| [UnitPanelActions.lua:140:76](../../../Mod/UI/UnitPanelActions.lua#L140) | `"投资专业化[NEWLINE]专业潜力已达到4级，无法继续投资。"` | `"投资专业化[NEWLINE]专业潜力已达 4 级，无法继续投资。"` |
| [UnitPanelActions.lua:142:10](../../../Mod/UI/UnitPanelActions.lua#L142) | `"投资专业化[NEWLINE]此前专业投资的结果尚待确认，暂时无法再次投资。"` | `"投资专业化[NEWLINE]上一次投资结果待确认，暂时无法再次投资。"` |
| [UnitPanelActions.lua:144:9](../../../Mod/UI/UnitPanelActions.lua#L144) | `"投资专业化[NEWLINE]将移民移动至本城的专业区域，即可投资城市专业化。"` | `"投资专业化[NEWLINE]将移民移动至本城的专业区域，即可投资专业化。"` |

## 覆盖与核对

已核对动态参数、原生图标键、六个机构实时数据标题和界面数值的拼接边界。语义复核依据现行 [科研](../../Design/Content/Research_D0059.json)、[文化](../../Design/Content/Culture_D0059.json)、[商业](../../Design/Content/Commerce_D0059.json)、[工业](../../Design/Content/Industry_D0059.json) 与 [共用规则](../../Design/Content/Shared_D0060.json)。本次为文字和源码复核。游戏内折行、图标显示和面板尺寸待接入后检查。

未列出改写的键沿用基线文字。诊断与旧验证条目的中文随原有调试入口保留。

| 当前文本文件 | 已核对 | 候选改写 | 沿用 | 诊断与旧验证 |
|---|---:|---:|---:|---:|
| [TestText.sql](../../../Mod/Text/TestText.sql) | 162 | 15 | 76 | 71 |
| [Restructuring.sql](../../../Mod/Text/Restructuring.sql) | 24 | 7 | 17 | 0 |
| [Commerce.sql](../../../Mod/Text/Commerce.sql) | 110 | 11 | 99 | 0 |
| [DevelopmentInvestment.sql](../../../Mod/Text/DevelopmentInvestment.sql) | 55 | 5 | 50 | 0 |
| [ExpeditionGate.sql](../../../Mod/Text/ExpeditionGate.sql) | 301 | 24 | 222 | 55 |
| [ClaimProjects.sql](../../../Mod/Text/ClaimProjects.sql) | 8 | 4 | 4 | 0 |
| [DialogueProjects.sql](../../../Mod/Text/DialogueProjects.sql) | 4 | 1 | 2 | 1 |
| [EngineeringStudy.sql](../../../Mod/Text/EngineeringStudy.sql) | 2 | 1 | 1 | 0 |
| [LevelBanners.sql](../../../Mod/Text/LevelBanners.sql) | 5 | 0 | 5 | 0 |
| [TestAmerica.sql](../../../Mod/Text/TestAmerica.sql) | 14 | 4 | 10 | 0 |
| 合计 | 685 | 72 | 486 | 127 |

直写文字共核对 169 处，50 处有文案改写，11 处给出仅显示的候选，108 处沿用。
