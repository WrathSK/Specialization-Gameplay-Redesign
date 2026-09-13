# B052 缺少模板按钮：部署备份同UUID冲突

Document Owner: Codex
Status: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; user restart verification required

用户报告没有Read templates。源包与部署包均为B052/modinfo68，哈希一致，XML中按钮可见，无位置重叠。当前Modding.log明确给出：

```text
[2575784.864] Loading Mod - .../Mods/.SpecializationP0-backup-oabsdi42/SpecializationP0.modinfo
[2575784.864] Loading Mod - .../Mods/SpecializationP0/SpecializationP0.modinfo
[2575803.864] GameplayScripts - Registering .../Mods/.SpecializationP0-backup-oabsdi42/Gameplay.lua
```

旧备份version67和当前version68使用相同UUID。此前部署工具错误地以隐藏目录方式将备份保留在Mods；游戏仍扫描隐藏目录，并在本次加载中注册旧备份脚本。不可把“部署文件一致”当成“游戏实际加载该文件”。

修正：
- 只移动已核验的本工具旧备份到`runtime_dir.parent.parent/SpecializationDeploymentBackups/.SpecializationP0-backup-oabsdi42`，与Mods同级，保留全部内容，未删除备份。前后哈希为`8d75ee5bf8c12d9c489ef0a15c01204140a22042de0e0c6c81536228b2380585`。
- deploy.py把stage、backup和失败包均置于上述非Mods目录；新增同UUID扫描冲突拒绝与路径保护。
- test_deployment.py在临时目录验证隐藏备份冲突拒绝、扫描树仅一个manifest、回滚与成功备份隔离；原hash/未知文件/符号链接/无关Mod保护继续通过。
- 当前运行包与源码均保持`59389309e2b0d39269642da118203854a48025e7f07fcb17c1434510906ab68d`，79文件，B052/modinfo68。没有新的玩法/Design/SQL修改，不升运行版本。

STATIC_CONFIRMED表示日志和文件静态证据；LOCAL_SIMULATION_PASS表示临时部署回归通过，不等于游戏通过。不将本事件记作模板学习逻辑失败或通过。用户完全退出游戏、重启后加载原存档，确认B052及Read templates/Next templates，再继续原B052测试。没有启动/关闭游戏或修改配置；没有清空缓存。
