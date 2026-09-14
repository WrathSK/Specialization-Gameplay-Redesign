# B064 备份通过、事件回调失败

Document Owner: Codex
Evidence: 用户口述及2026-09-13三张截图，回合24。

三图都保持Game账本rev2、城市备份rev1、UID DEV-B013-P0-6、INDUSTRY、投资3/模板6/pending nil。1.51.07原端点0/393221，五项当前与备份一致；1.51.38当前1/196610，五项City Property无、Game备份仍有；1.52.51读档后仍3/6，本次加载写入0。保存原因均SELECT。事件总序号均0，Hook均ON但InheritanceShadow.lua74报function expected instead of nil，堆栈指向table.unpack。

USER_GAME_TEST_PASS：手动选择后的独立备份、易主后读取、保存读档保留。不能把SELECT备份当加载自动备份已通过。
USER_GAME_TEST_FAIL：加载/转移事件回调不能执行，事件序号0。不是城市转移无事件的证据；注册ON不代表callback成功。正式继承未实现。

源码当时Probe.VERSION和XML标题确实漏留P0-B-063.89，modinfo90与B064新报告存在，不归因为用户没重启。B065修正。原截图与SHA256归档外部Evidence/B064-Backup-Pass-Callback-Fail，冻结不纳入Git。
