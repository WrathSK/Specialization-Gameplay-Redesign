# B260 — Investment controls and city-name badge alignment

## Scope and evidence

User accepts other B259 UI changes and authorizes three presentation fixes. Reviewed original screenshot archived under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B259/` with matching before/after SHA256. No gameplay, saved state, capacity, monetary rules or timers change. Institution softness and held gameplay/audits remain deferred.

## Measurement and implementation

Refresh used a centered child Label plus the native button-owned text offset of 6 units. This displaced the label down within a 24-unit button; SmallCaps18 was also applied to Chinese text. Remove the extra child offset and SmallCaps treatment, retain FontFlair14/shadow and existing button dimensions/actions. STATIC_CONFIRMED structure; actual font rendering still requires user review.

Native Base/Assets/UI/Choosers/EspionageChooser.xml MissionInstance uses Controls_ItemContainer55x55 at7,7, a centered32px district icon and text start70,7. Our46x46 at8,10 was smaller. Match the native backing/icon offsets and text start; row minimum76 follows its DestinationChooser_Button texture height. Variable state text still expands the row with bottom padding; its width shrinks7 units to preserve right clearance. No protocol changes.

Original3840x2160 screenshot Edinburgh crop720x150 at2600,1520: city-name strip visible approximately y69–123 (54px), excluding the defense strip; current hex visible approximately y29–111 (82px). Boundaries are antialiased estimates. At approximately1.875 physical pixels/UI unit, target visible height54/1.875=28.8 units. Existing32px artwork has about29 visible units (transparent edge padding), predicting about54–55 physical pixels. Reuse the approved32px atlas, exact32px Image and lookup, no new binary. Root32x37, badge at0,5, four7x4 segments at x0/8/16/24,y0. Thus the segments sit above the badge with one unit between controls; fills5x2 preserve outline/dim distinction. Root bottom inset changes6→4 to compensate for the badge's approximately2 transparent bottom units. Expected visible badge bottom stays at the prior segment baseline and its top aligns with the city-name strip, not the defense top. This is a measured calibration, not a native alignment PASS.

Rollback reference: B259 runtime source acd0c0d uses49px atlas/control,49x53 root, bottom inset6 and four10x4 segments below. Existing artwork remains intact; reversing presentation geometry restores it without gameplay migration.

## Validation

LOCAL_SIMULATION_PASS:22 targeted methods covering actual Lua state projection/lifetime, no-governor Potential-only investment refresh, atlas/control match, upper segment bounds, native backing/text clearance, Refresh request behavior, four-card/error layout, resize bounds, active-first sorting, pending/held distinction, strict confirmation guards, package closure, SQL and Lua syntax. The initial broader loader also picked historical B252/B258 dimension assertions and imported test classes; those failures concern superseded layouts. The final suite explicitly selects applicable classes/methods; no full-suite PASS claim and no historical assertions weakened. Local fixtures cannot render native fonts/textures.

## Native check

1. Inspect one city badge: four segments above; hex top/bottom align with the city-name strip. No reinvestment needed.
2. Open “发展投资”: check district icon backing spacing and “刷新报价” text centering; click Refresh once. Existing contract information and accepted layout remain unchanged.

## Deployment

B260.287/modinfo287 DEVELOP_ACTIVE; source `f9442e784ddb00e7177df909ed900c810bab84ef`; receipt `B260.287-f9442e7-playtest.json`;279/279 MATCH; digest `ea615e1b262c1ac8921e805525faa64c33ce6c2bb1aa4738c01ab3576e819cff`. Fresh game-exit checks, exact B259 restoration and B260 activation passed. Stable/outgoing recovery verified; no pending marker, game launch, main or configuration change.

22 scoped checks and279-runtime/901-context integrity checks PASS;14 staged files passed publication scan. No new binary publication exception required. Native visual review pending.
