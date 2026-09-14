# AV2-I001 文档与隔离验证

Document Owner: Codex
Evidence: STATIC_CONFIRMED — 本地文档、源码读取及hash核对，不是Civ VI实机PASS。
Date: 2026-09-14
Source baseline: `e3651f9b7c90110f3a8890a7b12ca299996b306b`

## 本地检查

- 34组状态归属、29条依赖、37组模块评级、298条事件目录记录；记录数不等于引擎事件实际触发数，部分同事件双listener在work列合并注明。
- 索引覆盖Mod全部72个Lua文件的SHA256；manifest启动入口及注册/Property原文摘录保留。
- 独立匹配当前非隔离源码的直接`.Add`注册（7处）、字面量helper注册（37处）和Context生命周期/SetUpdate：目录缺项0。循环注册在Event_Catalog展开并对照Source_Index；自动匹配不替代实际事件存在/顺序的实机证据。
- 目录分类限定DIRECT / INDIRECT / RECONCILIATION / DIAGNOSTIC；所有SourceLine在实际文件范围内。ContextPtr冒号调用和TradeRouteProbe load hook引用已校正。
- 新增Markdown相对文件链接全部检查；`git diff --check`检查本批空白错误。历史文档的旧外部路径未改写。
- 未运行会改变runtime的测试；没有请求新实机验证，没有引入source/cache/carrier/listener/UI改动。

## Stable保护

- main HEAD仍为`e3651f9b7c90110f3a8890a7b12ca299996b306b`，worktree clean。
- develop源码、main源码、外部SpecializationP0三方115文件完全相同；modinfo96。
- 三方Mod SHA256摘要：`7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`。算法：按相对路径排序的文件SHA256字典，紧凑JSON后SHA256，与现有deploy工具一致；只调用只读snapshot，没有apply。
- D0025 SHA256：`81dc772c1038718e567496cfdb165167e6090fae2b7b472b7301435d766d994b`，与source baseline相同。
- Mod / Design / DevelopmentTests / tools相对baseline无差异。没有写main、运行副本、存档或配置。

## 发布门禁

本批仅Architecture/Status及v2调查文档。提交后检查develop clean，再正常push origin/develop并确认HEAD一致；main与baseline tag不变。Git最终hash与远程结果见本轮交付，不以生成本文代替push成功检查。

尚未授权任何重构或develop实机切包。所有TARGET、A–E批次和milestone tag建议都待用户审阅。
