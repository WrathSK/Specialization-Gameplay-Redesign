# 城市易主：独立永久账本与转移关联研究

Document Owner: Codex
Design: D0024 unchanged
Runtime: B063.89 unchanged
Scope: 静态调查和实施方案；本轮不接运行代码，不恢复测试城。

## 结论与证据等级

USER_GAME_TEST_PASS仅指B063只读观察：自由城市转换及用户所述赠送AI后，五项City Property均缺失。永久数据不能只在City对象中保存。城市物理区域保留不代表Lua Property或内部city ID保留。普通军事征服、取回、事件参数/顺序仍未实测。

STATIC_CONFIRMED为本机源码证据，不能替代游戏事件实测：

| 参考 | 已确认内容 | 不能据此推断 |
|---|---|---|
| Mod/BindingProbe.lua key/ledger/gameWrite | 现有Game Property按玩家保存编号和旧owner/cityID/坐标；写后读回、B013正常保存读档已验证 | 此表没有投资/模板正文，单独不能救回丢失账本；旧32城DEV限制不是正式UID方案 |
| Mod/StorageProbe.lua；B012/B013既有结果 | 整局表格读写已有项目先例 | 新跨Owner协议已验证 |
| HD Gameplay/Buildings.lua 221–234 | Game:GetProperty/SetProperty保存全局玩家列表 | 任意大表容量无上限或跨多个键原子事务 |
| HD Gameplay/Misc.lua 732–770 | Plot属性记录城邦状态；GameEvents.CityConquered(newPlayerId,oldPlayerId,newCityId,x,y)调用重新处理 | 该事件覆盖赠送/自由城市；移除事件必然表示永久毁城 |
| HD Gameplay/Commemorations.lua 94–126、CivilizationTraits.lua 2527–2550 | Gameplay注册同CityConquered参数，可获得旧玩家、新玩家、新city ID和坐标 | 旧city ID在参数内；回调时仍可取旧City Property |
| 原版Expansion2/UI/Loaders/TutorialLoader_Expansion1.lua 282–293 | Events.CityTransfered(playerID,city)供教程用；CityInitialized另有注册 | UI签名等于Gameplay可用签名，或包含旧Owner/旧CityID |
| 原版CityBannerManager.lua CityRemovedFromMap | 移除事件参数playerID/cityID | 移除即最终毁城；可直接删除永久成果 |
| Cheat1528155583 MakeFreeCity | 调用CityManager.TransferCityToFreeCities | 原生内部对象重建细节 |

HD路径相对本机Workshop/2465378070；原版路径相对Civ6.app/Contents/Assets。均只读，不复制第三方源码。

## 推荐架构（HOW，不改玩法）

以Game Property为持久主账本；City Property以后只是当前城市可重建的关联/兼容投影。不能同时维持两份互相独立权威。初期先增加影子账本核验，确认与既有有效账本一致后才切换读写权威；不在一次补丁中直接放宽所有Owner校验。

建议记录：schema、全局单调serial、稳定uid、revision、foundation证据、当前owner/cityID/plot、生命周期状态；专业Identity与首次完成依据、已确认投资receipt/单位UID、标准化learned模板、以后LegacySet/初始化分支。Pending不可逆投资单独保留阶段，不能把INTENT当已支付，也不能丢掉CONSUMED_CONFIRMED而让用户重复花移民。

不持久化ACTIVE、网络集合/路线、加成载体或Prepared UI为权威；按新Owner资格/总督/当前路线重建。原投资的付款者、历史首次区域ID等保持历史语义；只更新当前关联字段，不把全部旧owner/id字符串盲改成新值。

持久化时机：新身份确认、投资事务阶段变更、模板新增、转移确认、LegacySet首次冻结各自落盘并校验revision；不等转手后读不存在的旧City对象，不靠每帧/每回合全城备份。加载时对已知注册城市做一次一致性核对，旧有效记录可一次迁入；已经丢失的记录不能从现有建筑或猜测Potential自动补造。

## 生命周期映射与毁城隔离

1. 新城创建分配新的单调UID和新generation；已注销旧城即便坐标相同也不能复用。旧DEV token保留为migration alias/历史证据，不能作为长期按Owner编号的生成器。
2. CityConquered若实测可用，旧Owner+已注册位置定位旧UID，新Owner/newCityID+实际位置校验新端点；重复同迁移revision无操作。它不提供旧city ID，旧映射必须在事件前已经落盘。
3. CityRemovedFromMap先标记暂离/待核对，不能立刻注销；CityAddedToMap/CityInitialized/CityTransfered只作为候选信号，读取实际对象再决定。未知事件参数必须原样记录，而不是按UI先例猜参数。
4. 同位置存在新Owner本身不足以证明同一城市。必须结合转移事件、原绑定、未发生新建/已注销证据；不确定则保留原账本并暂停关联，不静默授予，也不删除成果。若只有移除+新增，先验证在同一事件批次是否能与CityBuilt明确区分。
5. 确认毁城写tombstone，保留审计，清理当前关联。建城generation另起。没有可靠毁城终结事件时需明确记录支持边界，不能用固定超时猜死亡。
6. 保存读档重建由持久主记录与当前关联校验；不能依赖B063 Record内存或聊天截图。关联只完成一半时停在可解释状态，不以旧位置直接复活记录。多键存储需pending/commit恢复协议，不能声称多次SetProperty原子。
7. 无论新Owner是否启用，都跟踪已登记UID转移并保留永久数据；只对启用Owner应用收益。自由城市/AI持有时不因资格false跳过生命周期记录，返回时再重算ACTIVE。不能把所有AI城市都扫描、自动获得本Mod资格。

## 方案比较

| 方案 | 评价 |
|---|---|
| 只保留City Property | 两种易主路径现有证据不支持，排除 |
| Game Property完整账本 + 经验证转移映射 | 推荐；不依赖City保留数据，适合receipt/模板表，已有读写先例 |
| Plot Property全量账本 | HD有标记先例，可做辅助；毁城重建容易串账且仍需生命周期，不能仅以坐标永续继承 |
| 虚拟建筑储存完整身份/投资 | 可做收益载体，无法自然承载完整receipt/模板历史，且征服移除/替代规则另需测试；不作为主账本 |
| 仅转移事件到来时抢救旧City | 可能已经太迟，不采用作为唯一保存时机 |

## 下一最小实施/验证门槛

下一版先做独立影子账本和有上限的事件日志，不应用继承/不改收益：自动对当前合法原始账本建立快照，在已有写入点保持同步；记录CityConquered/Transfered/Added/Removed/Initialized/CityBuilt实际参数顺序与端点存在性。只记录相关已登记城市/事件，无周期全扫描。

该版完成本地模拟后，用户再做一组易主前后+读档观察：整局快照仍有3笔投资/6模板，City Property可丢失但完整主记录保留，事件指出新Owner/ID；不要求现在重复同样的只读B063测试。赠送和自由城事件覆盖不能由当前截图替代。若事件仍无法安全关联，再针对缺口给一个测试，而非扩大到十几个异常场景。

本轮未新增LOCAL_SIMULATION_PASS：没有实现上述账本协议，不能以文字方案当已测。已有B063模拟不证明新协议。当前无需要用户改Design的结论；已有丢失数据的测试局不自动恢复，后续测试优先使用易主前保存的副本。
