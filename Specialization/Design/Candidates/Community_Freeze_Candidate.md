# 社区／大都会：用户提交的强冻结候选

2026-09-28接收。状态 **STRONG FREEZE CANDIDATE**，不升级为DESIGN_FROZEN或实施授权。当前D0035 COMM-001～011保留既有接受来源；下文是新候选及其明确修订方向，不能与旧冲突规则叠加。正式revision迁移尚未执行。当前v0.1仍仅科研、文化、商业、工业。

[完整中文阅读版](../Community.md)。附件SHA256：`8d1894a83bf4295a554af1366753031cf562e39d8ca059c06efbaeb35da37dcf`。下方保留提交原文全部内容。

## 接收审查与来源差异

| 旧正式来源 | 本次候选方向 | 处理 |
|---|---|---|
| COMM-006：III升5F/5P、I有国际移民 | 各级沿用基础支持；III才开启国际移民 | 候选明确取消旧升级/旧开放时点；正文不混用，正式Spec未就地改写 |
| COMM-007：A=H+2M+D+2E，M只取正值 | 移除专家E；宜居度可负；Housing＋Amenities＋Urban Development，精确公式开放 | 不沿用旧权重拼出新公式；负吸引力如何处理进度未定义 |
| COMM-009：三个互斥政策模式 | 两个独立开关，含双关闭组合 | 新正文按独立开关；默认组合、成本/项目方式不能擅自补定 |
| COMM-004第一版排序；COMM-008国际公式 | 排序与世界接触/地图公式均开放 | 旧值仅基线参考，不伪装本次冻结值 |
| 旧Lv2/IV本地能力缺口 | 职住融合、众力营城、都会脉络、城市肌理等完整结构 | 补入候选阅读，不按新能力反推技术实现 |

### 延续、待定与直接依赖

- COMM-001特殊身份候选、锁定优先关系未在新稿解决，保留；未给出的Housing/GPP基础规则不照搬其它专业。
- 两个Development用途分开：相邻单区域→职住融合；全城Urban Development→吸引力。Shared D接入、Gold转换、资格和小数处理均待定，不自动归一化、不套用已实现Research floor。
- 候选将全部数值留给v0.x，但若干项目不只是数值：政策执行方式、排序/同分、分发解锁、四级以前移民追溯、区域/交通资格及跨城共享边归属。保留未定，不在接收阶段要求全部回答，也不因此称核心身份不完整。
- 原文§19“paused or restricted”较宽，§52标OFF；按最终开关表呈现关闭方向，精确是否存在减速模式未授权，不自行新增第三档。旧暂停保留进度、不补算可作为未冲突既有合同列出，和新开关生命周期统一仍需正式收束。
- 众力营城只以Districts＋Buildings为正面范围；普通/特殊建筑、Wonder边界及叠加口径需明确，不能从数据库Building分类推导给Wonder收益。
- Urbanization每条合格共享边只计一次；跨城相邻、City Center/Wonder/施工/掠夺等资格未给定。0.5%为首测值；19/31/44/57边是提交材料估算参考，本轮未做几何证明。
- 国内分流搬运实际人口，不生成Migrant、不造新人口；旧k×L×sqrt(N)生成模型保持退出。外交移民协议按某盟友压力份额的合同保留，但新国际公式最终如何兼容仍待衔接。移除E后娱乐虚拟专家进入吸引力不再属于本候选路径；不扩展其其它功能。
- HD交通分类与专家槽是材料提出的调查方向，本轮未查源码/数据库；无技术PASS。AI/MP/Ownership及保存边界未借本次补造。
- 名称按原文候选程度保留；开放大都会KEEP/preferred，不将整组名称升级LOCKED。国内人口网络正式名称TBD，人口分流目前是开关状态名。

## 用户提交原文

# Community / Metropolis（社区／大都会）— Design Talk

Status:

> **STRONG FREEZE CANDIDATE**
>
> Core identity, Lv1–Lv4 progression, named ability structure, International Immigration, Domestic Population Distribution, Community specialist role, high-density urbanization direction, transportation identity, and policy structure are substantially settled.
>
> Exact coefficients, thresholds, Development mapping, transportation throughput, Amenities-to-Attractiveness curve, and implementation details are intentionally deferred to v0.x prototyping and balance testing.

---

# 1. Specialization Identity

Community / Metropolis is not:

- a simple Population Growth specialization;
- a fertility specialization;
- a Housing specialization;
- a generic specialist-yield specialization.

Its core identity is:

> **Population Hub + Urban Employment + International Immigration + Domestic Population Distribution + High-Density Urbanization + Metropolitan Connectivity**

The fundamental population loop is:

> **Foreign World → Metropolis → Domestic Network → Empire**

International Immigration:

> creates real additional Population for the civilization.

Domestic Population Distribution:

> redistributes existing owned Population from the Metropolis to other domestic cities.

It does **not** create extra Population.

The specialization therefore asks:

> **How does a city become a place where people gather, work, build, move, and eventually form a true metropolis?**

---

# 2. Progression Philosophy

The progression follows the shared presentation rhythm:

> Lv1 — 0 named abilities  
> Lv2 — 1 named ability  
> Lv3 — 2 named abilities  
> Lv4 — 3 named abilities

The institutional and gameplay story is:

> **街区共建**
> → **城区协作**
> → **都会发展**
> → **都会事务统筹**

Conceptually:

> **community formation**
> → **functional integration**
> → **metropolitan growth**
> → **world-metropolis governance**

---

# 3. Institution Chain

## Lv1 — 街区共建会

Status:

> **STRONG CANDIDATE / close to locked**

The Lv1 institution represents residents jointly building, maintaining, and improving the urban neighborhood in which they live.

It is not primarily:

- local political autonomy;
- neighborhood government;
- charity.

Its theme is:

> **people actively participating in the creation and maintenance of urban community life.**

This establishes the spatial and social foundation for later urban development.

---

## Lv2 — 城区协作所

Status:

> **STRONG CANDIDATE / close to locked**

Lv2 represents the point where Community no longer functions only as an internal residential/employment space.

It begins to interact systematically with surrounding urban functions:

- Campus;
- Commercial Hub;
- Industrial Zone;
- Theater Square;
- Holy Site;
- other functional Districts.

The institution therefore represents:

> **coordination between residential/community space and the specialized functions of the surrounding city.**

---

## Lv3 — 都会发展局

Status:

> **STRONG CANDIDATE / close to locked**

Lv3 is the point where the city becomes a true Metropolis.

Its major new characteristics are:

- International Immigration;
- population policy;
- population-scale construction efficiency.

The city is no longer merely locally successful.

It begins to:

> **attract people from the wider world and convert population scale into urban development capacity.**

---

## Lv4 — 都会事务总署

Status:

> **STRONG CANDIDATE / close to locked**

Lv4 represents a mature metropolitan authority managing the city as a complete high-density system.

Its scope includes:

- long-term international population accumulation;
- outward resettlement and expansion;
- transportation completeness;
- domestic population distribution;
- urban form and agglomeration;
- large-scale metropolitan coordination.

“都会事务” is intentionally broad.

Lv4 is not only:

- a transport authority;
- an immigration office;
- an urban planning department.

It is:

> **the integrated institutional form of the mature metropolis.**

---

# 4. Lv1 Foundation — 基础社区支持

Lv1 has no named ability.

Display label:

> **基础社区支持**

Community Specialists should not be interpreted as elite intellectual specialists.

They represent a broad range of modern urban employment:

- white-collar work;
- blue-collar work;
- services;
- administration;
- ordinary urban occupations.

Their gameplay role is:

> **to provide employment for Population that can no longer all be efficiently assigned to high-quality worked tiles.**

---

## Base Specialist Support

Current direction:

> Each actually worked Community Specialist receives approximately:
>
> **+3 Food / +3 Production**

Exact final values remain balance-sensitive.

This support is intended to allow Community employment to approximately support the Population assigned to it.

It does not mean:

> Community Specialists should automatically outperform high-quality worked tiles.

A strong worked tile may remain superior.

Community employment instead provides:

> **large-scale urban job capacity.**

---

# 5. Removed Legacy — No Lv3 5F/5P Escalation

The previous design increased Community Specialist support at Lv3 from:

> +3F/+3P

to:

> +5F/+5P.

This escalation is removed.

Reasons:

1. it originally served narrative progression;
2. it originated from an older cross-specialization specialist template;
3. other expert specializations no longer require the same escalation;
4. it is mechanically uninteresting;
5. Metropolis growth should be represented by new urban systems, not simple specialist stat inflation.

Therefore:

> **Lv1 base support persists; there is no later automatic 5F/5P upgrade.**

---

# 6. Lv2 Ability — 职住融合

Name:

> **职住融合**

Status:

> **STRONG CANDIDATE / close to locked**

Core concept:

> Community employment begins to absorb the functions of the surrounding city.

A Community is not merely residential.

Its Population participates in:

- services;
- support labor;
- administration;
- supply chains;
- secondary employment;
- surrounding professional activities.

---

# 7. 职住融合 — Core Mechanic

Each actually worked Community Specialist receives additional yields based on:

> **the Development / completeness of adjacent functional Districts.**

First prototype:

> **Adjacent District contribution ≈ D × 0.1**

where:

> D = the Development / infrastructure-completeness value of the adjacent District.

Example:

If an adjacent Campus has:

> D = 10

then each worked Community Specialist in that Community receives approximately:

> **+1 Science**

from that Campus.

---

# 8. District Yield Mapping

Conceptual mapping:

- Campus → Science
- Theater Square → Culture
- Industrial Zone → Production
- Commercial Hub → Gold
- Holy Site → Faith
- other functional Districts → their corresponding primary output

Exact:

- Gold conversion;
- special District mapping;
- auxiliary District mapping;
- Development source;
- compatibility with Shared Development definitions;

remain:

> **BALANCE / MAPPING / IMPLEMENTATION REQUIRED**

---

# 9. Multiple Adjacent Districts

Current direction:

> **A Community may benefit from multiple adjacent Districts simultaneously.**

This is intentional.

A Community surrounded by several mature functional Districts should become:

> a highly valuable urban employment center.

The design does not currently impose:

- one-District-only selection;
- a hard total-yield cap;
- a single “dominant District.”

These may be reconsidered only if v0.x testing demonstrates an actual extreme-case problem.

The system should preserve the value of:

> **mixed urban spatial planning.**

---

# 10. Player Choice in Lv2

职住融合 creates an important workforce choice.

The player decides whether Population should:

- work a high-quality physical tile;
- work a Community Specialist slot;
- work another specialist slot.

Community employment value depends on:

> **where the Community is built and what functions surround it.**

This means:

> urban layout and workforce allocation both matter.

A city can shift its emphasis by changing Population assignments without rebuilding the entire city.

---

# 11. Lv3-A — 四海汇聚

Name:

> **四海汇聚**

Status:

> **STRONG CANDIDATE / close to locked**

Lv3 is when the city formally gains:

> **International Immigration**

International Immigration does **not** exist as a normal Lv1 baseline.

This is an intentional redesign.

The story is:

> Lv1 establishes community life.
>
> Lv2 integrates the community with the city’s functional economy.
>
> Lv3 finally becomes developed enough to attract sustained international population movement.

---

# 12. Attractiveness

International Immigration is driven by:

> **City Attractiveness**

Current conceptual inputs:

> **Housing + Amenities + Urban Development**

Community Specialist count is explicitly removed from Attractiveness.

The city attracts people because:

1. there is room to live;
2. quality of life is high;
3. the city itself is developed and offers opportunities.

---

# 13. Removed Attractiveness Input — Community Specialists

The old model included:

> Community Specialist count

as a positive Attractiveness term.

This is removed.

Reason:

> Community Specialists represent ordinary urban employment, not a special elite population that inherently attracts immigrants.

Removing this term also breaks an unnecessary feedback loop:

> Immigration
> → Population
> → more Community Specialists
> → more Attractiveness
> → more Immigration.

Community employment remains valuable through:

- base support;
- 职住融合;
- urban job capacity;

not through immigration attraction.

---

# 14. Housing

Housing contributes to Attractiveness primarily through:

> **available residential capacity**

rather than total Housing alone.

However, Housing is not expected to function as the primary long-term hard cap for a mature Metropolis.

Community and its infrastructure can provide substantial Housing.

Therefore:

> Housing matters, but it is not the final population-control mechanism.

Exact formula remains:

> **BALANCE REQUIRED**

---

# 15. Amenities as Metropolitan Soft Cap

Amenities are expected to become the more important long-term constraint.

High Population:

> increases Amenity demand.

Poor Amenities:

- reduce city-wide economic efficiency;
- should also reduce International Immigration Attractiveness.

The design intentionally prefers:

> **soft population pressure**

over a hard maximum Population cap.

---

## Negative Amenities Contribution

The previous design only allowed positive Amenities to contribute to Attractiveness.

Current direction:

> **Amenities should be allowed to contribute negatively to Attractiveness.**

Conceptually:

- high Amenities → strong positive attraction;
- comfortable city → modest positive attraction;
- neutral conditions → near-zero contribution;
- poor Amenities → negative attraction;
- severe dissatisfaction → strongly suppress Immigration.

The design does **not** currently require:

> a hard “Amenities ≤ X = Immigration disabled” rule.

Instead:

> Attractiveness may naturally fall to zero or below.

Exact curve remains:

> **BALANCE REQUIRED**

---

# 16. Urban Development Input

The city’s overall built development contributes to Attractiveness.

The exact Development formula is intentionally deferred.

The conceptual rule is:

> **completed, functional urban infrastructure attracts population.**

This should reward:

- mature districts;
- buildings;
- employment and services;
- actual developed urban functions.

It should not simply reward:

> empty District shells.

Exact relationship to the shared Development system remains:

> **TBD**

---

# 17. International Immigration Progress

The previous first prototype used a world-contact-based progress model:

> Attractiveness × contacted major civilizations

against a map-scaled threshold.

The exact formula is not frozen.

The important conceptual rules are:

- more attractive Metropolis → faster Immigration;
- broader contact with the world → larger international migration pool;
- larger maps should not automatically produce uncontrolled linear scaling;
- immigration does not deduct Population from a specific foreign AI city;
- no specific foreign origin city needs to be tracked.

International Immigration represents:

> **world-scale migration into the Metropolis.**

---

# 18. Population Policy — Two Independent Switches

Population policy is not a separate named ability.

It is:

> a low-frequency control interface for the International Immigration and Domestic Distribution systems.

There are two independent policy dimensions.

---

# 19. International Immigration Policy

## 开放大都会

Status:

> **KEEP / preferred name**

Effect:

> International Immigration enabled.

Narrative:

> the city is open to continued international settlement.

This name is an important RP anchor and should be preserved.

---

## 限制入境

Effect:

> International Immigration paused or restricted.

Domestic Population Distribution is not automatically disabled.

The city may stop accepting new international population while continuing to redistribute existing excess Population domestically.

---

# 20. Domestic Population Policy

## 人口分流

Effect:

> Domestic Population Distribution enabled.

Population above the protected Metropolis baseline may flow to eligible domestic cities.

---

## 人口留存

Effect:

> Domestic Population Distribution paused.

International Immigration may continue.

Purpose:

> deliberately grow the Metropolis itself.

This can be useful for:

- reaching Population thresholds;
- increasing urban construction efficiency;
- filling job slots;
- unlocking more District capacity;
- strengthening later metropolitan systems.

---

# 21. Policy State Space

The two switches are conceptually independent.

Therefore the system may represent:

1. 开放大都会 + 人口分流
2. 开放大都会 + 人口留存
3. 限制入境 + 人口分流
4. 限制入境 + 人口留存

The final UI does not need to display them as a four-option list.

The important contract is:

> International Immigration and Domestic Distribution are separate controls.

---

# 22. Lv3-B — 众力营城

Name:

> **众力营城**

Status:

> **STRONG CANDIDATE**

Core philosophy:

> **Population scale helps the Metropolis build itself.**

High Population represents:

- labor scale;
- specialization of work;
- larger local markets;
- mature urban services;
- greater construction organization.

---

# 23. 众力营城 — Current Prototype

Use discrete Population tiers.

Current first-test direction:

> **Every 10 Population = 1 Metropolitan Scale tier**

Each tier:

> approximately **+5% Production toward Districts and Buildings**

Examples:

- 10–19 Population → +5%
- 20–29 → +10%
- 30–39 → +15%
- 40–49 → +20%
- 50–59 → +25%

These are:

> **prototype balance values**

not final locked numbers.

---

# 24. Construction Scope

众力营城 applies to:

> **Districts + Buildings**

It does not primarily accelerate:

- Units
- Wonders
- Projects
- Settlers
- Space Race Projects

The purpose is:

> **urban completion**

not universal Production dominance.

This distinction protects Industry’s identity.

---

# 25. Why Metropolis Needs Construction Efficiency

Metropolis has unusually high internal construction demand.

A mature Metropolis wants:

- many functional Districts;
- many Buildings;
- multiple Communities;
- transportation infrastructure;
- dense urban development.

Therefore:

> a moderate construction bonus does not automatically make it a better general Production city than Industry.

It may simply help the city finish:

> the unusually large amount of infrastructure required by its own identity.

---

# 26. Domestic Population Distribution Network

Community / Metropolis has a dedicated domestic Network.

Its role:

> redistribute real Population from the Metropolis to other eligible domestic cities.

It does not create Population.

It does not create Migrant units.

It should not require constant manual city-by-city selection.

---

# 27. Population Distribution Eligibility

A recipient city should generally require:

- valid Network connection / eligibility;
- sufficient Housing;
- acceptable Amenities;
- ability to productively use additional Population.

Candidate prioritization may consider:

- lower Population;
- greater Housing surplus;
- better Amenities;
- other marginal-population-value factors.

Exact sorting remains:

> **TBD**

---

# 28. Protected Population Floor

The Metropolis must retain a protected local Population baseline.

Domestic Distribution only moves:

> Population above that baseline.

This prevents the Network from draining the city into an empty transit hub.

The floor may later depend on:

- specialization level;
- Community infrastructure;
- other metropolitan maturity measures.

Exact values are deferred.

---

# 29. Domestic Distribution Throughput

The Network should not instantaneously move unlimited Population.

A natural migration system should have:

> finite throughput / frequency.

This is especially important because Lv4 transportation will improve that capacity.

The base throughput is not yet defined.

It should not be artificially painful merely to make the transportation ability useful.

Instead:

> population movement should have a reasonable natural pace,
>
> and metropolitan transportation should improve that pace.

---

# 30. Lv4-A — 移民拓居

Name:

> **移民拓居**

Status:

> **STRONG CANDIDATE / close to locked**

Core concept:

> International immigrants gather in the Metropolis, and over time some of that accumulated population becomes capable of establishing new settlements elsewhere.

This is not primarily:

- colonial conquest;
- territorial expansion;
- biological reproduction.

It is:

> **migrants continuing outward to establish new places to live.**

---

# 31. 移民拓居 — Core Mechanic

Successful International Immigrants are accumulated over time.

After reaching a threshold:

> generate a Settler.

Previous prototype:

> **8 International Immigrants → 1 Settler**

This threshold remains:

> **BALANCE REQUIRED**

The generated Settler may be used for:

- founding new cities;
- Specialization investment.

---

# 32. Immigrant Counting

The count is based on:

> successful International Immigration events.

It is not based on:

- current Population remaining in the Metropolis;
- domestic distribution destination;
- net Population growth of the source city.

If an immigrant enters the Metropolis and is later distributed domestically:

> the international immigration event still counts.

Whether Immigration accumulated before ACTIVE IV counts retroactively remains:

> **TBD**

---

# 33. Settler Balance Philosophy

The Settler reward is not currently considered structurally invalid.

The mature Metropolis has already required:

- multiple Settler investments;
- Governor investment;
- infrastructure;
- population management;
- Amenities;
- urban development.

Therefore:

> a strong long-term population return is appropriate.

Whether the threshold is:

- 8;
- 10;
- 12;
- another value;

should be decided through actual v0.x Immigration-rate testing.

No automatic escalating threshold is currently required.

---

# 34. Lv4-B — 都会脉络

Name:

> **都会脉络**

Status:

> **STRONG CANDIDATE / close to locked**

Core theme:

> **a true Metropolis requires a complete transportation system.**

HD already contains a Transport Facility concept / classification that may include:

- Railway infrastructure;
- Airport-related infrastructure;
- Harbor-related infrastructure;
- other recognized transportation facilities.

Exact technical taxonomy must be verified later.

---

# 35. Transportation Completeness

都会脉络 rewards:

> **different transportation types**

rather than repeatedly building the same type.

The goal is:

> completeness, not spam.

Examples conceptually include:

- rail;
- air;
- maritime;
- other valid transportation categories.

Repeated facilities of the same category:

> should not repeatedly increase completeness.

---

# 36. Coastal vs Inland Metropolis

A coastal Metropolis may naturally have access to:

> maritime transportation

in addition to rail and air.

This can be a legitimate geographic advantage.

However:

> an inland Metropolis should not become fundamentally nonfunctional simply because it cannot construct a Harbor.

Exact type eligibility and maximum completeness must therefore respect:

> geographic availability.

---

# 37. 都会脉络 — Reward Direction

Transportation Completeness strengthens:

> **Domestic Population Distribution**

not International Immigration.

Core story:

> better transportation allows the Metropolis to move Population through the domestic urban system more efficiently.

Possible reward dimensions include:

- higher throughput;
- higher frequency;
- more Population per distribution cycle;
- other simple domestic mobility improvements.

Exact implementation:

> **TBD**

---

# 38. Lv4-C — 城市肌理

Name:

> **城市肌理**

Status:

> **STRONG CANDIDATE / close to locked**

This is one of the defining spatial abilities of the specialization.

The goal is not:

> construct one of every District type.

The goal is:

> **create a physically continuous, dense, visibly urbanized city.**

The player should continue building Community even after major functional District categories are already present.

---

# 39. Urbanization

Urbanization is measured through:

> **shared edges between eligible District tiles.**

Each edge shared by two eligible urbanized District tiles:

> contributes 1 Urbanization point.

Each shared edge is counted once.

---

# 40. Why Shared Edges

Shared-edge counting rewards:

> **density**

rather than simple connectivity.

A long thin chain of Districts may be connected but contains relatively few shared edges.

A compact urban block contains:

> many internal shared edges.

Therefore the mechanic encourages:

> **clusters, infill, compact urban fabric.**

---

# 41. Community as Urban Infill

Community is particularly important for 城市肌理.

Even after the city already contains:

- Campus;
- Commercial Hub;
- Industrial Zone;
- Theater Square;
- Entertainment;
- other functional Districts;

the player can continue constructing Community to:

> fill the spaces between them.

A Community placed in a gap may create:

> several new urban shared edges at once.

This gives Community a late-game spatial role beyond:

- Housing;
- employment;
- specialist slots.

It becomes:

> **urban infill.**

---

# 42. Urbanized Tile Scope

Current clean direction:

> primarily count District tiles.

Community / Neighborhood counts.

Transportation Improvements do not need to be forced into the Urbanization metric because:

> transportation already has its own Lv4 ability.

Exact District eligibility remains:

> **MAPPING REQUIRED**

---

# 43. 城市肌理 — Reward Direction

Current first-test direction:

> **Each eligible urban shared edge provides approximately +0.5% city-wide yields.**

This represents:

> **Agglomeration Effects**

such as:

- lower interaction costs;
- more concentrated services;
- easier exchange of labor and goods;
- faster knowledge transfer;
- more efficient urban organization.

The benefit is not intended to be:

> a specific adjacency yield.

It represents:

> **overall metropolitan efficiency.**

---

# 44. All-Yield Direction

Current design preference is:

> **true city-wide yield improvement**

rather than automatically excluding Food or Production.

Food is not currently considered the primary runaway risk.

In mature Metropolis gameplay:

- Community employment approximately consumes much of its own Food support;
- natural Population growth becomes increasingly slow at high Population;
- International Immigration is expected to become the main late-game Population source.

Therefore extra Food primarily helps:

> sustain a large urban Population.

---

# 45. Production — Primary Balance Risk

Production is the main feedback variable requiring later testing.

Potential loop:

> Urbanization
> → Production bonus
> → faster District construction
> → more Urbanization
> → more Production.

This does not automatically invalidate the mechanic.

The reward grows gradually as the city is actually built.

The correct first step is:

> test the coefficient.

If Production feedback is excessive, possible later adjustments include:

- reducing the per-edge coefficient;
- diminishing returns at very high edge counts;
- modifying the eligible yield set.

No pre-emptive exclusion is currently locked.

---

# 46. Current Urbanization Prototype

First-test candidate:

> **+0.5% city-wide yields per shared urban edge**

Approximate dense-layout reference:

- 10 urbanized tiles → around 19 internal edges → ~+9.5%
- 15 tiles → around 31 edges → ~+15.5%
- 20 tiles → around 44 edges → ~+22%
- 25 tiles → around 57 edges → ~+28.5%

Actual maps will usually be less geometrically optimal because of:

- terrain;
- coast;
- mountains;
- resources;
- Wonders;
- placement restrictions;
- tactical planning.

These values are:

> **BALANCE REFERENCE ONLY**

not frozen.

---

# 47. Specialist Economy vs Tile Economy

Metropolis is expected to gradually shift from:

> **tile-heavy labor**

toward:

> **urban specialist employment**

as Population rises.

This does not mean:

> all physical tiles should become inferior.

High-quality:

- Farms;
- Mines;
- Resources;
- unique Improvements;
- other valuable worked tiles;

should remain meaningful.

Community employment becomes important because:

> there are only so many high-quality tiles,
>
> while Population can continue to grow through International Immigration.

---

# 48. Community Marginal Value

A Community may simultaneously provide:

- Housing;
- specialist employment;
- Lv1 base specialist support;
- Lv2 职住融合 yields;
- additional Urbanization edges;
- late-game urban visual continuity.

This is intentional.

However, its total marginal value should eventually be tested against:

> retaining a strong worked tile.

The goal is:

> strong incentive toward urbanization,

not:

> universal elimination of every non-District tile.

---

# 49. International Immigration vs Natural Growth

The mature Metropolis is not expected to rely primarily on Food-based natural Population growth.

At high Population:

> natural growth costs become increasingly large.

International Immigration becomes the more important Population source.

Therefore the player’s population-management problem is not simply:

> maximize Food.

It becomes:

- maintain acceptable Amenities;
- create jobs;
- provide Housing;
- maintain Attractiveness;
- decide when to accept Immigration;
- decide when to retain or distribute Population.

---

# 50. Amenities as Player-Controlled Brake

Because International Immigration can continue supplying Population beyond natural growth limits, the player needs an active brake.

That brake is:

> **population policy + Amenities pressure**

The player can choose:

### 开放大都会
when the city can still productively accept international Population.

### 限制入境
when Amenities, jobs, infrastructure, or urban development cannot support additional intake.

### 人口留存
when the player deliberately wants to strengthen the Metropolis itself.

### 人口分流
when excess Population is more valuable elsewhere in the empire.

The system therefore avoids:

> automatic uncontrolled Population intake.

---

# 51. Current Naming Set

## Lv1 Institution
> **街区共建会**

## Lv1 Foundation
> **基础社区支持**

## Lv2 Institution
> **城区协作所**

## Lv2 Ability
> **职住融合**

## Lv3 Institution
> **都会发展局**

## Lv3-A
> **四海汇聚**

## Lv3-B
> **众力营城**

## Lv4 Institution
> **都会事务总署**

## Lv4-A
> **移民拓居**

## Lv4-B
> **都会脉络**

## Lv4-C
> **城市肌理**

---

# 52. Population Policies

## International Immigration ON
> **开放大都会**

## International Immigration OFF
> **限制入境**

## Domestic Distribution ON
> **人口分流**

## Domestic Distribution OFF
> **人口留存**

These are:

> two independent policy dimensions,

not one four-state named ability.

---

# 53. Network Naming

The formal name of the Domestic Population Distribution Network remains:

> **TBD**

“人口分流” is currently used as the policy-state name.

The Network should therefore likely use a distinct institutional/system name.

Possible future direction may reference:

- domestic population network;
- population circulation;
- metropolitan population network.

No final name is required before v0.x unless needed for UI.

---

# 54. Full Gameplay Story

The complete specialization progression is:

### Lv1 — 街区共建
> Residents establish a functioning urban community and employment base.

### Lv2 — 城区协作
> Community employment begins to participate in the functions of surrounding Districts.

### Lv3 — 都会发展
> The city becomes attractive to international population and begins to convert population scale into faster urban construction.

### Lv4 — 都会事务
> The mature Metropolis becomes a national population hub, transportation center, dense urban organism, and source of new settlement capacity.

---

# 55. Operational Identity

Community / Metropolis gameplay revolves around:

### Place
Where should Community be built relative to functional Districts?

### Employ
Which Population should work high-quality tiles, and which should work urban Community jobs?

### Attract
Is the city attractive enough to justify continued International Immigration?

### Retain
Should new Population remain in the Metropolis?

### Distribute
Should Population flow to other domestic cities?

### Build
Can the growing Population accelerate completion of the urban environment?

### Connect
Has the Metropolis developed a complete transportation system?

### Urbanize
Can Community and other Districts be arranged into a dense, contiguous urban fabric?

---

# 56. Strategic Tensions

The specialization should create several recurring decisions.

## Worked Tile vs Community Employment

A strong tile may provide greater immediate output.

A Community job may provide:

- sustainable urban employment;
- functional adjacency yields;
- Housing;
- later Urbanization value.

---

## Population Retention vs Domestic Distribution

Retaining Population may provide:

- higher construction tier;
- more workers;
- more District capacity;
- more urbanization potential.

Distributing Population may provide:

> stronger empire-wide growth.

---

## Accept Immigration vs Restrict Immigration

Immigration is desirable only while the Metropolis can support:

- Amenities;
- Housing;
- jobs;
- urban infrastructure.

More Population is not automatically always better.

---

## Preserve Productive Land vs Urbanize

Building more Districts and Community may strengthen:

- job capacity;
- urban functions;
- 城市肌理.

But it consumes:

- workable land;
- resources;
- Improvement space;
- alternative spatial opportunities.

---

# 57. Key Design Principle

Community / Metropolis should not become:

> a Population number that automatically generates everything.

Its strength comes from:

> **turning Population into a spatial, economic, and network-management problem.**

Population must be:

- housed;
- employed;
- made comfortable;
- integrated into urban functions;
- retained or distributed;
- supported by transport;
- expressed spatially through the built city.

---

# 58. What the Map Should Look Like

A mature Metropolis should be visually recognizable.

The player should see:

> **a large, dense, contiguous field of Districts and Communities**

rather than:

> a conventional Civ VI city with a few isolated Districts surrounded by unchanged rural tiles.

Community provides:

> a repeatable urban infill tool.

The visual identity of the specialization is therefore:

> **a city that increasingly becomes city.**

---

# 59. Relationship to Other Specializations

## Industry

Industry is about:

> production systems, standardization, construction capability, industrial organization.

Metropolis may accelerate:

> its own Districts and Buildings

through Population scale.

It does not become:

> a universal Production specialization.

---

## Commerce

Commerce is about:

> capital, commercialization, investment, allocation, contracts, restructuring.

Metropolis may produce a strong urban economy, but its identity is:

> Population and urban concentration,

not capital management.

---

## Landscape

Landscape asks:

> how land can remain plural, managed, productive, and protected.

Metropolis asks:

> how land becomes increasingly urbanized and densely organized.

The map identities should visibly diverge:

> managed landscape
>
> vs
>
> dense urban fabric.

---

# 60. Balance Items Deferred to v0.x

The following should **not** be frozen now:

1. Base Community Specialist support exact value.
2. 职住融合 `D × coefficient`.
3. Gold conversion ratio.
4. Eligible adjacent District mappings.
5. Multiple adjacent District stacking behavior if testing exposes extremes.
6. Attractiveness exact formula.
7. Housing contribution.
8. Amenities positive/negative curve.
9. Urban Development contribution.
10. World-contact / map-size Immigration formula.
11. Immigration threshold.
12. Population policy switch cost / project duration.
13. Domestic Distribution frequency.
14. Protected Population Floor.
15. recipient sorting.
16. 众力营城 Population tier size.
17. 众力营城 Production per tier.
18. Settler Immigration threshold.
19. pre-Lv4 Immigration retroactivity.
20. Transport Facility taxonomy.
21. 都会脉络 throughput effect.
22. Urbanized District eligibility.
23. 城市肌理 per-edge coefficient.
24. whether extreme Urbanization requires diminishing returns.
25. whether Production needs special treatment after actual testing.

---

# 61. Implementation Feasibility Questions

Development should later investigate:

- actual Community specialist-slot access;
- dynamic specialist yield modification from adjacent District Development;
- reading Development values efficiently;
- decimal/fractional specialist yield handling;
- dynamic Attractiveness UI;
- International Immigration progress storage;
- actual Population addition/removal;
- population policy state switching;
- finite Domestic Distribution throughput;
- deterministic recipient selection;
- Population transfer between cities;
- Settler generation from accumulated Immigration count;
- Transport Facility classification;
- unique transport-type counting;
- shared District-edge counting;
- city-wide yield modifiers based on dynamic Urbanization;
- event-driven updates rather than expensive constant scanning.

Implementation limitations should be reported back to Design.

They should not silently redefine the gameplay contract.

---

# 62. Current Maturity

## Core Identity
> **SET**

## Progression Story
> **SET / STRONG FREEZE CANDIDATE**

## Institution Chain
> **SUBSTANTIALLY SET**

## Ability Structure
> **SUBSTANTIALLY SET**

## Population Policies
> **SET IN DIRECTION**

## International Immigration
> **SET IN CONCEPT / BALANCE OPEN**

## Domestic Distribution
> **SET IN CONCEPT / THROUGHPUT OPEN**

## Urbanization
> **SET IN CONCEPT / BALANCE OPEN**

## Transportation
> **SET IN CONCEPT / REWARD FORMULA OPEN**

## Numerical Balance
> **DEFERRED TO v0.x**

## Implementation
> **NOT YET VALIDATED**

---

# 63. Current Design Summary

Community / Metropolis now has a coherent identity:

> **build a functioning community, integrate it with surrounding city functions, grow into an international population magnet, use population scale to complete the city, then turn the mature metropolis into a dense, connected population hub for the entire civilization.**

The specialization no longer needs additional abilities.

Remaining work should focus on:

> **prototype implementation, numerical balance, system interaction, and UI clarity**

rather than further expansion of the conceptual design.