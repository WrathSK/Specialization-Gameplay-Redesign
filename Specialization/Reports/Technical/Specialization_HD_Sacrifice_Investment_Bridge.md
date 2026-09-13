# HD献祭/回收先例与投资账本衔接

Document Owner: Codex
Design: D0009 unchanged
Runtime: B031 / modinfo39 unchanged
Status: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS

## 已查清的调用链

本机HD根目录为Steam/steamapps/workshop/content/289070/2465378070。

- UI/Additions/HD_UnitCommandDefs.lua:97–171：RECYCLE配置EventName=HDRecyclingPlantRecycle，UI检查陆海空类别、己方对应区域、回收中心Property、满血与移动力。
- 同文件:177–226：SACRIFICE_CHICHEN_ITZA配置EventName=HDChiChenItzaSacrifice，UI检查陆战、拥有奇观、SACRIFICED_CHICHEN_ITZA类型账本、奇观所在plot、满血与移动力。
- UI/Replacement/DL_UnitPanel.lua:528–548：点击读取当前选择单位，先RequestCommand(EXECUTE_SCRIPT, EventName)；默认未设置DoNotDelete=true时，再发DELETE。CanStartCommand DELETE不成立则发HDDestroyUnit EXECUTE_SCRIPT。
- Gameplay/UnitAbilities.lua:258–282：回收读取生产/资源成本并加Gold；该奖励函数本身不删单位。
- 同文件:286–305：献祭写player的单位类型Property、按Combat计算奖励、AttachModifier；该函数本身不删单位，也没有完整重复请求/现场资格复验。
- Gameplay/Misc.lua:674–681：HDDestroyUnit重新GetUnit，存在则Players[playerId]:GetUnits():Destroy(unit)。

STATIC_CONFIRMED说明源码存在这些路径，不证明本项目同一回调消耗后的单位查询立即更新，也不证明HD两请求原子提交。可借鉴单位按钮/脚本请求/Gameplay删除，不直接复制奖励+删除的两请求结构。Specialization未来只发一个操作请求，由Gameplay检查资格、保存意图、消耗确认和提交。若未来使用HD通用按钮框架，必须DoNotDelete=true，避免框架再次删除；本轮没有修改HD文件或挂载该框架。

HD特定的满血/剩余移动力/建筑plot限制不是PROG-002设计，不移植。目标位置的最小DEV支持范围在真实入口准备时明确，不将技术支持范围写为永久Design限制。

## 存储候选已实现

DevelopmentTests/InvestmentStoreBridge.lua包裹现有CitySpecializationState和SettlerInvestmentExecutor，接受已核对的B020 SupportFacts形状。保留B015/B020建立专业时的potential=1与first记录，不写旧记录；新增账本只持久化投资凭据、revision、pending及城市/首个区域anchor。

总Potential由1+有效凭据数推导，不保存第二个可独立修改的总Potential。specialization仍从原专业事实读取；账本anchor中的specialization仅作一致性校验，不能覆盖原专业。读空账本只返回基础状态，不隐式写入或迁移。发现anchor变化、无已建立专业、账本不合法或未确认投资，不提供可结算高级事实。有效ACTIVE继续由既有规则计算，不作为永久事实存储。

此模块仍为MOCK_ONLY：foundation回调将来应调用实际SupportFacts而非自行推测区域历史；token只沿用DEV身份，未证明跨owner永久UID。合成firstCompletion/eventID仅为离线reducer适配引用，不伪造新引擎事件。跨owner征服、完整账本丢失、unitID代际重用没有因本候选而解决；不重复展开极端恢复。

## 本地验证与接入清单

test_investment_store_bridge.py通过：真实形状foundation + executor连续1→4、基础表不变、账本不另存Potential/ACTIVE、读取不写、重建adapter/executor与重复操作不重复消耗、总督离开ACTIVE1而Potential4、token/first区域变化、重复单位凭据、pending、无专业拒绝。此处重建对象不等于实际游戏存读档。test_settler_investment_executor.py回归通过。

接下来：原生Property adapter；统一有效事实入口给Lv1及网络（现NetworkBridge potential==1不可沿用）；请求绑定具体移民和城市并重新核对；完成这些后再开放最小实机按钮。本轮没有新UI、真实消耗或实际收益，运行/Design未改，无用户测试要求。小数收益研究仍暂停。
