# HAPPY HIPPO — Original Kids Animation Studio Brief

Version: 1.0  
Audience: preschool children ages 1–5  
Budget: free tools only; no paid APIs, services, or hosting.  
Mission: one gentle early-learning lesson per episode. All characters, scripts, songs, artwork, and melodies must be original.

## Channel identity (locked)
- Name: HAPPY HIPPO
- Tone: warm, joyful, safe, reassuring; never scary, violent, sarcastic, or promotional.
- Learning areas: kindness, sharing, colors, counting, manners, bedtime, healthy food, feelings, and everyday safety.
- Signature: brief original intro sting, one recurring “Spot the …” mini-game, and the sign-off “Big smiles, little steps — see you next time!”
- No external links or promotional messages in child-facing video content.

## Fixed character canon
The canonical character bible is `characters/character_bible.md`. Character silhouettes, palettes, clothes, accessories, and voice IDs are immutable. Use existing approved character assets; never silently substitute or redesign them. If a required layered asset does not exist, fail the asset readiness check rather than pretending it exists.

## Script contract
- Read `episode_log.json` before selecting a topic, plot, chorus, or song.
- Do not reuse an episode topic + plot combination or song lyrics. Log every approved and published episode.
- Hook/action/question in the first 3 seconds.
- One explicit learning goal, reinforced three different ways.
- Preschool language: short sentences, concrete vocabulary, usually 3–7 words.
- Include a call-and-response with an actual pause.
- Include an original 8–16 line chorus/song, unless the format is explicitly marked as a non-musical pilot.
- Emotional arc: small problem → try → setback → try again → success → celebration/reassurance.
- End with a recap and the fixed sign-off.
- Vary structure between adventure, mystery, helping a friend, mistake-and-repair, rainy-day game, and surprise visitor.
- JSON must validate against the episode schema used by the pipeline. Never fabricate QA scores.

## Visual contract
- Vertical Shorts: 1080×1920, 30 fps, 45–60 seconds. Long episodes: 1920×1080, 30 fps, 2–3 minutes.
- Every shot must contain visible scene or character motion beyond a slow zoom: body/limb movement, blink, expression/mouth change, object motion, or parallax.
- Use fixed reusable transparent character layers and layered backgrounds. Blink roughly every 3–4 seconds when appropriate.
- Lip-sync mouth shapes to actual speech timing. Camera choices should vary (wide, close-up, tracking, over-shoulder, push-in) while remaining gentle.
- Never use rapid flashing, harsh strobing, frightening imagery, or unsafe color/lighting effects.
- If layered assets or true animation/lip-sync are not implemented, mark QA as FAIL; do not call a static illustration a completed animation.

## Audio contract
- Fixed voice ID per character and fixed narrator ID; record IDs/settings in `characters/character_bible.md`.
- Voice should be warm, clear, slow enough for preschool comprehension, and consistent across episodes.
- Use only original generated music or properly license-cleared music/SFX. Keep a licence/source note beside each external track.
- Music should be bright and gentle, normally 90–110 BPM, with voice clearly foregrounded.
- Mix voice/music, normalize with FFmpeg loudnorm, check clipping, and detect silence longer than 1.5 seconds.
- Do not claim a voice change worked without comparing the actual generated audio.

## QA release gate
Score these dimensions 1–10: character consistency, motion, originality/learning value, voice clarity/emotion, child safety, and parent suitability. Every dimension must score at least 8, and the parent suitability answer must be YES. Automated technical checks are necessary but not sufficient. Any missing visual/audio review is NOT APPROVED. Maximum two regeneration attempts; then skip the episode and alert the owner.
- Technical QA must validate dimensions, fps, duration, audio stream, clipping/silence, and per-shot motion.
- Visual review samples at least six frames and checks against the bible.
- Audio review listens to the rendered narration/music; it must not infer voice identity from settings alone.
- A successful render/upload is not a quality approval.

## Free-tool policy
Use free/open-source tools where possible: Python, Pillow, FFmpeg, espeak-ng for fallback only, Rhubarb Lip Sync when installed, and GitHub Actions. Free-tier hosted AI tools are optional and must not become a hidden paid dependency. No paid API keys are required for the baseline. Any optional tool must fail gracefully and never silently downgrade quality.

## Daily pipeline
1. Daily schedule in Asia/Kolkata.
2. Read this brief and `episode_log.json`.
3. Select a genuinely unused topic/plot/structure/song.
4. Generate episode JSON and independently evaluate it.
5. Retry at most twice if any score <8.
6. Commit dated episode source and audit metadata.
7. Dispatch GitHub render worker.
8. Render assets, narration, lip-sync, animation, subtitles, audio mix, and technical QA.
9. Produce a preview artifact and review report.
10. Require explicit approval before public publishing until the owner authorizes a proven auto-pass policy.
11. Set `madeForKids=true`; apply any required synthetic/altered-content disclosures.
12. Update the episode log only after the agreed success point. On failure, preserve evidence and alert the owner.

## Production safety
Public publishing remains blocked unless a review report explicitly passes every release gate. Never remove or bypass this gate to make a workflow green. Keep secrets out of source files, artifacts, and logs. Never upload test videos publicly.
