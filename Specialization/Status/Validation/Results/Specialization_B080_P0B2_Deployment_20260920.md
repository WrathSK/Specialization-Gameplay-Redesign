# B080.107 / P0-B2 deployment — 2026-09-20

Implementation: `c56c6de793ba5bac4d6c5a6de61f360c3490d81a`. Authorization: standing W0003 development-test deployment, not stable promotion. Source clean and pushed before activation. Native game validation pending.

- Before restore AND activation, read-only OS process check found no Civilization/Civ6/Aspyr process. No process launched or terminated.
- Existing temporary_playtest restore→activate transaction; no raw file-copy bypass or tool changes.
- Live modinfo107; all126 files equal committed Mod/ per-file hash and file set.
- Package SHA256: `65bcf9271d282a7510174df810ca0453f1eea02be2dd512e79b4c04233ceedb5`.
- B079.106 recovery: `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups/.temporary-develop-backup-3g5mcdu9`; exact126 files/digest `c4b54513bf1b7becd7b7836743703d7532361bd617577f8278cca1f04f23fc5f` verified after restore.
- New active receipt: `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups/B080.107-c56c6de-playtest.json` (DEVELOP_ACTIVE). Old B079 receipt now STABLE_RESTORED and points to B079 recovery.
- Stable backup retained by new receipt, equals main B069.96 digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`. Main HEAD unchanged `e3651f9b7c90110f3a8890a7b12ca299996b306b`.
- No pending deployment marker. All backups outside Mods; no duplicate runtime UUID.

Runtime: `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Mods/SpecializationP0`.

Minimal user check: open game manually, header `P0-B-080.107`. Use one prepared ACTIVE>=II city and `基础设施 / Lv2住房与专家`. Check housing expected/carrier; assign0→1→2 working specialists, added base GPP should0→2→4 per matching class (Culture three classes each). Compare native housing/Great People rate with other sources held fixed. No forced pillage/disaster/war; engine pillage timing remains untested. Existing advanced effects remain outside this delta. Do not overwrite an important stable long-play save.

Hash verification is not engine PASS. [Implementation/local evidence](../../../Architecture/v2/P0_B2_Lv2_Qualification.md). P0-C not started; stop for user validation.
