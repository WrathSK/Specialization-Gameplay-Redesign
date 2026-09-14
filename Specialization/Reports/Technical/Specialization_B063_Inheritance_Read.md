# B063 收尾与城市继承观察

Document Owner: Codex
Design: D0024 unchanged

四专业Lv1–4主要收益、Crew、网络/标准化/Boost/巨作已有运行实现和按Status标注的用户证据。不要将暂缓的商业C/P实测或未覆盖组合冒充完整测试，也不以全部核心收益存在宣称v0.1完成。

当前完整v0.1缺口：PROG004已有身份跨Owner永久投资继承；PROG006–010无身份城市在易主时冻结LegacySet并走Claim或正常完成分支；ELIG通用运行资格和玩家入口清理。Claim成本未决，Future辅助系统不自动纳入。

Binding/CityFlow/CityJournal/EffectiveFacts/Standardization已有Owner/CityID/token交叉锚点。只放宽Owner或重置账本会丢投资/复制成果，不这样处理。B063先用原位置定位读取五项City Property深拷贝对照，坐标不是永久身份；不写/迁移状态，无周期扫描。先验证引擎保留行为，再设计受校验的正式迁移。

模块CityInheritanceRead.lua；Gameplay仅请求入口；P0新增Record/Read inheritance，暂隐藏Commerce OFF/TEST5，保留代码及AUTO/Read。不修改商业收益/SQL/Design。测试入口DevelopmentTests/test_b063_inheritance_read.py：真实新模块无写入，Owner/ID变化、深表差异、Property丢失、位置无城、权限及加载重置；串联B062生产代码与SQL回归。LOCAL_SIMULATION_PASS不是原生继承通过。

## 本轮验证与部署

2026-09-13：test_b063_inheritance_read.py及串联B062/前批回归成功；git diff --check通过。B063.89源/运行包109文件SHA256均为993622980827e87b9503ac38eef0423621e003193aa0c6d82ac7a508f32d3412。完整旧包保存在外部SpecializationDeploymentBackups/.SpecializationP0-backup-00mapkt7。D0024 SHA256仍为4f7d0169a3a8abce67501010a9c8ca600e345ce8b1ae23f3af6c28be069144f1。未启动游戏、未commit/push。
