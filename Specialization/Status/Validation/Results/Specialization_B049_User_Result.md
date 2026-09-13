# B049 用户结果与网络提示整理

Document Owner: Codex
Build after fix: P0-B-049 / modinfo63

## 用户结果

USER_GAME_TEST_PASS（用户实机验证通过），范围来自本轮口述：水力作坊提供的非相邻区域产出可正常读取，符合设计；工业网络最高输出来源可读取，总督调离可撤销；整体只读批次通过。未建立行业，不把此证据写成行业实测。不是50%正式收益发放通过，移民UX未在本次口述中独立确认。

唯一截图已逐张查看并按原名归档到../Evidence/B049/，manifest记录SHA256，移动前后一致。图中Stirling(Test)#65536 Research ACTIVE4，工业区Production4，科研50%预期2。工业读取显示NETWORK_REFRESH_PENDING，原始Lua堆栈/路径被直接附到报告中。

用户描述该城未接入工业网络；截图本身只证明网络快照尚未满足新鲜度检查，不能把pending解释成“无网络”。没有确定pending的具体触发原因，也没有修改网络刷新/资格逻辑。

## 修正

仅Lv4CopyRead.lua展示分支和manifest62→63：
- 新鲜数据、无来源：本城尚未接收工业网络；本项生产力预期为0。
- 新鲜数据、有工业接收资格但无ACTIVE4来源：已接收工业网络，但当前没有有效工业四级来源；本项预期0。
- NETWORK_REFRESH_PENDING/CURRENT_COUNT_CHANGED：网络数据正在刷新，暂不能判断接收状态；稍后重新读取。不把未知填0。
- 尚未就绪/其它失败：简短中文；详细堆栈保留Lua.log的COPY_NETWORK_DETAIL/COPY_READ_DETAIL，不塞进面板。

科研本地计算在网络等待时继续显示。没有修改来源选择、max、50%、商路集合、投资、施工或任何SQL。D0012 hash不变。

## 本地验证及下一步

LOCAL_SIMULATION_PASS（本地模拟通过，不等于游戏验证）：test_b049_network_notice.py覆盖上述状态、路径/堆栈过滤、科研显示保留，并重跑实际移民/Crew/来源读取回归。其余运行文件逐字未变。新提示USER_GAME_TEST_REQUIRED，但不派独立测试，后续使用时顺便观察。

本轮测试关闭，无需补图/重做。下一步仍为固定50%小数收益的精确发放与撤销调查；现有通过只解决基数读取和来源选择，不解决原生小数承载。
