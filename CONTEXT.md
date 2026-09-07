# Photo Dialogue

Photo Dialogue is an agent-neutral Plog skill for turning real photographs of people, landscapes, streets, food, objects and pets into static, share-ready photo journals while preserving the source scene. Agent capabilities and configured image services determine execution, not an agent brand. Multiple photos are processed independently as a coordinated series, with one source and revision record per photo.

## Language

**Plog**:
A photo journal grounded in real photographs, combining a scene-specific short caption or diary voice with typography and photographic treatment. A series coordinates independent Finished Images without merging source identities or revision histories.

**Scene Fidelity**:
The preservation of terrain, coastlines, architecture, streets, objects, pets and visible people from the Source Photo. Color and typography may change; material structural drift or invented landmarks prevent acceptance. Identity Fidelity adds person-specific checks when people are present.

**Agent Capability Contract**:
The required ability to observe images, edit an actual photo, compare the result, execute local file operations and deliver the saved PNG in the current session. Native tools, configured plugins or compatible APIs may satisfy it; agent names and installation success do not prove runtime readiness.


**Source Photo**:
A real user-provided photograph serving as the visual truth for a finished image; people are optional.
_Avoid_: Input image, raw material

**Scene Description**:
The user's short account of the place, occasion, experience and any relevant relationships; it is authoritative for context that cannot be safely observed from the photograph.
_Avoid_: Prompt, caption

**Narrative Treatment**:
The combined use of dialogue, inner voice, narration, typography, composition, and restrained visual styling to make a Source Photo express a story.
_Avoid_: Packaging, beautification

**Voice Element**:
A readable story unit attributed to a person or narrator, such as spoken dialogue, inner voice, or narration.
_Avoid_: Copy block, text sticker

**Confirmed Quote**:
Words that the user explicitly identifies as having been spoken in the photographed scene and that should remain verbatim unless the user asks for an edit. Confirmation does not override privacy, human-dignity, or reputational-safety boundaries; a disallowed quote is omitted or replaced with non-factual narration, never silently rewritten and still presented as confirmed.
_Avoid_: Rewritten quote, inferred speech

**Creative Voice**:
An imagined Voice Element generated for Narrative Treatment that must not be represented as a factual record of what someone said or thought.
_Avoid_: Real quote, testimony

**Scene Evidence**:
A concrete landscape feature, light pattern, action, object, expression, spatial relationship, or user-confirmed event that makes a Voice Element specific to its Source Photo.
_Avoid_: Generic sentiment, interchangeable caption

**Primary Voice Mode**:
The single dominant form used by a Finished Image: spoken dialogue, inner voice, narrator voice, or deliberate silence.
_Avoid_: Mixed voice stack, text collage

**Voice Budget**:
The readability limit for a Finished Image: normally no more than three Voice Elements or 32 Chinese characters in total, with each Voice Element kept between 5 and 16 characters.
_Avoid_: Caption dump, one bubble per person

**Look**:
A coherent visual treatment combining composition, typography, photographic color and light, contrast, grain, and restrained material texture, determined anew from each Source Photo, its narrative context, and the user's stated style preferences. No fixed filter, atmosphere, font, text color, or composition is implied by a previously accepted example. It includes the photograph's atmosphere as well as the Voice Elements' appearance; effects that do not serve the photograph may be omitted.
_Avoid_: Filter, preset

**Atmosphere Treatment**:
The coordinated handling of light softness, warm and cool tones, shadow color, highlight roll-off, grain, and restrained bloom within a Look. It supports the photographed moment while preserving recognizable people and natural skin tones.
_Avoid_: Uniform yellow wash, decorative overlay pack

**Identity Fidelity**:
The requirement that recognizable faces, expressions, age cues, bodies, skin tone, clothing, and interpersonal gestures remain faithful to the Source Photo. Generative treatment may change pixels, but must preserve these identity invariants; an output with material drift or unverifiable fidelity cannot be accepted as a Finished Image.
_Avoid_: Likeness enhancement, face optimization

**Submission Authority**:
The working assumption that a user may use an ordinary private Source Photo they submit. It removes the need for a mandatory consent form but is not proof of every depicted person's consent, and it does not permit identification, surveillance, harassment, humiliation, or retaliation.
_Avoid_: Verified consent, ownership proof

**Sensitive Context**:
A private or protected fact explicitly supplied by the user, such as health, disability, ethnicity, religion, or gender identity. It may be used only when the user directly requests it, it is necessary to the story, and the treatment remains neutral; it must never be inferred from appearance or turned into a joke or further inference.
_Avoid_: Sensitive inference, visual diagnosis

**Minor Safeguard**:
The additional protection applied whenever a Source Photo contains a baby, child, teen, or a person whose adult age is uncertain: no sexualization, humiliation, adultification, dangerous-behavior glorification, body or ability jokes, age or body alteration, reduced clothing coverage, or unnecessary exposure of identifying location or school details.
_Avoid_: Child mode, cute exception

**Generative Art Direction**:
The default creation approach in which the photograph and its intended Chinese Voice Elements are composed together into an integrated visual work, guided by a Look determined for that Source Photo. The generated result must be checked against the source people, scene and intended text before acceptance.
_Avoid_: Fixed style transfer, unverified one-shot output

**Per-run Processing Authorization**:
The user's informed authorization to send the identified photos to the stated vision and image-edit services for the current treatment. Clear authorization already given for that operation is carried forward without a repeated confirmation or password-like phrase; it does not authorize unrelated photographs, services or public sharing.
_Avoid_: Silent upload, permanent blanket consent, repeated consent ritual

**Privacy Exposure**:
Clearly visible information in a Source Photo that creates a material sharing risk, such as an address, license plate, identity document, school identifier, private screen content, or recognizable uninvolved bystander. It triggers one minimal clarification unless the Narrative Treatment can naturally exclude it; location-revealing details involving a minor may not be silently retained.
_Avoid_: Background detail, automatic redaction

**Source Preservation**:
The rule that the original Source Photo is never overwritten. Temporary derivatives are removed after success or failure, and every Finished Image is exported without EXIF, IPTC, XMP, location, or device metadata.
_Avoid_: In-place edit, metadata copy

**Core Rendering Capability**:
The ability to create the requested integrated image, inspect its scene, visible people and Chinese text against the source, and deliver a valid private output. An unavailable creation service or an unmet verification requirement prevents completion; a simpler local result is not an automatic equivalent.
_Avoid_: Full feature set, degraded image quality

**Enhanced Placement**:
Optional assistance for locating subject-safe space for Voice Elements without covering faces or key interactions. It supports composition but does not replace inspection of the finished result.
_Avoid_: Required face recognition, guessed safe area

**Edge Narration**:
A Voice Element placed in added canvas below the Source Photo. It is an available composition choice when appropriate to the photograph and narrative, not a mandatory group layout or an automatic response to failed generation.
_Avoid_: Overlay fallback, guessed bubble placement

**Layout Recipe**:
A composition approach that relates the Source Photo, Voice Elements, attribution, and reading order within one Finished Image while preserving the source orientation. Recipes guide per-photo art direction rather than prescribe fixed positions or an exhaustive set of templates.
_Avoid_: Template, preset, people-count layout

**Safety-gated Hybrid**:
The previously prototyped family of Single-voice Overlay, Two-voice Overlay, and Edge Narration, retained as optional composition approaches. All protect faces, gestures, shared objects, and Interaction Paths; they do not exhaust the generative layout choices or define a mandatory fallback.
_Avoid_: People-count template set, always-overlay layout

**Single-voice Overlay**:
One spoken, inner, or narrator Voice Element placed in a verified safe region inside the Source Photo; person-attributed voice uses a directional tail and narrator voice does not.
_Avoid_: Floating caption, multi-bubble scatter

**Two-voice Overlay**:
One ordered two-person exchange placed in verified safe space inside the Source Photo, with each Voice Element pointing to its confirmed or neutrally located speaker.
_Avoid_: Ambiguous attribution, unordered bubbles

**Revision Record**:
A minimal, user-inspectable local record saved with the results to support continuing a Directed Revision: the source reference, exact image text, visual intent, and relationships between accepted versions. It does not imply a retained copy of the Source Photo, authorize new processing, or guarantee pixel-identical reproduction. It excludes face embeddings, identity-recognition results, source metadata, inferred Sensitive Context, and unrelated private information.
_Avoid_: Biometric profile, hidden dossier

**Revision Recovery**:
Restoring the selected Accepted Version, source reference, exact text, and visual intent from a Revision Record so a new request can continue the work. Missing or changed source material requires the user to provide or identify it; a finished image is not silently substituted for the Source Photo.
_Avoid_: Automatic identity reconstruction, permanent source archive

**Safe Continuation**:
A conservative Narrative Treatment that preserves the user's safe intent after declining only an unsafe or unsupported part of a request. The entire request stops only when its source scenario or central purpose is itself unsafe or out of scope.
_Avoid_: Silent sanitization, blanket refusal

**Memorial Treatment**:
A Narrative Treatment centered on death, grief, afterlife, revival, or unconfirmed final words or inner voice attributed to a deceased person. An ordinary evidence-grounded scene does not become Memorial Treatment merely because the user says that a depicted person later died.
_Avoid_: Any photo containing a deceased person, ordinary remembrance

**Reputational Fabrication**:
Creative Voice that makes a real person appear to state or reveal a consequential fact, endorsement, political position, crime, insult, sexual history, medical condition, relationship conflict, or other potentially harmful claim. It is never permitted, even when formatted as playful dialogue.
_Avoid_: Harmless Creative Voice, Confirmed Quote

**Human Dignity**:
The protection owed to every depicted person, regardless of age: no sexualization, humiliation, or jokes or narratives built around body, ability, trauma, violence, or criminality.
_Avoid_: Adult exception, consent to ridicule

**Sensitive Scene**:
A non-graphic care, recovery, hospital-visit, injury, or emotionally weighty family scene whose private context comes from the user and is treated with Quiet Documentary. Nudity or sexual content, graphic injury or death, abuse, exploitation, and victim-shaming are not Sensitive Scenes supported by v1.
_Avoid_: Visual diagnosis, trauma spectacle

**Warm Wit**:
An optional narrative register for light interactions: affectionate, observant, and lightly surprising without ridicule, adultification, or jokes about a person's body or ability.
_Avoid_: Roast, meme voice

**Childlike Contrast**:
A playful register for babies and children that may use a lightly grown-up inner voice while keeping the subject age-credible and free of adult sexual, cynical, or demeaning implications.
_Avoid_: Adultified child voice, baby talk

**Restrained Romance**:
A register for couples and spouses that expresses familiarity or affection without inventing conflict, jealousy, pregnancy, control, or other private relationship facts.
_Avoid_: Manufactured drama, sentimental cliché

**Quiet Documentary**:
A restrained observational register for quiet landscapes, everyday scenes and emotionally weighty moments where narration supports the photograph.
_Avoid_: Inspirational quote, melodrama

**Primary Register**:
The one narrative register governing a Finished Image, optionally adjusted by a single intensity modifier such as lightly humorous or especially restrained.
_Avoid_: Averaged tone mix, style stack

**Neutral Attribution**:
A Voice Element that does not assert an unconfirmed relationship, identity, or private fact when the Scene Description leaves it unspecified.
_Avoid_: Relationship guess, inferred identity

**Strong Look**:
An explicitly requested increase in visual stylization beyond the source-responsive treatment selected for the current image. It remains subject to Scene Fidelity and, when people are present, Identity Fidelity and is distinct from the generative technique used by the default workflow.
_Avoid_: Synonym for all generation, automatic maximum stylization

**Directed Revision**:
A natural-language request to change specified aspects of a Finished Image based on a selected Accepted Version, while retaining unrelated narrative and visual decisions. The revised result is checked again; a failed revision does not replace an accepted result.
_Avoid_: Restart, regenerate everything

**Accepted Version**:
A generated or revised image that has passed the required checks and is retained as an available result. A newer accepted image does not overwrite an earlier one; a failed attempt is not an Accepted Version. Acceptance here does not imply the user's final aesthetic approval.
_Avoid_: Latest attempt, unchecked candidate

**Delivery Verification**:
The checks applied to each generated or revised candidate before it becomes an Accepted Version, including fidelity to the Source Photo, exact intended text, attribution, visual coherence, and valid private delivery. An unresolved or unverifiable candidate cannot pass.
_Avoid_: Generation succeeded, user aesthetic approval

**Release Evaluation**:
The assessment of a candidate product version against a fixed set of photographs, revisions, and failure scenarios, including human review of complete images for visual quality. It retains failed attempts in the evidence and is distinct from each image's Delivery Verification.
_Avoid_: Best-example showcase, automatic quality score, per-user approval step

**Revision Base**:
The Accepted Version selected as the starting point for a Directed Revision, together with the Source Photo needed to verify fidelity. It defaults to the latest accepted result unless the user chooses another retained version.
_Avoid_: Failed draft, source substitute

**Group Narration**:
A shared narrator or collective Voice Element used when individual attribution would overcrowd a photograph containing many people.
_Avoid_: One bubble per person

**Finished Image**:
One static, share-ready image produced from a Source Photo and Scene Description without requiring intermediate design choices; it preserves the source orientation unless the user requests a platform-specific format.
_Avoid_: Draft, talking-head video
