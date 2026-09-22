# B093.120 单城映射实验暂停：实机复核

USER_GAME_TEST_FAIL：本次实验被运行时函数调用错误阻断，不能确认自动保存/冷恢复闭环。单张截图不能判断发生在启用、转移或加载的哪一步，也不证明新key是否曾写入。

截图明确：P0-B-093.120，T8；报告 `ACK | 身份映射实验暂停： function expected instead of nil`；当前选中EDINBURGH (TEST)。不是正常HELD证据不足结论，不归因为用户没有选城市。原图已归档，移动前后SHA256一致，见旁侧Evidence JSON。

## 定向代码证据

STATIC_CONFIRMED：CityIdentityMapping.lua两处新事件包装使用`table.unpack`，在进入observe的ready/record/相关城市检查之前求值。guard会锁存该异常。旧CityIdentityExperiment采用`pcall(observe,n,...)`，没有此新依赖。当前Mod搜索仅新文件使用table.unpack。

LOCAL_SIMULATION_CONFIRMED（故障注入，不是原生根因证明）：使用实际模块和现有fixture，将table.unpack设nil；未Begin时触发一个无关CityAddedToMap，立刻锁存`attempt to call a nil value (field 'unpack')`，writes=0，之后Begin显示实验暂停。Lua55默认提供该函数，原回归没有覆盖缺失接口。

此模型证明存在具体兼容性薄弱点，但原生截图措辞不含调用位置，不能确认Civ VI当前context的table.unpack确实缺失或排除其它nil调用。本次未找到工作区内Lua.log，未修改日志配置。真实失败阶段、实际写入次数仍UNKNOWN。

## 建议的最小修复（尚未实施）

复用旧模块已使用的直接varargs/pcall传参，取消table.unpack依赖；在事件入口尽早检查是否已启用及是否暂停。诊断错误增加简短阶段标记（加载/登记/事件名/核对），不打印堆栈或扩大日志。补充table.unpack缺失环境、未启用无关通知及真实路径测试，保持新key/旧账本隔离。

不要求用户重复失败测试。修复须另行授权；本轮仅证据、状态、只读故障定位，无runtime/Design/main修改，无部署，不进入E2/F。B090保存与B092事件shadow既有局部PASS保留，不被本次错误推翻。
