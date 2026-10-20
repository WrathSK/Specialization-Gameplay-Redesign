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

## B254 embedded serif levels

`SPC_Level_{Research,Culture,Industry,Commerce}_{1..4}.svg` are the approved A-palette refinements: explicit serif paths, uniform7% numeral reduction, shortened serif overhangs and optical spacing; no horizontal compression or font dependency. They share the B252 gradient/bevel palette. Institution rows select their own tier; banner emblems select ACTIVE and draw the four segments with native Box controls. Original B251 and B252 sources/blobs remain unchanged.

Render16 SVGs at256px per cell with the isolated browser SVG renderer, downsample a4×4 atlas once to32/64px cells, and encode lossless BGRA8 DDS without mipmaps. Decode must reproduce the raw raster exactly. See [B254 scope and validation](../../Specialization/Status/Validation/Results/Specialization_B254_Level_Icons.md).

| Runtime asset | Bytes | Reviewed SHA256 |
|---|---:|---|
| `SPC_Level_Icons_32.dds` |65664|`b08fe38e9a66bb0b157d9baf0b6ab818cb6431e4fdaa39cb6a801273559fde89`|
| `SPC_Level_Icons_64.dds` |262272|`308bdf3bad9e027da81b9284c7b3a11c37fbb6312819995c9be763f1437e778e`|

The user explicitly approved a one-time publication exception for exactly these two blobs. They are committed separately; no permanent binary allowance or hook-policy change. Source/SVGs and all other changes use the normal publication gate.

## B258 exact map size

The existing approved B254 SVGs produce an additional58px-cell atlas for the58-unit map Image control. Institution32px and existing64px files remain unchanged. Lossless BGRA8,232x232, no mipmaps; decoded raw pixels match exactly. `SPC_Level_Icons_58.dds`:215424 bytes; SHA256 `9d3277bca2704363223d7346592cbbcadd793883a851a2f190a1c0434258ad54`. The user explicitly approves a one-time publication exception for this exact blob only. See [B258](../../Specialization/Status/Validation/Results/Specialization_B258_Badge_Investment_UI.md).
