# B012 用户实机结果

Document Owner: Codex
Build: P0-B-012 / modinfo19
Verification: USER_GAME_TEST_PASS
Evidence: 用户操作顺序说明与五张原始截图，逐张查看

USER_GAME_TEST_PASS：用户已在实际游戏中验证通过，仅限本次单人测试文明存档中的合成Game Property表。

| 图 | 操作（用户说明） | 状态 | 本次加载写入尝试 | writeCall |
|---|---|---|---:|---|
| 1 | Write test table | MATCH | 1 | RETURNED |
| 2 | 重复Write | MATCH_NO_WRITE | 1 | RETURNED |
| 3 | 保存重载后，只Read storage | MATCH | 0 | NONE |
| 4 | 重载后Write | MATCH_NO_WRITE | 0 | NONE |
| 5 | 再重复Write | MATCH_NO_WRITE | 0 | NONE |

B012-1通过：本次加载有一次实际写入，重复点击未增加。虽未提供最初EMPTY屏，但代码只有读到空值才写，图1的MATCH/attempts=1足以支持本次写入与读回，不要求补拍。
B012-2通过：用户明确说明保存读档；图3在未重新写入时MATCH且attempts=0，之后两次Write仍不写。不是自动补写掩盖丢失。

五张均B012、ACK，无错误状态。MATCH是程序完整逐键比较结果，屏幕下面DEV字段属于预期值说明，不把它们当独立原始读数。程序已比对revision=1、counter=2、两个字符串键记录、嵌套数值0.5/42、17/0以及true/false。

结果允许继续准备持久身份/事实表适配，不证明真实城市代际、任意大小或结构Property、多人、崩溃原子性、跨Property事务或专业/收益通过。B010仍延后，无新增用户测试。

## 当前原图清单

原名保留于Specialization/ScreenShots；本轮不移动、压缩或删除。下面只记录文件名/大小/hash，不承诺临时收件箱永久可用。

| 图 | 文件名 | 字节数 | SHA256 |
|---|---|---:|---|
| 1 | Screenshot 2026-09-11 at 5.53.02 PM.png | 10925609 | `2eaac79b62b6d731146fd3bf200f046e982ef10f5d52d877dad9ffb399082cc3` |
| 2 | Screenshot 2026-09-11 at 5.53.14 PM.png | 10930036 | `3ddf2bfe5a3cf3a2fe0b05b5e4176305bfe94944d550b2a6278f3fec3a2cab2d` |
| 3 | Screenshot 2026-09-11 at 5.54.22 PM.png | 10931563 | `b23c61bc2a88d2f013ea95ec224207a006a79166384298dee448927b0a5436af` |
| 4 | Screenshot 2026-09-11 at 5.54.24 PM.png | 10914651 | `b064e58bebd361ee8272c5df9e986f3ac0693b25634bee880d50ce62d145caad` |
| 5 | Screenshot 2026-09-11 at 5.54.27 PM.png | 10916425 | `623be2963ef0a8683f3179a5a99de90fc54e566760521eb94bb5ef3ba051b196` |

## 旧证据可用性与归档建议

用户说明习惯清空ScreenShots后投入新图。当前原目录仅有B012五张；B011原14张已不在该目录，原结果报告的图像链接因此不再可用。保留B011当时逐张判读、时间/数值/hash及用户说明；不重写冻结报告，不把hash当可恢复原图，也不因原图后续清理撤销当时有证据的PASS。没有要求用户重拍。

建议未来由用户只投递ScreenShots，助手完成判读后将关键原图按批次存Status/Validation/Evidence/<batch-date>/，保留原文件名并记录索引；重复图只保留必要证据，不默认自动删除任何原图。归档尚为建议，未执行，目录/owner规则未变更。正常报告长期保存，图像按里程碑保留/用户确认后清理，避免无限增长。

本轮只更新结果和状态/入口，运行源码、Tests、Design及截图均未编辑，没有运行游戏。
