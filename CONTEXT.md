# Photo Dialogue

Photo Dialogue is a Codex-first skill for turning a real photograph containing people into a static, share-ready narrative image while preserving the people as they appeared in the source.

## Language

**Source Photo**:
A real user-provided photograph containing one or more people and serving as the visual truth for the finished image.
_Avoid_: Input image, raw material

**Scene Description**:
The user's short account of what is happening and how the people are related; it is authoritative for context that cannot be safely observed from the photograph.
_Avoid_: Prompt, caption

**Narrative Treatment**:
The combined use of dialogue, inner voice, narration, typography, composition, and restrained visual styling to make a Source Photo express a story.
_Avoid_: Packaging, beautification

**Voice Element**:
A readable story unit attributed to a person or narrator, such as spoken dialogue, inner voice, or narration.
_Avoid_: Copy block, text sticker

**Confirmed Quote**:
Words that the user explicitly identifies as having been spoken in the photographed scene and that should remain verbatim unless the user asks for an edit.
_Avoid_: Rewritten quote, inferred speech

**Creative Voice**:
An imagined Voice Element generated for Narrative Treatment that must not be represented as a factual record of what someone said or thought.
_Avoid_: Real quote, testimony

**Scene Evidence**:
A concrete action, object, expression, spatial relationship, or user-confirmed event that makes a Voice Element specific to its Source Photo.
_Avoid_: Generic sentiment, interchangeable caption

**Primary Voice Mode**:
The single dominant form used by a Finished Image: spoken dialogue, inner voice, narrator voice, or deliberate silence.
_Avoid_: Mixed voice stack, text collage

**Voice Budget**:
The readability limit for a Finished Image: normally no more than three Voice Elements or 32 Chinese characters in total, with each Voice Element kept between 5 and 16 characters.
_Avoid_: Caption dump, one bubble per person

**Look**:
A coherent visual treatment selected from the Source Photo's light, color, mood, and narrative context; it must not be treated as an indiscriminate whole-image filter.
_Avoid_: Filter, preset

**Identity Fidelity**:
The requirement that recognizable faces, expressions, age cues, bodies, clothing, and interpersonal gestures remain faithful to the Source Photo unless the user explicitly requests a stronger transformation.
_Avoid_: Likeness enhancement, face optimization

**Warm Wit**:
The default narrative register: affectionate, observant, and lightly surprising without ridicule, adultification, or jokes about a person's body or ability.
_Avoid_: Roast, meme voice

**Childlike Contrast**:
A playful register for babies and children that may use a lightly grown-up inner voice while keeping the subject age-credible and free of adult sexual, cynical, or demeaning implications.
_Avoid_: Adultified child voice, baby talk

**Restrained Romance**:
A register for couples and spouses that expresses familiarity or affection without inventing conflict, jealousy, pregnancy, control, or other private relationship facts.
_Avoid_: Manufactured drama, sentimental cliché

**Quiet Documentary**:
A restrained observational register for emotionally weighty family moments where narration should support the photograph rather than turn it into a joke.
_Avoid_: Inspirational quote, melodrama

**Primary Register**:
The one narrative register governing a Finished Image, optionally adjusted by a single intensity modifier such as lightly humorous or especially restrained.
_Avoid_: Averaged tone mix, style stack

**Neutral Attribution**:
A Voice Element that does not assert an unconfirmed relationship, identity, or private fact when the Scene Description leaves it unspecified.
_Avoid_: Relationship guess, inferred identity

**Strong Look**:
An explicitly requested Look that may substantially reinterpret the photograph while remaining subject to Identity Fidelity.
_Avoid_: Default style, automatic restyle

**Directed Revision**:
A natural-language request to change one aspect of a Finished Image while preserving unrelated narrative and visual decisions.
_Avoid_: Restart, regenerate everything

**Group Narration**:
A shared narrator or collective Voice Element used when individual attribution would overcrowd a photograph containing many people.
_Avoid_: One bubble per person

**Finished Image**:
One static, share-ready image produced from a Source Photo and Scene Description without requiring intermediate design choices; it preserves the source orientation unless the user requests a platform-specific format.
_Avoid_: Draft, talking-head video
