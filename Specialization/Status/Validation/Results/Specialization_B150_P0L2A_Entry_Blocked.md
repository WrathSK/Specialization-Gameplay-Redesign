# B150.177 — L2A原生入口中止与打包漏项

Evidence: USER_GAME_TEST_BLOCKED_ENTRY；STATIC_CONFIRMED；局部LOCAL故障路径复现。原生小数精度/归属/退出仍PRECISION_NOT_TESTED。
Baseline: develop记录4692582，运行源码c66b053、B150.177 / modinfo177。本轮不改源码、测试、Design或部署；[原LOCAL结果](Specialization_B150_P0L2A_Local.md)保留其范围。

## 截图直接证据

一图已逐张查看，原件移动至Git忽略目录 `local/legacy-workspace/Specialization/Status/Validation/Evidence/B150_P0L2A_Entry_Blocked_20261002/`。同目录manifest保存原名、字节数、SHA256及本结果关联；移动前后1/1 MATCH，不复制进Git。

图为T60、Edinburgh已选中，专业按钮显示文化4级，左侧可见学院/图书馆、商业中心/集市；诊断显示 `P0-B-150.177 | ACK | 意义延展验证：城市或接口暂不可读。`。没有阶段、W、D、载体配置或原生差值。文化4级标签不单独证明ACTIVE4；也未从本图确认合格W、点击次数、左/右键或当前实验模式。

ACK只证明匹配版本/token的回复，不证明实验操作成功。不得据本图判定0.5被截断、primitive不支持小数、收益已施加或旧GWA已暂停。用户已中止测试，暂不请求更多同类截图。

## 确认的工程缺陷

- `Mod/SpecializationP0.modinfo`总`Files`列出`CultureMeaningModel.lua`和`CultureMeaningProbe.lua`，但现有`InGameActions/ImportFiles`两项均缺失；相邻Aesthetic两个Lua均有导入。这是STATIC_CONFIRMED打包漏项。
- `Gameplay`先注册请求监听，再加载/启动Meaning。外层pcall包住城市、模块、View、Describe，失败后丢弃实际异常，统一返回截图文字；Advance本身另有内层pcall，单独拒绝应显示具体操作错误。
- 先前新测试仅检查总Files、SQL action和include文字；继承的模拟include直接读磁盘，不受ImportFiles名单限制。LOCAL通过没有覆盖实际action导入可见性及真实新请求外围。这是本批验证缺口，不修改旧证据冒充当时已查。

首要解释是漏导入使后台模块不可用，已注册监听仍可回ACK。未取得本次引擎原始include/启动异常，**具体原生失败行尚未确认**。若成功View/token已发布，UI应追加原生段；截图未见该段，静态顺序更支持在成功发布View之前失败，但不替代trace。

## 局部复现的边界

使用已有Lua55依赖、当前原样Gameplay请求块，注入Advance拒绝得到正常描述/具体错误；注入缺城市、缺View、View/Describe异常得到截图通用文字。另按实际ImportFiles名单限制模拟include，以未导入脚本不可见/返回false为明确假设，复现启动nil与随后ACK通用错误。模拟没有修改游戏、DB、源码或测试文件；不是原生VFS行为实测，不证明其它潜在异常已排除。

## 建议的最小修复（尚未授权/实施）

1. 仅将两个Lua加入现有SPCP0_Common ImportFiles，不改变能力规则、载体公式或默认关闭状态。
2. 请求外围保留简短阶段与有界实际错误，区分城市、模块、操作、View、Describe；开始清掉旧view，成功后发布本次view。未知不写0，不新增长期debug体系。
3. 补action导入断言、受导入名单限制的加载检查及真实新请求入口正常/失败覆盖；不以磁盘可读代替引擎加载注册。
4. 修复获授权且完成本地验证/安全部署后，只先核对同城入口；能显示正常基线再继续原定精度流程。未进入测试模式的报错截图不要求重做整套长测；若原生仍失败，根据保留的具体阶段定域处理。

当前无新Gameplay决定，不采用Floor、不进入L2B。可能已执行到哪个实验阶段不能从图确定；恢复测试宜用未开启probe的存档副本冷启动，避免凭报错猜测模式。当前运行包仍B150，本轮不关闭/启动游戏、不部署。等待用户授权上述入口修复；[最新切片](../../../Architecture/v2/P0_L2_Meaning.md#当前切片与停止点)及[Status](../../Specialization_P0_Status.md#current-authoritative-state)记录停止点。
