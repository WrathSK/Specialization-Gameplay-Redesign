# 旧工作区资料迁移与历史路径映射

2026-10-02。用户已授权完整迁出游戏支持目录下的旧Specialization，并明确增加全局旧路径引用审计为删除前门禁。本说明仅维护资料位置；不改变Design、玩法、部署或验证结论。

## 本次实施计划与删除门禁

1. 扫描main/develop受跟踪文本、现有本地配置、游戏支持工作区入口，以及旧Specialization/DevelopmentReports/DevelopmentTests/DevelopmentBackups的相关文本；检查直接路径、W路径、编码形式和相对链接的实际解析结果。不扫描无关私人目录、游戏数据库、原始日志或其它Mod。
2. 当前有效入口和导航必须直接修正；冻结历史、验证原件、既有hash/迁移清单不改正文；用途不明的引用列出后停止删除，不以批量替换处理。
3. 完整复制旧目录，保留内部相对结构和原件，比较目录/文件集合、大小及逐文件SHA256。
4. 切换当前归档位置和工作区路由，重新扫描；没有未解决的active旧目录依赖、没有未知分类、源内容未变化，才移除旧目录。
5. 原始截图、映射核验原件和大体积材料只保存在Git忽略的local/，不提交Git；本说明及必要当前导航按分支单独提交。无软链接/redirect目录替代已移除的旧目录。

## 当前入口

- 正式开发资料：develop的`Specialization/`；源码为同一worktree的`Mod/`。main继续维护稳定源码及自己的配套说明。
- 新截图投递：develop根目录`ScreenShots/`。
- 已归档截图及后续原图归档：develop根目录`local/legacy-workspace/Specialization/Status/Validation/Evidence/<Batch>/`。
- 旧文档完整留存：develop根目录`local/legacy-workspace/Specialization/`。这里的旧README/AGENTS/Status是历史原件，不作为活动指令加载。
- `ScreenShots/`与`local/`整目录均被Git忽略；克隆Git不会取得这些本地原件。

## Relocation mapping / legacy path mapping

定义：W为原游戏应用支持工作区；R为当前develop worktree；M为main worktree。旧记录里的绝对路径、file链接、URL编码、JSON转义均先解码，再按下表定位；内部文件名/相对后缀不变。 冻结原件中的相对链接先以该原件**迁移前所在目录**解析，再应用映射；若链接跨出旧Specialization指向W内的Tests/Backups/运行包，则目标仍在W原位置，不按新归档目录直接拼接。

| 历史路径表达 | 当前对应位置／用途 |
|---|---|
| `W/Specialization/<relative-path>` | `R/local/legacy-workspace/Specialization/<relative-path>`：定位当时的原件，不替换成不同版本的当前文档 |
| `W/Specialization/Status/Validation/Evidence/<relative-path>` | `R/local/legacy-workspace/Specialization/Status/Validation/Evidence/<relative-path>`：原图与manifest原样保留 |
| 历史结果中的相对`../Evidence/<relative-path>`或本地缺失的`Specialization/Status/Validation/Evidence/<relative-path>` | 按上行证据根定位；它不表示Git里包含图片 |
| `W/Specialization/ScreenShots/` | 当前投递入口为`R/ScreenShots/`；原收件箱此前已迁出，不虚构旧截图副本 |
| 旧入口所指“当前Design/Architecture/Status” | 使用`R/Specialization/README.md`及Authority当前指针；查看当年原件则使用第一行映射 |
| `W/DevelopmentBackups/`、`W/DevelopmentReports/`、`W/DevelopmentTests/` | 不随本次迁移；冻结备份/旧测试留在原处，纯跳转页的链接更新。当前测试从R/DevelopmentTests进入 |
| W内真实运行Mod、存档、日志、数据库及部署恢复目录 | 不迁移、不改配置；仍按部署合同及实际receipt确认 |

`local/config.json:legacy_workspace`若仍为W，不自动改成新归档根：W内其它外部材料仍在原位。现行截图归档直接使用上述R下的明确位置；不依赖缺失的本机配置。Phase1_External_Materials及既有迁移清单描述当时位置，原文保留，当前位置以本映射与现行入口为准。

外层DevelopmentReports的纯跳转页：历史文件转向实际存在的对应R文档（路径不一致时转向保留的归档原件）；“当前Status/Architecture/README”转向R中的活动入口。不能把冻结历史报告的当前/下一步表述当作新授权。

## 核验与证据边界

完整文件清单、源/目标SHA256、引用分类和删除前后检查保存在忽略的`R/local/legacy-workspace/relocation-20261002.json`，只是一份本次迁移核验记录，不是新的authority、工作流状态系统或实机证据。任何缺失的历史目标仍按原来的缺口处理，路径映射不证明从未存在的材料已经恢复。

截图归档依旧逐张阅读、批次明确后移动、比较SHA256，保留同名冲突与未读内容，不擅自删除/压缩冻结原件。后续读取历史证据时沿本映射定位，不能仅因旧绝对路径不存在就宣称证据丢失。

本次迁移完成：1275个文件、6425348262字节，文件/目录集合及逐文件SHA256一致；删除前活动旧目录依赖0、未知分类0，74个更新后本地导航链接目标核验通过。游戏支持目录下的旧Specialization已移除。此结果只证明本次迁移完整性，不增加玩法或实机PASS。
