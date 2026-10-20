# Institution icon sources

The original B251 set contains16 SVGs that are the user-supplied institution icons, renamed without changing their bytes. The original delivery remains outside the repository. No new license or third-party rights claim is introduced.

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

## B252 backdrops

B252 renders stage numerals as native UI text, so the new artwork contains no numeral or central district symbol. Four code-native SVGs were redrawn from the user-provided district-icon visual reference after a bounded native-asset lookup found no verified separate shaded district backing. The face gradient, colored bevel and native-like palette are retained; this is a redraw, not an extracted game asset. No screenshot pixels or external local paths are embedded. Old B251 files remain unchanged.

| Source | Atlas column | Palette |
|---|---:|---|
| `SPC_Institution_Backdrop_Research.svg` |0|Campus blue|
| `SPC_Institution_Backdrop_Culture.svg` |1|Theater purple|
| `SPC_Institution_Backdrop_Industry.svg` |2|Industrial bronze|
| `SPC_Institution_Backdrop_Commerce.svg` |3|Commercial gold|

Generation: render the256px SVGs as one transparent4×1 atlas with the installed browser's SVG renderer in an isolated temporary profile, downsample to32/64px cells, then store lossless BGRA8 DDS without mipmaps. This preserves gradients without block-compression artifacts; Roman labels use the native font independently. Decoding each DDS reproduces the reviewed raw raster bytes exactly. Review includes contact-sheet appearance, alpha, gradients, ordering, headers and exact file sizes. Native game loading/rendering still awaits the B252 visual check.

| Runtime asset | Bytes | Reviewed SHA256 |
|---|---:|---|
| `SPC_Institution_Backdrops_32.dds` |16512|`d6ced03eb0a7a91717eb008269c859a5da4efe99471b80902e223aa2c0458eec`|
| `SPC_Institution_Backdrops_64.dds` |65664|`912e8f148ea8698941d5e0be5482b70fdef9966340364b806b9b05c3ff03b0ce`|

The user explicitly approved only these two fixed blobs for a separate, one-time binary publication exception. Every other B252 file still uses the ordinary staged gate. No permanent policy/hook/configuration change. See [B252 scope and checks](../../Specialization/Status/Validation/Results/Specialization_B252_Commerce_UI.md).
