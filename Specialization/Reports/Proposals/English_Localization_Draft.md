# English localization candidate

Review draft for B489.516 on develop (`932f875fdb39`). GPT‑6.1 Terra drafted the English. Primary reviewed it against the [Chinese candidate](Chinese_Localization_Draft.md), the [approved English pilot](English_Localization_Sample.md), the loaded text sources, and the [accepted Design](../../Design/Content/README.md). The ten approved pilot values and eight approved institution names are reproduced verbatim.

The 382 proposed text-key changes include 57 missing English entries and 238 entries whose English value contains Chinese. Another 20 existing English values carry forward. The 283 remaining keys belong to developer diagnostics, legacy experiments, or the isolated test civilization. The review includes 167 English renderings for Chinese text written directly in Lua, XML, or the mod listing. Source links identify the loaded baseline. Official Civilopedia history comes from the game.

Institution descriptions open with a short introduction, then list effects and requirements. Use **Active Level** and **Potential Level** for specialization, **tier** for buildings and Construction Crews, and **percentage points** for additions to existing rates. Game icons and dynamic parameters are written in their in-game forms. Paragraph breaks and table line breaks represent `[NEWLINE]`.

## Research institutions · 科研

### Scholarly Circle · 学者结社

[`LOC_SPC_RESEARCH_INSTITUTION_1`](../../../Mod/Text/TestText.sql#L385) · [`LOC_SPC_RESEARCH_INSTITUTION_1_HELP`](../../../Mod/Text/TestText.sql#L387)

```text
Scholars gather here to study and lay the groundwork for the city's research.

Basic Specialist Support:
Each working Research specialist provides +3 [ICON_Food] Food and +3 [ICON_Production] Production.
```

### Institute of Inquiry · 研修院

[`LOC_SPC_RESEARCH_INSTITUTION_2`](../../../Mod/Text/TestText.sql#L389) · [`LOC_SPC_RESEARCH_INSTITUTION_2_HELP`](../../../Mod/Text/TestText.sql#L391)

```text
With places to study and train, scholars make research a lasting pursuit.

Scholarly Training:
[ICON_BULLET] Each working Research specialist provides +2 base [ICON_GreatScientist] Great Scientist points.
[ICON_BULLET] Gain +1 [ICON_Housing] Housing from the Campus and +1 for each tier of eligible buildings it contains.
```

### Research Consortium · 学术联合会

[`LOC_SPC_RESEARCH_INSTITUTION_3`](../../../Mod/Text/TestText.sql#L393) · [`LOC_SPC_RESEARCH_INSTITUTION_3_HELP`](../../../Mod/Text/TestText.sql#L395)

```text
Scholars bring discoveries from different fields into everyday use.

Interdisciplinary Research:
[ICON_BULLET] Gain [ICON_Science] Science equal to 50% of the combined base adjacency yields of this city’s other eligible specialization districts. Only completed, unpillaged districts count.

Applied Learning:
[ICON_BULLET] Each working Research specialist gains yields from this city’s other eligible specialization fields. The yields increase with each field’s infrastructure depth.
```

### Academic Directorate · 学术总署

[`LOC_SPC_RESEARCH_INSTITUTION_4`](../../../Mod/Text/TestText.sql#L397) · [`LOC_SPC_RESEARCH_INSTITUTION_4_HELP`](../../../Mod/Text/TestText.sql#L399)

```text
Well-equipped campuses support deeper inquiry and a lasting tradition of scholarship.

Research Infrastructure:
[ICON_BULLET] Each working Research specialist provides +1 base [ICON_Science] Science per point of infrastructure depth in this city's Campus, up to +10 per specialist.

Academic Stewardship:
[ICON_BULLET] Each working Research specialist adds +1 base [ICON_Science] Science to each eligible, unpillaged tier 1–4 Campus building in this city.

Academic Tradition:
[ICON_BULLET] This city starts building Academic Tradition when its Research Potential reaches Level 4. It continues as long as the city specializes in Research, even while Level 4 is inactive. Progress pauses if the city leaves Research and resumes if it returns.
[ICON_BULLET] With Research active at Level 4, this city gains +5% [ICON_Science] Science, plus 5 percentage points for every 10 accumulated turns at Standard Speed, up to +25%.
```

## Culture institutions · 文化

### Arts Society · 文艺同好会

[`LOC_SPC_CULTURE_INSTITUTION_1`](../../../Mod/Text/TestText.sql#L221) · [`LOC_SPC_CULTURE_INSTITUTION_1_HELP`](../../../Mod/Text/TestText.sql#L229)

```text
Artists and enthusiasts gather here to share their work.

Basic Specialist Support:
[ICON_BULLET] Each working Culture specialist provides +3 [ICON_Food] Food and +3 [ICON_Production] Production.
```

### Patrons’ Guild · 赞助人行会

[`LOC_SPC_CULTURE_INSTITUTION_2`](../../../Mod/Text/TestText.sql#L223) · [`LOC_SPC_CULTURE_INSTITUTION_2_HELP`](../../../Mod/Text/TestText.sql#L231)

```text
Steady patronage and commissions help literature, art, and music flourish.

Arts Patronage:
[ICON_BULLET] This city's Theater Square provides +1 [ICON_Housing] Housing, plus 1 for each tier of eligible buildings it contains. Each tier counts once.
[ICON_BULLET] Each working Culture specialist provides +2 base [ICON_GreatWriter] Great Writer points, +2 base [ICON_GreatArtist] Great Artist points, and +2 base [ICON_GreatMusician] Great Musician points.
```

### Humanities Federation · 人文联合会

[`LOC_SPC_CULTURE_INSTITUTION_3`](../../../Mod/Text/TestText.sql#L225) · [`LOC_SPC_CULTURE_INSTITUTION_3_HELP`](../../../Mod/Text/TestText.sql#L233)

```text
Great Works from many eras find new interpretations and enrich the life of the city.

Dialogue of Eras:
[ICON_BULLET] This project takes 1 full turn of Production. Each city can complete it once per game era. A completion counts toward the era in which the project began.
[ICON_BULLET] On completion, each distinct era represented in the city's eligible collection adds 5 percentage points to its [ICON_Tourism] Tourism bonus for Great Works. The city keeps the accumulated bonus. It applies while Culture is active at Level 3 or higher.

Cultivated Taste:
[ICON_BULLET] Each eligible, unpillaged building gains +1 [ICON_Tourism] Tourism per era represented by the city's current eligible Great Works.
```

### Academy of the Liberal Arts · 博雅总院

[`LOC_SPC_CULTURE_INSTITUTION_4`](../../../Mod/Text/TestText.sql#L227) · [`LOC_SPC_CULTURE_INSTITUTION_4_HELP`](../../../Mod/Text/TestText.sql#L235)

```text
Scholars draw on many fields to reinterpret Great Works and find inspiration in the art and customs of other civilizations.

Extended Meaning:
[ICON_BULLET] Eligible Great Works gain extra yields based on the infrastructure depth of this city's qualifying district types. Theming bonuses apply. Dialogue of Eras boosts only the Great Works' own Tourism. Government Plazas and Diplomatic Quarters currently grant no extra Culture through this ability.

Great Works Inspiration:
[ICON_BULLET] This city gains +3% [ICON_GreatPerson] Great Person points for each era represented in its eligible collection, up to +24%. Only types with base points in this city benefit.

Humanities Expedition:
[ICON_BULLET] Train a Humanities Expedition and send it to a foreign major civilization you have met. Your civilization can have 1 at a time. Each source city earns 1 Cultural Insight the first time each mission type succeeds in a given civilization.
[ICON_BULLET] Eligible Cultural Insights increase the source city's [ICON_Tourism] Tourism. If that city collects all three types from a single civilization, Trade Routes can grant [ICON_Culture] Culture to eligible working specialists in connected cities.
```

## Industry institutions · 工业

### Artisans’ Workshop · 匠作坊

[`LOC_SPC_INDUSTRY_INSTITUTION_1`](../../../Mod/Text/TestText.sql#L247) · [`LOC_SPC_INDUSTRY_INSTITUTION_1_HELP`](../../../Mod/Text/TestText.sql#L248)

```text
Craftspeople gather here to share tools and perfect their trades.

Basic Specialist Support:
[ICON_BULLET] Each working Industry specialist provides +3 [ICON_Food] Food and [ICON_Production] Production equal to the Industrial Zone’s base adjacency bonus.
```

### Guildhall · 百工会馆

[`LOC_SPC_INDUSTRY_INSTITUTION_2`](../../../Mod/Text/TestText.sql#L251) · [`LOC_SPC_INDUSTRY_INSTITUTION_2_HELP`](../../../Mod/Text/TestText.sql#L252)

```text
The city’s trades work together and train new engineers.

Division of Labor:
[ICON_BULLET] Gain +1 [ICON_Housing] Housing from the Industrial Zone and +1 for each tier of eligible buildings it contains. Each tier counts once.
[ICON_BULLET] Each working Industry specialist provides +2 base [ICON_GreatEngineer] Great Engineer points.
```

### Engineering Bureau · 工程局

[`LOC_SPC_INDUSTRY_INSTITUTION_3`](../../../Mod/Text/TestText.sql#L255) · [`LOC_SPC_INDUSTRY_INSTITUTION_3_HELP`](../../../Mod/Text/TestText.sql#L256)

```text
Engineers turn construction experience into standards and organize crews for new projects.

Standardization:
[ICON_BULLET] +10% [ICON_Production] Production toward districts and buildings matching a template. Templates can be shared through Trade Routes. Only the highest bonus applies to a given target.

Construction Crews:
[ICON_BULLET] Unlocks the tier 1–3 Construction Crew projects. While Industry is active at Level 3, each crew costs 150% of its base Production contribution to form. Each source city can support up to 2 crews at a time.
[ICON_BULLET] Consume a crew to contribute [ICON_Production] Production to the Wonder the city is currently building. Excess Production does not carry over.
```

### Directorate of Civil Engineering · 土木工程总局

[`LOC_SPC_INDUSTRY_INSTITUTION_4`](../../../Mod/Text/TestText.sql#L259) · [`LOC_SPC_INDUSTRY_INSTITUTION_4_HELP`](../../../Mod/Text/TestText.sql#L260)

```text
Engineers study the Wonders of the past to inform the great works of today.

Engineering Tradition:
[ICON_BULLET] This city can complete 1 study for each distinct era of Wonders your civilization has built. Count each Wonder's own era. Each study takes 1 full turn of Production.
[ICON_BULLET] While Industry is active at Level 4, each completed study raises the Standardization [ICON_Production] Production bonus and the purchase discount for eligible buildings by 2 percentage points each.

Engineering Practice:
[ICON_BULLET] Unlocks the tier 4 and 5 Construction Crew projects. At 1, 3, and 6 Wonders built in this city, crew costs fall to 140%, 130%, and 120% of their base Production contribution, respectively.

Macro-Engineering:
[ICON_BULLET] +10%, +20%, or +30% [ICON_Production] Production toward Wonders from 1, 2, or at least 3 eras before your civilization’s current era, respectively. This bonus also applies to Construction Crew contributions.
```

## Commerce institutions · 商业

### Merchant Settlement · 商贾聚落

[`LOC_SPC_COMMERCE_INSTITUTION_1`](../../../Mod/Text/Restructuring.sql#L22) · [`LOC_SPC_COMMERCE_INSTITUTION_1_HELP`](../../../Mod/Text/Restructuring.sql#L23)

```text
Merchants gather here and form the city’s first trading community.

Basic Specialist Support:
[ICON_BULLET] Each working Commerce specialist provides +3 [ICON_Food] Food and +3 [ICON_Production] Production.
```

### Merchants’ Guild · 同业公会

[`LOC_SPC_COMMERCE_INSTITUTION_2`](../../../Mod/Text/Restructuring.sql#L24) · [`LOC_SPC_COMMERCE_INSTITUTION_2_HELP`](../../../Mod/Text/Restructuring.sql#L25)

```text
Merchants form guilds and train the next generation of traders.

Trade Associations:
[ICON_BULLET] Each working Commerce specialist provides +2 base [ICON_GreatMerchant] Great Merchant points.
[ICON_BULLET] Gain +1 [ICON_Housing] Housing from the Commercial Hub and +1 for each tier of eligible buildings it contains.
```

### Exchange · 交易所

[`LOC_SPC_COMMERCE_INSTITUTION_3`](../../../Mod/Text/Restructuring.sql#L26) · [`LOC_SPC_COMMERCE_INSTITUTION_3_HELP`](../../../Mod/Text/Restructuring.sql#L27)

```text
Merchants find value across fields and weigh the risks of putting their capital to work.

Commercialization:
[ICON_BULLET] Each working Commerce specialist can commercialize one field for which this city has the corresponding district.
[ICON_BULLET] Earn extra [ICON_Gold] Gold based on the highest yield among this city and your cities of the matching specialization linked by a direct domestic Trade Route. Linked cities qualify even while their specialization is inactive. The Harbor field uses total [ICON_Food] Food. Source yields are retained.

Capital Investment:
[ICON_BULLET] Invest 25% of your Treasury in Research, Culture, or Industry. Each city can hold one unsettled contract per field. Contracts mature after 10 turns at Standard Speed.
[ICON_BULLET] Stable investments return principal and the quoted profit. A successful venture earns three times the stable profit. A failed venture returns 50% of principal, plus any Commercial Reputation bonus.
```

### Capital Trust · 资本信托

[`LOC_SPC_COMMERCE_INSTITUTION_4`](../../../Mod/Text/Restructuring.sql#L28) · [`LOC_SPC_COMMERCE_INSTITUTION_4_HELP`](../../../Mod/Text/Restructuring.sql#L29)

```text
Investors fund new projects along trade routes, give old industries a fresh start, and build a reputation over time.

Development Investment:
[ICON_BULLET] Invest [ICON_Gold] Gold in a city reached by a direct domestic Trade Route from this city. Eligible buildings in the target district receive +50% [ICON_Production] Production. The contract ends when the next eligible building is completed.

Asset Restructuring:
[ICON_BULLET] An Asset Restructuring Team can liquidate assets in one of your specialized cities with Potential at Level 2 or higher. This permanently lowers that city's Potential by 1 level. During restructuring, non-Food yields and [ICON_Food] surplus Food used for growth are reduced by 75%.
[ICON_BULLET] After 5 full turns, use the team to allocate assets in another eligible district in the same city. This consumes the team and changes the city's specialization.

Commercial Reputation:
[ICON_BULLET] Once the Level 4 institution is established, the city earns 1 Reputation per full turn while it specializes in Commerce, up to 40 at Standard Speed. It loses its Reputation if it leaves Commerce.
[ICON_BULLET] While Commerce is active at Level 4, each point of Reputation increases Gold from Commercialization by 0.5% and the share of principal returned after a failed Venture Investment by 0.5 percentage points. At the cap, income is 20% higher and failed Venture Investments return 70% of principal.
```

## Other game text

### Institution labels, city details, and Construction Crew

| Source key | Candidate English |
|---|---|
| [`LOC_PROJECT_SPC_CREW_1000_DESCRIPTION`](../../../Mod/Text/TestText.sql#L51) | Forms a Tier 4 Construction Crew with 1,000 base [ICON_Production] Production at Standard Speed.<br><br>Requires Industry active at Level 4. Cost locks when production starts. Engineering Practice can reduce the cost at Active Level 4. Cost and contribution scale with game speed. Each source city can support up to 2 living Crews for its current owner. |
| [`LOC_PROJECT_SPC_CREW_1000_NAME`](../../../Mod/Text/TestText.sql#L50) | Form Tier 4 Construction Crew |
| [`LOC_PROJECT_SPC_CREW_1360_DESCRIPTION`](../../../Mod/Text/TestText.sql#L59) | Forms a Tier 5 Construction Crew with 1,360 base [ICON_Production] Production at Standard Speed.<br><br>Requires Industry active at Level 4. Cost locks when production starts. Engineering Practice can reduce the cost at Active Level 4. Cost and contribution scale with game speed. Each source city can support up to 2 living Crews for its current owner. |
| [`LOC_PROJECT_SPC_CREW_1360_NAME`](../../../Mod/Text/TestText.sql#L58) | Form Tier 5 Construction Crew |
| [`LOC_PROJECT_SPC_CREW_250_DESCRIPTION`](../../../Mod/Text/TestText.sql#L27) | Forms a Tier 1 Construction Crew with 260 base [ICON_Production] Production at Standard Speed.<br><br>Requires Industry active at Level 3. Cost locks when production starts. Engineering Practice can reduce the cost at Active Level 4. Cost and contribution scale with game speed. Each source city can support up to 2 living Crews for its current owner. |
| [`LOC_PROJECT_SPC_CREW_250_NAME`](../../../Mod/Text/TestText.sql#L26) | Form Tier 1 Construction Crew |
| [`LOC_PROJECT_SPC_CREW_420_DESCRIPTION`](../../../Mod/Text/TestText.sql#L35) | Forms a Tier 2 Construction Crew with 420 base [ICON_Production] Production at Standard Speed.<br><br>Requires Industry active at Level 3. Cost locks when production starts. Engineering Practice can reduce the cost at Active Level 4. Cost and contribution scale with game speed. Each source city can support up to 2 living Crews for its current owner. |
| [`LOC_PROJECT_SPC_CREW_420_NAME`](../../../Mod/Text/TestText.sql#L34) | Form Tier 2 Construction Crew |
| [`LOC_PROJECT_SPC_CREW_750_DESCRIPTION`](../../../Mod/Text/TestText.sql#L43) | Forms a Tier 3 Construction Crew with 750 base [ICON_Production] Production at Standard Speed.<br><br>Requires Industry active at Level 3. Cost locks when production starts. Engineering Practice can reduce the cost at Active Level 4. Cost and contribution scale with game speed. Each source city can support up to 2 living Crews for its current owner. |
| [`LOC_PROJECT_SPC_CREW_750_NAME`](../../../Mod/Text/TestText.sql#L42) | Form Tier 3 Construction Crew |
| [`LOC_SPC_CITY_INSTITUTION_SHORTCUT`](../../../Mod/Text/TestText.sql#L404) | {1} Specialization · Active Level {2}<br>View institutions, districts, buildings, and Wonders. |
| [`LOC_SPC_CREW_BASE_CONFIRM`](../../../Mod/Text/TestText.sql#L303) | Consume this Construction Crew to contribute {1_Input} base [ICON_Production] Production to the Wonder the city is currently building. Applicable bonuses can increase the contribution.<br>This cannot be undone. |
| [`LOC_SPC_CREW_BASE_PREVIEW`](../../../Mod/Text/TestText.sql#L301) | Base capacity: {1_Capacity} [ICON_Production] Production<br>Base contribution: {2_Input}<br>Unused: {3_Unused}<br>Applicable bonuses can increase the contribution. Excess Production does not carry over. |
| [`LOC_SPC_CREW_BASE_READY`](../../../Mod/Text/TestText.sql#L305) | Base capacity: {1_Capacity} [ICON_Production] Production. Applicable bonuses can increase the contribution.<br>Select Construct to preview the contribution. |
| [`LOC_SPC_CREW_FORMATION_ERROR`](../../../Mod/Text/TestText.sql#L290) | Could not confirm Crew formation ({1}). See the Industry report. |
| [`LOC_SPC_CREW_FORMATION_HELP`](../../../Mod/Text/TestText.sql#L286) | Living Crews and unfinished formations share this city’s slots. Resuming a formation keeps its cost and progress. |
| [`LOC_SPC_CREW_LOCKED_PRICE`](../../../Mod/Text/TestText.sql#L297) | Locked cost: {1_Cost} [ICON_Production] Production. Resume to continue from the saved progress. |
| [`LOC_SPC_CREW_OCCUPANCY`](../../../Mod/Text/TestText.sql#L310) | This city’s slots: {1} living Crews, {2} unfinished formations ({3} resumed). |
| [`LOC_SPC_CREW_RESUME_CAPACITY_HELD`](../../../Mod/Text/TestText.sql#L311) | Crew slots are full. Cost and progress are saved. Resume when a slot opens. |
| [`LOC_SPC_CULTURE_INSIGHTS_TOOLTIP`](../../../Mod/Text/TestText.sql#L219) | View recorded and currently effective Cultural Insights for the selected city you own. |
| [`LOC_SPC_INSTITUTION_PREVIEW`](../../../Mod/Text/TestText.sql#L318) | Not yet established |
| [`LOC_SPC_INST_ACCUMULATION_PAUSED`](../../../Mod/Text/TestText.sql#L342) | Accumulation paused. History retained. |
| [`LOC_SPC_INST_ACTIVE_HELP`](../../../Mod/Text/TestText.sql#L364) | This institution is active. Individual abilities may have additional requirements. |
| [`LOC_SPC_INST_ACTIVE_PENDING`](../../../Mod/Text/TestText.sql#L358) | Active Level awaiting confirmation |
| [`LOC_SPC_INST_CATEGORY`](../../../Mod/Text/TestText.sql#L371) | {1} Specialization · Level {2} Institution |
| [`LOC_SPC_INST_COMMERCE`](../../../Mod/Text/TestText.sql#L383) | Commerce |
| [`LOC_SPC_INST_CULTURE`](../../../Mod/Text/TestText.sql#L379) | Culture |
| [`LOC_SPC_INST_DIALOGUE`](../../../Mod/Text/TestText.sql#L324) | Dialogue of Eras |
| [`LOC_SPC_INST_DIALOGUE_VALUE`](../../../Mod/Text/TestText.sql#L346) | Accumulated bonus: +{1}% [ICON_Tourism] Tourism from Great Works. |
| [`LOC_SPC_INST_ENGINEERING`](../../../Mod/Text/TestText.sql#L328) | Engineering Tradition |
| [`LOC_SPC_INST_ENGINEERING_VALUE`](../../../Mod/Text/TestText.sql#L350) | Completed study levels: {1}<br>At Active Level 4, the [ICON_Production] Standardization bonus and eligible building [ICON_Gold] Gold discount each gain {2} percentage points. |
| [`LOC_SPC_INST_EXPEDITION`](../../../Mod/Text/TestText.sql#L326) | Humanities Expedition |
| [`LOC_SPC_INST_INACTIVE_HELP`](../../../Mod/Text/TestText.sql#L366) | This institution is established. Its abilities require a higher Active Level. |
| [`LOC_SPC_INST_INDUSTRY`](../../../Mod/Text/TestText.sql#L381) | Industry |
| [`LOC_SPC_INST_INSIGHTS_VALUE`](../../../Mod/Text/TestText.sql#L348) | Cultural Insights: {1} |
| [`LOC_SPC_INST_LEGACY_HELP`](../../../Mod/Text/TestText.sql#L360) | A historical institution from a former specialization. Its abilities are not active. |
| [`LOC_SPC_INST_NOT_STARTED`](../../../Mod/Text/TestText.sql#L336) | Accumulation has not started |
| [`LOC_SPC_INST_PENDING`](../../../Mod/Text/TestText.sql#L332) | Value awaiting confirmation |
| [`LOC_SPC_INST_PENDING_SHORT`](../../../Mod/Text/TestText.sql#L334) | Pending |
| [`LOC_SPC_INST_PREVIEW_HELP`](../../../Mod/Text/TestText.sql#L362) | Established at Potential Level {1}. |
| [`LOC_SPC_INST_REPUTATION`](../../../Mod/Text/TestText.sql#L322) | Commercial Reputation |
| [`LOC_SPC_INST_REPUTATION_VALUE`](../../../Mod/Text/TestText.sql#L344) | Accumulated Reputation {1}/40. [ICON_Gold] Commercialization bonus +{2}%. |
| [`LOC_SPC_INST_REQUIREMENT`](../../../Mod/Text/TestText.sql#L373) | Requires {1} active at Level {2}. |
| [`LOC_SPC_INST_RESEARCH`](../../../Mod/Text/TestText.sql#L377) | Research |
| [`LOC_SPC_INST_STANDARDIZATION`](../../../Mod/Text/TestText.sql#L330) | Standardization |
| [`LOC_SPC_INST_STANDARDIZATION_PAUSED`](../../../Mod/Text/TestText.sql#L356) | This city does not currently provide Standardization bonuses. Recorded templates are retained. |
| [`LOC_SPC_INST_STANDARDIZATION_VALUE`](../../../Mod/Text/TestText.sql#L354) | Matching templates: +{1}% [ICON_Production] Production<br>Eligible buildings: {2}% [ICON_Gold] Gold discount. |
| [`LOC_SPC_INST_STATE`](../../../Mod/Text/TestText.sql#L375) | Current status: {1} |
| [`LOC_SPC_INST_TEMPLATES_VALUE`](../../../Mod/Text/TestText.sql#L352) | Templates recorded: {1} buildings, {2} districts. |
| [`LOC_SPC_INST_TRADITION`](../../../Mod/Text/TestText.sql#L320) | Academic Tradition |
| [`LOC_SPC_INST_TRADITION_NEXT`](../../../Mod/Text/TestText.sql#L340) | {1} turns until the next threshold. |
| [`LOC_SPC_INST_TRADITION_VALUE`](../../../Mod/Text/TestText.sql#L338) | Accumulated turns: {1}<br>Academic Tradition: +{2}% [ICON_Science] Science in this city. |
| [`LOC_SPC_LV4_CULTURE_PERCENT_NAME`](../../../Mod/Text/TestText.sql#L67) | Level 4 Specialist Culture Bonus |
| [`LOC_SPC_LV4_RESEARCH_PERCENT_NAME`](../../../Mod/Text/TestText.sql#L63) | Level 4 Specialist Science Bonus |
| [`LOC_UNIT_SPC_CREW_1000_DESCRIPTION`](../../../Mod/Text/TestText.sql#L49) | Use once on the tile of a Wonder the city is building. Contributes 1,000 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.<br><br>Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility. |
| [`LOC_UNIT_SPC_CREW_1000_NAME`](../../../Mod/Text/TestText.sql#L48) | Tier 4 Construction Crew |
| [`LOC_UNIT_SPC_CREW_1360_DESCRIPTION`](../../../Mod/Text/TestText.sql#L57) | Use once on the tile of a Wonder the city is building. Contributes 1,360 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.<br><br>Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility. |
| [`LOC_UNIT_SPC_CREW_1360_NAME`](../../../Mod/Text/TestText.sql#L56) | Tier 5 Construction Crew |
| [`LOC_UNIT_SPC_CREW_250_DESCRIPTION`](../../../Mod/Text/TestText.sql#L18) | Use once on the tile of a Wonder the city is building. Contributes 260 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.<br><br>Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility. |
| [`LOC_UNIT_SPC_CREW_250_NAME`](../../../Mod/Text/TestText.sql#L17) | Tier 1 Construction Crew |
| [`LOC_UNIT_SPC_CREW_420_DESCRIPTION`](../../../Mod/Text/TestText.sql#L33) | Use once on the tile of a Wonder the city is building. Contributes 420 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.<br><br>Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility. |
| [`LOC_UNIT_SPC_CREW_420_NAME`](../../../Mod/Text/TestText.sql#L32) | Tier 2 Construction Crew |
| [`LOC_UNIT_SPC_CREW_750_DESCRIPTION`](../../../Mod/Text/TestText.sql#L41) | Use once on the tile of a Wonder the city is building. Contributes 750 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.<br><br>Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility. |
| [`LOC_UNIT_SPC_CREW_750_NAME`](../../../Mod/Text/TestText.sql#L40) | Tier 3 Construction Crew |

### Asset Restructuring Team and actions

| Source key | Candidate English |
|---|---|
| [`LOC_SPC_INSTITUTION_LEGACY`](../../../Mod/Text/Restructuring.sql#L12) | Historical Institution |
| [`LOC_SPC_REST_CONFIGURE`](../../../Mod/Text/Restructuring.sql#L6) | Allocate Assets |
| [`LOC_SPC_REST_CONFIRM`](../../../Mod/Text/Restructuring.sql#L7) | Confirm {1_Name} |
| [`LOC_SPC_REST_CURRENT_SITE`](../../../Mod/Text/Restructuring.sql#L15) | Move the team to the completed, unpillaged district corresponding to the target city’s current specialization. |
| [`LOC_SPC_REST_LIQUIDATE`](../../../Mod/Text/Restructuring.sql#L5) | Liquidate Assets |
| [`LOC_SPC_REST_MOVE`](../../../Mod/Text/Restructuring.sql#L10) | Liquidation: move the team to the district corresponding to the current specialization of a city with at least Level 2 potential.<br>Allocation: move the team to another eligible specialization district in the same city. |
| [`LOC_SPC_REST_OTHER_SITE`](../../../Mod/Text/Restructuring.sql#L16) | Move the team to another eligible specialization district in the same city. |
| [`LOC_SPC_REST_PENDING`](../../../Mod/Text/Restructuring.sql#L11) | The action or team is awaiting confirmation. Keep the logs and do not confirm again. |
| [`LOC_SPC_REST_PHASE`](../../../Mod/Text/Restructuring.sql#L4) | Restructuring |
| [`LOC_SPC_REST_POTENTIAL_GATE`](../../../Mod/Text/Restructuring.sql#L18) | Requires a target city with Potential Level 2 or higher and no pending Settler investment. |
| [`LOC_SPC_REST_PREVIEW`](../../../Mod/Text/Restructuring.sql#L8) | Target city: {1_City}<br>Potential after liquidation: Level {2_Potential}<br><br>Liquidation permanently removes 1 Level of Potential. During restructuring, non-Food yields and surplus [ICON_Food] Food for growth fall by 75%.<br><br>After 5 full turns, use Allocate Assets in another eligible specialization district in this city. This consumes the team and completes restructuring. |
| [`LOC_SPC_REST_SAME_CITY`](../../../Mod/Text/Restructuring.sql#L17) | Allocate assets in the city where you liquidated them. |
| [`LOC_SPC_REST_TEAM`](../../../Mod/Text/Restructuring.sql#L2) | Asset Restructuring Team |
| [`LOC_SPC_REST_TEAM_HELP`](../../../Mod/Text/Restructuring.sql#L3) | Use this team to change the specialization of one of your cities with at least Potential Level 2.<br><br>Liquidate Assets in the city’s current specialization district to permanently lose 1 Level of Potential. After 5 full turns, use Allocate Assets in another eligible specialization district in the same city. This consumes the team. Each former specialization retains history according to its own rules.<br><br>Trained with [ICON_Production] Production in a city with Commerce active at Level 4. The team retreats from enemies and cannot be captured. |
| [`LOC_SPC_REST_WAIT`](../../../Mod/Text/Restructuring.sql#L9) | Bound city: {1_City}<br>Current Potential: Level {2_Potential}<br>Wait {3_Turns} more full turns before choosing Allocate Assets. The city remains in restructuring until you do. |
| [`LOC_SPC_REST_WAIT_GATE`](../../../Mod/Text/Restructuring.sql#L14) | At least 5 full turns must pass first. |

### Commercialization and Capital Investment

| Source key | Candidate English |
|---|---|
| [`LOC_SPC_CAPITAL_ACTUAL_DEBIT`](../../../Mod/Text/Commerce.sql#L185) | Gold paid: {1} [ICON_Gold] |
| [`LOC_SPC_CAPITAL_AVAILABLE`](../../../Mod/Text/Commerce.sql#L183) | Quote available |
| [`LOC_SPC_CAPITAL_BACK`](../../../Mod/Text/Commerce.sql#L184) | Back |
| [`LOC_SPC_CAPITAL_BALANCE`](../../../Mod/Text/Commerce.sql#L89) | Treasury: {1} [ICON_Gold] |
| [`LOC_SPC_CAPITAL_BASIS_TITLE`](../../../Mod/Text/Commerce.sql#L175) | Quote Basis |
| [`LOC_SPC_CAPITAL_BELOW_SAFE`](../../../Mod/Text/Commerce.sql#L102) | This venture has a lower expected profit than the stable investment. |
| [`LOC_SPC_CAPITAL_CLOSE`](../../../Mod/Text/Commerce.sql#L88) | Close |
| [`LOC_SPC_CAPITAL_CONFIRM_STABLE`](../../../Mod/Text/Commerce.sql#L108) | Confirm Stable Investment |
| [`LOC_SPC_CAPITAL_CONFIRM_VENTURE`](../../../Mod/Text/Commerce.sql#L109) | Confirm Venture Investment |
| [`LOC_SPC_CAPITAL_CONTRACT`](../../../Mod/Text/Commerce.sql#L104) | Contract status: {1}<br>Principal: {2} [ICON_Gold]<br>Maturity: Turn {3} |
| [`LOC_SPC_CAPITAL_CONTRACT_MODE`](../../../Mod/Text/Commerce.sql#L186) | Investment type: {1} |
| [`LOC_SPC_CAPITAL_CONTRACT_PENDING`](../../../Mod/Text/Commerce.sql#L182) | Contract awaiting verification |
| [`LOC_SPC_CAPITAL_CULTURE`](../../../Mod/Text/Commerce.sql#L91) | Culture |
| [`LOC_SPC_CAPITAL_CURRENT_TITLE`](../../../Mod/Text/Commerce.sql#L176) | Current Contract |
| [`LOC_SPC_CAPITAL_DETAIL_TITLE`](../../../Mod/Text/Commerce.sql#L172) | Capital Investment Details |
| [`LOC_SPC_CAPITAL_ERROR`](../../../Mod/Text/Commerce.sql#L114) | Unavailable: {1} |
| [`LOC_SPC_CAPITAL_FUNDAMENTALS`](../../../Mod/Text/Commerce.sql#L97) | Infrastructure depth: {1}<br>Specialization strength: {2}<br>Commercialization modifier: {3}<br>Profit rate: {4}% |
| [`LOC_SPC_CAPITAL_HELP`](../../../Mod/Text/Commerce.sql#L111) | Each city can hold one unsettled contract per field. Each new quote uses the remaining Treasury.<br><br>Signing locks the terms and the venture outcome. If the investing city or the quoted strength source changes hands while the contract is open, it ends and any invested Gold is lost. |
| [`LOC_SPC_CAPITAL_INDUSTRY`](../../../Mod/Text/Commerce.sql#L92) | Industry |
| [`LOC_SPC_CAPITAL_INVESTING`](../../../Mod/Text/Commerce.sql#L181) | Investing |
| [`LOC_SPC_CAPITAL_LOCKED_TERMS`](../../../Mod/Text/Commerce.sql#L105) | Infrastructure depth: {1}<br>Specialization strength: {2}<br>Commercialization modifier: {3}<br>Strength source at signing: {4} |
| [`LOC_SPC_CAPITAL_MODE_STABLE`](../../../Mod/Text/Commerce.sql#L177) | Stable Investment |
| [`LOC_SPC_CAPITAL_MODE_TITLE`](../../../Mod/Text/Commerce.sql#L171) | Investment Type |
| [`LOC_SPC_CAPITAL_MODE_VENTURE`](../../../Mod/Text/Commerce.sql#L178) | Venture Investment |
| [`LOC_SPC_CAPITAL_NEGATIVE_EV`](../../../Mod/Text/Commerce.sql#L101) | This venture has a negative expected net return. You can still invest. |
| [`LOC_SPC_CAPITAL_NO_CONTRACT`](../../../Mod/Text/Commerce.sql#L103) | No contract in this field. |
| [`LOC_SPC_CAPITAL_NO_SOURCE`](../../../Mod/Text/Commerce.sql#L96) | No eligible source. Uses a specialization strength of 1. |
| [`LOC_SPC_CAPITAL_OPEN_HELP`](../../../Mod/Text/Commerce.sql#L87) | Make a stable or venture investment without using the city’s Production queue. |
| [`LOC_SPC_CAPITAL_PAUSE_CALLING`](../../../Mod/Text/Commerce.sql#L125) | The payment record could not be confirmed. No Gold was charged. Keep the logs. |
| [`LOC_SPC_CAPITAL_PAUSE_CREDIT`](../../../Mod/Text/Commerce.sql#L128) | Settlement is awaiting confirmation. The return or its receipt could not be verified. |
| [`LOC_SPC_CAPITAL_PAUSE_DEBIT`](../../../Mod/Text/Commerce.sql#L126) | The Gold payment is awaiting confirmation. Do not confirm again. |
| [`LOC_SPC_CAPITAL_PAUSE_INTENT`](../../../Mod/Text/Commerce.sql#L124) | The contract could not be saved. No Gold was charged. |
| [`LOC_SPC_CAPITAL_PAUSE_RECEIPT`](../../../Mod/Text/Commerce.sql#L127) | Payment was attempted. The contract receipt is awaiting confirmation. Do not confirm again. |
| [`LOC_SPC_CAPITAL_PAUSE_STATE`](../../../Mod/Text/Commerce.sql#L129) | The saved contract is awaiting confirmation. Refreshing the quote does not charge Gold again. |
| [`LOC_SPC_CAPITAL_PRINCIPAL`](../../../Mod/Text/Commerce.sql#L98) | Principal: {1} [ICON_Gold] (25% of the Treasury)<br>Term: 10 turns · Matures on turn {2} |
| [`LOC_SPC_CAPITAL_QUOTE_TITLE`](../../../Mod/Text/Commerce.sql#L173) | Quote and Investment |
| [`LOC_SPC_CAPITAL_REFRESH`](../../../Mod/Text/Commerce.sql#L110) | Refresh Quote |
| [`LOC_SPC_CAPITAL_REQUEST_WAIT`](../../../Mod/Text/Commerce.sql#L113) | Confirming… |
| [`LOC_SPC_CAPITAL_RESEARCH`](../../../Mod/Text/Commerce.sql#L90) | Research |
| [`LOC_SPC_CAPITAL_RESULT_FAILURE`](../../../Mod/Text/Commerce.sql#L119) | Venture Failed |
| [`LOC_SPC_CAPITAL_RESULT_SUCCESS`](../../../Mod/Text/Commerce.sql#L118) | Venture Succeeded |
| [`LOC_SPC_CAPITAL_RETURNS_TITLE`](../../../Mod/Text/Commerce.sql#L174) | Returns and Risk |
| [`LOC_SPC_CAPITAL_SETTLED`](../../../Mod/Text/Commerce.sql#L106) | Total returned: {1} [ICON_Gold]<br>Net return: {2} |
| [`LOC_SPC_CAPITAL_SOURCE`](../../../Mod/Text/Commerce.sql#L94) | Strength source: {1} · Active Level {2} |
| [`LOC_SPC_CAPITAL_SOURCE_NONE`](../../../Mod/Text/Commerce.sql#L95) | No eligible source |
| [`LOC_SPC_CAPITAL_STABLE_BRIEF`](../../../Mod/Text/Commerce.sql#L204) | Return at maturity: {1} [ICON_Gold] |
| [`LOC_SPC_CAPITAL_STABLE_DETAIL`](../../../Mod/Text/Commerce.sql#L99) | Return at maturity: {1} [ICON_Gold]<br>Profit: +{2} |
| [`LOC_SPC_CAPITAL_STABLE_SUMMARY`](../../../Mod/Text/Commerce.sql#L179) | Returns the principal and quoted profit at maturity. |
| [`LOC_SPC_CAPITAL_SUBJECT`](../../../Mod/Text/Commerce.sql#L93) | Investment field: {1} |
| [`LOC_SPC_CAPITAL_TERMINATED`](../../../Mod/Text/Commerce.sql#L107) | Contract terminated. Any Gold already paid is lost. |
| [`LOC_SPC_CAPITAL_TITLE`](../../../Mod/Text/Commerce.sql#L86) | Capital Investment |
| [`LOC_SPC_CAPITAL_VENTURE_BRIEF`](../../../Mod/Text/Commerce.sql#L205) | Success chance: {1}%<br>Return if successful: {2} [ICON_Gold]<br>Return if unsuccessful: {3} [ICON_Gold] |
| [`LOC_SPC_CAPITAL_VENTURE_DETAIL`](../../../Mod/Text/Commerce.sql#L100) | Success chance: {1}%<br>Return if successful: {2} [ICON_Gold]<br>Return if unsuccessful: {3} [ICON_Gold]<br>Expected total return: {4}<br>Expected net return: {5} |
| [`LOC_SPC_CAPITAL_VENTURE_SUMMARY`](../../../Mod/Text/Commerce.sql#L180) | A successful venture earns three times the stable profit. On failure, you recover part of the principal. |
| [`LOC_SPC_CAPITAL_WAITING`](../../../Mod/Text/Commerce.sql#L112) | Waiting for the quote… |
| [`LOC_SPC_COMMERCE_BACK`](../../../Mod/Text/Commerce.sql#L150) | Back to Fields |
| [`LOC_SPC_COMMERCE_BINDING_WAIT`](../../../Mod/Text/Commerce.sql#L73) | Waiting to confirm the city before applying yields. |
| [`LOC_SPC_COMMERCE_CLOSE`](../../../Mod/Text/Commerce.sql#L4) | Close |
| [`LOC_SPC_COMMERCE_DETAIL_TITLE`](../../../Mod/Text/Commerce.sql#L135) | Commercialization Details |
| [`LOC_SPC_COMMERCE_DISABLE`](../../../Mod/Text/Commerce.sql#L17) | Disable |
| [`LOC_SPC_COMMERCE_DOMAIN_CAMPUS`](../../../Mod/Text/Commerce.sql#L11) | Campus · [ICON_Science] Science |
| [`LOC_SPC_COMMERCE_DOMAIN_DETAIL`](../../../Mod/Text/Commerce.sql#L9) | Infrastructure depth: {1}<br>Source yield: {2}<br>Base [ICON_Gold] Gold: {3} → {4} after rounding down |
| [`LOC_SPC_COMMERCE_DOMAIN_HARBOR`](../../../Mod/Text/Commerce.sql#L15) | Harbor · [ICON_Food] Food |
| [`LOC_SPC_COMMERCE_DOMAIN_HOLY_SITE`](../../../Mod/Text/Commerce.sql#L14) | Holy Site · [ICON_Faith] Faith |
| [`LOC_SPC_COMMERCE_DOMAIN_INDUSTRIAL_ZONE`](../../../Mod/Text/Commerce.sql#L13) | Industrial Zone · [ICON_Production] Production |
| [`LOC_SPC_COMMERCE_DOMAIN_THEATER`](../../../Mod/Text/Commerce.sql#L12) | Theater Square · [ICON_Culture] Culture |
| [`LOC_SPC_COMMERCE_EFFECTIVE`](../../../Mod/Text/Commerce.sql#L19) | Active |
| [`LOC_SPC_COMMERCE_EMPTY`](../../../Mod/Text/Commerce.sql#L23) | No field selected |
| [`LOC_SPC_COMMERCE_ENABLE`](../../../Mod/Text/Commerce.sql#L16) | Enable |
| [`LOC_SPC_COMMERCE_ERROR`](../../../Mod/Text/Commerce.sql#L25) | Unavailable: {1} |
| [`LOC_SPC_COMMERCE_FORMULA`](../../../Mod/Text/Commerce.sql#L8) | Base [ICON_Gold] Gold per field = 0.05 × this city’s infrastructure depth × highest eligible source yield × (1 + 0.005 × effective Reputation). Round each field down, then add the results.<br><br>The source is this city or a city of the matching specialization linked by a direct domestic Trade Route. Harbors use total [ICON_Food] Food. The game’s Gold modifiers apply to the total. |
| [`LOC_SPC_COMMERCE_INACTIVE`](../../../Mod/Text/Commerce.sql#L27) | Requires Commerce active at Level 3. |
| [`LOC_SPC_COMMERCE_LIFO_HELP`](../../../Mod/Text/Commerce.sql#L24) | If specialist slots fall, the most recently enabled fields pause first. They resume in the order you enabled them as slots return. Stop a field to remove it. Leaving Commerce or a change of city ownership clears the selection. |
| [`LOC_SPC_COMMERCE_LOCAL_DISTRICT_REQUIRED`](../../../Mod/Text/Commerce.sql#L77) | Requires the corresponding district in this city. |
| [`LOC_SPC_COMMERCE_NETWORK_WAIT`](../../../Mod/Text/Commerce.sql#L30) | Waiting to verify Trade Routes. |
| [`LOC_SPC_COMMERCE_NOT_SELECTED`](../../../Mod/Text/Commerce.sql#L29) | Not enabled |
| [`LOC_SPC_COMMERCE_NO_SOURCE`](../../../Mod/Text/Commerce.sql#L79) | Source yield unavailable while this field is inactive or awaiting confirmation. |
| [`LOC_SPC_COMMERCE_NO_WORKERS`](../../../Mod/Text/Commerce.sql#L28) | Not enough working Commerce specialists. Newer fields pause first. |
| [`LOC_SPC_COMMERCE_OPEN_HELP`](../../../Mod/Text/Commerce.sql#L5) | Commercialize fields for which this city has the matching district. Each working Commerce specialist supports one field. Uses no Production turns. |
| [`LOC_SPC_COMMERCE_PICK_DOMAIN`](../../../Mod/Text/Commerce.sql#L145) | Select a field. |
| [`LOC_SPC_COMMERCE_READBACK_UNKNOWN`](../../../Mod/Text/Commerce.sql#L71) | Awaiting confirmation |
| [`LOC_SPC_COMMERCE_REPUTATION`](../../../Mod/Text/Commerce.sql#L7) | Commercial Reputation: {1}/40 · Effective: {2} |
| [`LOC_SPC_COMMERCE_REPUTATION_NOT_STARTED`](../../../Mod/Text/Commerce.sql#L32) | The Level 4 Commerce institution has not yet been established. |
| [`LOC_SPC_COMMERCE_REPUTATION_UNKNOWN`](../../../Mod/Text/Commerce.sql#L31) | The start of Commercial Reputation could not be confirmed. |
| [`LOC_SPC_COMMERCE_REQUEST_WAIT`](../../../Mod/Text/Commerce.sql#L26) | Confirming selection |
| [`LOC_SPC_COMMERCE_RULES_TITLE`](../../../Mod/Text/Commerce.sql#L138) | Operating Conditions |
| [`LOC_SPC_COMMERCE_RUNNING`](../../../Mod/Text/Commerce.sql#L148) | Commercializing |
| [`LOC_SPC_COMMERCE_SELECTED`](../../../Mod/Text/Commerce.sql#L18) | Selected |
| [`LOC_SPC_COMMERCE_SELECTED_PAUSED`](../../../Mod/Text/Commerce.sql#L149) | Enabled · Paused |
| [`LOC_SPC_COMMERCE_SIDEBAR_CAPACITY`](../../../Mod/Text/Commerce.sql#L134) | Active fields: {1} / {2} |
| [`LOC_SPC_COMMERCE_SOURCE`](../../../Mod/Text/Commerce.sql#L10) | Current source: {1} |
| [`LOC_SPC_COMMERCE_SOURCE_AFTER_ENABLE`](../../../Mod/Text/Commerce.sql#L144) | The source and yield appear when the field becomes active. |
| [`LOC_SPC_COMMERCE_SOURCE_DETAIL`](../../../Mod/Text/Commerce.sql#L143) | Source city: {1}<br>Total source yield: {2}<br>Local infrastructure depth: {3}<br>Effective Commercial Reputation: {4} |
| [`LOC_SPC_COMMERCE_SOURCE_IDENTITY_UNKNOWN`](../../../Mod/Text/Commerce.sql#L81) | Source city specialization is awaiting confirmation |
| [`LOC_SPC_COMMERCE_SOURCE_TITLE`](../../../Mod/Text/Commerce.sql#L137) | Yield Source |
| [`LOC_SPC_COMMERCE_START`](../../../Mod/Text/Commerce.sql#L146) | Start Commercialization |
| [`LOC_SPC_COMMERCE_STATUS`](../../../Mod/Text/Commerce.sql#L33) | Current Status |
| [`LOC_SPC_COMMERCE_STATUS_TITLE`](../../../Mod/Text/Commerce.sql#L139) | Current Status |
| [`LOC_SPC_COMMERCE_STOP`](../../../Mod/Text/Commerce.sql#L147) | Stop Commercialization |
| [`LOC_SPC_COMMERCE_SUMMARY`](../../../Mod/Text/Commerce.sql#L6) | Active fields: {1}/{2} · Selected: {3}<br>Base [ICON_Gold] Gold: +{4} |
| [`LOC_SPC_COMMERCE_SUSPENDED`](../../../Mod/Text/Commerce.sql#L20) | Paused (selection retained) |
| [`LOC_SPC_COMMERCE_TITLE`](../../../Mod/Text/Commerce.sql#L3) | Commercialization / Commercial Reputation |
| [`LOC_SPC_COMMERCE_TOTAL`](../../../Mod/Text/Commerce.sql#L34) | Total Base Gold |
| [`LOC_SPC_COMMERCE_UNAVAILABLE`](../../../Mod/Text/Commerce.sql#L21) | Currently unavailable |
| [`LOC_SPC_COMMERCE_VALUE_AFTER_ENABLE`](../../../Mod/Text/Commerce.sql#L142) | Yield appears when the field becomes active. |
| [`LOC_SPC_COMMERCE_VALUE_DETAIL`](../../../Mod/Text/Commerce.sql#L140) | Base [ICON_Gold] Gold from this field: +{1}<br>Before rounding: {2}<br>Total after rounding each field down: +{3}<br>The city’s Gold modifiers apply to the total. |
| [`LOC_SPC_COMMERCE_VALUE_PAUSED`](../../../Mod/Text/Commerce.sql#L141) | This field will resume in its original order when it qualifies again. |
| [`LOC_SPC_COMMERCE_VALUE_TITLE`](../../../Mod/Text/Commerce.sql#L136) | Commercialization Yield |
| [`LOC_SPC_COMMERCE_WAITING`](../../../Mod/Text/Commerce.sql#L22) | Waiting for yields to be confirmed. |
| [`LOC_SPC_COMMERCE_WRITE_UNCONFIRMED`](../../../Mod/Text/Commerce.sql#L69) | The new yield is awaiting confirmation.<br>Base [ICON_Gold] Gold currently read from the city: {1} |

### Development Investment

| Source key | Candidate English |
|---|---|
| [`LOC_SPC_DEVELOPMENT_ACTIVE_REQUIRED`](../../../Mod/Text/DevelopmentInvestment.sql#L14) | Requires Commerce active at Level 4 in this city. |
| [`LOC_SPC_DEVELOPMENT_BACK`](../../../Mod/Text/DevelopmentInvestment.sql#L50) | Back |
| [`LOC_SPC_DEVELOPMENT_BALANCE`](../../../Mod/Text/DevelopmentInvestment.sql#L7) | Treasury: {1} [ICON_Gold]  Slots used: {2} / {3} |
| [`LOC_SPC_DEVELOPMENT_CAPACITY`](../../../Mod/Text/DevelopmentInvestment.sql#L58) | Slots used: {1} / {2} |
| [`LOC_SPC_DEVELOPMENT_CAPACITY_FULL`](../../../Mod/Text/DevelopmentInvestment.sql#L15) | All working specialist slots are in use. Existing contracts continue. |
| [`LOC_SPC_DEVELOPMENT_CITIES`](../../../Mod/Text/DevelopmentInvestment.sql#L38) | Target Cities |
| [`LOC_SPC_DEVELOPMENT_CITY_ID`](../../../Mod/Text/DevelopmentInvestment.sql#L8) | City #{1} |
| [`LOC_SPC_DEVELOPMENT_CITY_OPTIONS`](../../../Mod/Text/DevelopmentInvestment.sql#L43) | {1} districts available for investment |
| [`LOC_SPC_DEVELOPMENT_CLOSE`](../../../Mod/Text/DevelopmentInvestment.sql#L4) | Close |
| [`LOC_SPC_DEVELOPMENT_CONFIRM`](../../../Mod/Text/DevelopmentInvestment.sql#L5) | Confirm Development Investment |
| [`LOC_SPC_DEVELOPMENT_CONTRACT`](../../../Mod/Text/DevelopmentInvestment.sql#L12) | Contract status: {1}<br>Approved investment: {2} [ICON_Gold]<br>Gold paid: {3} [ICON_Gold] |
| [`LOC_SPC_DEVELOPMENT_CONTRACT_TITLE`](../../../Mod/Text/DevelopmentInvestment.sql#L48) | Most Recent Contract |
| [`LOC_SPC_DEVELOPMENT_CURRENT_TITLE`](../../../Mod/Text/DevelopmentInvestment.sql#L68) | Current Contract |
| [`LOC_SPC_DEVELOPMENT_DETAILS`](../../../Mod/Text/DevelopmentInvestment.sql#L40) | Investment Details |
| [`LOC_SPC_DEVELOPMENT_DISTRICTS`](../../../Mod/Text/DevelopmentInvestment.sql#L39) | Target Districts |
| [`LOC_SPC_DEVELOPMENT_DISTRICT_READY`](../../../Mod/Text/DevelopmentInvestment.sql#L44) | Available · {1} [ICON_Gold] |
| [`LOC_SPC_DEVELOPMENT_EFFECT_TITLE`](../../../Mod/Text/DevelopmentInvestment.sql#L46) | Effect and Completion |
| [`LOC_SPC_DEVELOPMENT_HELP`](../../../Mod/Text/DevelopmentInvestment.sql#L13) | Signing requires Commerce active at Level 4, a free working Commerce specialist slot, and a direct domestic Trade Route from this city to the target.<br><br>Existing contracts continue if the route, specialists, or Active Level changes. If either city changes hands, the contract ends immediately and any Gold paid is lost. |
| [`LOC_SPC_DEVELOPMENT_INVESTING`](../../../Mod/Text/DevelopmentInvestment.sql#L63) | Investing |
| [`LOC_SPC_DEVELOPMENT_MONEY_HELD`](../../../Mod/Text/DevelopmentInvestment.sql#L25) | The Gold payment is awaiting confirmation. Keep the logs and do not confirm again. |
| [`LOC_SPC_DEVELOPMENT_NETWORK_PENDING`](../../../Mod/Text/DevelopmentInvestment.sql#L19) | Verifying Trade Routes from this city… |
| [`LOC_SPC_DEVELOPMENT_NO_BUILDING`](../../../Mod/Text/DevelopmentInvestment.sql#L17) | This district has no eligible next-tier building available. |
| [`LOC_SPC_DEVELOPMENT_NO_CONTRACT`](../../../Mod/Text/DevelopmentInvestment.sql#L69) | The selected district has no current contract. |
| [`LOC_SPC_DEVELOPMENT_NO_DISTRICTS`](../../../Mod/Text/DevelopmentInvestment.sql#L52) | No districts are currently available for investment. |
| [`LOC_SPC_DEVELOPMENT_NO_GOLD`](../../../Mod/Text/DevelopmentInvestment.sql#L22) | Insufficient Gold |
| [`LOC_SPC_DEVELOPMENT_NO_OPTIONS`](../../../Mod/Text/DevelopmentInvestment.sql#L51) | No target cities are currently available. Check the requirements or refresh the quote. |
| [`LOC_SPC_DEVELOPMENT_NO_OUTGOING`](../../../Mod/Text/DevelopmentInvestment.sql#L18) | No direct domestic Trade Routes from this city to your other cities. |
| [`LOC_SPC_DEVELOPMENT_NO_QUOTE`](../../../Mod/Text/DevelopmentInvestment.sql#L59) | No quote is available. Check the contract status or refresh the quote. |
| [`LOC_SPC_DEVELOPMENT_OCCUPIED`](../../../Mod/Text/DevelopmentInvestment.sql#L16) | The target city already has an active Development Investment. |
| [`LOC_SPC_DEVELOPMENT_OPEN_HELP`](../../../Mod/Text/DevelopmentInvestment.sql#L3) | Invest along an outgoing domestic Trade Route to grant +50% [ICON_Production] Production toward eligible buildings in the target district. |
| [`LOC_SPC_DEVELOPMENT_PRICE_UNKNOWN`](../../../Mod/Text/DevelopmentInvestment.sql#L20) | Could not verify the purchase price. A contract is unavailable for this district. |
| [`LOC_SPC_DEVELOPMENT_QUOTE`](../../../Mod/Text/DevelopmentInvestment.sql#L10) | Reference building: {1}<br>Lowest theoretical purchase price: {2} [ICON_Gold]<br>Investment cost (15%): {3} [ICON_Gold] (same-tier candidates: {4}) |
| [`LOC_SPC_DEVELOPMENT_QUOTE_TITLE`](../../../Mod/Text/DevelopmentInvestment.sql#L45) | Quote and Investment |
| [`LOC_SPC_DEVELOPMENT_QUOTE_VALUES`](../../../Mod/Text/DevelopmentInvestment.sql#L64) | Lowest theoretical purchase price: {1} [ICON_Gold]<br>Investment (15%): {2} [ICON_Gold]<br>Same-tier candidates: {3} |
| [`LOC_SPC_DEVELOPMENT_REFRESH`](../../../Mod/Text/DevelopmentInvestment.sql#L6) | Refresh Quote |
| [`LOC_SPC_DEVELOPMENT_RULES_TITLE`](../../../Mod/Text/DevelopmentInvestment.sql#L47) | Signing and Continuation |
| [`LOC_SPC_DEVELOPMENT_SELECT`](../../../Mod/Text/DevelopmentInvestment.sql#L9) | Select a target city and district |
| [`LOC_SPC_DEVELOPMENT_SELECT_CITY`](../../../Mod/Text/DevelopmentInvestment.sql#L41) | Select a target city |
| [`LOC_SPC_DEVELOPMENT_SELECT_DISTRICT`](../../../Mod/Text/DevelopmentInvestment.sql#L42) | Select a target district |
| [`LOC_SPC_DEVELOPMENT_SOURCE`](../../../Mod/Text/DevelopmentInvestment.sql#L49) | Source city: {1} |
| [`LOC_SPC_DEVELOPMENT_SPEED`](../../../Mod/Text/DevelopmentInvestment.sql#L24) | Development Investment requires Standard Speed. |
| [`LOC_SPC_DEVELOPMENT_STALE`](../../../Mod/Text/DevelopmentInvestment.sql#L21) | Requirements or prices changed. Refresh the quote before confirming. |
| [`LOC_SPC_DEVELOPMENT_STATE_ACTIVE`](../../../Mod/Text/DevelopmentInvestment.sql#L30) | Active |
| [`LOC_SPC_DEVELOPMENT_STATE_COMPLETED`](../../../Mod/Text/DevelopmentInvestment.sql#L31) | Completed |
| [`LOC_SPC_DEVELOPMENT_STATE_DEBIT_CALLING`](../../../Mod/Text/DevelopmentInvestment.sql#L29) | Payment awaiting confirmation |
| [`LOC_SPC_DEVELOPMENT_STATE_DEBIT_INTENT`](../../../Mod/Text/DevelopmentInvestment.sql#L28) | Confirming |
| [`LOC_SPC_DEVELOPMENT_STATE_HELD`](../../../Mod/Text/DevelopmentInvestment.sql#L26) | On hold |
| [`LOC_SPC_DEVELOPMENT_STATE_TERMINATED`](../../../Mod/Text/DevelopmentInvestment.sql#L32) | Terminated |
| [`LOC_SPC_DEVELOPMENT_STATE_UNKNOWN`](../../../Mod/Text/DevelopmentInvestment.sql#L34) | Status cannot currently be confirmed: {1} |
| [`LOC_SPC_DEVELOPMENT_STATUS_TITLE`](../../../Mod/Text/DevelopmentInvestment.sql#L53) | Current Status |
| [`LOC_SPC_DEVELOPMENT_TERMS`](../../../Mod/Text/DevelopmentInvestment.sql#L11) | +50% [ICON_Production] Production toward eligible buildings in the target district. This bonus adds to Standardization.<br><br>The contract ends when the next eligible building in the district is finished, whether built, bought with [ICON_Gold] Gold, or completed another way. It can be a different building from the one in the quote.<br>The contract stays in place if the city switches production. |
| [`LOC_SPC_DEVELOPMENT_TITLE`](../../../Mod/Text/DevelopmentInvestment.sql#L2) | Development Investment |
| [`LOC_SPC_DEVELOPMENT_TREASURY`](../../../Mod/Text/DevelopmentInvestment.sql#L57) | Treasury: {1} [ICON_Gold] |
| [`LOC_SPC_DEVELOPMENT_WAITING`](../../../Mod/Text/DevelopmentInvestment.sql#L27) | Checking contract… |
| [`LOC_SPC_DEVELOPMENT_WORKERS_UNKNOWN`](../../../Mod/Text/DevelopmentInvestment.sql#L23) | Waiting to confirm Commerce specialist slots. |

### Specialization claim projects

| Source key | Candidate English |
|---|---|
| [`LOC_PROJECT_SPC_CLAIM_COMMERCE_DESCRIPTION`](../../../Mod/Text/ClaimProjects.sql#L7) | Establishes Commerce specialization at Potential Level 1 in this city. The other claim projects are removed.<br><br>Keep this as the only item in the Production queue for 1 full turn. Saving and loading preserves the timer. Switching targets starts the timer over when you select the project again. Unassigned [ICON_Production] Production and Production earned during this project do not carry over. |
| [`LOC_PROJECT_SPC_CLAIM_COMMERCE_NAME`](../../../Mod/Text/ClaimProjects.sql#L7) | Claim Commerce Specialization |
| [`LOC_PROJECT_SPC_CLAIM_CULTURE_DESCRIPTION`](../../../Mod/Text/ClaimProjects.sql#L3) | Establishes Culture specialization at Potential Level 1 in this city. The other claim projects are removed.<br><br>Keep this as the only item in the Production queue for 1 full turn. Saving and loading preserves the timer. Switching targets starts the timer over when you select the project again. Unassigned [ICON_Production] Production and Production earned during this project do not carry over. |
| [`LOC_PROJECT_SPC_CLAIM_CULTURE_NAME`](../../../Mod/Text/ClaimProjects.sql#L3) | Claim Culture Specialization |
| [`LOC_PROJECT_SPC_CLAIM_INDUSTRY_DESCRIPTION`](../../../Mod/Text/ClaimProjects.sql#L5) | Establishes Industry specialization at Potential Level 1 in this city. The other claim projects are removed.<br><br>Keep this as the only item in the Production queue for 1 full turn. Saving and loading preserves the timer. Switching targets starts the timer over when you select the project again. Unassigned [ICON_Production] Production and Production earned during this project do not carry over. |
| [`LOC_PROJECT_SPC_CLAIM_INDUSTRY_NAME`](../../../Mod/Text/ClaimProjects.sql#L5) | Claim Industry Specialization |
| [`LOC_PROJECT_SPC_CLAIM_RESEARCH_DESCRIPTION`](../../../Mod/Text/ClaimProjects.sql#L1) | Establishes Research specialization at Potential Level 1 in this city. The other claim projects are removed.<br><br>Keep this as the only item in the Production queue for 1 full turn. Saving and loading preserves the timer. Switching targets starts the timer over when you select the project again. Unassigned [ICON_Production] Production and Production earned during this project do not carry over. |
| [`LOC_PROJECT_SPC_CLAIM_RESEARCH_NAME`](../../../Mod/Text/ClaimProjects.sql#L1) | Claim Research Specialization |

### Dialogue of Eras

| Source key | Candidate English |
|---|---|
| [`LOC_PROJECT_SPC_ERA_DIALOGUE_DESCRIPTION`](../../../Mod/Text/DialogueProjects.sql#L4) | Permanently adds 5 percentage points to this city's [ICON_Tourism] Tourism bonus for Great Works for each distinct era in its eligible collection. The bonus applies while Culture is active at Level 3 or higher.<br><br>Requires Culture active at Level 3. Keep this as the only item in the Production queue for 1 full turn. Each city can complete it once per game era, counted from the start of the project.<br><br>Interrupting the project leaves that era’s opportunity available. Unassigned [ICON_Production] Production and Production earned during the project do not carry over. |
| [`LOC_PROJECT_SPC_ERA_DIALOGUE_NAME`](../../../Mod/Text/DialogueProjects.sql#L2) | Dialogue of Eras |
| [`LOC_SPC_DIALOGUE_CARRIER_HINT`](../../../Mod/Text/DialogueProjects.sql#L10) | View this city's completed eras, accumulated Tourism bonus, and current activation status. Either mouse button opens a read-only report. |
| [`LOC_SPC_DIALOGUE_PROJECT_REPORT`](../../../Mod/Text/DialogueProjects.sql#L6) | Dialogue of Eras |

### Engineering Tradition Study

| Source key | Candidate English |
|---|---|
| [`LOC_PROJECT_SPC_ENGINEERING_STUDY_DESCRIPTION`](../../../Mod/Text/EngineeringStudy.sql#L5) | Gain 1 permanent study level in this city. At Industry Active Level 4, each level adds 2 percentage points to Standardization’s [ICON_Production] Production bonus and purchase discount for eligible buildings.<br><br>Requires Industry active at Level 4. This city can complete one study for each distinct era of Wonders your civilization built. Keep this as the only item in the Production queue for 1 full turn.<br><br>Interrupting the project, losing eligibility, or a change of city ownership cancels this attempt. Completed studies are retained. Unassigned Production and Production earned during the project do not carry over. |
| [`LOC_PROJECT_SPC_ENGINEERING_STUDY_NAME`](../../../Mod/Text/EngineeringStudy.sql#L3) | Engineering Tradition Study |

### Humanities Expedition

| Source key | Candidate English |
|---|---|
| [`LOC_SPC_EXPEDITION_GATE_CLOSE`](../../../Mod/Text/ExpeditionGate.sql#L5) | Close |
| [`LOC_SPC_EXPEDITION_GATE_NO_TARGET`](../../../Mod/Text/ExpeditionGate.sql#L13) | No destinations available. |
| [`LOC_SPC_EXPEDITION_GATE_OPEN`](../../../Mod/Text/ExpeditionGate.sql#L3) | Expedition Verification |
| [`LOC_SPC_EXPEDITION_IDLE_DENIED`](../../../Mod/Text/ExpeditionGate.sql#L716) | This action is currently unavailable. |
| [`LOC_SPC_EXPEDITION_IDLE_READ_ERROR`](../../../Mod/Text/ExpeditionGate.sql#L720) | Could not read available actions. Wait for the unit’s status to update. |
| [`LOC_SPC_EXPEDITION_IDLE_UNAVAILABLE`](../../../Mod/Text/ExpeditionGate.sql#L718) | Waiting to confirm available actions. |
| [`LOC_SPC_EXPEDITION_SPY_ACTION_TRAVEL`](../../../Mod/Text/ExpeditionGate.sql#L437) | Travel to a New City |
| [`LOC_SPC_EXPEDITION_SPY_ACTION_UNAVAILABLE`](../../../Mod/Text/ExpeditionGate.sql#L441) | This action is unavailable for the selected Expedition or destination. |
| [`LOC_SPC_EXPEDITION_SPY_ACTIVITY_ASLEEP`](../../../Mod/Text/ExpeditionGate.sql#L344) | Mission in progress. The team becomes available when it finishes. |
| [`LOC_SPC_EXPEDITION_SPY_ACTIVITY_BLOCKED`](../../../Mod/Text/ExpeditionGate.sql#L350) | The mission is paused. Keep the Expedition Verification report. |
| [`LOC_SPC_EXPEDITION_SPY_ACTIVITY_RECOVER`](../../../Mod/Text/ExpeditionGate.sql#L546) | Checking the Expedition after loading… |
| [`LOC_SPC_EXPEDITION_SPY_ACTIVITY_START_DECLINED`](../../../Mod/Text/ExpeditionGate.sql#L710) | The Expedition could not enter its mission state. The mission did not start and no Cultural Insight was awarded. |
| [`LOC_SPC_EXPEDITION_SPY_ACTIVITY_START_EXPIRED`](../../../Mod/Text/ExpeditionGate.sql#L709) | Mission start was not confirmed. No opportunity was used and no Cultural Insight was awarded. Select a mission again. |
| [`LOC_SPC_EXPEDITION_SPY_ACTIVITY_WAIT`](../../../Mod/Text/ExpeditionGate.sql#L354) | Wait for the current mission to finish. |
| [`LOC_SPC_EXPEDITION_SPY_BOUND_REQUIRED`](../../../Mod/Text/ExpeditionGate.sql#L215) | The source city is awaiting confirmation. Travel is unavailable. |
| [`LOC_SPC_EXPEDITION_SPY_DESCRIPTION`](../../../Mod/Text/ExpeditionGate.sql#L167) | Send this unit to a foreign major civilization you have met. The first success of each mission type in that civilization earns 1 Cultural Insight for its source city.<br><br>Uses 1 Spy slot. The unit carries out expedition missions only. |
| [`LOC_SPC_EXPEDITION_SPY_MANAGE`](../../../Mod/Text/ExpeditionGate.sql#L236) | Manage Expedition |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_DONE`](../../../Mod/Text/ExpeditionGate.sql#L632) | Already completed for this source city and civilization |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_FACTS_UNKNOWN`](../../../Mod/Text/ExpeditionGate.sql#L643) | The target is awaiting confirmation. Eligibility has not changed and no Cultural Insight was awarded by this check. |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_PEOPLE_NAME`](../../../Mod/Text/ExpeditionGate.sql#L618) | Survey Local Customs |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_PEOPLE_TOOLTIP`](../../../Mod/Text/ExpeditionGate.sql#L624) | Study the civilization’s customs in its current capital under its control.<br><br>The first successful survey earns 1 Cultural Insight for the source city. Each source city can complete it once per civilization. |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_PLACES_TOOLTIP`](../../../Mod/Text/ExpeditionGate.sql#L628) | Visit a city of this civilization with a completed Wonder.<br><br>The first successful pilgrimage earns 1 Cultural Insight for the source city. Each source city can complete it once per civilization. |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_TARGET_UNKNOWN`](../../../Mod/Text/ExpeditionGate.sql#L647) | Target awaiting confirmation |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_UNAVAILABLE`](../../../Mod/Text/ExpeditionGate.sql#L636) | This mission is unavailable here or has already been completed. |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_WORKS_NAME`](../../../Mod/Text/ExpeditionGate.sql#L620) | Study Great Works |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_WORKS_TOOLTIP`](../../../Mod/Text/ExpeditionGate.sql#L626) | Visit a city of this civilization with an eligible Great Work. Its Great Works stay in place.<br><br>The first successful study earns 1 Cultural Insight for the source city. Each source city can complete it once per civilization. |
| [`LOC_SPC_EXPEDITION_SPY_NAME_CONFIRMING`](../../../Mod/Text/ExpeditionGate.sql#L590) | Confirming the Expedition’s name and source city… |
| [`LOC_SPC_EXPEDITION_SPY_NAME_NOT_OBSERVED`](../../../Mod/Text/ExpeditionGate.sql#L584) | The Expedition’s identity is awaiting confirmation. |
| [`LOC_SPC_EXPEDITION_SPY_NAME_NOT_STARTED`](../../../Mod/Text/ExpeditionGate.sql#L582) | Could not start the Expedition’s identity check. Keep the report. |
| [`LOC_SPC_EXPEDITION_SPY_NAME_PENDING`](../../../Mod/Text/ExpeditionGate.sql#L573) | Identity awaiting confirmation: {1_Reason}. The source and slot are reserved. |
| [`LOC_SPC_EXPEDITION_SPY_NAME_READING`](../../../Mod/Text/ExpeditionGate.sql#L586) | Checking the Expedition’s name… |
| [`LOC_SPC_EXPEDITION_SPY_NAME_REASON_ACK`](../../../Mod/Text/ExpeditionGate.sql#L600) | source binding awaiting confirmation |
| [`LOC_SPC_EXPEDITION_SPY_NAME_REASON_OBSERVER`](../../../Mod/Text/ExpeditionGate.sql#L606) | identity check failed |
| [`LOC_SPC_EXPEDITION_SPY_NAME_REASON_OFFMAP`](../../../Mod/Text/ExpeditionGate.sql#L598) | cannot check the names of Spies in transit |
| [`LOC_SPC_EXPEDITION_SPY_NAME_REASON_READ`](../../../Mod/Text/ExpeditionGate.sql#L604) | could not read the Expedition’s name |
| [`LOC_SPC_EXPEDITION_SPY_NAME_REASON_RETRIES`](../../../Mod/Text/ExpeditionGate.sql#L602) | identity check has stopped |
| [`LOC_SPC_EXPEDITION_SPY_NAME_REASON_UNASSIGNED`](../../../Mod/Text/ExpeditionGate.sql#L594) | name not yet assigned |
| [`LOC_SPC_EXPEDITION_SPY_NAME_REASON_UNIT`](../../../Mod/Text/ExpeditionGate.sql#L596) | new Expedition not yet visible |
| [`LOC_SPC_EXPEDITION_SPY_NAME_RETRY_WAIT`](../../../Mod/Text/ExpeditionGate.sql#L592) | Identity awaiting confirmation: {1_Reason}. Reselect the Expedition or wait until next turn. The source and slot are reserved. |
| [`LOC_SPC_EXPEDITION_SPY_NAME_STOPPED`](../../../Mod/Text/ExpeditionGate.sql#L577) | Identity could not be confirmed: {1_Reason}. Keep the report. The Expedition still occupies its slot. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_DESTINATION`](../../../Mod/Text/ExpeditionGate.sql#L457) | Current city or destination: {1} |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_CREATION`](../../../Mod/Text/ExpeditionGate.sql#L513) | The Expedition is paused because ordinary Spy status could not be verified. See Expedition Verification in P0. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_NATIVE`](../../../Mod/Text/ExpeditionGate.sql#L517) | Travel was rejected or has not been confirmed. Do not submit again. See Expedition Verification in P0. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_TARGET`](../../../Mod/Text/ExpeditionGate.sql#L515) | The destination changed or could not be confirmed. Open the destination list again. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_FAILURE_UNKNOWN`](../../../Mod/Text/ExpeditionGate.sql#L519) | The Expedition is paused or the action failed. Keep the Expedition Verification report. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_LOCATIONS_INCOMPLETE`](../../../Mod/Text/ExpeditionGate.sql#L537) | Locations awaiting confirmation |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_LOCATIONS_INCOMPLETE_TT`](../../../Mod/Text/ExpeditionGate.sql#L539) | Confirmed locations are shown here. Other locations are still being checked. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_MISSION_PREVIEW`](../../../Mod/Text/ExpeditionGate.sql#L529) | Mission Preview |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_NAME_UNKNOWN`](../../../Mod/Text/ExpeditionGate.sql#L461) | Unconfirmed |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_ONE_SHOT`](../../../Mod/Text/ExpeditionGate.sql#L463) | The mission has ended. Once the Expedition is ready, choose another available mission here or travel to a new city. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_ARRIVED`](../../../Mod/Text/ExpeditionGate.sql#L467) | Status: Arrived |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_CREATED`](../../../Mod/Text/ExpeditionGate.sql#L465) | Status: Ready to travel |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_ENDED`](../../../Mod/Text/ExpeditionGate.sql#L481) | Status: Expedition ended |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_ENDING`](../../../Mod/Text/ExpeditionGate.sql#L479) | Status: Ending |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_HELD`](../../../Mod/Text/ExpeditionGate.sql#L477) | Status: Paused, awaiting confirmation |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_TASK_COMPLETE`](../../../Mod/Text/ExpeditionGate.sql#L475) | Status: Mission ended |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_TASK_PREPARING`](../../../Mod/Text/ExpeditionGate.sql#L471) | Status: Preparing mission |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_TASK_RUNNING`](../../../Mod/Text/ExpeditionGate.sql#L473) | Status: Mission in progress |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PHASE_TRAVELLING`](../../../Mod/Text/ExpeditionGate.sql#L469) | Status: Traveling |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_PREFLIGHT_UNKNOWN`](../../../Mod/Text/ExpeditionGate.sql#L511) | The Expedition or destination could not be verified. No travel request was sent. Reopen the destination list. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_REMAINING`](../../../Mod/Text/ExpeditionGate.sql#L459) | Turns remaining: {1} |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_SELECTION_CHANGED`](../../../Mod/Text/ExpeditionGate.sql#L451) | Checking the selected Expedition. If you changed units, reopen this window from the new selection. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_SELECT_CITY`](../../../Mod/Text/ExpeditionGate.sql#L525) | Select a destination. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_SELECT_TASK`](../../../Mod/Text/ExpeditionGate.sql#L527) | Select a mission to start. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_START_TASK`](../../../Mod/Text/ExpeditionGate.sql#L501) | Start Mission |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_TEAM`](../../../Mod/Text/ExpeditionGate.sql#L453) | Expedition: {1} |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_TIMING_UNKNOWN`](../../../Mod/Text/ExpeditionGate.sql#L509) | Travel time unavailable. It will be checked when you confirm. |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_TRAVEL_CONFIRM`](../../../Mod/Text/ExpeditionGate.sql#L447) | Confirm Travel |
| [`LOC_SPC_EXPEDITION_SPY_SIDEBAR_TASK_HINT`](../../../Mod/Text/ExpeditionGate.sql#L488) | Choose a mission, then select Start Mission. |
| [`LOC_SPC_EXPEDITION_SPY_SIDEBAR_TRAVEL_HINT`](../../../Mod/Text/ExpeditionGate.sql#L486) | Select a destination. Check travel time and available missions before confirming. |
| [`LOC_SPC_EXPEDITION_SPY_TASK_NATIVE_NOT_IDLE`](../../../Mod/Text/ExpeditionGate.sql#L248) | Could not confirm the Expedition is idle. The mission did not start. |
| [`LOC_SPC_EXPEDITION_SPY_TASK_REQUIRES_ARRIVAL`](../../../Mod/Text/ExpeditionGate.sql#L246) | The Expedition must arrive and have a confirmed source city before starting a mission. |
| [`LOC_SPC_EXPEDITION_SPY_TRAINED_COUNT`](../../../Mod/Text/ExpeditionGate.sql#L571) | Trained Expeditions: {1_Count}/1 |
| [`LOC_SPC_EXPEDITION_SPY_TRAINING_ERROR`](../../../Mod/Text/ExpeditionGate.sql#L564) | Training is awaiting confirmation: {1_Reason}. Keep the report. The slot remains reserved. |
| [`LOC_SPC_EXPEDITION_TRAINING_HELP`](../../../Mod/Text/ExpeditionGate.sql#L560) | Train a Humanities Expedition in a city with Culture active at Level 4. Your civilization can have 1 at a time, including queued Expeditions.<br><br>Training uses the Spy cost formula and counts Expeditions separately. When trained, the unit is bound to this city. Use Travel to a New City or Tasks. |
| [`LOC_SPC_EXPEDITION_TRAINING_NATIVE_DENIED`](../../../Mod/Text/ExpeditionGate.sql#L566) | Training could not start. Check the Production requirements, including available Spy slots. |

### City banners

| Source key | Candidate English |
|---|---|
| [`LOC_SPC_LEVEL_BANNER_HELP`](../../../Mod/Text/LevelBanners.sql#L6) | {1_Name} Specialization<br>Active Level: {2_Active}<br>Potential Level: {3_Potential}<br><br>Filled: active<br>Bright outline: unlocked, inactive<br>Dim: locked |

### Test civilization and Civilopedia introduction

| Source key | Candidate English |
|---|---|
| [`LOC_PEDIA_CIVILIZATIONS_PAGE_CIVILIZATION_SPC_AMERICA_TITLE`](../../../Mod/Text/TestAmerica.sql#L37) | America (Specialization Test) |
| [`LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_CAPSULE_BODY`](../../../Mod/Text/TestAmerica.sql#L35) | A city specialization test version of Teddy Roosevelt (Bull Moose). |
| [`LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_DETAILED_BODY`](../../../Mod/Text/TestAmerica.sql#L36) | Cities can specialize in Research, Culture, Commerce, or Industry. America’s and Roosevelt’s unique abilities, units, and buildings are disabled. |
| [`LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_TITLE`](../../../Mod/Text/TestAmerica.sql#L34) | Teddy Roosevelt (Bull Moose, Specialization Test) |
| [`LOC_SPC_ABILITY_DESCRIPTION`](../../../Mod/Text/TestAmerica.sql#L14) | Cities can specialize in Research, Culture, Commerce, or Industry. Each specialization grants its own institutions and abilities. |
| [`LOC_SPC_ABILITY_NAME`](../../../Mod/Text/TestAmerica.sql#L13) | City Specialization |
| [`LOC_SPC_AMERICA_ADJECTIVE`](../../../Mod/Text/TestAmerica.sql#L7) | American |
| [`LOC_SPC_AMERICA_DESCRIPTION`](../../../Mod/Text/TestAmerica.sql#L6) | America (Specialization Test) |
| [`LOC_SPC_AMERICA_NAME`](../../../Mod/Text/TestAmerica.sql#L5) | America (Specialization Test) |
| [`LOC_SPC_BLANK_LEADER_DESCRIPTION`](../../../Mod/Text/TestAmerica.sql#L12) | Uses the appearance and biography of Teddy Roosevelt (Bull Moose). America’s and Roosevelt’s unique abilities, units, and buildings are disabled. |
| [`LOC_SPC_BLANK_LEADER_NAME`](../../../Mod/Text/TestAmerica.sql#L11) | Specialization Test Leader |
| [`LOC_SPC_ROOSEVELT_NAME`](../../../Mod/Text/TestAmerica.sql#L8) | Teddy Roosevelt (Bull Moose, Specialization Test) |
| [`LOC_SPC_SYSTEM_DESCRIPTION`](../../../Mod/Text/TestAmerica.sql#L10) | Cities can specialize in Research, Culture, Commerce, or Industry. Each specialization grants its own institutions and abilities. |
| [`LOC_SPC_SYSTEM_NAME`](../../../Mod/Text/TestAmerica.sql#L9) | City Specialization |

## English labels carried forward

| Source key | Reviewed value |
|---|---|
| [`LOC_SPC_CREW_RESUME_NAME`](../../../Mod/Text/TestText.sql#L295) | {1_Name} (resume) |
| [`LOC_SPC_INSTITUTIONS_HEADER`](../../../Mod/Text/TestText.sql#L77) | Institutions |
| [`LOC_SPC_INSTITUTION_CURRENT`](../../../Mod/Text/TestText.sql#L78) | Current |
| [`LOC_SPC_INSTITUTION_ENABLED`](../../../Mod/Text/TestText.sql#L79) | Active |
| [`LOC_SPC_INSTITUTION_INACTIVE`](../../../Mod/Text/TestText.sql#L80) | Inactive |
| [`LOC_SPC_INSTITUTION_UNKNOWN`](../../../Mod/Text/TestText.sql#L81) | Pending |
| [`LOC_SPC_EXPEDITION_SPY_ACTION_TASK`](../../../Mod/Text/ExpeditionGate.sql#L439) | Tasks |
| [`LOC_SPC_EXPEDITION_SPY_INSIGHTS`](../../../Mod/Text/ExpeditionGate.sql#L638) | Cultural Insights: {1_History} recorded, {2_Effective} effective |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_AVAILABLE`](../../../Mod/Text/ExpeditionGate.sql#L630) | Available · 2 turns |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_NO_TARGET`](../../../Mod/Text/ExpeditionGate.sql#L634) | No eligible target in this city |
| [`LOC_SPC_EXPEDITION_SPY_MISSION_PLACES_NAME`](../../../Mod/Text/ExpeditionGate.sql#L622) | Wonder Pilgrimage |
| [`LOC_SPC_EXPEDITION_SPY_NAME`](../../../Mod/Text/ExpeditionGate.sql#L165) | Humanities Expedition |
| [`LOC_SPC_EXPEDITION_SPY_NORMAL_SOURCE`](../../../Mod/Text/ExpeditionGate.sql#L455) | Source city: {1} |
| [`LOC_SPC_EXPEDITION_SPY_SIDEBAR_CIV_UNKNOWN`](../../../Mod/Text/ExpeditionGate.sql#L496) | Civilization unavailable |
| [`LOC_SPC_EXPEDITION_SPY_SIDEBAR_TASK_LOCATION`](../../../Mod/Text/ExpeditionGate.sql#L494) | [ICON_LocationPip] Current city |
| [`LOC_SPC_INSIGHT_TOURISM_NAME`](../../../Mod/Text/ExpeditionGate.sql#L651) | Cultural Insight Tourism |
| [`LOC_SPC_LEVEL_COMMERCE`](../../../Mod/Text/LevelBanners.sql#L5) | Commerce |
| [`LOC_SPC_LEVEL_CULTURE`](../../../Mod/Text/LevelBanners.sql#L3) | Culture |
| [`LOC_SPC_LEVEL_INDUSTRY`](../../../Mod/Text/LevelBanners.sql#L4) | Industry |
| [`LOC_SPC_LEVEL_RESEARCH`](../../../Mod/Text/LevelBanners.sql#L2) | Research |

## Text written directly in the UI

The source column identifies each occurrence by line and column. Quotes show the bounds of fragments with spaces, including fragments that follow a dynamic value. The localization keys above cover the accompanying action descriptions.

For the later integration, route the reason text below through localized display values. Claim and Dialogue reasons are also published to other code. In particular, the queue checks for the literal strings `生产未确认` and `队列必须只有`. Keep those operands and the corresponding original reason intact. Translate the copy shown to the player at the point of display. [Queue reason check](../../../Mod/UI/TimedProjectQueueIntent.lua#L144)

### Institution levels

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [InstitutionPresentation.lua:124:16](../../../Mod/InstitutionPresentation.lua#L124) | “一” | “1” | UI text |
| [InstitutionPresentation.lua:124:20](../../../Mod/InstitutionPresentation.lua#L124) | “二” | “2” | UI text |
| [InstitutionPresentation.lua:124:24](../../../Mod/InstitutionPresentation.lua#L124) | “三” | “3” | UI text |
| [InstitutionPresentation.lua:124:28](../../../Mod/InstitutionPresentation.lua#L124) | “四” | “4” | UI text |

### Construction and Settler investment

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [UnitPanelActions.lua:123:10](../../../Mod/UI/UnitPanelActions.lua#L123) | “施工预览<br>当前目标：” | “Construction Preview<br>Current Wonder: ” | UI text |
| [UnitPanelActions.lua:123:38](../../../Mod/UI/UnitPanelActions.lua#L123) | “<br>当前进度：” | “<br>Progress: ” | UI text |
| [UnitPanelActions.lua:125:4](../../../Mod/UI/UnitPanelActions.lua#L125) | “确认施工<br>” | “Confirm Construction<br>” | UI text |
| [UnitPanelActions.lua:127:31](../../../Mod/UI/UnitPanelActions.lua#L127) | “施工<br>” | “Construct<br>” | UI text |
| [UnitPanelActions.lua:128:9](../../../Mod/UI/UnitPanelActions.lua#L128) | “施工<br>将施工队移动至正在建造奇观的单元格，即可进行施工。” | “Construct<br>Move the Crew to the tile of a Wonder the city is building.” | UI text |
| [UnitPanelActions.lua:131:24](../../../Mod/UI/UnitPanelActions.lua#L131) | “科研” | “Research” | UI text |
| [UnitPanelActions.lua:131:37](../../../Mod/UI/UnitPanelActions.lua#L131) | “文化” | “Culture” | UI text |
| [UnitPanelActions.lua:131:51](../../../Mod/UI/UnitPanelActions.lua#L131) | “商业” | “Commerce” | UI text |
| [UnitPanelActions.lua:131:65](../../../Mod/UI/UnitPanelActions.lua#L131) | “工业” | “Industry” | UI text |
| [UnitPanelActions.lua:131:81](../../../Mod/UI/UnitPanelActions.lua#L131) | “政府” | “Government” | UI text |
| [UnitPanelActions.lua:131:95](../../../Mod/UI/UnitPanelActions.lua#L131) | “军事” | “Military” | UI text |
| [UnitPanelActions.lua:133:10](../../../Mod/UI/UnitPanelActions.lua#L133) | “专业投资预览<br>当前专业：” | “Specialization Investment Preview<br>Current specialization: ” | UI text |
| [UnitPanelActions.lua:134:6](../../../Mod/UI/UnitPanelActions.lua#L134) | “<br>当前潜力：” | “<br>Current Potential: Level ” | UI text |
| [UnitPanelActions.lua:134:37](../../../Mod/UI/UnitPanelActions.lua#L134) | “级<br>投资后潜力：” | “<br>Potential after investment: Level ” | UI text |
| [UnitPanelActions.lua:134:74](../../../Mod/UI/UnitPanelActions.lua#L134) | “级” | “” | UI text |
| [UnitPanelActions.lua:135:6](../../../Mod/UI/UnitPanelActions.lua#L135) | “<br>本次消耗：1 名移民<br><br>提示：更高阶的专业能力仍需满足对应的总督就职与晋升条件方可启用。” | “<br>Cost: 1 Settler<br><br>Higher-Level abilities still require an established Governor with the appropriate promotions.” | UI text |
| [UnitPanelActions.lua:136:4](../../../Mod/UI/UnitPanelActions.lua#L136) | “确认专业投资<br>消耗此移民，使本城的专业潜力永久提升至 ” | “Confirm Specialization Investment<br>Consume this Settler to permanently increase this city’s Potential to Level ” | UI text |
| [UnitPanelActions.lua:136:60](../../../Mod/UI/UnitPanelActions.lua#L136) | “ 级。<br>此操作一旦确认无法撤销。” | “.<br>This cannot be undone.” | UI text |
| [UnitPanelActions.lua:138:31](../../../Mod/UI/UnitPanelActions.lua#L138) | “投资专业化<br>消耗 1 名移民，使本城的专业潜力永久提升 1 级。” | “Invest in Specialization<br>Consume 1 Settler to permanently raise this city’s Potential by 1 Level.” | UI text |
| [UnitPanelActions.lua:139:5](../../../Mod/UI/UnitPanelActions.lua#L139) | “<br>潜力变化：” | “<br>Potential: Level ” | UI text |
| [UnitPanelActions.lua:139:36](../../../Mod/UI/UnitPanelActions.lua#L139) | “ 级 → ” | “ → Level ” | UI text |
| [UnitPanelActions.lua:139:62](../../../Mod/UI/UnitPanelActions.lua#L139) | “ 级<br>点击以预览投资结果并进行最终确认。” | “<br>Select to preview the investment.” | UI text |
| [UnitPanelActions.lua:140:76](../../../Mod/UI/UnitPanelActions.lua#L140) | “投资专业化<br>专业潜力已达到4级，无法继续投资。” | “Invest in Specialization<br>This city has reached Potential Level 4.” | UI text |
| [UnitPanelActions.lua:142:10](../../../Mod/UI/UnitPanelActions.lua#L142) | “投资专业化<br>此前专业投资的结果尚待确认，暂时无法再次投资。” | “Invest in Specialization<br>The previous investment is awaiting confirmation.” | UI text |
| [UnitPanelActions.lua:144:9](../../../Mod/UI/UnitPanelActions.lua#L144) | “投资专业化<br>将移民移动至本城的专业区域，即可投资城市专业化。” | “Invest in Specialization<br>Move a Settler to this city’s specialization district to invest.” | UI text |
| [UnitPanelActions.lua:221:103](../../../Mod/UI/UnitPanelActions.lua#L221) | “确认投资” | “Confirm Investment” | UI text |
| [UnitPanelActions.lua:221:113](../../../Mod/UI/UnitPanelActions.lua#L221) | “确认施工” | “Confirm Construction” | UI text |
| [UnitPanelActions.xml:13:58](../../../Mod/UI/UnitPanelActions.xml#L13) | “确认” | “Confirm” | UI text |

### Capital Investment panel

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [CapitalInvestmentPanel.lua:20:39](../../../Mod/UI/CapitalInvestmentPanel.lua#L20) | “该领域已有未结算合同” | “An unsettled contract already exists in this field.” | UI text |
| [CapitalInvestmentPanel.lua:20:80](../../../Mod/UI/CapitalInvestmentPanel.lua#L20) | “签约需要商业 ACTIVE III” | “Requires Commerce active at Level 3.” | UI text |
| [CapitalInvestmentPanel.lua:21:27](../../../Mod/UI/CapitalInvestmentPanel.lua#L21) | “等待商路网络核验” | “Waiting to verify Trade Routes.” | UI text |
| [CapitalInvestmentPanel.lua:21:73](../../../Mod/UI/CapitalInvestmentPanel.lua#L21) | “同级来源缺少可靠机构建立时间” | “Could not verify when the tied source cities reached this level.” | UI text |
| [CapitalInvestmentPanel.lua:22:28](../../../Mod/UI/CapitalInvestmentPanel.lua#L22) | “等待商业状态更新” | “Waiting for the city’s Commercialization status.” | UI text |
| [CapitalInvestmentPanel.lua:22:59](../../../Mod/UI/CapitalInvestmentPanel.lua#L22) | “报价已变化，请核对新报价后再次确认” | “The quote changed. Review the new quote before confirming.” | UI text |
| [CapitalInvestmentPanel.lua:23:29](../../../Mod/UI/CapitalInvestmentPanel.lua#L23) | “金币实际变化与请求不符，已停止重复操作；请交回日志” | “The Gold payment could not be verified. Keep the logs and do not confirm again.” | UI text |
| [CapitalInvestmentPanel.lua:24:34](../../../Mod/UI/CapitalInvestmentPanel.lua#L24) | “金币回执尚未确认；合同已暂停” | “The contract is paused while its Gold receipt is verified.” | UI text |
| [CapitalInvestmentPanel.lua:24:74](../../../Mod/UI/CapitalInvestmentPanel.lua#L24) | “当前没有可投入金币” | “No Gold available to invest.” | UI text |
| [CapitalInvestmentPanel.lua:25:26](../../../Mod/UI/CapitalInvestmentPanel.lua#L25) | “专业来源暂不可确认” | “Could not verify the source city for specialization strength.” | UI text |
| [CapitalInvestmentPanel.lua:25:68](../../../Mod/UI/CapitalInvestmentPanel.lua#L25) | “城市归属暂不可确认” | “Could not verify city ownership.” | UI text |
| [CapitalInvestmentPanel.lua:26:32](../../../Mod/UI/CapitalInvestmentPanel.lua#L26) | “国库暂不可读取” | “Treasury balance unavailable.” | UI text |
| [CapitalInvestmentPanel.lua:26:69](../../../Mod/UI/CapitalInvestmentPanel.lua#L26) | “信誉暂不可确认；风险投资暂停，稳健投资仍按独立资格判断” | “Commercial Reputation is awaiting confirmation. Venture investments are paused. Stable investments remain subject to their own requirements.” | UI text |
| [CapitalInvestmentPanel.lua:26:127](../../../Mod/UI/CapitalInvestmentPanel.lua#L26) | “本版资本投资仅支持标准速度” | “Capital Investment requires Standard Speed.” | UI text |
| [CapitalInvestmentPanel.lua:32:31](../../../Mod/UI/CapitalInvestmentPanel.lua#L32) | “稳健投资不使用商业信誉。” | “Commercial Reputation applies to Venture Investment only.” | UI text |
| [CapitalInvestmentPanel.lua:33:48](../../../Mod/UI/CapitalInvestmentPanel.lua#L33) | “已确认商业信誉：” | “Confirmed Commercial Reputation: ” | UI text |
| [CapitalInvestmentPanel.lua:34:57](../../../Mod/UI/CapitalInvestmentPanel.lua#L34) | “当前等级不使用信誉加成（R=0）。” | “No Commercial Reputation bonus at the current Active Level.” | UI text |
| [CapitalInvestmentPanel.lua:35:54](../../../Mod/UI/CapitalInvestmentPanel.lua#L35) | “信誉记录异常；本次按无信誉加成政策计价（R=0），原记录保留。” | “The quote uses no Commercial Reputation bonus. The original record is retained.” | UI text |
| [CapitalInvestmentPanel.lua:36:9](../../../Mod/UI/CapitalInvestmentPanel.lua#L36) | “商业信誉暂不可确认，风险投资暂停。” | “Commercial Reputation is awaiting confirmation. Venture Investment is paused.” | UI text |
| [CapitalInvestmentPanel.lua:108:24](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “执行中” | “Active” | UI text |
| [CapitalInvestmentPanel.lua:108:38](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “已结算” | “Settled” | UI text |
| [CapitalInvestmentPanel.lua:108:55](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “已终止” | “Terminated” | UI text |
| [CapitalInvestmentPanel.lua:108:66](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “需核对回执” | “Receipt pending” | UI text |
| [CapitalInvestmentPanel.lua:108:87](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “确认中” | “Confirming” | UI text |
| [CapitalInvestmentPanel.lua:108:107](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “需核对扣款” | “Payment pending” | UI text |
| [CapitalInvestmentPanel.lua:108:129](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “到期待结算” | “Matured, awaiting settlement” | UI text |
| [CapitalInvestmentPanel.lua:108:152](../../../Mod/UI/CapitalInvestmentPanel.lua#L108) | “需核对返还” | “Return pending” | UI text |
| [CapitalInvestmentPanel.lua:111:14](../../../Mod/UI/CapitalInvestmentPanel.lua#L111) | “<br>签约时：” | “<br>At signing: ” | UI text |

### Specialization claims

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [ClaimProjects.lua:27:13](../../../Mod/ClaimProjects.lua#L27) | “当前生产不可读” | “Current production is awaiting confirmation.” | Display only |
| [ClaimProjects.lua:27:30](../../../Mod/ClaimProjects.lua#L27) | “认领必须为唯一当前目标；队列数量=” | “Keep the claim project alone in the Production queue. Items queued: ” | Display only |
| [ClaimProjects.lua:54:110](../../../Mod/ClaimProjects.lua#L54) | “专业已认领，Potential 1” | “Specialization established at Potential Level 1.” | Display only |
| [ClaimProjects.lua:58:42](../../../Mod/ClaimProjects.lua#L58) | “已改选目标；重新选择须完整占用一回合” | “Production changed. Select the project again for 1 full turn.” | Display only |
| [ClaimProjects.lua:59:82](../../../Mod/ClaimProjects.lua#L59) | “当前队列未确认；不完成项目” | “Waiting to confirm the Production queue. The project cannot complete yet.” | Display only |
| [ClaimProjects.lua:60:61](../../../Mod/ClaimProjects.lua#L60) | “错过完整回合窗口；请重新选择” | “Select this project again to start a full turn.” | Display only |
| [ClaimProjects.lua:63:121](../../../Mod/ClaimProjects.lua#L63) | “当前队列未确认；等待相关事件，不完成项目” | “Waiting to confirm the Production queue. The project cannot complete yet.” | Display only |
| [ClaimProjects.lua:67:59](../../../Mod/ClaimProjects.lua#L67) | “当前项目没有计时；请先改选普通目标，再重选认领项目，重新占用完整一回合” | “The timer has not started. Select another production target, then select the claim project again.” | Display only |
| [ClaimProjects.lua:71:117](../../../Mod/ClaimProjects.lua#L71) | “选择一个候选项目，完成后认领专业” | “Complete a claim project to establish this city’s specialization.” | Display only |
| [ClaimProjects.lua:103:14](../../../Mod/ClaimProjects.lua#L103) | “改选另一认领项目” | “Another claim project was selected.” | Display only |
| [ClaimProjects.lua:108:63](../../../Mod/ClaimProjects.lua#L108) | “1回合；保存读档继续计时” | “1 turn. Saving and loading preserves progress.” | Display only |
| [ClaimProjects.lua:131:23](../../../Mod/ClaimProjects.lua#L131) | “找不到对应已完成区域；暂停认领” | “Claim paused. Could not find the required completed district.” | Display only |
| [ClaimProjects.lua:155:31](../../../Mod/ClaimProjects.lua#L155) | “当前目标已改变” | “The current production target changed.” | Display only |
| [ClaimProjects.lua:161:40](../../../Mod/ClaimProjects.lua#L161) | “未确认完整生产回合；请重新选择” | “A full turn of production could not be confirmed. Select the project again.” | Display only |
| [ClaimProjects.lua:163:56](../../../Mod/ClaimProjects.lua#L163) | “等待原生完成事件；结果未知时不重复调用” | “Completion is awaiting confirmation.” | Display only |
| [ClaimProjects.lua:193:71](../../../Mod/ClaimProjects.lua#L193) | “已改选目标；需重新占用完整回合” | “The production target changed. Select the project again to start a full turn.” | Display only |
| [ClaimProjectUI.lua:18:74](../../../Mod/UI/ClaimProjectUI.lua#L18) | “已暂停” | “Paused” | UI text |
| [ClaimProjectUI.lua:23:10](../../../Mod/UI/ClaimProjectUI.lua#L23) | “确认中” | “Confirming” | UI text |
| [ClaimProjectUI.lua:23:29](../../../Mod/UI/ClaimProjectUI.lua#L23) | “等待Gameplay确认；若持续如此请查看当前项目提示” | “Waiting to confirm the project start.” | UI text |
| [ClaimProjectUI.lua:25:13](../../../Mod/UI/ClaimProjectUI.lua#L25) | “认领需完整一回合；完成才建立专业。已有未分配生产与项目期间生产不留给后续目标。” | “Complete 1 full turn to establish the specialization. Unassigned Production and Production earned during this project do not carry over.” | UI text |
| [ClaimProjectUI.lua:38:60](../../../Mod/UI/ClaimProjectUI.lua#L38) | “读档同步未确认：” | “Load recovery awaiting confirmation: ” | UI text |
| [ClaimProjectUI.lua:38:89](../../../Mod/UI/ClaimProjectUI.lua#L38) | “读档同步等待确认；不会自动重发” | “Waiting to verify the project after loading.” | UI text |
| [ClaimProjectUI.lua:46:58](../../../Mod/UI/ClaimProjectUI.lua#L46) | “认领项目不能排在队列后面；请选为唯一当前目标” | “Select the claim project as the only item in the Production queue.” | UI text |
| [ClaimProjectUI.lua:49:40](../../../Mod/UI/ClaimProjectUI.lua#L49) | “等待原生选择确认” | “Waiting to confirm the production target.” | UI text |
| [ClaimProjectUI.lua:58:101](../../../Mod/UI/ClaimProjectUI.lua#L58) | “启动确认超时；请重新选择项目” | “The project start was not confirmed. Select it again.” | UI text |
| [ClaimProjectUI.lua:65:102](../../../Mod/UI/ClaimProjectUI.lua#L65) | “启动请求失败：” | “Could not start the project: ” | UI text |
| [ClaimProjectUI.lua:67:44](../../../Mod/UI/ClaimProjectUI.lua#L67) | “认领必须为唯一当前目标；队列数量=” | “Keep the claim project alone in the Production queue. Items queued: ” | UI text |
| [ClaimProjectUI.lua:68:48](../../../Mod/UI/ClaimProjectUI.lua#L68) | “等待队列确认；数量=” | “Waiting for the Production queue. Items queued: ” | UI text |

### Dialogue of Eras

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [DialogueProjects.lua:72:13](../../../Mod/DialogueProjects.lua#L72) | “当前生产不可读” | “Current production is awaiting confirmation.” | Display only |
| [DialogueProjects.lua:72:30](../../../Mod/DialogueProjects.lua#L72) | “时代对话必须为唯一当前生产目标” | “Keep Dialogue of Eras alone in the Production queue.” | Display only |
| [DialogueProjects.lua:112:42](../../../Mod/DialogueProjects.lua#L112) | “生产已中断；本轮取消，未消耗时代机会” | “Production was interrupted. The project was canceled and this era’s opportunity is still available.” | Display only |
| [DialogueProjects.lua:113:54](../../../Mod/DialogueProjects.lua#L113) | “资格已失效；本轮取消，未消耗时代机会” | “The city lost eligibility. This era’s opportunity is still available.” | Display only |
| [DialogueProjects.lua:116:62](../../../Mod/DialogueProjects.lua#L116) | “已改选生产；本轮取消，重新开始需完整一回合” | “Production changed. Select the project again to start a full turn.” | Display only |
| [DialogueProjects.lua:121:53](../../../Mod/DialogueProjects.lua#L121) | “本游戏时代已成功；不可重复” | “Dialogue of Eras has already been completed for this era.” | Display only |
| [DialogueProjects.lua:121:95](../../../Mod/DialogueProjects.lua#L121) | “从城市生产列表选择时代对话” | “Select Dialogue of Eras in the city’s Production list.” | Display only |
| [DialogueProjects.lua:121:114](../../../Mod/DialogueProjects.lua#L121) | “需要文化身份及ACTIVE III” | “Requires Culture active at Level 3.” | Display only |
| [DialogueProjects.lua:122:41](../../../Mod/DialogueProjects.lua#L122) | “当前资格尚不可确认；未清除历史，也不完成项目” | “Waiting to confirm eligibility. Recorded history is retained.” | Display only |
| [DialogueProjects.lua:123:83](../../../Mod/DialogueProjects.lua#L123) | “；可重新选择” | “. Select the project again.” | Display only |
| [DialogueProjects.lua:124:84](../../../Mod/DialogueProjects.lua#L124) | “当前资格或生产未确认；等待相关事件，不完成项目” | “Waiting to confirm eligibility or production. The project cannot complete yet.” | Display only |
| [DialogueProjects.lua:168:58](../../../Mod/DialogueProjects.lua#L168) | “改选后重新开始” | “Changing the production target restarts the timer.” | Display only |
| [DialogueProjects.lua:174:30](../../../Mod/DialogueProjects.lua#L174) | “需要已确认的文化ACTIVE III” | “Requires confirmed Culture Active Level 3 or higher.” | Display only |
| [DialogueProjects.lua:206:50](../../../Mod/DialogueProjects.lua#L206) | “完成前资格失效；未记奖励或额度” | “The city lost eligibility before completion. No bonus was awarded and the era’s opportunity is still available.” | Display only |
| [DialogueProjects.lua:209:28](../../../Mod/DialogueProjects.lua#L209) | “完成来源已不确定；不重放或补取之后的馆藏” | “Could not confirm completion. The collection will not be checked again for this attempt.” | Display only |
| [DialogueProjects.lua:223:28](../../../Mod/DialogueProjects.lua#L223) | “完成时事实未确认；不以之后的馆藏补算” | “Could not confirm the collection at completion. Later changes do not count toward this attempt.” | Display only |
| [DialogueProjects.lua:237:50](../../../Mod/DialogueProjects.lua#L237) · [DialogueProjects.lua:267:56](../../../Mod/DialogueProjects.lua#L267) | “资格已失效；本轮取消” | “The city lost eligibility. The attempt was canceled.” | Display only |
| [DialogueProjects.lua:242:61](../../../Mod/DialogueProjects.lua#L242) | “生产中断；本轮取消” | “Production was interrupted. The attempt was canceled.” | Display only |
| [DialogueProjects.lua:249:46](../../../Mod/DialogueProjects.lua#L249) | “未确认完整生产回合；请重新选择” | “A full turn of production could not be confirmed. Select the project again.” | Display only |
| [DialogueProjects.lua:276:21](../../../Mod/DialogueProjects.lua#L276) | “已放弃未确认轮次；历史与额度未增加” | “The unconfirmed attempt was canceled. The bonus and era’s opportunity are unchanged.” | Display only |
| [DialogueProjectUI.lua:21:13](../../../Mod/UI/DialogueProjectUI.lua#L21) | “时代对话：需连续占用完整的 1 个回合；完成后按本城合格馆藏覆盖的作品时代数，永久累计巨作原生旅游业绩倍率。” | “Complete 1 full turn. Each distinct era in this city’s eligible collection permanently adds 5 percentage points to its [ICON_Tourism] Tourism bonus for Great Works.” | UI text |
| [DialogueProjectUI.lua:26:42](../../../Mod/UI/DialogueProjectUI.lua#L26) | “待确认” | “Awaiting confirmation” | UI text |
| [DialogueProjectUI.lua:27:39](../../../Mod/UI/DialogueProjectUI.lua#L27) | “已暂停” | “Paused” | UI text |
| [DialogueProjectUI.lua:31:29](../../../Mod/UI/DialogueProjectUI.lua#L31) | “待计时” | “Awaiting start” | UI text |
| [DialogueProjectUI.lua:31:35](../../../Mod/UI/DialogueProjectUI.lua#L31) | “此项目须独占生产队列并连续占用完整的 1 个回合；计时等待Gameplay确认，未确认时不会完成项目。” | “Keep Dialogue of Eras alone in the Production queue for 1 full turn. Timing is awaiting confirmation.” | UI text |

### Engineering Tradition Study

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [EngineeringStudyUI.lua:13:44](../../../Mod/UI/EngineeringStudyUI.lua#L13) | “工程传统研习：完整一回合后，本城历史层数 +1。” | “Complete 1 full turn to gain 1 permanent study level in this city.” | UI text |
| [EngineeringStudyUI.lua:14:41](../../../Mod/UI/EngineeringStudyUI.lua#L14) | “待确认” | “Awaiting confirmation” | UI text |
| [EngineeringStudyUI.lua:14:47](../../../Mod/UI/EngineeringStudyUI.lua#L14) | “原生完成回执待确认；不会重复发放。” | “Waiting to confirm completion. The study level can be granted only once.” | UI text |
| [EngineeringStudyUI.lua:16:57](../../../Mod/UI/EngineeringStudyUI.lua#L16) · [EngineeringStudyUI.lua:17:10](../../../Mod/UI/EngineeringStudyUI.lua#L17) | “已暂停” | “Paused” | UI text |
| [EngineeringStudyUI.lua:16:63](../../../Mod/UI/EngineeringStudyUI.lua#L16) | “工程传统研习必须独占生产队列；移除其他项后自动核对计时。” | “Remove the other items from the Production queue to start timing.” | UI text |
| [EngineeringStudyUI.lua:17:16](../../../Mod/UI/EngineeringStudyUI.lua#L17) | “研习未确认，请查看工业历史报告。” | “Could not confirm the study. See the Industry History report.” | UI text |
| [EngineeringStudyUI.lua:22:29](../../../Mod/UI/EngineeringStudyUI.lua#L22) | “确认中” | “Confirming” | UI text |
| [EngineeringStudyUI.lua:22:35](../../../Mod/UI/EngineeringStudyUI.lua#L22) | “请选择为唯一当前项目；中断后需要重新选择。” | “Keep this project alone in the Production queue. Select it again after an interruption.” | UI text |
| [EngineeringStudyUI.lua:23:13](../../../Mod/UI/EngineeringStudyUI.lua#L23) | “需要工业 ACTIVE IV 且本城 L 小于全国 E；中断取消本轮。” | “Requires Industry active at Level 4 and a study opportunity from an era represented by your civilization’s Wonders.” | UI text |

### Production queue

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [TimedProjectQueueIntent.lua:86:39](../../../Mod/UI/TimedProjectQueueIntent.lua#L86) | “已达到当前可研习知识；若队列中仍有项目，请移除。” | “All available studies are complete. Remove this project if it is still queued.” | UI text |
| [TimedProjectQueueIntent.lua:86:68](../../../Mod/UI/TimedProjectQueueIntent.lua#L86) | “本游戏时代的时代对话机会已使用；若队列中仍有项目，请移除。” | “Dialogue of Eras is complete for this era. Remove this project if it is still queued.” | UI text |
| [TimedProjectQueueIntent.lua:88:10](../../../Mod/UI/TimedProjectQueueIntent.lua#L88) | “当前专业资格不满足；不会计时或发放奖励。” | “The city does not meet the requirements for this project.” | UI text |
| [TimedProjectQueueIntent.lua:94:30](../../../Mod/UI/TimedProjectQueueIntent.lua#L94) · [TimedProjectQueueIntent.lua:108:10](../../../Mod/UI/TimedProjectQueueIntent.lua#L108) · [TimedProjectQueueIntent.lua:176:45](../../../Mod/UI/TimedProjectQueueIntent.lua#L176) | “待入队” | “Awaiting queue” | UI text |
| [TimedProjectQueueIntent.lua:94:36](../../../Mod/UI/TimedProjectQueueIntent.lua#L94) | “入队请求尚未确认，不重复加入；等待相关队列变化。” | “Waiting for the queue to confirm the request.” | UI text |
| [TimedProjectQueueIntent.lua:97:46](../../../Mod/UI/TimedProjectQueueIntent.lua#L97) · [TimedProjectQueueIntent.lua:166:32](../../../Mod/UI/TimedProjectQueueIntent.lua#L166) | “不可开始” | “Unavailable” | UI text |
| [TimedProjectQueueIntent.lua:100:25](../../../Mod/UI/TimedProjectQueueIntent.lua#L100) · [TimedProjectQueueIntent.lua:174:25](../../../Mod/UI/TimedProjectQueueIntent.lua#L174) | “待核实” | “Awaiting confirmation” | UI text |
| [TimedProjectQueueIntent.lua:100:31](../../../Mod/UI/TimedProjectQueueIntent.lua#L100) | “生产队列暂不可确认，请稍后重新选择；不会重复加入项目。” | “Could not confirm the queue. Select the project again later.” | UI text |
| [TimedProjectQueueIntent.lua:103:48](../../../Mod/UI/TimedProjectQueueIntent.lua#L103) · [TimedProjectQueueIntent.lua:180:28](../../../Mod/UI/TimedProjectQueueIntent.lua#L180) · [TimedProjectQueueIntent.lua:184:26](../../../Mod/UI/TimedProjectQueueIntent.lua#L184) | “已暂停” | “Paused” | UI text |
| [TimedProjectQueueIntent.lua:103:56](../../../Mod/UI/TimedProjectQueueIntent.lua#L103) | “已排队” | “Queued” | UI text |
| [TimedProjectQueueIntent.lua:103:76](../../../Mod/UI/TimedProjectQueueIntent.lua#L103) · [TimedProjectQueueIntent.lua:180:34](../../../Mod/UI/TimedProjectQueueIntent.lua#L180) | “队列内存在重复项目，请只保留一项；不会重复发放。” | “Keep only one copy in the Production queue. The reward can be granted only once.” | UI text |
| [TimedProjectQueueIntent.lua:103:105](../../../Mod/UI/TimedProjectQueueIntent.lua#L103) | “此项目已在队列中，不会重复加入；成为唯一当前项目后才计时。” | “Already queued. Timing starts when this is the only item in the queue.” | UI text |
| [TimedProjectQueueIntent.lua:108:16](../../../Mod/UI/TimedProjectQueueIntent.lua#L108) · [TimedProjectQueueIntent.lua:176:51](../../../Mod/UI/TimedProjectQueueIntent.lua#L176) | “等待生产队列确认；尚未开始计时。” | “Waiting for the queue. The timer has not started.” | UI text |
| [TimedProjectQueueIntent.lua:153:14](../../../Mod/UI/TimedProjectQueueIntent.lua#L153) · [TimedProjectQueueIntent.lua:187:36](../../../Mod/UI/TimedProjectQueueIntent.lua#L187) · [TimedProjectQueueIntent.lua:204:54](../../../Mod/UI/TimedProjectQueueIntent.lua#L204) | “待确认” | “Awaiting confirmation” | UI text |
| [TimedProjectQueueIntent.lua:153:20](../../../Mod/UI/TimedProjectQueueIntent.lua#L153) | “本回合已有完成记录，无法确认此队列项是否为新一轮；请重新选择项目。” | “Could not verify this as a new attempt after this turn’s completion. Select the project again.” | UI text |
| [TimedProjectQueueIntent.lua:174:31](../../../Mod/UI/TimedProjectQueueIntent.lua#L174) | “生产队列尚不可确认，等待相关变化；不会完成项目。” | “Waiting to confirm the Production queue. The project cannot complete yet.” | UI text |
| [TimedProjectQueueIntent.lua:184:34](../../../Mod/UI/TimedProjectQueueIntent.lua#L184) | “排队中” | “Queued” | UI text |
| [TimedProjectQueueIntent.lua:184:55](../../../Mod/UI/TimedProjectQueueIntent.lua#L184) | “项目必须独占生产队列；移除其他项后自动核对计时。” | “Remove the other items from the Production queue to start timing.” | UI text |
| [TimedProjectQueueIntent.lua:184:84](../../../Mod/UI/TimedProjectQueueIntent.lua#L184) | “尚未成为唯一当前项目，不计时；轮到后自动核对。” | “Timing starts when this is the only item in the Production queue.” | UI text |
| [TimedProjectQueueIntent.lua:187:60](../../../Mod/UI/TimedProjectQueueIntent.lua#L187) | “等待专业资格与计时状态确认。” | “Waiting to confirm eligibility and the project timer.” | UI text |
| [TimedProjectQueueIntent.lua:191:29](../../../Mod/UI/TimedProjectQueueIntent.lua#L191) · [TimedProjectQueueIntent.lua:196:65](../../../Mod/UI/TimedProjectQueueIntent.lua#L196) | “待开始” | “Awaiting start” | UI text |
| [TimedProjectQueueIntent.lua:191:35](../../../Mod/UI/TimedProjectQueueIntent.lua#L191) | “本地回合已结束，等待下一个可靠回合起点开始完整计时。” | “Timing can start when your next turn is available.” | UI text |
| [TimedProjectQueueIntent.lua:196:71](../../../Mod/UI/TimedProjectQueueIntent.lua#L196) | “等待本地回合可操作状态确认；不补计排队时间。” | “Timing waits until your turn is available. Time spent queued does not count.” | UI text |
| [TimedProjectQueueIntent.lua:201:10](../../../Mod/UI/TimedProjectQueueIntent.lua#L201) | “确认中” | “Confirming” | UI text |
| [TimedProjectQueueIntent.lua:201:16](../../../Mod/UI/TimedProjectQueueIntent.lua#L201) | “正在确认完整一回合计时；不会重复提交同一轮。” | “Confirming the start of the 1-turn timer.” | UI text |
| [TimedProjectQueueIntent.lua:204:60](../../../Mod/UI/TimedProjectQueueIntent.lua#L204) | “启动请求结果未知；不会盲目重发，请保留日志。” | “Could not confirm the start request. Keep the logs.” | UI text |

### Production progress

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [TimedProjectCityPanel.lua:13:50](../../../Mod/UI/TimedProjectCityPanel.lua#L13) | “回合后完成” | “turn remaining” | UI text |
| [TimedProjectCityPanel.lua:13:61](../../../Mod/UI/TimedProjectCityPanel.lua#L13) | “计时项目” | “Project Timer” | UI text |
| [TimedProjectDisplay.lua:56:64](../../../Mod/UI/TimedProjectDisplay.lua#L56) | “计时已开启：1回合” | “Timer started: 1 turn” | UI text |
| [TimedProjectDisplay.lua:56:80](../../../Mod/UI/TimedProjectDisplay.lua#L56) | “计时：” | “Timer: ” | UI text |

### Mod listing

| Source | Current fragment | Candidate English | Use |
|---|---|---|---|
| [SpecializationP0.modinfo:4:5](../../../Mod/SpecializationP0.modinfo#L4) | “城市专业化（罗斯福进步党测试）” | “City Specialization (Bull Moose Test)” | UI text |
| [SpecializationP0.modinfo:5:5](../../../Mod/SpecializationP0.modinfo#L5) | “B443.470：恢复专业项目生产面板接入。” | “Test city specialization through institutions, investments, and domestic Trade Routes.” | UI text |

### Assembled unit tooltips

The values in braces below show where the existing UI inserts the city, target, progress, or level. Construction details continue to use the existing localized contribution text keys.

**Construction preview**

```text
Construction Preview
Current Wonder: {wonder}
Progress: {progress} / {cost}
Base capacity: {1_Capacity} [ICON_Production] Production
Base contribution: {2_Input}
Unused: {3_Unused}
Applicable bonuses can increase the contribution. Excess Production does not carry over.
```

**Settler investment preview**

```text
Specialization Investment Preview
Current specialization: {specialization}
Current Potential: Level {current}
Potential after investment: Level {next}
Cost: 1 Settler

Higher-Level abilities still require an established Governor with the appropriate promotions.
```

**Settler confirmation**

```text
Confirm Specialization Investment
Consume this Settler to permanently increase this city’s Potential to Level {next}.
This cannot be undone.
```

## Review coverage

| Source | Keys | Proposed | Existing English | Diagnostic or historical |
|---|---:|---:|---:|---:|
| [TestText.sql](../../../Mod/Text/TestText.sql) | 162 | 88 | 6 | 68 |
| [Restructuring.sql](../../../Mod/Text/Restructuring.sql) | 24 | 24 | 0 | 0 |
| [Commerce.sql](../../../Mod/Text/Commerce.sql) | 110 | 110 | 0 | 0 |
| [DevelopmentInvestment.sql](../../../Mod/Text/DevelopmentInvestment.sql) | 55 | 55 | 0 | 0 |
| [ClaimProjects.sql](../../../Mod/Text/ClaimProjects.sql) | 8 | 8 | 0 | 0 |
| [DialogueProjects.sql](../../../Mod/Text/DialogueProjects.sql) | 4 | 4 | 0 | 0 |
| [EngineeringStudy.sql](../../../Mod/Text/EngineeringStudy.sql) | 2 | 2 | 0 | 0 |
| [ExpeditionGate.sql](../../../Mod/Text/ExpeditionGate.sql) | 301 | 76 | 10 | 215 |
| [LevelBanners.sql](../../../Mod/Text/LevelBanners.sql) | 5 | 1 | 4 | 0 |
| [TestAmerica.sql](../../../Mod/Text/TestAmerica.sql) | 14 | 14 | 0 | 0 |
| **Total** | **685** | **382** | **20** | **283** |

The historical entries include Scotland’s test shell, prototype Crew and project strings, and the Expedition verification harness. The normal Expedition screens and mission rewards use the reviewed text above. Internal logs and reports fall outside the player-copy inventory. The inventory of direct strings follows the Chinese draft.

## Integration checks for a later implementation

- Match each live institution metric label to the English section heading. The six headings in this draft use an English colon. The current lookup recognizes a fullwidth colon. [Institution metric insertion](../../../Mod/InstitutionPresentation.lua#L107)
- Build complete localized sentences for the unit previews, then verify the result in each locale. English puts the level label before the number. Use the proposed English renderings where they appear in the UI and keep operational strings in the underlying state.
- Confirm button fit and live values in the game when the English copy is integrated. This review exercised the draft data only.
