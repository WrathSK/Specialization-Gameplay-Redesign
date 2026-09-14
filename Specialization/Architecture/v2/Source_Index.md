# 源码入口与注册证据索引

Source commit: `e3651f9b7c90110f3a8890a7b12ca299996b306b`

这是静态注册索引，不证明该事件在当前游戏API中存在或实际发出。源码链接行号以本commit为准。

| Action | ID | Entry |
| --- | --- | --- |
| AddUserInterfaces | SPC_B054_Eligibility | UI/DiscountEligibility.xml |
| AddUserInterfaces | SPC_B051_Background | UI/CopyYieldRefresh.xml |
| AddUserInterfaces | SPC_B036_IndustryRefresh | UI/IndustryRefresh.xml |
| AddUserInterfaces | SPC_B035_GPPRefresh | UI/GPPRefresh.xml |
| AddGameplayScripts | SPCP0_Gameplay | Gameplay.lua |
| AddUserInterfaces | SPCP0_UI | UI/P0Panel.xml |
| AddUserInterfaces | SPCP0_BackgroundRoutes | UI/BackgroundRoutes.xml |
| AddUserInterfaces | SPC_B068_CityPotential | UI/CityPotential.xml |
| AddUserInterfaces | SPC_B040_UnitSites | UI/UnitSites.xml |
| AddUserInterfaces | SPC_B041_TargetMarkers | UI/UnitTargetMarkers.xml |
| AddUserInterfaces | SPC_B043_UnitPanelActions | UI/UnitPanelActions.xml |
| ReplaceUIScript | SPC_B046_ProjectOrder | {'LoadOrder': '150100', 'LuaContext': 'ProductionPanel', 'LuaReplace': 'UI/CrewProjectOrder.lua'} |
| AddUserInterfaces | SPC_B055_Background | UI/BoostRefresh.xml |
| AddUserInterfaces | SPC_B059_Dialogue | UI/DialogueRefresh.xml |

## 模块清单与SHA256

| Module | SHA256 | Lifecycle |
| --- | --- | --- |
| BindingProbe.lua | ce6a8e07186332f424975da95daefa0b6af47eaa5a99e58b6e098d70693b126b | see Gameplay Start / UI manifest / helper include |
| BoostConfig.lua | 05c07baa343ff4f97cee940a24d328051af41095bc9d134d1b92b2eb763f6ef5 | see Gameplay Start / UI manifest / helper include |
| BoostIntegerConfig.lua | 8e43d3e3ce29758d770f58682cd53e8d8abba7659f2587b3226a62881a4f65ab | see Gameplay Start / UI manifest / helper include |
| CityFlowProbe.lua | a6a5eb9462f9a951274c259b84473e29460683d8f3bbab7a196b2018b0c19bf9 | see Gameplay Start / UI manifest / helper include |
| CityInheritance.lua | 98867d60bdc7d612842744e432d344743a05e2341b8b578458153b66d32a4618 | ISOLATED NOT STARTED |
| CityInheritanceRead.lua | 1ada898e632edcadc7ebfba549a6c312c47a98090f0838e3be999a1388d2b446 | ISOLATED NOT STARTED |
| CityJournalProbe.lua | d13212a7595fe383819ea5903b2f8c99c0a2ac537e7945fcf8d735784d3d4cbc | see Gameplay Start / UI manifest / helper include |
| CommerceConvergence.lua | d9b3836b2a43fd32385540312684c0b8a635c7161adde865145fc593e665d9ce | see Gameplay Start / UI manifest / helper include |
| CompletionProbe.lua | ef57f13f62a300f0cc06b7871ac038a5d1aad303f9aeb56ea0e16d88d6030c0b | see Gameplay Start / UI manifest / helper include |
| CompletionRecordProbe.lua | 4c1d6cc4cdd1555cd04fce2a6c7240ef0c1f38d212bee61bf6252e78fa0028cd | see Gameplay Start / UI manifest / helper include |
| ConstructionProbe.lua | fd5dfd146b376a96730321558f2da4e1585449ac7f9a906528acf70cae753127 | see Gameplay Start / UI manifest / helper include |
| CopyYields.lua | 5e8a29f472e48c17d56fefe0db9a10d564058177d01f2c2b5b11e10a7bfa8d73 | see Gameplay Start / UI manifest / helper include |
| CrewPrecision.lua | e086354e1662445191f7518bcf97ce43dba09fe855b60ebcb3d199fb8fbc4215 | see Gameplay Start / UI manifest / helper include |
| CrewProjects.lua | 8a5ccef4800620a2069dc45965178538e36e295c9891f6bd071051c742889425 | see Gameplay Start / UI manifest / helper include |
| DiagnosticLog.lua | fd4c52434a868a69f74177321a8588aef51ea3e55cc4b0e5d53715ca0b780db3 | see Gameplay Start / UI manifest / helper include |
| Dialogue.lua | d1f7980a3e2d0f9eabbdaa056d0d8184db1f252e10e008ee093ace696e44e057 | see Gameplay Start / UI manifest / helper include |
| DialogueModel.lua | a85b4ce35ef2a1558ce8462e65c401d30d4b1de8bca44f6488674a0b1240b607 | see Gameplay Start / UI manifest / helper include |
| EffectiveFacts.lua | eef44026a81b5c6ba31187a0c52eedc47f41190e46cf1483d25086f935bcbdf8 | see Gameplay Start / UI manifest / helper include |
| EligibilityProbe.lua | 6904268ee4a306c4bfeffb4d40f55b046d807a74d66c0c62a253e5e2b602385e | see Gameplay Start / UI manifest / helper include |
| EnvelopeProbe.lua | 2d48e35e287b3502c1a3e44bf10f77f12ee1da391228d2b4145e709153ed51cf | see Gameplay Start / UI manifest / helper include |
| FreshBindingHook.lua | c7bdef1fe0612731a95cadf4227df25281c45c9d23ff0a7347be6a19aecb60bd | see Gameplay Start / UI manifest / helper include |
| GPPReadout.lua | 94e5f5543a50a751bb64c1bce17fb9d141cebb5e32d356b721f002a43364c243 | see Gameplay Start / UI manifest / helper include |
| Gameplay.lua | 68464481a7a5a12c6ce40fd7edd67938b52902e13fed563ac64cac66f1bfa791 | see Gameplay Start / UI manifest / helper include |
| GreatWorkAdjacency.lua | ae99c82466ac700ea2a71e5b23c08515fd6c8fe4d0bea3c228890a0832f22697 | see Gameplay Start / UI manifest / helper include |
| GreatWorkAdjacencyModel.lua | f00c1b4a8fa056b86d44e8597ea3c193e46489f4ccfa8e12957c56ec61ad30e4 | see Gameplay Start / UI manifest / helper include |
| GreatWorkProbe.lua | 8c8b7e1d85190d0ffd60c7922aafd5cacc0e968823c85b057a8cfed9e43721db | see Gameplay Start / UI manifest / helper include |
| HalfYieldProbe.lua | aef824eb6fc83cc064d42908dbbefa91ba96099408ee09324f42cb0c6e25f499 | see Gameplay Start / UI manifest / helper include |
| IndustrySupport.lua | 9b2e52d7e20171444090daae1d69099f27a684394a54391ce6641ef3fb0df825 | see Gameplay Start / UI manifest / helper include |
| InheritanceShadow.lua | a7a109b518a449ed31ab9d3a525fce929625de2a0235d5d50b4af3bf910a26e1 | ISOLATED NOT STARTED |
| InvestmentAction.lua | dc2b76792302c7227d8c0f78da200e254eec477bddc962596db4394aa91640b2 | see Gameplay Start / UI manifest / helper include |
| Lv2GPP.lua | d4fee59c5a06d12211e05b9e6580683b3e66d38584ecd89267ada488b71dd788 | see Gameplay Start / UI manifest / helper include |
| Lv2Housing.lua | f7ba314a03f16d8afbf5c7b638037c50299050fa9d1308795a40a3f8b3188b50 | see Gameplay Start / UI manifest / helper include |
| Lv3Effects.lua | e87290464fac9d8a0dd90c93abd8facd4808cade06cc8bec28e48d3d9d727a22 | see Gameplay Start / UI manifest / helper include |
| Lv3Support.lua | e35e9d33e46a16e52d8bb959948b94b3838585e25cf2d6d039eaa01b74ba3916 | see Gameplay Start / UI manifest / helper include |
| Lv4CopyRead.lua | 5d58f139be76577107a7dda0f0088ad81cecaed49ca7c52653e40508369c627c | see Gameplay Start / UI manifest / helper include |
| Lv4Percent.lua | 25985f5336dfbc0bfb273f57a459ddd1dfe7051a19bb79a71352ea69cc90869a | see Gameplay Start / UI manifest / helper include |
| NetworkBoost.lua | 7757d3ebcf9289fc50d59ef5a194107da36b207dfd1717cfbdea73600e9b5bfd | see Gameplay Start / UI manifest / helper include |
| NetworkBridge.lua | 8d96e94493e1591e465e867d7183c85dbdcb9afbd3f98d1c944af20f5ec541a5 | see Gameplay Start / UI manifest / helper include |
| NetworkSender.lua | d7edcb8cf3f2dc5989861747661ecb8e0f40c93129cfd887c021718113924257 | see Gameplay Start / UI manifest / helper include |
| PerformanceCounters.lua | a49906fe65651d55cf810150b32777d1565a74ed1575cc1ec9ac76de79301c90 | see Gameplay Start / UI manifest / helper include |
| Probe.lua | 1f24b95f7fdbf63188b2b2a288b7cc5103980882637318c047a6912cba17090a | see Gameplay Start / UI manifest / helper include |
| PurchaseProbe.lua | 6cc99d4d0c86a3c27139c375212fec90f6c061ba21ab7e15ed05d28dec80e5f3 | see Gameplay Start / UI manifest / helper include |
| PurchaseProbeRead.lua | 8b01b03284548636d531d2305cdd70cdfc11a3f7f25f4acb5e0d53269c64ea24 | see Gameplay Start / UI manifest / helper include |
| QualificationProbe.lua | ba50636c2b083a9787126295470572561e10d405eb998d117492bef89a728a59 | see Gameplay Start / UI manifest / helper include |
| ResearchSupport.lua | dc436a43f10874765aff8ad75fb07e94c5e618ba4b5048638cbaa61dca5a6d6a | see Gameplay Start / UI manifest / helper include |
| ShadowRouteState.lua | 6f35992fd9e5b8d2429061acbaf83e3f7747300592bf050dbb23e1e5fe9163e6 | see Gameplay Start / UI manifest / helper include |
| SourceYieldProbe.lua | 64d9e41633024f4db8526d3c74504a6aeae3bc4b4bbd1e142fafa91a75cc3a4e | see Gameplay Start / UI manifest / helper include |
| Standardization.lua | db9a68bcd5d94790b486f3ad8e2c82b77abb955f5ccb302eede352dd7ce6e8a4 | see Gameplay Start / UI manifest / helper include |
| StandardizationCatalog.lua | df4f28def5d5bca9ed1bc947b89a46149dc6b19d475a34122063b51974c80bfa | see Gameplay Start / UI manifest / helper include |
| StandardizationDiscount.lua | 54893359d06bb501dd7431a47d429a093e232946da94590cc5a19c7d60f12866 | see Gameplay Start / UI manifest / helper include |
| StorageProbe.lua | 49834f4b4f360feafba9185081041dca55a450f1eeee67fae7bd1ce3bab85d4f | see Gameplay Start / UI manifest / helper include |
| TradeRouteProbe.lua | d87d68674052a1acd2c280dce5b1280b7fd47d8cb61c7cf4ea094a4d324572a1 | see Gameplay Start / UI manifest / helper include |
| UI/BackgroundRoutes.lua | 847add4e3fc5f862249d2d502adc80b1d3619a1f1537103edca4ccd1e22a7887 | see Gameplay Start / UI manifest / helper include |
| UI/BoostGreatWorkRead.lua | 2c73c0cc0b9146f8b5900f8ac155455a5293c0a889d693d8907527fa766d31e9 | see Gameplay Start / UI manifest / helper include |
| UI/BoostRefresh.lua | efa5ada911a77781831f8dfa3a04c34974e404b989159a7b1c3cffae8d777cbf | see Gameplay Start / UI manifest / helper include |
| UI/CityPotential.lua | bf7befbeed9efcc929fd8749e3a3cf727ec7582fa1792246a4a87c969df7d960 | see Gameplay Start / UI manifest / helper include |
| UI/CopyYieldRefresh.lua | 041eae1f478d758305da1452835d0eb4ebca0450c2aa7d1b5eb52528048e0f02 | see Gameplay Start / UI manifest / helper include |
| UI/CrewProjectOrder.lua | 8b902c93e450e5ffcf6620bd5154382c36f38b34418cd1aa0856da661cf45522 | see Gameplay Start / UI manifest / helper include |
| UI/DialogueRefresh.lua | 6effcde38e15b3b2d8877a60b616120cf4f2d76f02f40205b7d208d299c00aa5 | see Gameplay Start / UI manifest / helper include |
| UI/DiscountEligibility.lua | 9f573d28d1b9649084c71eb25d248eb1e5c6a506997db31bdea62f0d7a272e84 | see Gameplay Start / UI manifest / helper include |
| UI/GPPRefresh.lua | 6064f761608590e35314447145e9f746f699fbb3cbbcc714b8c608b2a55d8162 | see Gameplay Start / UI manifest / helper include |
| UI/GreatWorkBasis.lua | c76edc36a68408e790c0ff1d7bd05e5df0b11b473c6efb2baa0f54006f59574c | see Gameplay Start / UI manifest / helper include |
| UI/IndustryRefresh.lua | 1a15bd030515008cab22f859bb1c419941cf78294cd76d9c3944d2c78129f3a4 | see Gameplay Start / UI manifest / helper include |
| UI/P0Panel.lua | cb012cb8e2f4b60874f2bf976a3f0952b7426a78ced53b7934867304a43c8ac5 | see Gameplay Start / UI manifest / helper include |
| UI/UnitPanelActions.lua | 49491d8ff7de48f8cbf24c1d90789878fcfaf7b81857c129113e2e4a0497e91c | see Gameplay Start / UI manifest / helper include |
| UI/UnitSites.lua | 98e70745fdbc14aef01492d75487555b85ae260d23ff894bd03b242a57c042ff | see Gameplay Start / UI manifest / helper include |
| UI/UnitTargetMarkers.lua | 037d291fb402a3220e639e1f8bb05eb16f0374565c0cc31e95d60e7bb8e73a3d | see Gameplay Start / UI manifest / helper include |
| UnitActionSitePolicy.lua | 2ff1d9e151678a564e91a45a8324e320917eff617f86db8789b7ce068479dd7d | see Gameplay Start / UI manifest / helper include |
| UnitActions.lua | 0e87494ff86dbc2dd211865b092853025fec315272bac65e04129593b014e02b | see Gameplay Start / UI manifest / helper include |
| UnitSiteProbe.lua | f54c582cc46ba965ddbfc3c631dcba198bbb2663e14d982693d0503b8c7f1d43 | see Gameplay Start / UI manifest / helper include |
| UnitTargets.lua | 66f58e958a7ee1ebd4d0e19c2ed6b81c0db9e0e09e89562eaddfde613b88b08f | see Gameplay Start / UI manifest / helper include |
| YieldCarrierProbe.lua | 6f91b0f71c9811034da652c18bcb1a2e643a6b15fce41e963bdd36f44be3f22e | see Gameplay Start / UI manifest / helper include |

## 注册、桥接、持久写入的原文定位

包含循环声明上下文；辅助函数定义也保留以便核对间接注册。isolated文件不计当前活动listener。

### BindingProbe.lua

```text
1: -- B013 DEV-only. Never produces a specialization or a production UID.
2: SPCBindingProbe={}
3: function SPCBindingProbe.Start(P,shared)
4:  if shared.BindingProbe then return end
24:  end
25:  local function ledger(pid)
26:   local v=Game:GetProperty(key(pid))
27:   if v==nil then return nil end
41:  local function inspect(pid,city)
42:   assert(city and city:GetOwner()==pid,"CITY_OWNER_MISMATCH")
43:   local v=ledger(pid);local token=city:GetProperty(TOKEN)
44:   local r=v and v.records[tostring(city:GetID())]
73:   assert(same(ledger(pid),before,0),"STALE_LEDGER")
74:   b.gameWrites=b.gameWrites+1
75:   pcall(function() P.SetProperty(Game,key(pid),next) end)
76:   assert(same(ledger(pid),next,0),"GAME_WRITE_UNCONFIRMED")
91:    if old==nil then
92:     -- DEV bootstrap only: a missing ledger must not strand extant city tokens.
93:     for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan'); assert(c:GetProperty(TOKEN)==nil,"TOKEN_WITHOUT_LEDGER") end
94:    end
101:    city=CityManager.GetCity(pid,cid)
102:    assert(city and city:GetID()==cid and city:GetOwner()==pid and city:GetX()==x and city:GetY()==y
103:     and city:GetProperty(TOKEN)==nil,"CITY_CHANGED_BEFORE_WRITE")
104:    b.cityWrites=b.cityWrites+1;pcall(function() P.SetProperty(city,TOKEN,uid) end)
105:    assert(city:GetProperty(TOKEN)==uid,"CITY_WRITE_UNCONFIRMED")
106:    local confirmed=clone(next);confirmed.records[tostring(cid)].state="CONFIRMED"
107:    gameWrite(pid,b,next,confirmed)
108:    assert(inspect(pid,city)=="BOUND_MATCH","FINAL_BINDING_MISMATCH")
109:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'BindingProbe.lua') end
110:    b.last="NEW_CITY_BOUND"
111:    if shared.OnFreshCityBinding then shared.OnFreshCityBinding(pid,city) end
112:   end)
115:   print("[SPC][B013][BINDING] city="..tostring(cid).." "..b.last)
116:  end
117:  local function listen(ns,name,fn)
118:   local e=P.Field(ns,name)
119:   if e and type(e.Add)=="function" then
120:    local ok=pcall(e.Add,fn);data.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
121:   else data.hooks[name]="ABSENT" end
122:  end
123:  listen(GameEvents,"CityBuilt",foundation)
124:  listen(Events,"LoadScreenClose",function()
125:   data.phase="AFTER_LOAD_CLOSE"
```

### CityFlowProbe.lua

```text
1: -- B021 DEV normal-save recovery; existing matched records only, no missing-history adoption.
2: SPCCityFlowProbe={}
3: function SPCCityFlowProbe.Start(P,shared)
4:  local KEY="SPC_DEV_CITY_FLOW_B020"
20:  end
21:  local function read(pid,city)
22:   local v=city:GetProperty(KEY);if v==nil then return nil end
23:   local token=identity(pid,city)
36:   assert(same(read(pid,city),old),"STALE_FLOW")
37:   assert(identity(pid,city)==nextValue.token,"WRITE_IDENTITY_CHANGED")
38:   b.writes=b.writes+1;pcall(function() P.SetProperty(city,KEY,clone(nextValue)) end)
39:   assert(same(read(pid,city),nextValue),"FLOW_WRITE_UNCONFIRMED")
40:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'CityFlowProbe.lua') end
41:  end
62:    local city=CityManager.GetCity(e.owner,e.cityID);assert(identity(e.owner,city)==e.token,"FRESH_CHANGED")
63:    assert(read(e.owner,city)==nil,"NO_EXISTING_ADOPTION")
64:    local target=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
65:    assert(target and target.specialization=="NONE" and target.health=="TRACKING","FRESH_TARGET_CHANGED")
87:    local d=CityManager.GetDistrictAt(x,y);assert(d,"DISTRICT_UNAVAILABLE")
88:    local city=d:GetCity();assert(city and city:GetOwner()==pid and d:GetOwner()==pid and d:GetType()==index,"EVENT_IDENTITY")
89:    local raw=city:GetProperty(KEY)
90:    if raw==nil then bucket(pid).last="UNTRACKED_NO_WRITE";return end
94:    if old.facts.specialization~="NONE" then bucket(pid).last="LOCK_PRESERVED_NO_WRITE";return end
95:    local j=shared.CityJournalProbe.players[pid];assert(j and not j.halted,"LEGACY_COMPLETION_HELD")
96:    local target=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
97:    assert(target and target.health=="TRACKING" and target.token==token,"LEGACY_RECORD_INVALID")
122:   local v=read(pid,city)
123:   assert(v and v.stage=="DONE" and data.active[v.token],"SUPPORT_RECORD_NOT_ACTIVE")
124:   assert(same(v.facts,city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")),"SUPPORT_JOURNAL_MISMATCH")
125:   return clone(v.facts)
133:    and data.hooks.complete=="REGISTERED","LOAD_LISTENERS_NOT_READY")
134:   local b=j.players[pid];assert(b and not b.halted,"LOAD_LEGACY_HELD")
135:   local source=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
136:   assert(same(v.facts,source),"LOAD_SOURCE_MISMATCH")
160:  end
161:  local event=P.Field(GameEvents,"OnDistrictConstructed")
162:  if event and event.Add then local ok=pcall(event.Add,complete);data.hooks.complete=ok and "REGISTERED" or "ERROR" end
163:  local load=P.Field(Events,"LoadScreenClose")
164:  if load and load.Add then load.Add(function()
165:   data.ready=true
```

### CityInheritance.lua

```text
1: -- B066 existing-identity transfers only; no Claim or missing-history invention.
2: SPCCityInheritance={KEY='SPC_CITY_INHERITANCE_V1'}
3: function SPCCityInheritance.Start(P,shared)
4:  local KEY=SPCCityInheritance.KEY
12:  end
13:  local function read()
14:   local v=Game:GetProperty(KEY);if v==nil then return {schema=1,records={}} end
15:   assert(type(v)=='table' and v.schema==1 and type(v.records)=='table','INHERIT_BAD_LEDGER');return cp(v)
16:  end
17:  local function save(v) Game:SetProperty(KEY,cp(v));assert(eq(read(),v),'INHERIT_WRITE_FAILED') end
18:  local function shadow() return Game:GetProperty('SPC_INHERITANCE_SHADOW_V1') or {records={}} end
19:  local function valid(s)
33:  function d.Resolve(pid,c)
34:   local r=find(read(),pid,c:GetID())
35:   if r and r.x==c:GetX() and r.y==c:GetY() and c:GetProperty(TOKEN)==r.uid and (r.status=='APPLIED' or d.applying) then return r.uid,'BOUND_MATCH' end
36:  end
54:   valid(r.source);local a=projection(r)
55:   -- Validate all fields before the first write. Resume only our exact partial projection.
56:   for k,key in pairs(fields) do local now=c:GetProperty(key);assert(now==nil or eq(now,a[k]),'INHERIT_CITY_CONFLICT') end
57:   r.status='PROJECTING';save(v)
59:   local ok,e=pcall(function()
60:    for _,k in ipairs({'JOURNAL','FLOW','INVEST','TEMPLATES','TOKEN'}) do
61:     if a[k]~=nil and not eq(c:GetProperty(fields[k]),a[k]) then c:SetProperty(fields[k],cp(a[k]));assert(eq(c:GetProperty(fields[k]),a[k]),'INHERIT_CITY_WRITE_FAILED') end
62:    end
66:   d.applying=false;assert(ok,e)
67:   v=read();r=v.records[uid];r.status='APPLIED';save(v);d.changes=d.changes+1
68:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'INHERIT_APPLIED') end
69:   -- Reuse existing absolute reconciliation, never copy old ACTIVE or route sets.
90:   if p.s.owner==p.owner and p.s.cityID==p.id and (not p.r or p.s.revision>p.r.source.revision) then s=p.s end
91:   valid(s)
92:   local existing=c:GetProperty(TOKEN);assert(existing==nil or existing==p.uid,'INHERIT_DEST_TOKEN_CONFLICT')
93:   local r=p.r or {uid=p.uid,x=x,y=y,revision=0}
99:   local ok,e=pcall(fn,...);if not ok then local code=tostring(e):match('INHERIT_[A-Z_]+') or 'INHERIT_ERROR';d.errors.last=code;print('[SPC][B066] '..tostring(e)) end
100:  end
101:  local function hook(ns,n,fn) local e=ns and ns[n];if e and type(e.Add)=='function' then e.Add(function(...) safe(fn,...) end) end end
102:  hook(GameEvents,'CityConquered',function(newpid,oldpid,cid,x,y) transfer(newpid,cid,oldpid,x,y,'CityConquered') end)
103:  hook(Events,'CityTransfered',function(pid,cid)
104:   if type(pid)~='number' or type(cid)~='number' then return end
105:   local c=CityManager.GetCity(pid,cid);if c then transfer(pid,cid,nil,c:GetX(),c:GetY(),'CityTransfered') end
106:  end)
107:  hook(GameEvents,'CityBuilt',function(pid,cid,x,y)
108:   if not d.ready then return end
118:   if changed then save(v) end
119:  end)
120:  hook(Events,'LoadScreenClose',function()
121:   d.ready=true
```

### CityInheritanceRead.lua

```text
1: -- B063 read-only observer. Coordinates locate a watched plot, NOT an adopted permanent UID.
2: SPCCityInheritanceRead={}
3: function SPCCityInheritanceRead.Start(P,shared)
4:  local d={watch={}};shared.CityInheritanceRead=d
10:  local function sample(c)
11:   local s={owner=c:GetOwner(),id=c:GetID(),x=c:GetX(),y=c:GetY(),values={},districts={}}
12:   for k,key in pairs(keys) do s.values[k]=copy(c:GetProperty(key)) end
13:   for _,d in Players[s.owner]:GetDistricts():Members() do local city=d:GetCity()
```

### CityJournalProbe.lua

```text
1: -- B015 DEV submission experiment; not a permanent UID or production specialization.
2: SPCCityJournalProbe={}
3: function SPCCityJournalProbe.Start(P,shared)
4:  if shared.CityJournalProbe then return end
35:  local function read(pid,city)
36:   local token,state=shared.BindingProbe.Resolve(pid,city);assert(token,"BINDING_UNVERIFIED "..tostring(state))
37:   local v=city:GetProperty(KEY)
38:   if v~=nil then
54:   assert(equal(read(pid,city),old,0),"STALE_JOURNAL")
55:   b.writes=b.writes+1
56:   pcall(function() P.SetProperty(city,KEY,nextValue) end)
57:   assert(equal(read(pid,city),nextValue,0),"WRITE_UNCONFIRMED")
58:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'CityJournalProbe.lua') end
59:  end
81:  end
82:  -- Called only AFTER B013 creates a NEW confirmed binding, not on duplicate or load.
83:  shared.OnFreshCityBinding=function(pid,city)
84:   if not P.IsTestPlayer(pid) or j.phase~="AFTER_LOAD_CLOSE" then return end
116:    city=d:GetCity();assert(city and city:GetOwner()==pid and d:GetOwner()==pid and d:GetType()==index,"EVENT_OWNER_OR_TYPE_CONFLICT")
117:    run(pid,city,function(b)
118:     local raw=city:GetProperty(KEY)
119:     if raw==nil then b.last="UNTRACKED_NO_WRITE";return end -- no adoption of old cities
134:   local b=bucket(pid)
135:   local ok,line=pcall(function()
136:    local raw=city:GetProperty(KEY)
137:    if raw==nil then return "city="..city:GetID().." | UNTRACKED_NO_WRITE" end
150:   assert(j.phase=="AFTER_LOAD_CLOSE" and not bucket(pid).halted,"INHERIT_JOURNAL_HELD")
151:  end
152:  local function listen(ns,name,fn)
153:   local e=P.Field(ns,name)
154:   if e and type(e.Add)=="function" then local ok=pcall(e.Add,fn);j.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
155:   else j.hooks[name]="ABSENT" end
156:  end
157:  listen(GameEvents,"OnDistrictConstructed",completed)
158:  listen(Events,"LoadScreenClose",function()
159:   j.phase="AFTER_LOAD_CLOSE"
```

### CommerceConvergence.lua

```text
1: -- D0024: independently planned, absolute city-layer integer grants.
2: SPCCommerceConvergence={}
3: function SPCCommerceConvergence.Start(P,shared)
4:  local d={busy=false,ready=false,last={},errors={},mode={},testCity={},baseline={},writes=0};shared.CommerceConvergence=d
100:   return table.concat(rows,'\n')
101:  end
102:  local function hook(t,name) local e=P.Field(t,name);if e and e.Add then e.Add(d.Audit) end end
103:  for _,name in ipairs({'LoadScreenClose','PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','CityWorkerChanged','CityPopulationChanged','CityFocusChanged','CityTransfered'}) do hook(Events,name) end
104:  for _,name in ipairs({'CityBuilt','OnBuildingConstructed','OnDistrictConstructed'}) do hook(GameEvents,name) end
105: end
```

### CompletionProbe.lua

```text
1: -- B011: bounded read-only Gameplay observations; no specialization or Property writes.
2: SPCCompletionProbe={}
3: function SPCCompletionProbe.Start(P,shared)
4:  if shared.CompletionProbe then return end
81:   print("[SPC]["..P.VERSION.."][COMPLETION] "..row.text:gsub("\n"," | "))
82:  end
83:  local function listen(namespace,name,fn)
84:   local e=P.Field(namespace,name)
85:   if e and type(P.Field(e,"Add"))=="function" then
86:    local ok=pcall(e.Add,fn);data.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
87:   else data.hooks[name]="ABSENT" end
88:  end
89:  listen(GameEvents,"CityBuilt",function(pid,cid,x,y) observe("built",pid,cid,x,y) end)
90:  listen(GameEvents,"OnDistrictConstructed",function(pid,typeID,x,y) observe("constructed",pid,nil,x,y,typeID) end)
91:  -- Only the first six documented fields are used; do not guess progress payload positions.
92:  listen(Events,"DistrictAddedToMap",function(pid,did,cid,x,y,typeID) observe("added",pid,cid,x,y,typeID,did) end)
93:  listen(Events,"LoadScreenClose",function() data.phase="AFTER_LOAD_CLOSE" end)
94:  print("[SPC]["..P.VERSION.."][COMPLETION] INITIALIZED; memory-only observations, counters reset per load")
```

### CompletionRecordProbe.lua

```text
1: -- DEV first OBSERVED completion, not a proven historical first specialization.
2: SPCCompletionRecordProbe={}
3: function SPCCompletionRecordProbe.Start(P,shared)
4:  if shared.CompletionRecordProbe then return end
29:  end
30:  local function read(pid,city,token)
31:   local v=city:GetProperty(KEY)
32:   if v==nil then return nil end
74:     districtID=district:GetID(),districtType=info.DistrictType,observedFamily=f,turn=Game.GetCurrentGameTurn()}
75:    assert(integer(v.districtID) and integer(v.turn),"INVALID_EVENT_FIELDS")
76:    assert(shared.BindingProbe.Resolve(pid,city)==token and city:GetProperty(KEY)==nil,"STALE_BINDING_OR_RECORD")
77:    b.writes=b.writes+1;pcall(function() P.SetProperty(city,KEY,v) end)
78:    local after=read(pid,city,token);assert(after,"WRITE_UNCONFIRMED")
84:   print("[SPC][B014][RECORD] "..b.last)
85:  end
86:  local function listen(ns,name,fn)
87:   local e=P.Field(ns,name)
88:   if e and type(e.Add)=="function" then local ok=pcall(e.Add,fn);d.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
89:   else d.hooks[name]="ABSENT" end
90:  end
91:  listen(GameEvents,"OnDistrictConstructed",onComplete)
92:  listen(Events,"LoadScreenClose",function() d.phase="AFTER_LOAD_CLOSE" end)
93: end
```

### ConstructionProbe.lua

```text
1: -- B039 explicit DEV grant, not a Crew/project or unit-consumption implementation.
2: SPCConstructionProbe={}
3: function SPCConstructionProbe.Start(P,shared)
4:  local data={};shared.ConstructionProbe=data
```

### CopyYields.lua

```text
11:  return {integer=integer,bit=bit,coefficient=coefficient,amount=amount}
12: end
13: function SPCCopyYields.Start(P,shared)
14:  local data={ready=false,busy=false,generation=0,samples={},seq={},receiveErrors={},errors={},last={},changes=0};shared.CopyYields=data
138:   end
139:   lines[#lines+1]='原生总量 Science='..c:GetYield(P.Info('Yields','YIELD_SCIENCE').Index)..' / Production='..c:GetYield(P.Info('Yields','YIELD_PRODUCTION').Index)
140:   if c:GetProperty('SPC_B050_HALF_ENABLED') then lines[#lines+1]='注意：B050半点实验仍开启，请先Half OFF。' end
141:   lines[#lines+1]='读取不触发刷新；已配置不是实测增量。'
142:   return table.concat(lines,'\n')
143:  end
144:  local function hook(source,n,f) local e=P.Field(source,n);if e and e.Add then e.Add(f) end end
145:  -- Only lifecycle cleanup visits ineligible owners; no periodic specialization work for them.
152:   end end
153:  end
154:  hook(Events,'LoadScreenClose',function() data.ready=true;data.generation=data.generation+1;data.samples={};data.seq={};data.receiveErrors={};cleanupDormant();data.Audit() end)
155:  hook(Events,'CityTransfered',cleanupDormant)
156:  for _,n in ipairs({'PlayerTurnActivated','CityPopulationChanged','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','CityTransfered','DistrictRemovedFromMap'}) do hook(Events,n,data.Audit) end
157: end
```

### CrewPrecision.lua

```text
1: -- B046 observation only. No retries, setters, grant, rounding or consumption.
2: SPCCrewPrecision={}
3: function SPCCrewPrecision.Start(P,shared)
4:  local function before(pid,params)
```

### CrewProjects.lua

```text
1: -- B044 derived access only. The engine completes projects and grants units; no Lua grant replay.
2: SPCCrewProjects={}
3: function SPCCrewProjects.Start(P,shared)
4:  local data={ready=false,busy=false,errors={}};shared.CrewProjects=data
42:   data.busy=false
43:  end
44:  local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
45:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
46:  for _,n in ipairs({'PlayerTurnActivated','CityTransfered','DistrictBuildProgressChanged','DistrictRemovedFromMap','CityProductionCompleted'}) do hook(Events,n,data.Audit) end
47:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
48: end
```

### Dialogue.lua

```text
1: include('DialogueModel')
2: SPCDialogue={}
3: function SPCDialogue.Start(P,shared)
4:  local d={ready=false,busy=false,seq={},samples={},off={},test={},last={},errors={},changes=0,received={},generation=1};shared.Dialogue=d
106:  local function auditAll() for pid in pairs(Players) do d.Audit(pid) end end
107:  for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','PlayerTurnActivated','PlayerTurnDeactivated'}) do
108:   local e=P.Field(Events,name);if e and e.Add then e.Add(auditAll) end
109:  end
110:  local e=P.Field(Events,'CityTransfered');if e and e.Add then e.Add(function() d.ready=false;d.samples={};d.last={};d.Init();auditAll() end) end
111: end
```

### EffectiveFacts.lua

```text
1: -- B032: native read-only investment overlay. No Property writes or unit actions.
2: SPCEffectiveFacts={}
3: function SPCEffectiveFacts.Start(P,shared)
4:  local KEY='SPC_DEV_INVESTMENT_LEDGER_V1'
15:   local f=shared.CityFlowProbe.SupportFacts(pid,city)
16:   assert(f.owner==pid and f.cityID==city:GetID() and type(f.token)=='string','EFFECTIVE_FOUNDATION_IDENTITY')
17:   local ledger=city:GetProperty(KEY)
18:   local n=0
```

### EligibilityProbe.lua

```text
1: -- B016 read-only Gameplay diagnostics. Never a production gate or persistent fact.
2: SPCEligibilityProbe={}
3: function SPCEligibilityProbe.Start(P,shared)
4:  local trait="TRAIT_CIVILIZATION_SPC_TEST" -- explicit current carrier configuration only
45:  end
46:  local e=Events and Events.LoadScreenClose
47:  if e and type(e.Add)=="function" then
48:   local ok=pcall(e.Add,function() sample("LOAD_CLOSE") end)
49:   data.hooks.LoadScreenClose=ok and "REGISTERED" or "ERROR"
```

### EnvelopeProbe.lua

```text
28: local names={ [0]="EMPTY", "BEFORE_PENDING", "TARGET_PENDING", "DONE", "BEFORE_PENDING", "TARGET_PENDING", "DONE" }
29: local chinese={ [0]="空白测试记录", "计划已记；成果未写", "成果已写；待对账", "对账完成", "第二笔计划已记", "第二笔成果已写；待对账", "两笔均已完成" }
30: function M.Start(P,shared)
31:  local data={version=P.VERSION,players={},ready=false,hook="ABSENT"};shared.EnvelopeProbe=data
32:  local function read(pid)
33:   local ok,v=pcall(function() return Game:GetProperty("SPC_DEV_ENVELOPE_B019_P"..pid) end)
34:   if not ok then return nil,"READ_ERROR" end
52:     else
53:      b.attempts=b.attempts+1
54:      local ok=pcall(function() P.SetProperty(Game,"SPC_DEV_ENVELOPE_B019_P"..pid,M.Expected(pid,step+1)) end)
55:      local after=read(pid)
81:   end
82:  end
83:  if Events and Events.LoadScreenClose and Events.LoadScreenClose.Add then
84:   local ok=pcall(function() Events.LoadScreenClose.Add(onLoad) end)
85:   data.hook=ok and "REGISTERED" or "REGISTER_FAILED"
```

### FreshBindingHook.lua

```text
5:  assert(context=="DEV_ONLY","DEV_SCOPE_REQUIRED")
6:  assert(type(observer)=="function" and not shared.FreshHookCandidate,"OBSERVER_OR_SINGLE_INSTALL")
7:  local legacy=shared.OnFreshCityBinding
8:  assert(type(legacy)=="function" and shared.CityJournalProbe and shared.BindingProbe,"INSTALL_AFTER_B015")
19:   local function verify()
20:    assert(ok,err)
21:    assert(not b.halted and shared.OnFreshCityBinding==wrapper,"HOOK_CHANGED_OR_HALTED")
22:    assert(P.IsTestPlayer(pid) and journal.phase=="AFTER_LOAD_CLOSE","OUTSIDE_FRESH_PHASE")
27:    local token,status=shared.BindingProbe.Resolve(pid,city)
28:    assert(type(token)=="string" and status=="BOUND_MATCH","BINDING_UNCONFIRMED")
29:    local v=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
30:    assert(type(v)=="table" and v.schema==1 and v.kind=="DEV_FOUNDATION_JOURNAL" and v.owner==pid
45:   b.busy=false
46:  end
47:  shared.OnFreshCityBinding=wrapper
48:  return state
```

### Gameplay.lua

```text
333:   end
334:   stage("BEFORE_GET city="..tostring(params.CityID))
335:   local marker=city:GetProperty("SPC_P0_MARKER")
336:   stage("AFTER_GET marker="..P.Scalar(marker))
337:   if params.Action=="MARK_CITY" and marker==nil then
338:     stage("BEFORE_SET")
339:     P.SetProperty(city,"SPC_P0_MARKER",params.Token)
340:     stage("AFTER_SET")
341:     marker=city:GetProperty("SPC_P0_MARKER")
342:     if marker~=params.Token then stage("ERROR_ROUNDTRIP");return end
346:   stage("ACK "..shared.Snapshot)
347: end
348: GameEvents.SPC_P0_Request.Add(function(...)
349:   local ok,err=pcall(request,...)
366: end
367: local tradeEvent=P.Field(Events,"TradeRouteActivityChanged")
368: if tradeEvent and type(tradeEvent.Add)=="function" then
369:   tradeEvent.Add(function(...)
370:     local ok,err=pcall(onTradeActivity,...)
375: -- B004: automatic, read-only operation candidate diagnostics. No route authority.
376: include("TradeRouteProbe")
377: SPCTradeRouteProbe.Start(P,shared)
378:
379: -- B011 read-only completion lifecycle evidence. No state transitions.
380: include("CompletionProbe")
381: SPCCompletionProbe.Start(P,shared)
382:
383: include("StorageProbe")
384: SPCStorageProbe.Start(P,shared)
385:
386: include("BindingProbe")
387: SPCBindingProbe.Start(P,shared)
388:
389: include("CompletionRecordProbe")
390: SPCCompletionRecordProbe.Start(P,shared)
391:
392: include("CityJournalProbe")
393: SPCCityJournalProbe.Start(P,shared)
394:
395: -- B016: automatic read-only qualification evidence; does not replace legacy gates.
396: include("EligibilityProbe")
397: SPCEligibilityProbe.Start(P,shared)
398:
399: include("QualificationProbe")
400: SPCQualificationProbe.Start(P,shared)
401:
402: include("EnvelopeProbe")
403: SPCEnvelopeProbe.Start(P,shared)
404:
405: include("FreshBindingHook")
406: include("CityFlowProbe")
407: SPCCityFlowProbe.Start(P,shared)
408:
409: include("EffectiveFacts")
410: SPCEffectiveFacts.Start(P,shared)
411:
412: include("InvestmentAction")
413: SPCInvestmentAction.Start(P,shared)
414:
415: include("ResearchSupport")
416: SPCResearchSupport.Start(P,shared)
417: include("Lv2Housing")
418: SPCLv2Housing.Start(P,shared)
419: include("Lv2GPP")
420: SPCLv2GPP.Start(P,shared)
421:
422: include("NetworkBridge")
423: SPCNetworkBridge.Start(P,shared)
424:
425: include("IndustrySupport")
426: SPCIndustrySupport.Start(P,shared)
427:
428: include("Lv3Support")
429: SPCLv3Support.Start(P,shared)
430:
431: include("Lv3Effects")
432: SPCLv3Effects.Start(P,shared)
433:
434: include("ConstructionProbe")
435: SPCConstructionProbe.Start(P,shared)
436:
437: include("UnitActionSitePolicy")
438: include("UnitSiteProbe")
439: SPCUnitSiteProbe.Start(P,shared)
440:
441: include("UnitTargets")
442: SPCUnitTargets.Start(P,shared)
443:
444: include("UnitActions")
445: SPCUnitActions.Start(P,shared)
446:
447: include("CrewProjects")
448: SPCCrewProjects.Start(P,shared)
449:
450: include("CrewPrecision")
451: SPCCrewPrecision.Start(P,shared)
452:
453: include("Lv4Percent")
454: SPCLv4Percent.Start(P,shared)
455:
456: include("HalfYieldProbe")
457: SPCHalfYieldProbe.Start(P,shared)
458:
459: include("CopyYields")
460: SPCCopyYields.Start(P,shared)
461:
462: include("StandardizationCatalog")
463: include("Standardization")
464: SPCStandardization.Start(P,shared)
465:
466: include("PurchaseProbe")
467: SPCPurchaseProbe.Start(P,shared)
468:
469: include("StandardizationDiscount")
470: SPCStandardizationDiscount.Start(P,shared)
471:
472: include("NetworkBoost")
473: SPCNetworkBoost.Start(P,shared)
474: include("GreatWorkProbe")
475: SPCGreatWorkProbe.Start(P,shared)
476:
477: include("Dialogue")
478: SPCDialogue.Start(P,shared)
479:
480: include("GreatWorkAdjacency")
481: SPCGWAdjacency.Start(P,shared)
482:
483: include("CommerceConvergence")
484: SPCCommerceConvergence.Start(P,shared)
485:
489: shared.InheritanceShadow=nil
490: shared.CityInheritance=nil
491: shared.OnPermanentCityWrite=nil
492: shared.InheritanceIsolation=true
```

### GreatWorkAdjacency.lua

```text
1: include('GreatWorkAdjacencyModel')
2: SPCGWAdjacency={}
3: function SPCGWAdjacency.Start(P,shared)
4:  local M=SPCGWAdjacencyModel
```

### GreatWorkProbe.lua

```text
1: -- B055 isolated backend comparison. Not automatic era preservation or GW-002 gameplay.
2: SPCGreatWorkProbe={}
3: function SPCGreatWorkProbe.Start(P,shared)
4:  local d={ready=false};shared.GreatWorkProbe=d
35:    ..'\n这是手动实验，不是已完成的时代补贴/50%基础相邻能力。'
36:  end
37:  local e=P.Field(Events,'CityTransfered');if e and e.Add then e.Add(function() if d.ready then d.Clean() end end) end
38: end
```

### HalfYieldProbe.lua

```text
7:  return {bit=bit,coefficient=1/2^(bit+1),subtract=(odd-1)/2}
8: end
9: function SPCHalfYieldProbe.Start(P,shared)
10:  local data={ready=false,busy=false,errors={},baseline={}};shared.HalfYieldProbe=data
34:    local ok,err=pcall(function()
35:     for _,c in p:GetCities():Members() do P.Count('city_scan');
36:      local enabled=c:GetProperty(key)==true
37:      if enabled then
47:  end
48:  function data.Describe(pid,c)
49:   local enabled=c:GetProperty(key)==true;local t=totals(c);local base=data.baseline[pid..':'..c:GetID()]
50:   local text='B050固定半点实验 | city='..c:GetID()..' | '..(enabled and 'ON' or 'OFF')..' | 人口='..t.population
63:   if action=='HALF_ON' then
64:    SPCHalfYieldProbe.Plan(c:GetPopulation())
65:    if c:GetProperty(key)~=true then data.baseline[pid..':'..c:GetID()]=totals(c) end
66:    P.SetProperty(c,key,true);data.ready=true;data.Audit()
67:   elseif action=='HALF_OFF' then
68:    -- Revoke carriers before clearing flag, so an uncertain removal can be retried.
69:    reconcile(pid,c,nil);P.SetProperty(c,key,false);data.errors[pid..':'..c:GetID()]=nil
70:   end
71:   return data.Describe(pid,c)
72:  end
73:  local function hook(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f) end end
74:  hook('LoadScreenClose',function() data.ready=true;data.Audit() end)
75:  for _,n in ipairs({'CityPopulationChanged','PlayerTurnActivated','CityTransfered'}) do hook(n,data.Audit) end
76: end
```

### IndustrySupport.lua

```text
2: -- No actual-adjacency fallback, rounding or city-wide multiplication. Crew access is independently audited.
3: SPCIndustrySupport={}
4: function SPCIndustrySupport.Start(P,shared)
5:  local data={ready=false,busy=false,changes=0,errors={}};shared.IndustrySupport=data
84:    ..'\nRead only; verify native specialist yields. Crew projects available from Industry Lv1; project engine behavior requires B044 testing.'
85:  end
86:  local function hook(source,name,fn) local e=P.Field(source,name);if e and e.Add then e.Add(fn) end end
87:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
88:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','CityTransfered','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','CityWorkerChanged'}) do hook(Events,n,data.Audit) end
89:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
90: end
```

### InheritanceShadow.lua

```text
1: -- B064 shadow only: no city writes, no ownership adoption, no rewards.
2: SPCInheritanceShadow={KEY='SPC_INHERITANCE_SHADOW_V1'}
3: function SPCInheritanceShadow.Start(P,shared)
4:  local KEY=SPCInheritanceShadow.KEY
9:  local function count(t) local n=0;if type(t)=='table' then for _ in pairs(t) do n=n+1 end end;return n end
10:  local function read()
11:   local v=Game:GetProperty(KEY)
12:   if v==nil then return {schema=1,revision=0,records={},watch={},events={},sequence=0} end
17:   if eq(old,v) then return end
18:   assert(eq(read(),old),'SHADOW_STALE');v.revision=old.revision+1
19:   Game:SetProperty(KEY,cp(v));assert(eq(read(),v),'SHADOW_WRITE_UNCONFIRMED');d.writes=d.writes+1
20:  end
28:   local old=read();local v=cp(old);local r=v.records[token]
29:   if r then assert((r.owner==pid and r.cityID==c:GetID() and r.x==c:GetX() and r.y==c:GetY()) or (shared.CityInheritance and shared.CityInheritance.AllowsShadow(token,c)),'SHADOW_ANCHOR_CONFLICT') end
30:   local values={};for k,key in pairs(fields) do values[k]=cp(c:GetProperty(key)) end
31:   if r and eq(r.values,values) then return end
34:  end
35:  -- Called only after existing writes. A shadow failure is diagnostic, never a second unit charge.
36:  shared.OnPermanentCityWrite=function(c,reason) safe(function() d.Capture(c,reason) end) end
37:  function d.Select(pid,c)
49:    '备份专业='..tostring(j.specialization)..' | 投资='..count(inv.investments)..' | 模板='..count(std.learned)..' | pending='..tostring(inv.pending and inv.pending.stage),
50:    '保存原因='..tostring(r.reason)..' | 本次加载写入='..d.writes}
51:   for _,k in ipairs({'TOKEN','FLOW','JOURNAL','INVEST','TEMPLATES'}) do local now=c and c:GetProperty(fields[k]);lines[#lines+1]=k..' 备份='..(a[k]~=nil and '有' or '无')..' 当前='..(now~=nil and '有' or '无')..' 一致='..tostring(eq(a[k],now)) end
52:   lines[#lines+1]='事件记录总序号='..v.sequence..'（保留最近24条，显示最后6条）'
71:   if #v.events>24 then table.remove(v.events,1) end;save(old,v);print('[SPC][B064][EVENT] '..e.seq..' '..name..' '..e.args..' '..e.at)
72:  end
73:  local function hook(ns,name,fn,label)
74:   local e=ns and ns[name];local ok=e and type(e.Add)=='function' and pcall(e.Add,function(...) safe(fn,...) end)
75:   d.hooks[#d.hooks+1]=(label or name)..':'..(ok and 'ON' or 'ABSENT')
76:  end
77:  for _,name in ipairs({'CityTransfered','CityAddedToMap','CityRemovedFromMap','CityInitialized'}) do hook(Events,name,function(...) event(name,...) end) end
78:  for _,name in ipairs({'CityBuilt','CityConquered'}) do hook(GameEvents,name,function(...) event(name,...) end,'Game.'..name) end
79:  hook(Events,'LoadScreenClose',function()
80:   d.ready=true
```

### InvestmentAction.lua

```text
1: -- B033 bounded test-civ investment. One Gameplay request owns the entire debit.
2: SPCInvestmentAction={}
3: function SPCInvestmentAction.Start(P,shared)
4:  local KEY='SPC_DEV_INVESTMENT_LEDGER_V1';local UNIT_KEY='SPC_DEV_INVESTMENT_UNIT'
34:  local function write(pid,c,old,nextValue)
35:   assert(not halted[pid],'REENTRANT_HELD');facts(pid,c)
36:   assert(same(c:GetProperty(KEY),old),'STALE_LEDGER')
37:   P.SetProperty(c,KEY,cp(nextValue))
38:   assert(not halted[pid] and same(c:GetProperty(KEY),nextValue),'LEDGER_WRITE_UNCONFIRMED')
39:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'InvestmentAction.lua') end
40:   facts(pid,c) -- same native reader used by Lv1/network validates each state
44:   assert(op and op.stage=='CONSUMED_CONFIRMED','CONFIRMED_DEBIT_REQUIRED')
45:   local u=Players[pid]:GetUnits():FindID(op.unitID)
46:   assert(not u or u:GetProperty(UNIT_KEY)~=op.unitUID,'CONSUMED_UNIT_STILL_PRESENT')
47:   local nextValue=cp(ledger);nextValue.investments[op.receipt]=op.unitUID
59:    v.specialization=f.specialization;v.potential=f.potential;v.nextPotential=f.potential+1
60:    assert(not f.investmentPending,'PENDING_REQUIRES_REVIEW');assert(f.potential<4,'POTENTIAL_CAP_4')
61:    local u=Players[pid]:GetUnits():FindID(id);assert(u:GetProperty(UNIT_KEY)==nil,'UNIT_ALREADY_RESERVED')
62:    v.legal=true
64:    v.prepared=p~=nil and p.site and p.owner==pid and p.cityID==c:GetID() and p.unitID==id
65:     and p.turn==Game.GetCurrentGameTurn() and same(anchor(f),p.anchor)
66:     and same(c:GetProperty(KEY),p.ledger) and f.potential==p.potential
67:    if v.prepared then v.planToken=p.token end
84:    settler(pid,c,unitID,site)
85:    local plan={site=site==true,owner=pid,cityID=c:GetID(),unitID=unitID,token=f.token..':R'..(f.investmentCount+1)..':'..requestToken,
86:     turn=Game.GetCurrentGameTurn(),anchor=anchor(f),potential=f.potential,ledger=cp(c:GetProperty(KEY))}
87:    plans[pid]=plan
99:   local ok,out=pcall(function()
100:    assert(not halted[pid],'INVESTMENT_HELD')
101:    local f=facts(pid,c);local old=c:GetProperty(KEY)
102:    if old and old.investments[token] then return 'B033 ALREADY_COMMITTED\n'..shared.EffectiveFacts.Describe(pid,c) end
107:    assert(not f.investmentPending and f.potential>=1 and f.potential<4,'POTENTIAL_OR_PENDING_CHANGED')
108:    local u=settler(pid,c,p.unitID,p.site)
109:    assert(u:GetProperty(UNIT_KEY)==nil,'UNIT_ALREADY_RESERVED')
110:    local uid=f.token..':'..pid..':'..p.unitID..':'..token
113:     cityUID=f.token,expectedRevision=intent.revision}
114:    destructive=true;write(pid,c,old,intent)
115:    u=settler(pid,c,p.unitID,p.site);P.SetProperty(u,UNIT_KEY,uid)
116:    assert(u:GetProperty(UNIT_KEY)==uid and not halted[pid],'UNIT_RESERVATION_UNCONFIRMED')
117:    Players[pid]:GetUnits():Destroy(u)
129:  -- Invalidate a prepared unit if it is removed, even if its numeric ID is reused.
130:  local removed=P.Field(Events,'UnitRemovedFromMap')
131:  if removed and removed.Add then removed.Add(function(pid,id)
132:   if plans[pid] and plans[pid].unitID==id then plans[pid]=nil;shared.InvestmentPreview=nil end
133:  end) end
134:  local load=P.Field(Events,'LoadScreenClose')
135:  if load and load.Add then load.Add(function()
136:   plans={};shared.InvestmentPreview=nil
138:    if P.IsTestPlayer(pid) then
139:     for _,c in player:GetCities():Members() do P.Count('city_scan');
140:      local ledger=c:GetProperty(KEY)
141:      if type(ledger)=='table' and ledger.pending then
```

### Lv2GPP.lua

```text
1: -- B035: working-specialist count -> native building base GPP. No ChangePointsTotal.
2: SPCLv2GPP={}
3: function SPCLv2GPP.Start(P,shared)
4:  local data={ready=false,busy=false,changes=0,refreshes=0,errors={}};shared.Lv2GPP=data
110:   local out="B035 Lv2 GPP | "..(ok and result or "ERROR "..tostring(result));print("[SPC][B035] "..out);return out
111:  end
112:  local function bind(events,event,fn) local e=P.Field(events,event);if e and e.Add then e.Add(fn) end end
113:  bind(Events,"LoadScreenClose",function() data.ready=true;data.Audit() end)
114:  for _,event in ipairs({"CityWorkerChanged","CityFocusChanged","GovernorAssigned","GovernorEstablished","GovernorChanged","PlayerTurnActivated","PlayerTurnDeactivated","CityTransfered"}) do bind(Events,event,data.Audit) end
115:  for _,event in ipairs({"OnDistrictConstructed","BuildingConstructed","CityBuilt"}) do bind(GameEvents,event,data.Audit) end
116: end
```

### Lv2Housing.lua

```text
1: -- B034: disposable native housing carriers, rebuilt from effective city facts.
2: SPCLv2Housing={}
3: function SPCLv2Housing.Start(P,shared)
4:  local data={ready=false,busy=false,changes=0,errors={},events=0}
93:   print("[SPC][B034] "..out);return out
94:  end
95:  local function bind(events,name,fn)
96:   local e=P.Field(events,name);if e and e.Add then e.Add(fn) end
97:  end
98:  bind(Events,"LoadScreenClose",function() data.ready=true;data.Audit() end)
99:  for _,name in ipairs({"GovernorAssigned","GovernorEstablished","GovernorChanged","PlayerTurnActivated","CityTransfered","CityBuildingsChanged"}) do bind(Events,name,data.Audit) end
100:  for _,name in ipairs({"BuildingConstructed","OnDistrictConstructed","CityBuilt"}) do bind(GameEvents,name,data.Audit) end
101: end
```

### Lv3Effects.lua

```text
1: -- B038: native population yield per specialist; Commerce direct connected types.
2: SPCLv3Effects={}
3: function SPCLv3Effects.Start(P,shared)
4:  local data={ready=false,busy=false,errors={},changes=0,observed={}};shared.Lv3Effects=data
111:   return (ok and out or ('\nLv3 effects ERROR '..tostring(out)))..'\nLv3 effects status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
112:  end
113:  local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
114:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
115:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered','CityWorkerChanged','CityFocusChanged','CityPopulationChanged'}) do hook(Events,n,data.Audit) end
116:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
117: end
```

### Lv3Support.lua

```text
1: -- B037: Lv3 specialist support only. Incremental +2 upgrades Lv1 3 to 5, never 3+5.
2: SPCLv3Support={}
3: function SPCLv3Support.Start(P,shared)
4:  local data={ready=false,busy=false,errors={},changes=0};shared.Lv3Support=data
73:    ..'\nLv3 status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
74:  end
75:  local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
76:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
77:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered'}) do hook(Events,n,data.Audit) end
78:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
79: end
```

### Lv4Percent.lua

```text
1: -- B048: only RES-004/CUL-004 per-specialist percentage component.
2: SPCLv4Percent={}
3: function SPCLv4Percent.Start(P,shared)
4:  local data={ready=false,busy=false,errors={},changes=0};shared.Lv4Percent=data
69:   return ok and out or ('Lv4百分比读取失败：'..tostring(out))
70:  end
71:  local function hook(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
72:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
73:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered','CityWorkerChanged','CityFocusChanged','CityPopulationChanged','DistrictRemovedFromMap'}) do hook(Events,n,data.Audit) end
74:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
75: end
```

### NetworkBoost.lua

```text
12:  testRows[#testRows+1]='BUILDING_SPC_B057_'..kind..'_'..amount
13: end end
14: function SPCNetworkBoost.Start(P,shared)
15:  local d={ready=false,busy=false,applied={},plans={},errors={},changes=0,testRaw={}};shared.NetworkBoost=d
121:   return table.concat(out,'\n')
122:  end
123:  local function hook(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
124:  for _,n in ipairs({'GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','PlayerTurnActivated','PlayerTurnDeactivated'}) do hook(Events,n,d.Audit) end
125:  hook(Events,'CityTransfered',function() if d.ready and not d.busy then
126:   d.busy=true;local ok,err=pcall(d.Clean);d.busy=false
```

### NetworkBridge.lua

```text
1: -- B027 bounded single-player diagnostic bridge. No Property, Modifier or yields.
2: SPCNetworkBridge={}
3: function SPCNetworkBridge.Start(P,shared)
4:  local d={ready=false,players={}};shared.NetworkBridge=d
246:  end
247:  for _,name in ipairs({"OnDistrictConstructed","CityBuilt"}) do
248:   local ev=P.Field(GameEvents,name);if ev and ev.Add then ev.Add(d.Rebuild) end
249:  end
254:  end
255:  for _,name in ipairs({'TradeRouteActivityChanged','TradeRouteRemovedFromMap','UnitRemovedFromMap','CityRemovedFromMap','CityTransfered','DiplomacyDeclareWar'}) do
256:   local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(function() d.CheckEvidence(false) end) end
257:  end
258:  local turn=P.Field(Events,"PlayerTurnActivated");if turn and turn.Add then turn.Add(d.Rebuild) end
259:  local e=P.Field(Events,"LoadScreenClose");if e and e.Add then e.Add(function() d.ready=true end) end
260: end
```

### NetworkSender.lua

```text
29:   seq=math.max(seq,b and b.seq or 0)+1
30:   public.awaitingNetwork=true;flight={seq=seq,turn=s.turn,fingerprint=s.fingerprint};SPCPerformance.Flight(1);P.Count('net_send')
31:   local ok=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
32:    {OnStart='SPC_P0_Request',Action='NETWORK_PUSH',Token=P.VERSION..':net:'..seq,
```

### Probe.lua

```text
49:   end
50:   out[#out+1]="City="..tostring(cityID).." "..city:GetName().." | CIVILIZATION_SPC_TEST / LEADER_SPC_TEST"
51:   out[#out+1]="Marker="..tostring(val(city,"GetProperty","SPC_P0_MARKER")).." | Spec(test)="..tostring(val(city,"GetProperty","SPC_P0_FIRST_SPEC"))
52:   out[#out+1]="Potential/Active=NOT_IMPLEMENTED (no invented levels)"
74:     .." | promotions="..tostring(complete and promotions or "UNKNOWN")
75:     .." | titleCandidate="..tostring(complete and (gov and (1+nonbase) or 0) or "UNKNOWN").." (not historical spend)"
76:   out[#out+1]="Engine Req2/3/4 raw="..tostring(val(city,"GetProperty","SPC_P0_GOV_REQ_2")).."/"
77:     ..tostring(val(city,"GetProperty","SPC_P0_GOV_REQ_3")).."/"..tostring(val(city,"GetProperty","SPC_P0_GOV_REQ_4"))
78:   local enumOK,err=pcall(function()
199:       log(key,{name=city:GetName(),x=city:GetX(),y=city:GetY()})
200:       read(key.." POPULATION",city,"GetPopulation")
201:       read(key.." MARKER",city,"GetProperty","SPC_P0_MARKER")
202:       read(key.." FIRST_COMPLETION",city,"GetProperty","SPC_P0_FIRST_SPEC")
203:       read(key.." HISTORY_ELIGIBLE",city,"GetProperty","SPC_P0_FIRST_ELIGIBLE")
204:       for n=2,4 do read(key.." ENGINE_GOV_REQ_"..n,city,"GetProperty","SPC_P0_GOV_REQ_"..n) end
205:       local gov=read(key.." GOVERNOR",city,"GetAssignedGovernor")
312:   facts.identityKind="OWNER_CITY_ID_SNAPSHOT_ONLY"
313:   local function prop(key)
314:     local success,value=P.Call(city,"GetProperty",key)
315:     if not success then return false,nil end
362:   if action=="GOVERNOR" then
363:     out[#out+1]="lookup=NATIVE_REQUIREMENTS (no governor Lua getter)"
364:     local control=get(city,"GetProperty","SPC_P0_GOV_CONTROL_A007")
365:     local present=get(city,"GetProperty","SPC_P0_GOV_PRESENT")
366:     local established=get(city,"GetProperty","SPC_P0_GOV_ESTABLISHED")
367:     out[#out+1]="control="..P.Scalar(control).." | present="..P.Scalar(present).." established="..P.Scalar(established)
368:     local raw={}
369:     for n=2,4 do raw[#raw+1]=P.Scalar(get(city,"GetProperty","SPC_P0_GOV_REQ_"..n)) end
370:     out[#out+1]="Established title thresholds 2/3/4="..table.concat(raw,"/")
525: function P.CreateBuilding(object,id) P.Count('building_create');return object:CreateBuilding(id) end
526: function P.RemoveBuilding(object,id) P.Count('building_remove');return object:RemoveBuilding(id) end
527: function P.SetProperty(object,key,value) P.Count('property_write');return object:SetProperty(key,value) end
528: -- A live non-trader is a reliable negative. Missing/removed/unknown unit is not.
```

### PurchaseProbe.lua

```text
1: -- B053 manual currency-isolation fixture, never a network effect.
2: SPCPurchaseProbe={}
3: function SPCPurchaseProbe.Start(P,shared)
4:  local d={};shared.PurchaseProbe=d
26:  end
27:  local e=P.Field(Events,'LoadScreenClose')
28:  if e and e.Add then e.Add(function()
29:   -- Reload always leaves the experiment OFF, including a captured former test city.
```

### QualificationProbe.lua

```text
135:
136: end)()
137: function SPCQualificationProbe.Start(P,shared)
138:  local env={Players=Players,PlayerConfigurations=PlayerConfigurations,GameInfo=GameInfo,PlayerManager=PlayerManager}
198:  end
199:  local e=Events and Events.LoadScreenClose
200:  if e and type(e.Add)=="function" then
201:   local ok=pcall(e.Add,onLoad);data.hook=ok and "REGISTERED" or "ERROR"
202:  end
```

### ResearchSupport.lua

```text
1: -- B024 automatic constant Lv1 carriers; bounded existing DEV facts, not general eligibility.
2: SPCResearchSupport={}
3: function SPCResearchSupport.Start(P,shared)
4:  local data={changes=0,ready=false,errors={},scan="NOT_RUN",events=0};shared.ResearchSupport=data
115:  end
116:  local load=P.Field(Events,"LoadScreenClose")
117:  if load and load.Add then load.Add(function() data.ready=true;data.Audit() end) end
118:  for _,name in ipairs({"PlayerTurnActivated","CityTransfered"}) do
119:   local event=P.Field(Events,name);if event and event.Add then event.Add(data.Audit) end
120:  end
121:  -- Installed after B015/B021, so facts are committed before effects are reconciled.
122:  local event=P.Field(GameEvents,"OnDistrictConstructed")
123:  if event and event.Add then event.Add(completed) end
124:  local built=P.Field(GameEvents,"CityBuilt")
125:  if built and built.Add then built.Add(data.Audit) end
126: end
```

### Standardization.lua

```text
1: -- B052: persistent building knowledge. No Gold/Faith price or unlock modification.
2: SPCStandardization={KEY='SPC_STANDARDIZATION_LEDGER_V1'}
3: function SPCStandardization.Start(P,shared)
4:  local KEY=SPCStandardization.KEY
29:  end
30:  local function write(c,old,nextValue)
31:   assert(same(c:GetProperty(KEY),old),'STD_CONCURRENT_CHANGE')
32:   P.SetProperty(c,KEY,nextValue)
33:   assert(same(c:GetProperty(KEY),nextValue),'STD_WRITE_UNCONFIRMED')
34:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'Standardization.lua') end
35:   data.writes=data.writes+1
50:  end
51:  local function initialize(pid,c)
52:   local old=c:GetProperty(KEY)
53:   if old~=nil then validate(c,old);return false end
103:      if f.specialization~='INDUSTRY' then return end
104:      initialize(q.pid,c)
105:      local old=validate(c,c:GetProperty(KEY));assert(old.foundation==f.token,'STD_FOUNDATION_CHANGED')
106:      local nextValue=clone(old);local changed=false
122:  function data.ReadLedger(pid,c)
123:   local f=facts(pid,c);assert(f.specialization=='INDUSTRY','STD_SOURCE_CHANGED')
124:   local v=validate(c,c:GetProperty(KEY));assert(v.foundation==f.token,'STD_FOUNDATION_CHANGED')
125:   return clone(v)
128:   local ok,text=pcall(function()
129:    assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'STD_OWNER_CHANGED')
130:    local v=c:GetProperty(KEY);local cat=catalog();local lines={'B052 标准化模板 | '..tostring(c:GetName())..' | city='..c:GetID()}
131:    if v==nil then lines[#lines+1]='尚无账本：非工业专业或后台初始化尚未完成。'
150:   return ok and text or ('B052 读取未完成：'..(tostring(text):match('STD_[A-Z_]+') or 'STD_READ_FAILED'))
151:  end
152:  local function hook(src,n,fn)
153:   local ev=P.Field(src,n);if ev and ev.Add then ev.Add(fn);data.hooks[n]=true end
154:  end
155:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Discover();data.Flush() end)
156:  hook(Events,'PlayerTurnActivated',function(pid) data.Discover(pid);data.Flush() end)
157:  hook(GameEvents,'OnDistrictConstructed',function(pid) data.Discover(pid);data.Flush() end)
158:  for _,name in ipairs({'BuildingConstructed','OnBuildingConstructed'}) do
159:   hook(GameEvents,name,function(pid,cid,bid) data.Queue(pid,cid,bid,name);data.Flush() end)
160:  end
161:  -- HD RegionalYields.lua uses x,y,buildingId,playerId. Recheck this building only.
162:  hook(Events,'BuildingAddedToMap',function(x,y,bid,pid)
163:   if type(pid)~='number' or not P.IsTestPlayer(pid) then return end
168:   data.Flush()
169:  end)
170:  hook(Events,'GameCoreEventPublishComplete',data.Flush)
171: end
```

### StandardizationDiscount.lua

```text
1: -- B054: derived network discount, permanent templates remain owned by Standardization.
2: SPCStandardizationDiscount={}
3: function SPCStandardizationDiscount.Start(P,shared)
4:  local d={ready=false,busy=false,generation=0,plans={},samples={},seq={},applied={},errors={},changes=0};shared.StandardizationDiscount=d
112:   return table.concat(lines,'\n')
113:  end
114:  local function hook(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f) end end
115:  cleanupOtherOwners=function()
117:   if not ok then print('[SPC][B054][CLEANUP] '..tostring(err)) end
118:  end
119:  hook('LoadScreenClose',function() d.ready=true;d.generation=d.generation+1;d.samples={};d.seq={};d.applied={};cleanupOtherOwners();d.Audit() end)
120:  hook('CityTransfered',function() d.applied={};cleanupOtherOwners();d.Audit() end)
121:  for _,n in ipairs({'GameCoreEventPublishComplete','PlayerTurnActivated','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged'}) do hook(n,d.Audit) end
122: end
```

### StorageProbe.lua

```text
1: -- B012 synthetic Game Property only. No city identity or specialization writes.
2: SPCStorageProbe={}
3: function SPCStorageProbe.Start(P,shared)
4:  local data={version=P.VERSION,players={}};shared.StorageProbe=data
20:   local key="SPC_DEV_STORAGE_B012_P"..tostring(pid)
21:   local want=expected(pid)
22:   local ok,value=pcall(function() return Game:GetProperty(key) end)
23:   local state="READ_ERROR"
29:   if write and state=="EMPTY" then
30:    b.attempts=b.attempts+1
31:    local ack=pcall(function() P.SetProperty(Game,key,want) end)
32:    local readOK,after=pcall(function() return Game:GetProperty(key) end)
33:    state=readOK and (equal(after,expected(pid),0) and "MATCH" or "WRITE_UNCONFIRMED") or "READBACK_ERROR"
```

### TradeRouteProbe.lua

```text
2: -- Unit operation parameters are hypotheses, not certified active-route records.
3: SPCTradeRouteProbe={}
4: function SPCTradeRouteProbe.Start(P,shared)
5:   shared.AutoRouteProbe={}
116:     end
117:   end
118:   local function listen(namespace,name,fn)
119:     local event=P.Field(namespace,name)
120:     if event and type(P.Field(event,"Add"))=="function" then event.Add(fn)
121:     else print("[SPC]["..P.VERSION.."][TRADE_STATE_PROBE] EVENT_ABSENT "..name) end
124:   for _,name in ipairs({"TradeRouteActivityChanged","TradeRouteRemovedFromMap","UnitRemovedFromMap",
125:       "UnitOperationDeactivated","UnitOperationStarted","UnitOperationsCleared","CityRemovedFromMap","CityAddedToMap","DiplomacyDeclareWar"}) do
126:     local eventName=name;listen(Events,eventName,function(pid,id)
127:       if eventName:find('^Unit') then
132:   end
133:   for _,name in ipairs({"CityConquered","TradeRoutePlundered"}) do
134:     local eventName=name;listen(GameEvents,eventName,function() pending[eventName]=true;shared.RouteSignalRevision=shared.RouteSignalRevision+1 end)
135:   end
136:   listen(Events,"LoadScreenClose",function() refresh("LoadScreenClose") end)
137:   listen(Events,"PlayerTurnActivated",function(pid)
138:     if P.IsTestPlayer(pid) then refresh("PlayerTurnActivated") end
139:   end)
140:   listen(Events,"PlayerTurnDeactivated",function(pid)
141:     if P.IsTestPlayer(pid) then refresh("PlayerTurnDeactivated") end
```

### UI/BackgroundRoutes.lua

```text
125:   if not retryPending then
126:    local g=ExposedMembers.SPC_P0;local b=g and g.NetworkBridge
127:    if b then pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
128:     {OnStart='SPC_P0_Request',Action='NETWORK_REVALIDATE_FAILURE',Token=P.VERSION..':proof:'..generation,Epoch=b.epoch}) end
155:  if not ok then P.Count('route_failure');dirty=false;retryPending=false;public.revalidation='RETRY_STOPPED' end
156: end
157: local function bind(name,fn)
158:  local e=P.Field(Events,name)
159:  if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,callback=fn} end
160: end
169:   'CityAddedToMap','CityRemovedFromMap','CityTransfered','DiplomacyDeclareWar','PlayerTurnActivated','PlayerTurnDeactivated'}) do
170:   local eventName=name
171:   bind(name,function(pid,id)
172:    if eventName:find('^Unit') then
178:   end)
179:  end
180:  for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','SystemUpdateUI'}) do bind(name,flush) end
181:  flush()
182:  -- No recurring full-scan timer. Events and local turn boundaries remain primary.
183: end
184: ContextPtr:SetInitHandler(initialize)
185: ContextPtr:SetShutdown(function()
186:  active=false;normalized:Reset();ContextPtr:ClearUpdate()
```

### UI/BoostRefresh.lua

```text
9:  if s.NetworkBoost.ready and s.GreatWorkProbe and s.GreatWorkProbe.ready then return end
10:  busy=true
11:  local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='BOOST_INIT',Token=P.VERSION..':boost:init'})
12:  busy=false;if not ok then print('[SPC][B055][INIT] '..tostring(err)) end
13: end
14: ContextPtr:SetInitHandler(function()
15:  for _,name in ipairs({'SystemUpdateUI','LoadScreenClose','GameCoreEventPlaybackComplete'}) do
16:   local e=P.Field(Events,name);if e and e.Add then e.Add(refresh);hooks[#hooks+1]=e end
17:  end
18:  refresh()
19: end)
20: ContextPtr:SetShutdown(function() for _,e in ipairs(hooks) do if e.Remove then e.Remove(refresh) end end end)
```

### UI/CityPotential.lua

```text
46:   ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
47:   token=P.VERSION..':POTENTIAL:'..ExposedMembers.SPC_P0_UISequence;age=0
48:   local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
49:    {OnStart='SPC_P0_Request',Action='CITY_PRESENTATION_READ',CityID=c:GetID(),Token=token})
51:  end
52: end
53: ContextPtr:SetInitHandler(function() ContextPtr:SetHide(false);ContextPtr:SetUpdate(update) end)
54: ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Controls.Badge:SetHide(true) end)
```

### UI/CopyYieldRefresh.lua

```text
37:   seq=math.max(seq,shared.CopyYields.seq[pid] or 0)+1;local old=sent;sent=signature
38:   public.requests=public.requests+1;public.seq=seq;public.count=count
39:   local delivered,why=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
40:    {OnStart='SPC_P0_Request',Action='COPY_YIELD_SAMPLE',Token=P.VERSION..':copy:'..seq,Seq=seq,Generation=shared.CopyYields.generation,Turn=turn,Valid=ok and 1 or 0,Count=ok and count or 0,Data=payload})
50:  if not ok then busy=false;public.state='ERROR';public.error=code(err);print('[SPC][B051][BACKGROUND_ERROR] '..tostring(err)) end
51: end
52: local function bind(name,fn)
53:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
54: end
55: ContextPtr:SetInitHandler(function()
56:  -- Established event-driven path: runs even when this empty context receives no frame updates.
57:  for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(name,safelyRefresh) end
58:  bind('LoadScreenClose',function() initialized=false;sent=nil;safelyRefresh() end)
59:  bind('SystemUpdateUI',function()
60:   local shared=ExposedMembers.SPC_P0;local d=shared and shared.CopyYields
62:  end)
63:  safelyRefresh()
64:  ContextPtr:SetUpdate(function(dt)
65:   if type(dt)~='number' or dt<0 then return end
67:  end)
68: end)
69: ContextPtr:SetShutdown(function()
70:  ContextPtr:ClearUpdate()
```

### UI/DialogueRefresh.lua

```text
11:  dirty=true;revision=revision+1;public.reason=reason
12: end
13: -- Empty background contexts do not reliably receive SetUpdate in Civ VI.
14: -- Generic engine pulses may retransmit the SAME packet at most twice; never scan.
17: local function dispatch(pid,packet)
18:  public.sends=public.sends+1
19:  local ok,result=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
20:  public.transport=ok and tostring(result) or ('ERROR: '..tostring(result))
77: end
78: safe=function() local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';print('[SPC][B059][UI] '..tostring(err)) end end
79: local function bind(name,fn)
80:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
81: end
82: ContextPtr:SetInitHandler(function()
83:  -- These events describe collection/city/eligibility changes, not our own yield refreshes.
84:  for _,name in ipairs({'GreatWorkCreated','GreatWorkMoved','CityAddedToMap','CityRemovedFromMap','CityTransfered','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','PlayerTurnActivated','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','FeatureAddedToMap','CityTileOwnershipChanged'}) do
85:   local reason=name;bind(name,function() mark(reason) end)
86:  end
87:  bind('LoadScreenClose',function() mark('LOAD_SCREEN_CLOSE');safe() end)
88:  for _,name in ipairs({'SystemUpdateUI','GameCoreEventPublishComplete','GameCoreEventPlaybackComplete'}) do bind(name,pulse) end
89:  safe()
90: end)
91: ContextPtr:SetShutdown(function()
92:  stopRetry()
```

### UI/DiscountEligibility.lua

```text
12:   -- Background context may initialize after the one-shot gameplay load event.
13:   busy=true;public.state='REQUEST_INITIALIZATION'
14:   local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
15:    {OnStart='SPC_P0_Request',Action='DISCOUNT_INIT',Token=P.VERSION..':discount:init'})
39:  if signature~=sent or (d.seq[pid] or -1)~=seq then
40:   seq=math.max(seq,d.seq[pid] or 0)+1;local old=sent;sent=signature
41:   local delivered,why=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='DISCOUNT_ELIGIBILITY',Token=P.VERSION..':discount:'..seq,Seq=seq,Generation=generation,Revision=revision,Turn=turn,Valid=ok and 1 or 0,Count=ok and count or 0,Data=payload})
42:   if not delivered then sent=old;ok=false;err=why end
49:  local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';public.error=tostring(err);print('[SPC][B054][UI] '..tostring(err)) end
50: end
51: local function bind(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f);hooks[#hooks+1]={e,f} end end
52: ContextPtr:SetInitHandler(function()
53:  for _,n in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(n,safe) end
54:  bind('LoadScreenClose',function() sent=nil;initialized=false;safe() end)
55:  bind('SystemUpdateUI',function()
56:   local shared=ExposedMembers.SPC_P0;local d=shared and shared.StandardizationDiscount
59:  safe()
60: end)
61: ContextPtr:SetShutdown(function() for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end end)
```

### UI/GPPRefresh.lua

```text
16:  local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
17:  busy=true;dirty=false;seq=seq+1
18:  local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
19:   {OnStart="SPC_P0_Request",Action="LV2_GPP_DIRTY",Token=P.VERSION..":gpp:"..seq})
21:  busy=false
22: end
23: local function bind(name,fn)
24:  local e=P.Field(Events,name)
25:  if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
26: end
27: ContextPtr:SetInitHandler(function()
28:  if active then return end;active=true
29:  for _,name in ipairs({"CityWorkerChanged","CityFocusChanged","GovernorAssigned","GovernorChanged","GovernorEstablished","GovernorPromoted"}) do bind(name,mark) end
30:  for _,name in ipairs({"LoadScreenClose","PlayerTurnActivated","PlayerTurnDeactivated"}) do bind(name,function() mark();flush() end) end
31:  for _,name in ipairs({"GameCoreEventPublishComplete","GameCoreEventPlaybackComplete","SystemUpdateUI"}) do bind(name,flush) end
32:  flush()
33: end)
34: ContextPtr:SetShutdown(function()
35:  active=false
```

### UI/IndustryRefresh.lua

```text
27:      -- Mark before request to prevent synchronous publish recursion; retry send errors.
28:      local prior=sent[k];sent[k]=n
29:      local delivered,message=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
30:       {OnStart='SPC_P0_Request',Action='INDUSTRY_BASE',Token=P.VERSION..':industry:'..sequence,CityID=id,DistrictID=d:GetID(),BaseProduction=n})
39:  if not ok then print('[SPC][B036][BASE_UI_ERROR] '..tostring(err)) end
40: end
41: local function bind(name,fn)
42:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
43: end
44: ContextPtr:SetInitHandler(function()
45:  if active then return end;active=true
46:  for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','LoadScreenClose','PlayerTurnActivated'}) do bind(name,refresh) end
47:  -- Retry initialization only until first successful sample; no per-frame world scan.
48:  bind('SystemUpdateUI',function() if not initialized then refresh() end end)
49:  refresh()
50: end)
51: ContextPtr:SetShutdown(function() active=false;for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end;hooks={} end)
```

### UI/P0Panel.lua

```text
96:   end
97:   f.retries=f.retries+1;f.busy=true
98:   local ok,err=pcall(UI.RequestPlayerOperation,f.pid,PlayerOperations.EXECUTE_SCRIPT,f.packet)
99:   f.busy=false
104:   if displayResponse() then return end
105:   local elapsed=0
106:   ContextPtr:SetUpdate(function(dt)
107:     elapsed=elapsed+dt
153:   local packet={OnStart="SPC_P0_Request",Action=action,Token=pendingToken,ExpectedStage=action=="ENVELOPE_NEXT" and expectedStage or nil,CityID=city and city:GetID(),Page=page,UnitID=investmentUnitID,PlanToken=investmentPlanToken}
154:   if action:find('^GWA_') then gwaFlight={pid=playerID,packet=packet,pulses=0,retries=0,busy=true} end
155:   local ok,err=pcall(UI.RequestPlayerOperation,playerID,PlayerOperations.EXECUTE_SCRIPT,packet)
156:   if gwaFlight then gwaFlight.busy=false end
291:   showRoot();Controls.Window:SetHide(true)
292:   Controls.Title:SetText("SPC "..P.VERSION.." | Specialization diagnostics")
293:   Controls.OpenButton:RegisterCallback(Mouse.eLClick,function() Controls.Window:SetHide(false) end)
294:   Controls.CloseButton:RegisterCallback(Mouse.eLClick,function() Controls.Window:SetHide(true) end)
295:   Controls.QualificationButton:RegisterCallback(Mouse.eLClick,function()
296:     ContextPtr:ClearUpdate();pendingToken=nil
305:   end)
306:   local unknownPage=0
307:   Controls.EligibilityUnknownButton:RegisterCallback(Mouse.eLClick,function()
308:     ContextPtr:ClearUpdate();pendingToken=nil
332:     localReport=table.concat(lines,"\n");status(localReport:gsub("\n","[NEWLINE]"))
333:   end)
334:   Controls.EligibilityButton:RegisterCallback(Mouse.eLClick,function()
335:     ContextPtr:ClearUpdate();pendingToken=nil
355:     localReport=table.concat(lines,"\n");status(localReport:gsub("\n","[NEWLINE]"))
356:   end)
357:   Controls.CityJournalButton:RegisterCallback(Mouse.eLClick,function() request("CITY_JOURNAL_READ") end)
358:   Controls.CompletionRecordButton:RegisterCallback(Mouse.eLClick,function() request("COMPLETION_RECORD_READ") end)
359:   Controls.BindingReadButton:RegisterCallback(Mouse.eLClick,function() request("BINDING_READ") end)
360:   Controls.CarrierStepButton:RegisterCallback(Mouse.eLClick,function() request("NETWORK_DETAIL",true) end)
361:   Controls.CarrierOffButton:RegisterCallback(Mouse.eLClick,function() request("CARRIER_OFF") end)
362:   for _,a in ipairs({"READ","OFF","AUTO","TEST5"}) do local action=a;Controls["Commerce"..a.."Button"]:RegisterCallback(Mouse.eLClick,function() request("COMMERCE_"..action) end) end
363:   Controls.InheritRecordButton:RegisterCallback(Mouse.eLClick,function() request("SHADOW_SELECT") end)
364:   Controls.InheritReadButton:RegisterCallback(Mouse.eLClick,function() request("SHADOW_READ") end)
365:   Controls.SourceYieldButton:RegisterCallback(Mouse.eLClick,function() request("PROGRESSION_READ") end)
366:   Controls.ConstructionPreviewButton:RegisterCallback(Mouse.eLClick,function() request("CONSTRUCTION_PREVIEW") end)
367:   Controls.ConstructionApplyButton:RegisterCallback(Mouse.eLClick,function() request("CONSTRUCTION_APPLY") end)
368:   Controls.Lv2GPPButton:RegisterCallback(Mouse.eLClick,function() request("LV2_GPP_READ") end)
369:   Controls.Lv2HousingButton:RegisterCallback(Mouse.eLClick,function() request("LV2_HOUSING_READ") end)
370:   Controls.InvestPrepareButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_PREPARE") end)
371:   Controls.InvestConfirmButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_CONFIRM") end)
372:   Controls.NetworkButton:RegisterCallback(Mouse.eLClick,function() request("NETWORK_READ") end)
373:   Controls.Lv4PercentButton:RegisterCallback(Mouse.eLClick,function() request("LV4_PERCENT_READ") end)
374:   Controls.ResearchReadButton:RegisterCallback(Mouse.eLClick,function() request("RESEARCH_READ") end)
375:   Controls.CityFlowButton:RegisterCallback(Mouse.eLClick,function() request("CITY_FLOW_READ") end)
376:   Controls.EnvelopeReadButton:RegisterCallback(Mouse.eLClick,function() request("ENVELOPE_READ") end)
377:   Controls.EnvelopeNextButton:RegisterCallback(Mouse.eLClick,function() request("ENVELOPE_NEXT") end)
378:   Controls.StorageReadButton:RegisterCallback(Mouse.eLClick,function() request("STORAGE_READ") end)
379:   Controls.StorageWriteButton:RegisterCallback(Mouse.eLClick,function() request("STORAGE_WRITE") end)
380:   Controls.CompletionButton:RegisterCallback(Mouse.eLClick,function() showCompletion(false) end)
381:   Controls.CompletionNextButton:RegisterCallback(Mouse.eLClick,function() showCompletion(true) end)
382:   Controls.CaptureButton:RegisterCallback(Mouse.eLClick,function() request("CAPTURE") end)
383:   Controls.HalfReadButton:RegisterCallback(Mouse.eLClick,function() request('HALF_READ') end)
384:   Controls.HalfOnButton:RegisterCallback(Mouse.eLClick,function() request('HALF_ON') end)
385:   Controls.HalfOffButton:RegisterCallback(Mouse.eLClick,function() request('HALF_OFF') end)
386:   Controls.BoostTestZeroButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_ZERO') end)
387:   Controls.BoostTestHalfButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_HALF') end)
388:   Controls.BoostTestHighButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_HIGH') end)
389:   Controls.BoostTestAutoButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_AUTO') end)
390:   Controls.BoostReadButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_READ') end)
391:   Controls.BoostBaseButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_BASELINE') end)
392:   Controls.DialogueTest25Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST25') end)
393:   Controls.DialogueTest50Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST50') end)
394:   Controls.DialogueTest100Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST100') end)
395:   Controls.GWAReadButton:RegisterCallback(Mouse.eLClick,function() request('GWA_READ') end)
396:   Controls.GWAOffButton:RegisterCallback(Mouse.eLClick,function() request('GWA_OFF') end)
397:   Controls.GWAAutoButton:RegisterCallback(Mouse.eLClick,function() request('GWA_AUTO') end)
398:   Controls.GWBaselineButton:RegisterCallback(Mouse.eLClick,function() request('GW_BASELINE') end)
399:   Controls.GWReadButton:RegisterCallback(Mouse.eLClick,function() request('GW_READ') end)
400:   Controls.GWCityButton:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_AUTO') end)
401:   Controls.GWObjectButton:RegisterCallback(Mouse.eLClick,function() request('GW_OBJECT') end)
402:   Controls.GWOffButton:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_OFF') end)
403:   Controls.DiscountsButton:RegisterCallback(Mouse.eLClick,function() request('DISCOUNT_READ',true) end)
404:   Controls.NextDiscountsButton:RegisterCallback(Mouse.eLClick,function() request('DISCOUNT_READ',true) end)
405:   Controls.PurchaseBaseButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_BASE') end)
406:   Controls.PurchaseOnButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_ON') end)
407:   Controls.PurchaseOffButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_OFF') end)
408:   Controls.PurchaseReadButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_READ') end)
409:   Controls.TemplatesButton:RegisterCallback(Mouse.eLClick,function() request("STANDARDIZATION_READ",true) end)
410:   Controls.NextTemplatesButton:RegisterCallback(Mouse.eLClick,function() request("STANDARDIZATION_READ",true) end)
411:   Controls.Lv4CopyButton:RegisterCallback(Mouse.eLClick,function() request("LV4_COPY_READ") end)
412:   Controls.AdjacencyButton:RegisterCallback(Mouse.eLClick,function() request("ADJACENCY") end)
413:   Controls.BackgroundRoutesButton:RegisterCallback(Mouse.eLClick,function()
414:     ContextPtr:ClearUpdate();pendingToken=nil
419:     status(localReport:gsub("\n","[NEWLINE]"))
420:   end)
421:   Controls.RouteStateButton:RegisterCallback(Mouse.eLClick,function()
422:     ContextPtr:ClearUpdate();pendingToken=nil
431:     status(localReport:gsub("\n","[NEWLINE]"))
432:   end)
433:   Controls.RouteEventsButton:RegisterCallback(Mouse.eLClick,function() request("TRADE_EVENTS") end)
434:   Controls.TradeButton:RegisterCallback(Mouse.eLClick,function() request("TRADE") end)
435:   Controls.NextButton:RegisterCallback(Mouse.eLClick,function()
436:     if pageAction=="ADJACENCY" or pageAction=="TRADE" then request(pageAction,true) end
437:   end)
438:   Controls.GovernorButton:RegisterCallback(Mouse.eLClick,function() request("GOVERNOR") end)
439:   Controls.SpecialistsButton:RegisterCallback(Mouse.eLClick,function() request("SPECIALISTS") end)
440:   Controls.MarkButton:RegisterCallback(Mouse.eLClick,function() request("MARK_CITY") end)
441:   Controls.CopyButton:RegisterCallback(Mouse.eLClick,function() copy(false) end)
442:   Controls.BaselineButton:RegisterCallback(Mouse.eLClick,function() copy(true) end)
443:   Controls.UnitReadButton:RegisterCallback(Mouse.eLClick,function() request('UNIT_SITE_READ') end)
444:   status('请选择城市，再读取所需项目。[NEWLINE]模板 / 折扣 / 网络明细可重复点击翻页。移民 / 施工队请先选择单位。[NEWLINE]写入诊断日志会保存本次已读取内容与后台状态，不要求剪贴板。')
447: initialize=function()
448:  oldInitialize()
449:  Controls.PerformanceReadButton:RegisterCallback(Mouse.eLClick,function()
450:   ContextPtr:ClearUpdate();gwaFlight=nil;pendingToken=nil;pendingAction=nil;localReport=SPCPerformance.Describe(false);status(localReport:gsub('\n','[NEWLINE]'))
451:  end)
452:  Controls.PerformanceSnapshotButton:RegisterCallback(Mouse.eLClick,function()
453:   ContextPtr:ClearUpdate();gwaFlight=nil;pendingToken=nil;pendingAction=nil;P.Count('manual_snapshot');localReport=SPCPerformance.Describe(true)
455:  end)
456: end
457: ContextPtr:SetInitHandler(initialize)
458: Events.LoadScreenClose.Add(showRoot)
459: Events.SystemUpdateUI.Add(gwaPulse)
460: Events.SystemUpdateUI.Add(placeEntry)
461: ContextPtr:SetShutdown(function() Controls.OpenButton:SetHide(true);Events.SystemUpdateUI.Remove(placeEntry);gwaFlight=nil;Events.SystemUpdateUI.Remove(gwaPulse);ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
```

### UI/UnitPanelActions.lua

```text
29:   ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
30:   viewToken=P.VERSION..':VIEW:'..ExposedMembers.SPC_P0_UISequence;viewRequestedAt=clock;nextView=clock+0.5
31:   local ok=pcall(UI.RequestPlayerOperation,u:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,
32:    {OnStart='SPC_P0_Request',Action='UNIT_ACTION_VIEW',UnitID=u:GetID(),Token=viewToken})
75:  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
76:  pending=P.VERSION..':PANEL:'..Game.GetCurrentGameTurn()..':'..ExposedMembers.SPC_P0_UISequence;elapsed=0
77:  local ok,err=pcall(UI.RequestPlayerOperation,u:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,
78:   {OnStart='SPC_P0_Request',Action=confirm and 'UNIT_ACTION_CONFIRM' or 'UNIT_ACTION_PREPARE',UnitID=u:GetID(),Token=pending,PlanToken=p and p.token})
115:  parent:CalculateSize();parent:ReprocessAnchoring()
116: end
117: ContextPtr:SetInitHandler(function()
118:  timer=0;ContextPtr:SetHide(false)
119:  Controls.PrepareButton:RegisterCallback(Mouse.eLClick,function() dispatch(false) end)
120:  Controls.ConfirmButton:RegisterCallback(Mouse.eLClick,function() dispatch(true) end)
121:  ContextPtr:SetUpdate(update)
122: end)
123: ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Controls.ActionGroup:SetHide(true) end)
```

### UI/UnitSites.lua

```text
28:  token=P.VERSION..':SITE:'..Game.GetCurrentGameTurn()..':'..ExposedMembers.SPC_P0_UISequence
29:  elapsed=0;Controls.Window:SetHide(false);Controls.Report:SetText('Processing '..action..'...')
30:  local ok,err=pcall(UI.RequestPlayerOperation,Game.GetLocalPlayer(),PlayerOperations.EXECUTE_SCRIPT,
31:   {OnStart='SPC_P0_Request',Action=action,UnitID=u and u:GetID(),CityID=city and city:GetID(),Token=token,PlanToken=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.UnitActionPreview and ExposedMembers.SPC_P0.UnitActionPreview.token})
71: local function initialize()
72:  showRoot();refresh()
73:  Controls.PrecisionButton:RegisterCallback(Mouse.eLClick,precision)
74:  Controls.ReadButton:RegisterCallback(Mouse.eLClick,function() read() end)
75:  Controls.SpawnCrewButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_SPAWN') end)
76:  Controls.PrepareUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_PREPARE') end)
77:  Controls.ConfirmUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_CONFIRM') end)
78:  Controls.BuilderTargetsButton:RegisterCallback(Mouse.eLClick,function() LuaEvents.SPC_ToggleBuilderTargets() end)
79:  Controls.CloseButton:RegisterCallback(Mouse.eLClick,function() token=nil;Controls.Window:SetHide(true) end)
80:  local timer=0
81:  ContextPtr:SetUpdate(function(dt)
82:   timer=timer+dt;if timer<0.2 then return end
95:  print('[SPC][B040][UNIT_SITE_UI_READY] visibility fix 52')
96: end
97: ContextPtr:SetInitHandler(initialize)
98: Events.LoadScreenClose.Add(showRoot)
99: ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
```

### UI/UnitTargetMarkers.lua

```text
31:  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
32:  pending=P.VERSION..':TARGETS:'..ExposedMembers.SPC_P0_UISequence;age=0
33:  local ok,err=pcall(UI.RequestPlayerOperation,Game.GetLocalPlayer(),PlayerOperations.EXECUTE_SCRIPT,
34:   {OnStart='SPC_P0_Request',Action='UNIT_TARGETS_READ',Token=pending,UnitID=u:GetID(),BuilderPreview=builderPreview})
86: local function init()
87:  ContextPtr:SetHide(false);timer=0;age=0;active=true
88:  ContextPtr:SetUpdate(function(dt) if active then update(dt) end end)
89:  LuaEvents.SPC_ToggleBuilderTargets.Add(toggle)
90:  for _,name in ipairs({'UnitSelectionChanged','InterfaceModeChanged','LoadScreenClose'}) do
91:   local e=Events[name];if e then e.Add(changed);hooks[#hooks+1]={e,changed} end
92:  end
93: end
94: ContextPtr:SetInitHandler(init)
95: ContextPtr:SetShutdown(function()
96:  active=false;clear();ContextPtr:ClearUpdate();LuaEvents.SPC_ToggleBuilderTargets.Remove(toggle)
```

### UnitActions.lua

```text
1: -- B044: native project crews, explicit legacy DEV spawn, single-use capped injection.
2: SPCUnitActions={}
3: function SPCUnitActions.Start(P,shared)
4:  local data={};shared.UnitActions=data
21:  local function fresh(pid,u)
22:   assert(u:GetBuildCharges()==1,'CREW_REQUIRES_EXACTLY_ONE_CHARGE')
23:   assert(u:GetProperty('SPC_CREW_RESERVED')==nil,'CREW_RESERVED')
24:   local c=target(pid,u);local s=shared.ConstructionProbe.ReadSnapshot(pid,c)
83:      assert(v:GetX()~=c:GetX() or v:GetY()~=c:GetY() or vr.FormationClass~='FORMATION_CLASS_CIVILIAN','MOVE_CIVILIAN_OFF_CITY_CENTER')
84:     end
85:     local seen=Players[pid]:GetProperty('SPC_CREW_DEV_SPAWN') or {}
86:     assert(not seen[p.Token],'SPAWN_REQUEST_ALREADY_USED');seen[p.Token]=true
87:     P.SetProperty(Players[pid],'SPC_CREW_DEV_SPAWN',seen)
88:     destructive=true;UnitManager.InitUnit(pid,'UNIT_SPC_CREW_250',c:GetX(),c:GetY())
115:    local now,s=fresh(pid,u)
116:    assert(now:GetID()==c:GetID() and plan.turn==Game.GetCurrentGameTurn() and s.target==plan.target and s.cost==plan.cost and s.progress==plan.progress,'TARGET_CHANGED_PREPARE_AGAIN')
117:    local receipts=Players[pid]:GetProperty(KEY) or {};assert(not receipts[plan.token],'RECEIPT_EXISTS')
118:    local function record(state)
119:     receipts[plan.token]={state=state,unitID=plan.unitID,cityID=c:GetID(),target=s.target,amount=math.min(amount,s.cost-s.progress)}
120:     P.SetProperty(Players[pid],KEY,receipts)
121:    end
122:    destructive=true;record('INTENT');P.SetProperty(u,'SPC_CREW_RESERVED',plan.token)
123:    assert(u:GetProperty('SPC_CREW_RESERVED')==plan.token,'RESERVATION_UNCONFIRMED')
124:    Players[pid]:GetUnits():Destroy(u)
162:  end
163:  local removed=Events and Events.UnitRemovedFromMap
164:  if removed and removed.Add then removed.Add(function(pid,id)
165:   if plans[pid] and plans[pid].unitID==id then plans[pid]=nil end
```

### UnitSiteProbe.lua

```text
1: -- B040 read-only Gameplay location diagnostics. No grants, consumption or writes.
2: SPCUnitSiteProbe={}
3: function SPCUnitSiteProbe.Start(P,shared)
4:  local data={};shared.UnitSiteProbe=data
50:      -- actual wonder district on this plot; never accepted by itself.
51:      local wonder=P.Info('Districts','DISTRICT_WONDER')
52:      if wonder and plot:GetDistrictType()==wonder.Index and plot:GetProperty('HD_UNCOMPLETED_WONDER')==building.Index then
53:       targetPlot=plot;source='HD marker + current queue + wonder plot'
```

### UnitTargets.lua

```text
1: -- B041: target enumeration, derived read-only data. Not authority to consume units.
2: SPCUnitTargets={}
3: function SPCUnitTargets.Start(P,shared)
4:  local data={};shared.UnitTargets=data
49:         assert(type(index)=='number' and index>=0 and index%1==0,'CITY_PLOT_INDEX_INVALID')
50:         local p=Map.GetPlotByIndex(index)
51:         if not scanned[index] and p and p:GetOwner()==pid and p:GetDistrictType()==wi.Index and p:GetProperty('HD_UNCOMPLETED_WONDER')==b.Index then
52:          local pc=Cities.GetPlotPurchaseCity(p)
```

### YieldCarrierProbe.lua

```text
14:  return values
15: end
16: local function flags(p) return p:GetProperty('SPC_B029_ONE')==1,p:GetProperty('SPC_B029_HALF')==1 end
17: function SPCYieldCarrierProbe.Run(pid,c,action)
20:   if action=='OFF' then
21:    -- OFF always available, even if the SQL definitions are missing in this save.
22:    P.SetProperty(p,'SPC_B029_ONE',0);P.SetProperty(p,'SPC_B029_HALF',0)
23:   elseif action=='STEP' then
26:    end end
27:    if not one and not half then baseline[pid..':'..c:GetID()]=read(c) end
28:    P.SetProperty(p,'SPC_B029_ONE',1)
29:    P.SetProperty(p,'SPC_B029_HALF',one and 1 or 0)
30:   else assert(action=='READ','ACTION') end
```
