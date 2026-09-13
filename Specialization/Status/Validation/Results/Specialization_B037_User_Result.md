# B037 实机结果：收益正常，晋升触发遗漏

Document Owner: Codex
Tested Build: B037 / modinfo46

USER_GAME_TEST_PASS：用户明确其它行为均正常，按当前Lv3支持批次登记收益、撤销/恢复/重载正常范围；不要求补截图，不扩大至未实现高级能力。

USER_GAME_TEST_FAIL（限定操作顺序）：先投资Potential2→3，再同回合晋升已建立总督2→3，文化/商业专家Lv3载体仍0，收益未更新。先晋升再投资则正常。用户说明科研/工业总督原存档已3/4级，故不能据此推断故障只影响文化/商业。

截图11.38.33：CULTURE city131073，workers2，Lv3 top-up0F0P0G，READY。11.38.42：COMMERCE city327684，workers2，top-up0F0P0G，READY。11.44.20：CULTURE city131073，workers2，top-up2F2P0G，READY，已恢复。均回合24；第三图具体触发动作未由图片证明。

用户实际验证可触发恢复：调整专家、过回合、存读档、其它城市投资。其它城市的总督单独晋升不触发恢复；其它城总督此前已晋升3后再投资才恢复。未试再次晋升/投资、买建筑/单位、改队列等，不要求扩展。

与B035已接受GPP读数延迟不同：此处实际Lv3载体未应用，非仅全国最终率晚显示。静态发现Lv3与后台通知均遗漏GovernorPromoted事件；和而不同Gameplay/RegionalYields.lua:274使用该事件。符合用户观察，但修正后的引擎时序仍需实际证明。

三图按原名及SHA256归档于../Evidence/B037/manifest.json。
