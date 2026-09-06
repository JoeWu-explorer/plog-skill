# Synthetic Source Photo fixture set

This is the public, repository-safe core fixture set for Photo Dialogue v1. The six images are original AI-generated photographs of fictional people. They use no input or reference images and are not intended to depict or resemble any real person.

The set is sufficient for the map's layout, Look, Identity Fidelity, and evaluation decisions because it spans every supported participant count, all three source orientations, sparse and crowded compositions, different lighting conditions, individual and group interaction, and the age groups that trigger different narrative and safety behavior.

It does not prove real-person consent handling, camera-specific artifacts, or identity preservation across the full diversity of real photographs. Real-photo release checks must use explicitly provided or designated photographs and follow the [current generative processing contract](https://github.com/JoeWu-explorer/photo-dialogue/issues/15#issuecomment-5550078321) and [local revision-record contract](https://github.com/JoeWu-explorer/photo-dialogue/issues/16#issuecomment-5550212078). Informed authorization for the current image-service operation permits that processing; it does not permit public upload or publication. Sources, results, and private review details stay outside the repository. Accepted results and minimal records may be retained privately; do not duplicate originals by default. The acceptance decision sets the final release sample size and checks.

## Rights and permitted use

- Generator: OpenAI built-in image generation in Codex, 2026-09-04.
- Inputs: text prompts only; no reference images, real-person names, brands, copyrighted characters, or third-party assets.
- People: fictional; no model releases are required because no real people were photographed or intentionally represented.
- Dedication: the repository maintainer applies CC0-1.0 to any copyright and related rights they control in these six generated files. See [LICENSE.md](LICENSE.md).
- Permitted project uses: public repository fixtures, documentation, layout and Look prototypes, deterministic renderer tests, Identity Fidelity comparisons, and published examples.
- Prohibited interpretation: these images are not evidence that a real person consented, not biometric ground truth, and not suitable for face-identification or demographic-inference evaluation.

## Coverage and provenance

| File | People | Shape | Confirmed Scene Description | Primary stress | SHA-256 |
| --- | ---: | --- | --- | --- | --- |
| [01-solo-tea.png](01-solo-tea.png) | 1 adult | portrait, 1024×1535 | 周末早晨，她独自在窗边泡茶。 | Large negative space; single-subject attribution; cool soft light | `2f2a71be4090455bea72bf02df678baa36468d826c0d05f0c6eee34e6ce115b6` |
| [02-spouses-cooking.png](02-spouses-cooking.png) | 2 adults | landscape, 1536×1024 | 夫妻俩一起包饺子，丈夫正帮妻子搅拌馅料。 | Pair interaction; left-side negative space; mixed warm/cool light | `658fa4b463f40c5fcf48070cc86bf15567e75e25e4df1f86afab30d569145208` |
| [03-three-generation-play.png](03-three-generation-play.png) | older adult + adult + baby | portrait, 1024×1536 | 外婆把小球滚向宝宝，妈妈扶着宝宝坐稳。 | Three-person attribution; baby safeguard; faces at different heights | `ff7e199f6e0332d9c464e8028c8ba4819912cad1afbff017da0843f761c82d0d` |
| [04-four-person-picnic.png](04-four-person-picnic.png) | older adult + adult + teen + child | landscape, 1672×941 | 外公、爸爸和两个孩子一起把野餐毯带回车边。 | Four-person Group Narration boundary; outdoor highlights; uneven pockets of space | `c687dadce1dc2f1223967bda4f0b019c96826a1dc9d15c9ab5588f8035a24f2e` |
| [05-five-coworkers.png](05-five-coworkers.png) | 5 adults | square, 1254×1254 | 五位同事围着纸板模型讨论下一处修改。 | Dense square composition; Collective Lead; many hands and sightlines | `0ba428a52fa15e70f004b20493fa6d2a45911a2ffd0c76d6909858f8dd045660` |
| [06-six-person-lunch.png](06-six-person-lunch.png) | older adults + adults + teen + child | landscape, 1536×1024 | 一家六口在周末午餐时传递同一道菜。 | Maximum v1 count; crowded Group Narration; overlapping limbs and table objects | `ceb7df6538e680509ce079502a5e47a7b206d323f8129ce6a85bb63c5bc6072a` |

The relationship words above are Confirmed Person Context supplied by this fixture, not facts inferred from visible appearance. Tests must use the supplied Scene Description or replace it with explicitly neutral context.

## Acceptance inspection

Each accepted file was visually inspected at original resolution for:

- exact participant count, including reflections, pictures, and background people;
- clear, distinct faces at a size useful for before/after comparison;
- age-credible appearance and compliance with Minor Safeguard;
- coherent hands, limbs, gestures, gaze, and shared objects;
- absence of readable text, logos, watermarks, addresses, plates, school identifiers, documents, private screens, and recognizable bystanders;
- enough compositional variety to exercise individual Voice Elements and Group Narration.

PNG inspection found no EXIF, IPTC, or XMP profile and no orientation tag. Dimensions and checksums above are the fixture invariants.

## Generation prompts

All six files were generated independently with the built-in image generator. Prompts are retained verbatim so future replacements can preserve the intended test coverage; generation is nondeterministic, so checksums—not prompt reuse—identify the accepted fixtures.

### 01-solo-tea.png

```text
Use case: photorealistic-natural
Asset type: authorized synthetic Source Photo test fixture 01
Primary request: Create an original, natural-looking candid photograph of exactly one fictional adult person quietly making tea beside a bright apartment window.
Scene/backdrop: modest contemporary home interior with no identifying address, screens, documents, artwork, logos, or readable text.
Subject: exactly one adult, waist-up, natural expression, hands visibly interacting with a ceramic mug and kettle.
Style/medium: realistic unstaged family photography; ordinary skin texture, believable anatomy, no glamour retouching.
Composition/framing: vertical portrait orientation, person in the lower-left/middle with clean but photographic negative space in the upper-right for later narrative typography; do not add typography.
Lighting/mood: soft overcast window light, calm morning mood.
Constraints: fictional person with no intended resemblance to any real person; exactly one visible human including background, reflections, photos, and screens; preserve natural face, age cues, body, clothing, and gesture; no text, no watermark, no brand marks.
```

### 02-spouses-cooking.png

```text
Use case: photorealistic-natural
Asset type: authorized synthetic Source Photo test fixture 02
Primary request: Create an original candid photograph of exactly two fictional adult spouses cooking together and laughing over a bowl of dumpling filling.
Scene/backdrop: warm home kitchen with generic objects only, no visible brands, documents, screens, family photos, or readable text.
Subject: exactly two adults, both faces clearly visible at useful evaluation size; one holds the bowl while the other reaches for a spoon; clear mutual interaction without exaggerated posing.
Style/medium: realistic documentary family photography with ordinary skin texture and believable hands.
Composition/framing: landscape orientation, medium-wide shot, subjects grouped slightly right of center with usable quieter wall area on the left for later dialogue layout; do not add typography.
Lighting/mood: warm practical light mixed with cool evening window light.
Constraints: fictional people with no intended resemblance to real persons; exactly two visible humans including background/reflections; natural face, age cues, bodies, clothing, and gesture; no text, watermark, logos, or captions.
```

### 03-three-generation-play.png

```text
Use case: photorealistic-natural
Asset type: authorized synthetic Source Photo test fixture 03
Primary request: Create an original candid photograph of a fictional three-person family: one older adult grandmother, one adult daughter, and one baby, sharing a quiet play moment on a living-room rug.
Scene/backdrop: ordinary uncluttered home interior, generic soft toys, no address clues, screens, documents, logos, family photos, or readable text.
Subject: exactly three people; grandmother seated on the floor rolling a small plain ball toward the baby; adult daughter supports the seated baby; all faces visible and distinct, interaction easy to read.
Style/medium: realistic documentary family photography, age-credible appearance, natural skin and hands, no beauty retouching.
Composition/framing: vertical portrait orientation, full/three-quarter bodies, moderate visual density with safe margins around faces for later bubbles; do not add typography.
Lighting/mood: soft daylight, affectionate and restrained.
Constraints: all people fictional with no intended resemblance to real persons; exactly three visible humans including background/reflections/images; no sexualization or adultification; natural face, expression, age cues, body, skin tone, clothing, and gesture; no text, watermark, or logos.
```

### 04-four-person-picnic.png

```text
Use case: photorealistic-natural
Asset type: authorized synthetic Source Photo test fixture 04
Primary request: Create an original candid photograph of exactly four fictional family members—an older adult grandfather, an adult parent, a teenage child, and a younger child—walking back from a park picnic while carrying a folded blanket together.
Scene/backdrop: generic public park path with trees and grass, no landmarks, vehicles, school identifiers, house numbers, license plates, signs, logos, or readable text; no bystanders.
Subject: exactly four people, distinct positions and faces, shared action around the blanket, believable cross-generational interaction.
Style/medium: realistic editorial family photography, ordinary clothing without brands, natural skin texture and anatomy.
Composition/framing: wide landscape orientation with subjects spread across the center and uneven pockets of background for testing crowded dialogue placement; do not add typography.
Lighting/mood: late afternoon side light, lively but not sentimental.
Constraints: fictional people with no intended resemblance to real persons; exactly four visible humans including background/reflections/images; age-credible, no adultification; no text, watermark, logo, privacy-revealing detail, or extra limbs.
```

### 05-five-coworkers.png

```text
Use case: photorealistic-natural
Asset type: authorized synthetic Source Photo test fixture 05
Primary request: Create an original candid photograph of exactly five fictional adult coworkers assembling a handmade cardboard prototype around a shared worktable.
Scene/backdrop: generic small studio workspace with blank paper and plain tools; no company marks, screens, documents, badges, signs, posters, or readable text.
Subject: exactly five adults with visually distinct clothing and positions; one points at the model, two hold pieces, two react; all faces visible enough to test attribution but the scene should feel naturally busy.
Style/medium: realistic documentary workplace photography, believable hands and materials, no polished advertising look.
Composition/framing: square composition, dense group around the center with limited negative space to stress-test Group Narration; do not add typography.
Lighting/mood: neutral overhead light with soft daylight, focused and lightly playful.
Constraints: all people fictional with no intended resemblance to real persons; exactly five visible humans including background/reflections/images; no text, watermark, logos, or identifiable workplace details.
```

### 06-six-person-lunch.png

```text
Use case: photorealistic-natural
Asset type: authorized synthetic Source Photo test fixture 06
Primary request: Create an original candid photograph of exactly six fictional members of one extended family passing dishes around a round dining table during an ordinary weekend lunch.
Scene/backdrop: generic home dining room with plain tableware, no address clues, branded packaging, screens, documents, framed portraits, labels, logos, or readable text.
Subject: exactly six people spanning older adults, adults, one teen, and one child; each face and body belongs to one coherent person; shared action and eye-lines make a clear group interaction; nobody hidden completely.
Style/medium: realistic documentary family photography with natural skin texture, age-credible features, believable hands and table objects.
Composition/framing: landscape orientation, crowded but coherent group, faces distributed across the frame with no large clean text area, suitable for stress-testing Group Narration; do not add typography.
Lighting/mood: mixed warm indoor and soft daylight, everyday warmth without staged perfection.
Constraints: fictional people with no intended resemblance to real persons; exactly six visible humans including background/reflections/images; no sexualization or adultification; no text, watermark, logos, privacy-revealing details, duplicated people, or extra limbs.
```
