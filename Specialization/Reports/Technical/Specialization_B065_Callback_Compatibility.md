# B065 事件回调兼容性修复

Document Owner: Codex

用户B064三图：InheritanceShadow.lua74 function expected instead of nil，栈由safe/pcall捕获，事件0；手动Select和Game持久备份成功。该行唯一外部函数调用table.unpack，标准Lupa Lua55具备而游戏上下文无可用函数。修复直接safe(fn,...)→pcall(fn,...)，不尝试其它unpack兼容猜测。

加载自动Capture和全部事件原先同被阻断；不把手动SELECT成功当自动PASS。新增真实模块测试先禁table.unpack及unpack，确认加载与事件成功，nil/false/0不丢失；既有收益回归保留。短错误码/完整日志分开，未吞错误。Probe/XML版本标签漏改已修正为B065.91，manifest91。

没有接正式身份继承、没有改变Game备份结构或覆写旧成果。用户无需重测已经通过的持久保存，只有一张转移后的事件报告。D0025及25%模型/SQL字节不变。
