# Expedition: native Spy identity, name pools and source binding

Date: 2026-10-10. **Technical investigation / non-authoritative; no Design decision or implementation implied.** Reviewed develop `b4ea33d`, source/runtime baseline B188.215. User reports newly built ordinary Spies display only “间谍” and requests investigation of name pools, city associations and alternatives. This observation is user-reported, not a new inspected screenshot or native API trace.

The [B188 native failure](../../Status/Validation/Results/Specialization_B188_Expedition_Name_Eligibility_Native_Review.md) and earlier frozen records remain unchanged. No code, tests, Design, runtime or game state is modified. Findings below are STATIC_CONFIRMED unless explicitly marked inference/UNKNOWN; no new USER_GAME_TEST_PASS.

## Findings that change the next step

1. **The dedicated test civilization has no citizen-name pool.** This is a confirmed data omission and a concrete candidate explanation for generic Spy names. Native assignment timing/custom-type support remain unproved.
2. Native Spy continuity is not exposed as one universal stable Lua UnitID. On-map, off-map and captured UI paths use different references. The engine can maintain a separate Spy record; its internal identity algorithm is not exposed here.
3. A name pool is feasible as data. Reliably assigning a usable name and preserving it across travel are still native gates. Writing an association to a city does not itself solve those gates.
4. Recommended next implementation proposal: a scoped citizen-name-pool addition for the test civilization and observation of native automatic naming, preserving source/capacity and the existing no-reward travel/task experiment. Do not retry manual NAME_UNIT or change global veteran rules as the first response.

## What the native system actually exposes

Aliases: `CIV_ASSETS` = installed `Civ6.app/Contents/Assets`; `HD_CORE` = installed HD package2465378070. Relative source paths identify read-only external evidence, not public or portable local-file links.

| State / surface | Direct source | Confirmed behavior and limit |
|---|---|---|
| On-map selection and dispatch | `CIV_ASSETS/Base/Assets/UI/Choosers/EspionageChooser.lua:606–616`; `UI/Popups/EspionagePopup.lua:350–358` | Sends current unit object/current ID and destination into the native travel/mission API. No Lua identity-copy operation is visible. |
| Travel/off-map | `Base/Assets/UI/PartialScreens/EspionageOverview.lua:128–136,734–758` | `GetNthOffMapSpy` records expose Name, Level, ReturnTurn, XLocation and YLocation to this UI. A separate record exists while travelling. Its ordinal in enumeration is not a proved persistent ID. |
| Captured Spy | Same Overview`:802,817–831,870,883–894` | Uses **NameIndex** as the CAPTIVE deal ValueType, described by native code as the Spy index. This is an identity-like native field independent of a current map unit. Its live/off-map availability, scope, reuse and lifetime are UNKNOWN. No established bridge to our returning custom unit. |
| Renew completed mission | `Base/Assets/UI/Popups/EspionagePopup.lua:150–156` | Comment says mission history has no Spy UnitID; UI searches current Spies using raw `GetName()==history.Name`. This is a UI workaround, not evidence that the engine uses names as its only identity. The loop provides no duplicate-name proof. |
| HD per-Spy reward history | `HD_CORE/Gameplay/UnitAbilities.lua:530–560` | Exact UNIT_SPY path comments that travel changes ID while the name persists and uses name-keyed player Properties. It excludes the custom type. Useful ordinary-Spy precedent, not a proof of our custom name's uniqueness/preservation. |
| Component ID | `Base/Assets/UI/Panels/UnitPanel.lua:2740,2752–2757` | Reads GetComponentID and later resolves `.player/.id`; no stable serial across travel is demonstrated. Similar low bits in prior B186 IDs do not establish a valid identity contract. |

**A generic visible label is not proof of lost native identity, nor proof of a hidden unique raw name.** UnitPanel`:2231–2232` reads raw GetName and the type's default name separately;`:971–998` displays the localized raw name, adding a type tooltip when different. The inspected UI does not reveal exactly when an ordinary Spy gets a personal name. This user's fixture observation must not be generalized to all civilizations or all ordinary Spies.

The prior [B186 native evidence](../../Status/Validation/Results/Specialization_B186_Expedition_Marker_Native_Review.md) remains decisive for our implementation: an off-map unit Property was present, then absent on arrival, while the separate source reference survived. Native object deletion/recreation is still unproved. It is unsafe to copy the absent Property onto a candidate and call that proof of continuity.

## Two separate naming systems

### Native citizen / Spy name pool

[Identity.sql](../../../Mod/Data/Identity.sql):1–28 defines **CIVILIZATION_SPC_TEST as an independent civilization**. Its Scotland references provide presentation only. Lines14–17 insert three CityNames; they do not provide citizen names. [Players.sql](../../../Mod/Config/Players.sql) registers the independent player identity. A targeted Mod/Data and Mod/Config search finds no CivilizationCitizenNames insert for this civilization.

Read-only configured gameplay DB:

| Civilization | Citizen-name entries |
|---|---:|
| CIVILIZATION_SPC_TEST | **0** |
| CIVILIZATION_SCOTLAND | 40 |
| CIVILIZATION_ENGLAND | 40 |

The relevant native schema is `Base/Assets/Gameplay/Data/Schema/01_GameplaySchema.sql:678–684`: CivilizationCitizenNames has CivilizationType, CitizenName, Female and Modern, keyed by civilization/name. The native Civilizations navigation exposes CitizenNameCollection; `Base/Assets/Gameplay/Data/Gossip.xml:143–866` supplies pools. This is civilization-wide data, not a per-custom-unit list.

`HD_CORE/UpdateDataBase/DL_Units.sql:88` describes adding Spy names to avoid duplicates;89–104 propose extending CivilizationCitizenNames. **Those SQL statements are commented out.** They support the table's intended Spy-name use but do not actively fill our pool, prove assignment timing or guarantee name uniqueness.

**Inference:** the empty test-civilization pool is a plausible explanation for the user's generic ordinary Spy and our custom team's default label. It is a stronger data-backed lead than another timing-only repair. **UNKNOWN:** whether custom Spy1 created by InitUnit uses this pool, when it does so, pool exhaustion/reuse, whether names are raw localization keys or strings, and preservation across travel. CityNames and UnitNames cannot be substituted: UnitNames is the separate generic prefix/suffix table, without a demonstrated per-unit Spy pool.

### Manual veteran rename command

Native UnitPanel`:447–451,2806–2814` and HD `UI/Replacement/DL_UnitPanel.lua:114–118` use CanStartCommand(NAME_UNIT,true), then PARAM_NAME/RequestCommand. The native/HD guard uses Lua truthiness; [B188](../../../Mod/ExpeditionSpyRead.lua):195 requires boolean true. The screenshot establishes only that B188's comparison failed. A false/nil/other return was not captured, so neither exact ineligibility nor a return-type mismatch is a confirmed root cause.

`UNIT_EXPERIENCE_LEVEL_FOR_CUSTOM_NAME=2` exists in native GlobalParameters`:605` and loaded DB. Loaded custom Spy has InitialLevel1, CanEarnExperience0, ImmediatelyName0; ordinary Spy has InitialLevel1, CanEarnExperience1, ImmediatelyName0. The veteran restriction is plausible, not the exposed engine predicate. **Automatic Spy naming and veteran renaming are different routes**; fixing missing pool data does not prove NAME_UNIT becomes allowed, and the next candidate need not call that command at all.

No supported direct setter was established by bounded native DLC script/HD Gameplay searches. Loaded DynamicModifiers and Types contain no NAME-associated effect/modifier entries. The author-maintained [Unit](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/Unit) and [UnitManager](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/UnitManager) API inventories expose GetName and command APIs, without a documented direct name setter; these inventories are not exhaustive proof of absence. Web results for Civilization_SpyNames and many Unit:SetName examples concerned Civ V and were excluded. No unsupported setter or command bypass was executed.

## Assessment of the user's pool and city-Property idea

**A stable team identifier associated with a city is a sound candidate structure.** It must separate three things:

`verified team identity → current exact archive-city reference → readable city label`

A name drawn from an established pool could supply the first item **after** native assignment/readback and travel preservation are proved. It need not encode the city name. On an authorized reattachment, retain the team identity and update the city reference; derive the displayed city label from that record. This avoids needing another successful rename whenever the archive changes. Duplicate/default/ambiguous names still cannot be accepted. Uniqueness checks must include all currently tracked/reserved same-owner custom teams, including pending/off-map teams, not only units visible at the destination; the pool itself does not guarantee uniqueness.

A city Property could store a reference or navigation index, but it should not be the only owner of team identity/binding. Under [accepted source-loss and reattachment rules](../../Design/Content/Culture_D0049.json), the unit remains with its original player when the source city changes owner; the old archive becomes invalid, the team survives awaiting reattachment, and old city history stays put. Merely writing the same name into the new city would leave an old association unless deliberately invalidated. City name changes also must not redefine identity. Neither national cap1 nor one candidate at the destination alone proves continuity.

For the next prototype, the **existing session source record is enough**; no new city Property, persistent registry or saved-journey schema is needed to test naming. Formal persistence and reattachment remain separate N1 implementation. Their eventual authoritative mapping must survive periods without a valid source city and reject stale associations; this investigation does not choose a schema or change accepted ownership semantics.

## Alternatives and recommendation

| Path | Present evidence | Recommendation / remaining gate |
|---|---|---|
| Test-civilization citizen-name pool + native assigned name | Confirmed empty pool; native schema and HD naming precedent | **First candidate.** Add only this civilization's neutral/localized name data in a future approved patch; observe actual assigned raw name before relying on it. Applies to ordinary Spies of this test civilization too; not an Expedition-exclusive pool. Other civilizations/global naming rules stay untouched. |
| Native NameIndex / other exposed Spy record identity | Captured-Spy UI exposes NameIndex | Worth a bounded read-only diagnostic if available in the same native sample. Do not assume captured index equals a stable live/off-map key, hardcode citizen row IDs or use enumeration order. |
| Controlled arbitrary name using NAME_UNIT | Verified command exists; B188 permission check stops | Not the first repair candidate. Its exact return/predicate remains unresolved; no global threshold or XP workaround. |
| Direct setter / naming Modifier | No supported route established in searched sources | Do not implement an invented API or declare universal impossibility. |
| Unit Property, guessed ID bits, sole matching unit or city-name search | Marker failed natively; other routes lack identity guarantees | Not a substitute for an observed continuity link. |
| Own off-map travel / newly spawned arrival representation | Conceptually could keep our logical identity outside the native transition | Much wider travel/lifecycle work; not justified before checking the concrete name-pool gap. No implementation/design change proposed here. |

### Proposed next minimal batch — needs implementation approval

1. Add citizen-name data only for CIVILIZATION_SPC_TEST, preferably reusing an existing native neutral name set with its Female/Modern metadata. Do not alter other civilizations, Spy XP/promotions, the global naming threshold or native espionage reward paths. This is fixture completeness, not new Gameplay semantics.
2. Replace mandatory manual renaming in this bounded prototype with native-name observation on the exact freshly created custom team. Record raw name/default comparison, pool evidence and stage; wait only through a bounded known publication window. No name/pool-membership check alone proves uniqueness or continuity. Keep original source/cap reservation and exact owner/type/ID validation; default/ambiguous/unreadable names stop before dispatch.
3. If a usable name exists, retain it with the current session's own team/source record and require an unambiguous matching arrival with the correct current owner/type/target and valid source. Record available off-map identity fields as observations, not new authority. Do not serialize a NameIndex or guess its meaning without evidence.
4. Local validation: empty/default/duplicate names, delayed publication, unrelated units, source change, changed-ID arrival and unchanged capacity/task/END. Database tests establish only pool data, not engine naming. No additional shared save/load campaign.
5. One conditional native session after a separately approved patch: creation receives a non-default name → native travel retains it and source binding → existing no-reward task → END. A pre-creation fixture is appropriate; no promise that adding data retroactively renames an existing unnamed/off-map Spy. If the custom type stays generic despite verified loaded pool data, stop before more travel. This shows pool addition alone was insufficient, not that custom Spy naming is impossible; assignment timing/type/creation-path remain unresolved. Only then consider one bounded ordinary-Spy control to distinguish some of those hypotheses. Do not require that extra control in the first successful path.

This is a proposal only. No new B build, user test dispatch, deployment, native success or formal N1/N2/N3/U2/reward authorization is created. B188 remains the recorded runtime.

## Scope and maintenance

Read: current guidance/Authority/CURRENT/P0-N1; exact B186/B188 evidence; Gate/Read source; Identity/Players/custom-Spy definitions; accepted Expedition binding object; native Spy UI and naming schema/data; exact HD Spy reward/naming references; read-only loaded DB; narrowly targeted public API/source references. No full Mod/history scan, live API call, binary/save inspection or gameplay test. This report and minimal current pointers preserve the result; original evidence remains frozen.
