> 范围决定已完成：D0015 IND-NET-004/005是当前权威。本目录及JSON保留决定前的167栋调查快照，原“候选/待定”标记不再表示当前设计未决；不要将此JSON直接作为运行允许清单。

# 工业标准化建筑候选目录 — 待用户决定范围

Document Owner: Codex
Catalog Revision: CANDIDATE-001
Document State: PROPOSAL_NOT_ACCEPTED
Design Reference: D0014 / IND-NET-001..004
Runtime Reference: P0-B-051.67 / modinfo67 unchanged
Evidence: STATIC_CONFIRMED（只读数据库与源码证据，不等于实机通过）

## 用户摘要

已将本机HD分级表的**167栋建筑、17类区域、49个区域+Tier组**整理为中文候选目录，逐项编号见末尾附表。四个现有专业区域占50栋，但这不是自动批准的白名单。

本轮仅提供目录，不修改Design、不实现记录或购买折扣。你可先选区域，再决定特色建筑、信仰建筑、市中心和无法默认购买建筑等特殊项。区域中的建筑进入模板范围，不代表相应专业或辅助机制进入v0.1。

**关键含义：** 如果采用“同区域+同Tier”，工业源拥有某组内一个合格模板，就可能使接收城市另一栋同组建筑满足模板条件。例如同为工业区T4的燃煤/燃油/核电、互联网公司、物流中心会属于同一候选组。此目录只是让这层共享范围可见，尚未批准或实现。

## 1. 区域总览

| 区域 | 建筑数 | HD分级分布 |
|---|---:|---|
| 学院 | 13 | T1：2；T2：4；T3：4；T4：3 |
| 剧院广场 | 13 | T1：3；T2：2；T3：5；T4：3 |
| 商业中心 | 12 | T1：2；T2：3；T3：4；T4：3 |
| 工业区 | 12 | T1：2；T2：2；T3：3；T4：5 |
| 军营 | 11 | T1：5；T2：3；T3：3 |
| 圣地 | 27 | T1：2；T2：5；T3：18；T4：2 |
| 港口 | 8 | T1：2；T2：3；T3：3 |
| 航空港 | 2 | T1：2 |
| 水渠 | 5 | T1：4；T2：1 |
| 堤坝 | 1 | T1：1 |
| 社区 | 10 | T1：2；T2：1；T3：7 |
| 娱乐中心 | 9 | T1：3；T2：4；T3：2 |
| 水上乐园 | 6 | T1：2；T2：2；T3：2 |
| 保护区 | 7 | T1：1；T2：2；T3：4 |
| 市政广场 | 11 | T1：4；T2：4；T3：3 |
| 外交区 | 6 | T1：1；T2：1；T3：4 |
| 市中心 | 14 | T0：14 |

## 2. 中文分组目录

标记：〔特色〕=Buildings.TraitType非空；〔信仰〕=PurchaseYield为Faith；〔无默认购买〕=PurchaseYield为空。这些是数据库属性，不是最终游戏购买权限。未标记购买类别的条目本表均为Gold字段；仍可能受科技、市政、宗教、互斥、文明资格或Modifier影响。

HD Tier不等于专业等级，也不按建筑成本猜。尤其**机场和机库在当前HD表中都为T1**，本轮原样列出，不擅自改成T2。

### 学院

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 私塾、图书馆 |
| 2 | 城市学校、艾孜哈尔伊斯兰大学〔特色〕、航海学校〔特色〕、大学 |
| 3 | 建筑学院、实验室、文艺学院、研究院 |
| 4 | 数据中心、综合大学、理工学院 |

### 剧院广场

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 古罗马剧场、公民大会、毛利会堂〔特色〕 |
| 2 | 陈列室、官学 |
| 3 | 艺术刊社、大酒店、歌剧院、艺术博物馆、考古博物馆 |
| 4 | 广播中心、电影制片厂〔特色〕、媒体中心 |

### 商业中心

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 集市、货栈 |
| 2 | 铸币厂、市场、克拉科夫纺织会馆〔特色〕 |
| 3 | 银行、大巴扎〔特色〕、工商会馆、商人中心 |
| 4 | 商务写字楼、市场部、证券交易所 |

### 工业区

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 水力作坊、风车 |
| 2 | 手工工场、建造工坊 |
| 3 | 工厂、电子厂、化工厂 |
| 4 | 燃煤发电厂、燃油发电厂、互联网公司、物流中心、核电站 |

### 军营

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 兵营、皇家学堂〔特色〕、边关、斡耳朵〔特色〕、马厩 |
| 2 | 兵工厂、募兵所、补给站 |
| 3 | 军事政治处、军事研究院、军事学院 |

### 圣地

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 祭坛、神社 |
| 2 | 丹房、教堂、高棉庙堂〔特色〕、博尔贡木板教堂〔特色〕、寺庙 |
| 3 | 大教堂〔信仰〕、拜火神庙〔信仰〕、谒师所〔信仰〕、禅邸〔信仰〕、道观〔信仰〕、神道教神社〔信仰〕、隐修会〔信仰〕、印度神庙〔信仰〕、姆巴里〔信仰〕、柱廊神庙〔信仰〕、东正教堂〔信仰〕、羽蛇神庙〔信仰〕、礼拜堂〔信仰〕、清真寺〔信仰〕、藏经阁〔信仰〕、窣堵波〔信仰〕、犹太教堂〔信仰〕、佛寺〔信仰〕 |
| 4 | 花园〔信仰〕、济贫院〔信仰〕 |

### 港口

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 渔业码头、贸易码头 |
| 2 | 军港、商港、造船厂 |
| 3 | 海军基地、游轮码头、海港 |

### 航空港

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 机场、机库 |

### 水渠

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 水力纺车、浴场、水力锻锤、果园 |
| 2 | 下水道 |

### 堤坝

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 水电站坝 |

### 社区

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 官邸〔无默认购买〕、别墅 |
| 2 | 公交站 |
| 3 | 农贸市场、艺术街区、中心医院、房车营地、回收中心、客运中心、百货大楼 |

### 娱乐中心

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 竞技场、勾栏瓦舍、蹴球场〔特色〕 |
| 2 | 沙龙、植物园、温泉浴场〔特色〕、动物园 |
| 3 | 博览会、体育场 |

### 水上乐园

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 摩天轮、音乐游船 |
| 2 | 水族馆、游客接待中心 |
| 3 | 水上运动中心、纪念品商店 |

### 保护区

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 神谕碑 |
| 2 | 人文遗产保护部、自然环境保护部 |
| 3 | 地貌生态环保专局〔无默认购买〕、不可再生资源管理专局〔无默认购买〕、自然名胜旅游专局〔无默认购买〕、物种多样性维护专局〔无默认购买〕 |

### 市政广场

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 埃斯科里亚尔王宫〔特色、无默认购买〕、军阀宝座〔无默认购买〕、谒见厅〔无默认购买〕、会议堂〔无默认购买〕 |
| 2 | 贸易本埠〔无默认购买〕、主教座堂〔无默认购买〕、中书省〔无默认购买〕、女王图书馆〔特色、无默认购买〕 |
| 3 | 国家历史博物馆〔无默认购买〕、作战部〔无默认购买〕、皇家学会〔无默认购买〕 |

### 外交区

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 1 | 领事馆 |
| 2 | 总领馆 |
| 3 | 人权理事会〔无默认购买〕、国防部〔无默认购买〕、区域议会中心〔无默认购买〕、世界议会总部〔特色、无默认购买〕 |

### 市中心

| HD Tier | 同区域同Tier候选建筑 |
|---|---|
| 0 | 中世纪城墙〔无默认购买〕、会展中心、拦海堤〔无默认购买〕、粮仓、警署、法表、纪念碑、测量仪、宫殿〔无默认购买〕、沟渠〔特色〕、文艺复兴城墙〔无默认购买〕、堡垒〔特色、无默认购买〕、远古城墙〔无默认购买〕、磨坊 |

## 3. 必须单独看清的范围

### 3.1 市中心：14栋全部是Tier 0

粮仓、纪念碑、磨坊、宫殿、各级城墙、拦海堤等全部同组。直接套“同区域+同Tier”，可能意味着一个低级建筑模板满足另一完全不同市中心建筑的模板条件。建议本轮暂不自动纳入；若你想包含，请选择具体建筑并另定合理组。此建议不是已生效排除规则。

### 3.2 购买币种与不可直接购买项

- 字段为Gold：121栋。
- 字段为Faith：20栋，全在圣地；18栋祭祀建筑为T3，花园/济贫院为T4。
- 字段为空：26栋，包括市政广场11栋、外交区T3四栋、保护区T3四栋、社区官邸及部分市中心建筑。

**记录模板**与**实际获得金币折扣**是两件事。即使决定记录某栋Faith/无默认购买建筑，也不能因此使它可Gold购买或改变Faith价格。当前本机字段不能证明所有政策/Mod条件下绝对不可Gold购买；Gold-only原生效果仍是后续技术验证，目录不替它作结论。

### 3.3 特色建筑与替代关系

当前17栋建筑有Trait限制；其中部分并无BuildingReplaces记录。不能仅依据“特色”字样推断替代对象。

| 特色建筑 | 区域/Tier | 数据库明确替代 |
|---|---|---|
| 艾孜哈尔伊斯兰大学 | 学院 / T2 | 无显式BuildingReplaces行 |
| 航海学校 | 学院 / T2 | 城市学校 |
| 沟渠 | 市中心 / T0 | 磨坊 |
| 堡垒 | 市中心 / T0 | 中世纪城墙 |
| 克拉科夫纺织会馆 | 商业中心 / T2 | 无显式BuildingReplaces行 |
| 大巴扎 | 商业中心 / T3 | 银行 |
| 世界议会总部 | 外交区 / T3 | 区域议会中心 |
| 皇家学堂 | 军营 / T1 | 兵营、马厩 |
| 斡耳朵 | 军营 / T1 | 马厩 |
| 蹴球场 | 娱乐中心 / T1 | 竞技场 |
| 温泉浴场 | 娱乐中心 / T2 | 沙龙 |
| 埃斯科里亚尔王宫 | 市政广场 / T1 | 无显式BuildingReplaces行 |
| 女王图书馆 | 市政广场 / T2 | 无显式BuildingReplaces行 |
| 高棉庙堂 | 圣地 / T2 | 寺庙 |
| 博尔贡木板教堂 | 圣地 / T2 | 无显式BuildingReplaces行 |
| 毛利会堂 | 剧院广场 / T1 | 公民大会 |
| 电影制片厂 | 剧院广场 / T4 | 媒体中心 |

若纳入特色模板，是否与同区域同Tier的普通建筑共享模板资格，应由你确认。无论如何，不能借折扣解锁玩家本来无资格购买的特色建筑。本次JSON另保留DistrictReplaces关系；没有将特色区域归一化规则默认为已批准。

### 3.4 看似正常但不属于候选的虚拟建筑

除167条HD分类外，发现17条Buildings中非InternalOnly、非Wonder、有区域却不在HD Tier表的记录；**全部同时列于HD_DUMMY_BUILDINGS**，包括运河标记、云韶府和奇观派生dummy。不应仅按InternalOnly=0将它们当成可用建筑；它们在附件JSON单列，未混入167栋目录。

本机167条均有对应Buildings记录，区域一致，无Wonder/InternalOnly/dummy污染。没有未分类的其它普通建筑被悄悄补Tier；不同Mod组合中新增加的未知建筑仍须重新分类。

## 4. 供你选择的范围方式

请按你想要的玩法选，而不是被实现难度迫使缩小范围：

1. **区域范围**：只选学院/剧院/商业/工业四类；或逐项添加军营、港口、圣地、航空港、水渠、堤坝、社区、娱乐/水上乐园、保护区、政府类区域；也可以选全部再列排除项。
2. **特色建筑**：全部纳入同组共享、全部暂排除，或指定例外。
3. **Faith / 无默认购买建筑**：是否也记录永久模板（不会自动获得Gold购买资格或Faith折扣）。
4. **市中心Tier0**：暂排除，或列出具体建筑后另定分组。

Codex建议便于首批验证的起点：四个现有专业区域的普通建筑（44栋）先作为候选，6栋特色建筑单独确认；其它区域按你的意图扩展，市中心Tier0不自动大组共享。这只是建议，并未落入Design或代码。你不必逐条抄167个ID，只需回复区域范围与特殊项处理。

当前全部条目仍为**DESIGN_DECISION_REQUIRED**；这里指“待选允许范围”，不是质疑D0013已确认的任意合法获得、首次补录与事件增量规则。

## 5. 证据与再生成方式

来源为外部只读DebugGameplay.sqlite的HD_BuildingTiers/Buildings/BuildingReplaces/DistrictReplaces/HD_DUMMY_BUILDINGS；分类源码为HD UpdateDataBase/HD_BuildingTiers.sql（对应hash见JSON）。该表按前置建筑逐层构建Tier，特殊处理圣地，删除HD dummy；其用途包含城邦收益分类，不应自动等同本项目已批准的模板分组。

中文名优先本机HD与HD区域扩展Text，再以本机原版/DLC或相关扩展文本补齐；每条记录保存name_source。已全部找到中文名，但没有完整重放游戏本地化加载顺序，因此名称是有出处的展示标签，BuildingType才是精确对象。不复制外部数据库、Mod源码或美术资产进入repo，仅保留本次候选清单与引用。

复核查询核心：
```sql
SELECT h.BuildingType,h.PrereqDistrict,h.Tier,h.ReplacesOther,
       b.Name,b.PurchaseYield,b.TraitType,b.InternalOnly,b.IsWonder
FROM HD_BuildingTiers h JOIN Buildings b USING(BuildingType)
ORDER BY h.PrereqDistrict,h.Tier,h.BuildingType;
```

[逐条结构化清单](Specialization_Standardization_Catalog_Candidate.json)包含167项、17项dummy对照、替代关系和名称出处。它是研究数据，**不被运行Mod加载，不是已接受allowlist**。

## 6. 精确对象附表

| 中文名 | BuildingType | 区域 / HD Tier | 标记 |
|---|---|---|---|
| 私塾 | `BUILDING_JNR_ACADEMY` | 学院 / 1 | 普通候选 |
| 图书馆 | `BUILDING_LIBRARY` | 学院 / 1 | 普通候选 |
| 城市学校 | `BUILDING_JNR_SCHOOL` | 学院 / 2 | 普通候选 |
| 艾孜哈尔伊斯兰大学 | `BUILDING_MADRASA` | 学院 / 2 | 特色/特质限制；玩家数量上限 |
| 航海学校 | `BUILDING_NAVIGATION_SCHOOL` | 学院 / 2 | 特色/特质限制；替代建筑 |
| 大学 | `BUILDING_UNIVERSITY` | 学院 / 2 | 普通候选 |
| 建筑学院 | `BUILDING_JNR_ARCHITECTURE` | 学院 / 3 | 普通候选 |
| 实验室 | `BUILDING_JNR_LABORATORY` | 学院 / 3 | 普通候选 |
| 文艺学院 | `BUILDING_JNR_LIBERAL_ARTS` | 学院 / 3 | 普通候选 |
| 研究院 | `BUILDING_JNR_REAL_ACADEMY` | 学院 / 3 | 普通候选 |
| 数据中心 | `BUILDING_HD_DATA_CENTER` | 学院 / 4 | 玩家数量上限 |
| 综合大学 | `BUILDING_JNR_EDUCATION` | 学院 / 4 | 普通候选 |
| 理工学院 | `BUILDING_RESEARCH_LAB` | 学院 / 4 | 普通候选 |
| 古罗马剧场 | `BUILDING_AMPHITHEATER` | 剧院广场 / 1 | 普通候选 |
| 公民大会 | `BUILDING_JNR_ASSEMBLY` | 剧院广场 / 1 | 普通候选 |
| 毛利会堂 | `BUILDING_MARAE` | 剧院广场 / 1 | 特色/特质限制；替代建筑 |
| 陈列室 | `BUILDING_JNR_CABINET` | 剧院广场 / 2 | 普通候选 |
| 官学 | `BUILDING_JNR_MANSION` | 剧院广场 / 2 | 普通候选 |
| 艺术刊社 | `BUILDING_HD_ART_PUBLISHING_HOUSE` | 剧院广场 / 3 | 普通候选 |
| 大酒店 | `BUILDING_JNR_GRAND_HOTEL` | 剧院广场 / 3 | 普通候选 |
| 歌剧院 | `BUILDING_JNR_OPERA` | 剧院广场 / 3 | 普通候选 |
| 艺术博物馆 | `BUILDING_MUSEUM_ART` | 剧院广场 / 3 | 普通候选 |
| 考古博物馆 | `BUILDING_MUSEUM_ARTIFACT` | 剧院广场 / 3 | 普通候选 |
| 广播中心 | `BUILDING_BROADCAST_CENTER` | 剧院广场 / 4 | 普通候选 |
| 电影制片厂 | `BUILDING_FILM_STUDIO` | 剧院广场 / 4 | 特色/特质限制；替代建筑 |
| 媒体中心 | `BUILDING_JNR_MEDIA_CENTER` | 剧院广场 / 4 | 普通候选 |
| 集市 | `BUILDING_FAIR` | 商业中心 / 1 | 普通候选 |
| 货栈 | `BUILDING_JNR_WAYSTATION` | 商业中心 / 1 | 普通候选 |
| 铸币厂 | `BUILDING_JNR_MINT` | 商业中心 / 2 | 普通候选 |
| 市场 | `BUILDING_MARKET` | 商业中心 / 2 | 普通候选 |
| 克拉科夫纺织会馆 | `BUILDING_SUKIENNICE` | 商业中心 / 2 | 特色/特质限制；玩家数量上限 |
| 银行 | `BUILDING_BANK` | 商业中心 / 3 | 普通候选 |
| 大巴扎 | `BUILDING_GRAND_BAZAAR` | 商业中心 / 3 | 特色/特质限制；替代建筑 |
| 工商会馆 | `BUILDING_JNR_GUILDHALL` | 商业中心 / 3 | 普通候选 |
| 商人中心 | `BUILDING_JNR_MERCHANT_QUARTER` | 商业中心 / 3 | 普通候选 |
| 商务写字楼 | `BUILDING_JNR_COMMODITY_EXCHANGE` | 商业中心 / 4 | 普通候选 |
| 市场部 | `BUILDING_JNR_MARKETING_AGENCY` | 商业中心 / 4 | 普通候选 |
| 证券交易所 | `BUILDING_STOCK_EXCHANGE` | 商业中心 / 4 | 普通候选 |
| 水力作坊 | `BUILDING_IZ_WATER_MILL` | 工业区 / 1 | 普通候选 |
| 风车 | `BUILDING_JNR_WIND_MILL` | 工业区 / 1 | 普通候选 |
| 手工工场 | `BUILDING_JNR_MANUFACTURY` | 工业区 / 2 | 普通候选 |
| 建造工坊 | `BUILDING_WORKSHOP` | 工业区 / 2 | 普通候选 |
| 工厂 | `BUILDING_FACTORY` | 工业区 / 3 | 普通候选 |
| 电子厂 | `BUILDING_HD_ELECTRONICS_FACTORY` | 工业区 / 3 | 普通候选 |
| 化工厂 | `BUILDING_JNR_CHEMICAL` | 工业区 / 3 | 普通候选 |
| 燃煤发电厂 | `BUILDING_COAL_POWER_PLANT` | 工业区 / 4 | 普通候选 |
| 燃油发电厂 | `BUILDING_FOSSIL_FUEL_POWER_PLANT` | 工业区 / 4 | 普通候选 |
| 互联网公司 | `BUILDING_HD_INTERNET_COMPANY` | 工业区 / 4 | 普通候选 |
| 物流中心 | `BUILDING_JNR_FREIGHT_YARD` | 工业区 / 4 | 普通候选 |
| 核电站 | `BUILDING_POWER_PLANT` | 工业区 / 4 | 普通候选 |
| 兵营 | `BUILDING_BARRACKS` | 军营 / 1 | 普通候选 |
| 皇家学堂 | `BUILDING_BASILIKOI_PAIDES` | 军营 / 1 | 特色/特质限制；替代建筑 |
| 边关 | `BUILDING_JNR_TARGET_RANGE` | 军营 / 1 | 普通候选 |
| 斡耳朵 | `BUILDING_ORDU` | 军营 / 1 | 特色/特质限制；替代建筑 |
| 马厩 | `BUILDING_STABLE` | 军营 / 1 | 普通候选 |
| 兵工厂 | `BUILDING_ARMORY` | 军营 / 2 | 普通候选 |
| 募兵所 | `BUILDING_JNR_CAVALIER` | 军营 / 2 | 普通候选 |
| 补给站 | `BUILDING_JNR_DEPOT` | 军营 / 2 | 普通候选 |
| 军事政治处 | `BUILDING_JNR_ARSENAL` | 军营 / 3 | 普通候选 |
| 军事研究院 | `BUILDING_JNR_PRISON` | 军营 / 3 | 普通候选 |
| 军事学院 | `BUILDING_MILITARY_ACADEMY` | 军营 / 3 | 普通候选 |
| 祭坛 | `BUILDING_JNR_ALTAR` | 圣地 / 1 | 普通候选 |
| 神社 | `BUILDING_SHRINE` | 圣地 / 1 | 普通候选 |
| 丹房 | `BUILDING_HD_ALCHEMY_ROOM` | 圣地 / 2 | 普通候选 |
| 教堂 | `BUILDING_JNR_MONASTERY` | 圣地 / 2 | 普通候选 |
| 高棉庙堂 | `BUILDING_PRASAT` | 圣地 / 2 | 特色/特质限制；替代建筑 |
| 博尔贡木板教堂 | `BUILDING_STAVE_CHURCH` | 圣地 / 2 | 特色/特质限制；玩家数量上限 |
| 寺庙 | `BUILDING_TEMPLE` | 圣地 / 2 | 普通候选 |
| 大教堂 | `BUILDING_CATHEDRAL` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 拜火神庙 | `BUILDING_DAR_E_MEHR` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 谒师所 | `BUILDING_GURDWARA` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 禅邸 | `BUILDING_JNR_CANDI` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 道观 | `BUILDING_JNR_DAOGUAN` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 神道教神社 | `BUILDING_JNR_JINJA` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 隐修会 | `BUILDING_JNR_KHALWAT` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 印度神庙 | `BUILDING_JNR_MANDIR` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 姆巴里 | `BUILDING_JNR_MBARI` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 柱廊神庙 | `BUILDING_JNR_PERIPTEROS` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 东正教堂 | `BUILDING_JNR_SOBOR` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 羽蛇神庙 | `BUILDING_JNR_TZACUALLI` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 礼拜堂 | `BUILDING_MEETING_HOUSE` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 清真寺 | `BUILDING_MOSQUE` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 藏经阁 | `BUILDING_PAGODA` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 窣堵波 | `BUILDING_STUPA` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 犹太教堂 | `BUILDING_SYNAGOGUE` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 佛寺 | `BUILDING_WAT` | 圣地 / 3 | 默认Faith购买；宗教解锁 |
| 花园 | `BUILDING_JNR_GARDEN` | 圣地 / 4 | 默认Faith购买 |
| 济贫院 | `BUILDING_JNR_HOSPITIUM` | 圣地 / 4 | 默认Faith购买 |
| 渔业码头 | `BUILDING_JNR_LIGHTHOUSE_FISHING` | 港口 / 1 | 普通候选 |
| 贸易码头 | `BUILDING_LIGHTHOUSE` | 港口 / 1 | 普通候选 |
| 军港 | `BUILDING_JNR_ENTREPOT` | 港口 / 2 | 普通候选 |
| 商港 | `BUILDING_JNR_FISH_MARKET` | 港口 / 2 | 普通候选 |
| 造船厂 | `BUILDING_SHIPYARD` | 港口 / 2 | 普通候选 |
| 海军基地 | `BUILDING_JNR_NAVAL_BASE` | 港口 / 3 | 普通候选 |
| 游轮码头 | `BUILDING_JNR_OFFSHORE_TERMINAL` | 港口 / 3 | 普通候选 |
| 海港 | `BUILDING_SEAPORT` | 港口 / 3 | 普通候选 |
| 机场 | `BUILDING_AIRPORT` | 航空港 / 1 | 普通候选 |
| 机库 | `BUILDING_HANGAR` | 航空港 / 1 | 普通候选 |
| 水力纺车 | `BUILDING_HD_HYDRAULIC_SPINNING_WHEEL` | 水渠 / 1 | 普通候选 |
| 浴场 | `BUILDING_JNR_BATHHOUSE` | 水渠 / 1 | 普通候选 |
| 水力锻锤 | `BUILDING_JNR_HAMMER_WORKS` | 水渠 / 1 | 普通候选 |
| 果园 | `BUILDING_JNR_ORCHARD` | 水渠 / 1 | 普通候选 |
| 下水道 | `BUILDING_SEWER` | 水渠 / 2 | 普通候选 |
| 水电站坝 | `BUILDING_HYDROELECTRIC_DAM` | 堤坝 / 1 | 普通候选 |
| 官邸 | `BUILDING_HD_MANSION` | 社区 / 1 | 未设购买币种；玩家数量上限 |
| 别墅 | `BUILDING_HD_VILLA` | 社区 / 1 | 普通候选 |
| 公交站 | `BUILDING_HD_BUS_STOP` | 社区 / 2 | 普通候选 |
| 农贸市场 | `BUILDING_FOOD_MARKET` | 社区 / 3 | 普通候选 |
| 艺术街区 | `BUILDING_JNR_ART_GALLERY` | 社区 / 3 | 玩家数量上限 |
| 中心医院 | `BUILDING_JNR_HOSPITAL` | 社区 / 3 | 玩家数量上限 |
| 房车营地 | `BUILDING_JNR_MEDITATION` | 社区 / 3 | 玩家数量上限 |
| 回收中心 | `BUILDING_JNR_RECYCLING_PLANT` | 社区 / 3 | 玩家数量上限 |
| 客运中心 | `BUILDING_JNR_TRANSIT_HUB` | 社区 / 3 | 玩家数量上限 |
| 百货大楼 | `BUILDING_SHOPPING_MALL` | 社区 / 3 | 普通候选 |
| 竞技场 | `BUILDING_ARENA` | 娱乐中心 / 1 | 普通候选 |
| 勾栏瓦舍 | `BUILDING_JNR_TOURNEY` | 娱乐中心 / 1 | 普通候选 |
| 蹴球场 | `BUILDING_TLACHTLI` | 娱乐中心 / 1 | 特色/特质限制；替代建筑 |
| 沙龙 | `BUILDING_HD_SALON` | 娱乐中心 / 2 | 普通候选 |
| 植物园 | `BUILDING_JNR_BOTANICAL_GARDEN` | 娱乐中心 / 2 | 普通候选 |
| 温泉浴场 | `BUILDING_THERMAL_BATH` | 娱乐中心 / 2 | 特色/特质限制；替代建筑 |
| 动物园 | `BUILDING_ZOO` | 娱乐中心 / 2 | 普通候选 |
| 博览会 | `BUILDING_JNR_THEME_PARK` | 娱乐中心 / 3 | 普通候选 |
| 体育场 | `BUILDING_STADIUM` | 娱乐中心 / 3 | 普通候选 |
| 摩天轮 | `BUILDING_FERRIS_WHEEL` | 水上乐园 / 1 | 普通候选 |
| 音乐游船 | `BUILDING_JNR_MARINA` | 水上乐园 / 1 | 普通候选 |
| 水族馆 | `BUILDING_AQUARIUM` | 水上乐园 / 2 | 普通候选 |
| 游客接待中心 | `BUILDING_JNR_CASINO` | 水上乐园 / 2 | 普通候选 |
| 水上运动中心 | `BUILDING_AQUATICS_CENTER` | 水上乐园 / 3 | 普通候选 |
| 纪念品商店 | `BUILDING_JNR_FOOD_COURT` | 水上乐园 / 3 | 普通候选 |
| 神谕碑 | `BUILDING_GROVE` | 保护区 / 1 | 普通候选 |
| 人文遗产保护部 | `BUILDING_HD_CULTURE_HERITAGE_PRESERVE` | 保护区 / 2 | 普通候选 |
| 自然环境保护部 | `BUILDING_SANCTUARY` | 保护区 / 2 | 普通候选 |
| 地貌生态环保专局 | `BUILDING_HD_LANDFORM_EPO` | 保护区 / 3 | 未设购买币种；玩家数量上限 |
| 不可再生资源管理专局 | `BUILDING_HD_RESOURCE_EPO` | 保护区 / 3 | 未设购买币种；玩家数量上限 |
| 自然名胜旅游专局 | `BUILDING_HD_SCENIC_EPO` | 保护区 / 3 | 未设购买币种；玩家数量上限 |
| 物种多样性维护专局 | `BUILDING_HD_SPECIES_EPO` | 保护区 / 3 | 未设购买币种；玩家数量上限 |
| 埃斯科里亚尔王宫 | `BUILDING_EL_ESCORIAL_PALACE` | 市政广场 / 1 | 未设购买币种；特色/特质限制 |
| 军阀宝座 | `BUILDING_GOV_CONQUEST` | 市政广场 / 1 | 未设购买币种 |
| 谒见厅 | `BUILDING_GOV_TALL` | 市政广场 / 1 | 未设购买币种 |
| 会议堂 | `BUILDING_GOV_WIDE` | 市政广场 / 1 | 未设购买币种 |
| 贸易本埠 | `BUILDING_GOV_CITYSTATES` | 市政广场 / 2 | 未设购买币种 |
| 主教座堂 | `BUILDING_GOV_FAITH` | 市政广场 / 2 | 未设购买币种 |
| 中书省 | `BUILDING_GOV_SPIES` | 市政广场 / 2 | 未设购买币种 |
| 女王图书馆 | `BUILDING_QUEENS_BIBLIOTHEQUE` | 市政广场 / 2 | 未设购买币种；特色/特质限制 |
| 国家历史博物馆 | `BUILDING_GOV_CULTURE` | 市政广场 / 3 | 未设购买币种 |
| 作战部 | `BUILDING_GOV_MILITARY` | 市政广场 / 3 | 未设购买币种 |
| 皇家学会 | `BUILDING_GOV_SCIENCE` | 市政广场 / 3 | 未设购买币种 |
| 领事馆 | `BUILDING_CONSULATE` | 外交区 / 1 | 玩家数量上限 |
| 总领馆 | `BUILDING_CHANCERY` | 外交区 / 2 | 玩家数量上限 |
| 人权理事会 | `BUILDING_HD_HUMAN_RIGHTS_COUNCIL` | 外交区 / 3 | 未设购买币种；玩家数量上限 |
| 国防部 | `BUILDING_HD_MINISTRY_OF_NATIONAL_DEFENSE` | 外交区 / 3 | 未设购买币种；玩家数量上限 |
| 区域议会中心 | `BUILDING_HD_REGIONAL_COUNCIL_CENTER` | 外交区 / 3 | 未设购买币种；玩家数量上限 |
| 世界议会总部 | `BUILDING_HD_WORLD_PARLIAMENT_HEADQUARTERS` | 外交区 / 3 | 未设购买币种；特色/特质限制；替代建筑；玩家数量上限 |
| 中世纪城墙 | `BUILDING_CASTLE` | 市中心 / 0 | Tier0需单独分组；未设购买币种 |
| 会展中心 | `BUILDING_EXHIBITION` | 市中心 / 0 | Tier0需单独分组 |
| 拦海堤 | `BUILDING_FLOOD_BARRIER` | 市中心 / 0 | Tier0需单独分组；未设购买币种 |
| 粮仓 | `BUILDING_GRANARY` | 市中心 / 0 | Tier0需单独分组 |
| 警署 | `BUILDING_HD_POLICE_STATION` | 市中心 / 0 | Tier0需单独分组 |
| 法表 | `BUILDING_HD_TABLES_OF_LAW` | 市中心 / 0 | Tier0需单独分组；玩家数量上限 |
| 纪念碑 | `BUILDING_MONUMENT` | 市中心 / 0 | Tier0需单独分组 |
| 测量仪 | `BUILDING_NILOMETER_HD` | 市中心 / 0 | Tier0需单独分组 |
| 宫殿 | `BUILDING_PALACE` | 市中心 / 0 | Tier0需单独分组；未设购买币种；首都限定；玩家数量上限 |
| 沟渠 | `BUILDING_PALGUM` | 市中心 / 0 | Tier0需单独分组；特色/特质限制；替代建筑 |
| 文艺复兴城墙 | `BUILDING_STAR_FORT` | 市中心 / 0 | Tier0需单独分组；未设购买币种 |
| 堡垒 | `BUILDING_TSIKHE` | 市中心 / 0 | Tier0需单独分组；未设购买币种；特色/特质限制；替代建筑 |
| 远古城墙 | `BUILDING_WALLS` | 市中心 / 0 | Tier0需单独分组；未设购买币种 |
| 磨坊 | `BUILDING_WATER_MILL` | 市中心 / 0 | Tier0需单独分组 |
