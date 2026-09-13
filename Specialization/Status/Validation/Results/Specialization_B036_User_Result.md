# B036 用户实机结果：工业Lv1专家支持

Document Owner: Codex
Build: P0-B-036 / modinfo44
Result: USER_GAME_TEST_PASS（以下已观察范围）
Evidence: ../Evidence/B036/manifest.json；八张原图已读取后归档，原名与SHA256保持。

城市巴尔的摩 city=524295，四组均1名工作专家、回合3、error=NONE。

|组|报告截图时间|专家截图时间|BASE|carrier新增|专家总收益|工业区显示|changes|
|---|---|---|---|---|---|---|---|
|初始|10.36.16|10.36.19|1|3F1P|3F3P|1P|2|
|完成航空港后|10.37.38|10.37.06|4|3F4P|3F6P|4P|4|
|完成水渠后|10.37.58|10.37.54|6|3F6P|3F8P|6P|5|
|相邻100%卡|10.38.42|10.38.34|6|3F6P|3F8P|12P|5|

组2–4的组内时间顺序是专家图在前、报告在后，按内容对应，不按用户概述强行交换图义。航空港/水渠操作与政策名称依用户说明，截图独立显示结果变化。

## +2P来源

只读当前 DebugGameplay.sqlite：District_CitizenYieldChanges中DISTRICT_INDUSTRIAL_ZONE / YIELD_PRODUCTION / YieldChange=2。这是区域原有专家基础产出。B036九个Building_CitizenYieldChanges仅提供Food3与基础相邻二进制权重。四组实际总值均准确等于原有2P加本Mod新增1/4/6/6P，无重复加2P的证据。STATIC_CONFIRMED为数据库证据；结合截图支持本局实际原生叠加。

IND-001的“增加相当于Base adjacency的Production”按附加收益实现，不替换或扣除原有专家基础。此前交付/报告expected未明确强调新增而非总量，现以此记录澄清；不更改Accepted Design或收益源码。未来诊断建议改为Added per worker并提示原生总量另含基础收益。

## 验证边界

USER_GAME_TEST_PASS：整数基础相邻1→4→6动态收益；相邻翻倍后区域12但专家仍8P，carrier变化数仍5；1名专家原生Food3及新增BaseP。用户另明确确认存读档无问题、工业专业可正常网络接入/分发，分别作为人工回报PASS，不伪称八图包含重载或商路证据。

未扩大至：多个工业专家、负数/小数/超范围、AI/多人、所有异常撤销、网络正式收益、施工队。无需为这些边界立即补测。B035共同Lv2 GPP仍未测。

面板固定标题仍SPC P0-B-035，但ACK/正文P0-B-036；属于漏更新显示文字，登记下一次UI整理修正，不推断运行了错误版本。
