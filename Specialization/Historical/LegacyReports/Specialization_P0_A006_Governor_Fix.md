> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

# A006 总督查询修订

用户确认：专业区域存在与否、建造完成状态、区域类型、专家读取与数量正确。登记USER_GAME_TEST_PASS，已通过分支不改、不重测。

用户截图 Screenshot 2026-09-10 at 10.03.44 PM（系统文件名包含窄空格，原图保留在ScreenshotInbox）显示：

```text
SPC P0-A-005
READ FAILED: GOVERNOR
At: BEFORE_GetAssignedGovernor
Probe.lua:295: GetAssignedGovernor:ABSENT
```

这是P.Call发现方法不是function后返回ABSENT，不能解释为没有派遣总督。登记USER_GAME_TEST_FAIL。当前没有证据说明IsEstablished或HasPromotion失败，因为尚未运行到这些步骤。

A006只改查询入口：player:GetGovernors():GetAssignedGovernor(city)。本机官方Expansion1/UI/Additions/GovernorAssignmentChooser.lua:90使用该形式。返回nil才按无总督显示；方法缺失继续报错，不伪造assigned=false。还不能承诺该对象在Gameplay与UI一致。

本地模拟删除旧城市方法，玩家管理器核验city参数，并测试两层缺失、nil、晋升与建立状态；test_specialization_p0.py通过。未在游戏中验证。

## 仅一次复测

1. 用户下次手动重启游戏，加载现有存档，确认面板P0-A-006。
2. 选已派遣总督的城市，只点Read governor一次。无需等待建立或过回合。
3. 将自动显示的结果截图放ScreenshotInbox，保留默认文件名。

入口PASS：出现ACK、lookup=PlayerGovernors.GetAssignedGovernor(city)、assigned=true及established值/晋升计数/Req2/3/4；这些值还需后续单变量实验验证语义。FAIL：READ FAILED，保存At及错误文字；NO RESPONSE则记录为请求链异常。先停止，不重试多回合。不要重测Specialist。

如果玩家管理器方法也不可用，下一轮研究UI只读Governor数据与Gameplay原生Req属性分开展示。UI数据不回写权威状态，网络激活应使用Gameplay可验证依据。
