# Institution icon sources

These16 SVGs are the user-supplied institution icons, renamed without changing their bytes. The original delivery remains outside the repository. No new license or third-party rights claim is introduced.

| Delivery prefix | Repository name | Atlas row |
|---|---|---:|
| `tier_campus_` | `SPC_Institution_Research_1.svg` through `_4.svg` |0|
| `tier_theater_` | `SPC_Institution_Culture_1.svg` through `_4.svg` |1|
| `tier_industrial_` | `SPC_Institution_Industry_1.svg` through `_4.svg` |2|
| `tier_commercial_` | `SPC_Institution_Commerce_1.svg` through `_4.svg` |3|

Columns0–3 correspond to levels1–4. The extra frame template from the delivery is unused. Runtime assets live in [Mod/Textures](../../Mod/Textures/), with16 definitions and32/64px atlas registrations in [Icons.sql](../../Mod/Data/Icons.sql).

B251 generation: render the16 original256px SVGs into a transparent4×4 atlas with the installed browser's SVG renderer, then resize with ImageMagick and encode DDS DXT5 with alpha, no mipmaps. A separate temporary browser profile was used. Review covered the source SVG structure, rendered contact sheet, decoded DDS, dimensions, cell order and exact payload lengths. No screenshot, session data, external reference or source directory path is embedded.

| Runtime asset | Bytes | Reviewed SHA256 |
|---|---:|---|
| `SPC_Institutions_32.dds` |16512|`a3f389f0a82e16599371e42fda5384868d915a3432e92e5f3f14ae678267fa91`|
| `SPC_Institutions_64.dds` |65664|`9fb525ddd843b5d3b1d472195804dcce60e4368f3ba3c5123f06504de988be81`|

The user explicitly approved a **one-batch publication exception for only these two fixed blobs**. They receive a separate binary-only commit; the ordinary staged checker correctly reports binary content as NOT_RUN. All text/SVG files use the normal publication check. No permanent gate exception or hook/configuration change is introduced. See [B251 review](../../Specialization/Status/Validation/Results/Specialization_B251_Institution_UI.md).
