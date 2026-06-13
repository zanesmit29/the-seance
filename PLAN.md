# PLAN.md — The Séance
> BuildSmall Hackathon: Thousand Token Wood | 2-day sprint
> Repo: https://github.com/zanesmit29/the-seance

---

## Project Overview

**What you're building:**
The Séance is a multi-modal Gradio app where users type a concept that doesn't exist — "the last color light ever made", "the sound a shadow makes" — and three distinct AI entities channel it back simultaneously: a cold field-note Scientist (Nemotron-Nano-4B), an ancient folkloric Mythologist (MiniCPM3-4B), and a visual Dreamer (FLUX.1-schnell). Outputs compose a single downloadable artifact card.

**Core value proposition:**
AI weirdness is the product, not the feature. Every summoning is unique and unrepeatable. The artifact card is inherently shareable — the social post writes itself.

**Judging criteria alignment:**
- Delight: The three-voice format is inherently surprising and replayable
- AI is load-bearing: Remove any model and the experience collapses entirely
- Originality: No utility. No dashboard. The séance IS the product.
- Gradio polish: Custom dark UI, sequential reveal, download — targets Off-Brand badge

---

## Current Repo State

| File | Status | Notes |
|------|--------|-------|
| `agents/scientist.py` | ✅ Live + fallback | 4-bit load; tries Nemotron first, falls back to Qwen2.5-3B-Instruct on Windows when Nemotron deps are unavailable |
| `agents/mythologist.py` | ✅ Live | MiniCPM3-4B running in 4-bit locally on GPU |
| `agents/dreamer.py` | ✅ Live via API | Uses Hugging Face `InferenceClient` for FLUX.1-schnell instead of local model download |
| `pipeline/seance_pipeline.py` | ✅ Running | Full chain works end-to-end and returns an image path |
| `prompts/scientist.txt` | ✅ Scaffolded | System prompt v1 — live-tested, still needs refinement |
| `prompts/mythologist.txt` | ✅ Scaffolded | System prompt v1 — live-tested, still needs refinement |
| `prompts/flux_constructor.py` | ✅ Running | Chained prompt builder producing API-ready FLUX prompts |
| `app.py` | ✅ Live | Full-screen dark UI; violent flicker animations; gothic UnifrakturMaguntia title font; neon green Scientist; cloudy desaturated Dreamer image; sequential reveal |
| `prompts/flux_constructor.py` | ✅ Enhanced | Dynamic STYLE_SUFFIXES (5 styles); tone extraction from agent text; concept-hashed style selection; richer prompt composition |
| `tests/test_pipeline.py` | ✅ Passing | 6 pytest tests passing in mock mode |
| `docs/architecture.md` | ✅ Scaffolded | Pipeline diagram + ZeroGPU notes |
| `Dockerfile` | ✅ Scaffolded | |
| `requirements.txt` | ✅ Updated in practice | Runtime now depends on `bitsandbytes`, `optimum`, model-specific extras, and HF API access |
| `.env.example` | ✅ Scaffolded | Matches current API-first Dreamer behaviour |
| Prompt testing & refinement | ⚠️ In progress | Voices are distinct, but repetition/style tuning still needed |
| FLUX prompt chaining validation | ⚠️ In progress | Prompts generate and images return, but visual quality still needs review |
| Real model inference (live mode) | ✅ Working with caveats | Scientist uses fallback on this Windows setup; Mythologist local; Dreamer hosted |
| HF Spaces deployment | ❌ Not started | Issue #5 |
| Demo video | ❌ Not started | Issue #5 |
| Field Notes blog post | ❌ Not started | Issue #5 |

---

## Recent Progress

- `.env` loading was fixed across the project so `HF_TOKEN` and `MOCK_MODE` now apply consistently.
- The Scientist was moved to 4-bit loading and made resilient: it attempts Nemotron first, then falls back to `Qwen/Qwen2.5-3B-Instruct` when `mamba_ssm` / `causal_conv1d` are unavailable on Windows.
- The Mythologist was switched off the unstable GPTQ path and now runs as `openbmb/MiniCPM3-4B` in 4-bit locally on GPU.
- The Dreamer no longer downloads FLUX locally; it now uses Hugging Face hosted inference through `InferenceClient` and returns `output/artifact_image.png`.
- The full pipeline was validated end-to-end: Scientist text, Mythologist text, FLUX prompt, and image path are all returned.
- Local Hugging Face cache cleanup was needed after a large FLUX download attempt; local FLUX pipeline use is no longer the preferred path.
- **UI overhaul:** Full-screen layout (100vw); pure-black background with violent multi-drop flicker animation on the scene and title; gothic `UnifrakturMaguntia` blackletter font loaded via Google Fonts for the title; neon green (`#00ff41`) terminal glow for the Scientist; purple breathing glow for the Mythologist (unchanged); desaturated + dimmed Dreamer image with animated fog-drift overlay; larger body text on all three entity panels; all Gradio default borders and focus rings suppressed via CSS variable overrides.
- **FLUX prompt constructor enhanced:** Static `STYLE_SUFFIX` replaced with a pool of 5 distinct style moods; new `extract_tone_words()` function detects emotional vocabulary from both agent outputs and injects mood hints into the prompt; style is selected deterministically via `hash(concept)` for reproducibility.

---

## Day-by-Day Sprint Plan

### Day 1 — Core pipeline working locally in mock mode

**Morning (Issues #1, #2):**
- [x] Clone repo: `git clone https://github.com/zanesmit29/the-seance`
- [x] Install: `pip install -r requirements.txt`
- [x] Run in mock mode: `MOCK_MODE=true python app.py` — confirm UI opens
- [x] Run tests: `pytest tests/` — all 6 current tests pass
- [ ] Test system prompts on 5 concepts (see Issue #2)
- [ ] Iterate prompts until Scientist and Mythologist voices are clearly distinct
- [ ] Commit final prompts to `prompts/scientist.txt` and `prompts/mythologist.txt`

**Afternoon (Issues #2, #3):**
- [ ] Test FLUX prompt constructor on 5 concepts — print outputs, review quality
- [x] Confirm chained prompt references both text outputs visibly
- [x] Add your HF_TOKEN to `.env` (copy from `.env.example`)
- [x] Set `MOCK_MODE=false`, test live MiniCPM3-4B inference first (smallest model)
- [x] Test live Nemotron-Nano-4B inference
- [ ] Note actual latency for each model

Notes:
- Nemotron did not stay fully usable on this Windows stack because its custom code requires `mamba_ssm` and `causal_conv1d`.
- The current Scientist mitigation is automatic fallback to `Qwen/Qwen2.5-3B-Instruct`.
- Dreamer was moved to Hugging Face hosted inference because local FLUX downloads and memory footprint were not practical on this laptop.

**Evening (Issue #4 UI):**
- [ ] Confirm custom CSS renders correctly — no Gradio chrome visible
- [ ] Test sequential panel reveal: Scientist → Mythologist → image
- [ ] Test download button — confirm artifact card PNG saves correctly
- [ ] Screenshot the UI — this is your social post image

---

### Day 2 — HF Spaces deployment + submission deliverables

**Morning (Issue #5):**
- [ ] Create HF Space: https://huggingface.co/new-space
  - SDK: Gradio
  - Hardware: ZeroGPU (requires Pro account or apply for grant)
  - Name: `the-seance`
- [ ] Add HF Space YAML frontmatter to README.md:
  ```yaml
  ---
  title: The Séance
  emoji: ✦
  colorFrom: indigo
  colorTo: black
  sdk: gradio
  sdk_version: 4.36.0
  app_file: app.py
  pinned: true
  ---
  ```
- [ ] Add `@spaces.GPU` decorator to `summon()` function in `app.py` for ZeroGPU
- [ ] Push repo to HF Space: `git remote add space https://huggingface.co/spaces/zanesmit29/the-seance`
- [ ] Confirm Space builds without errors

**Afternoon:**
- [ ] Test live inference on ZeroGPU — note cold start time
- [ ] If VRAM issues: switch text models to HF Inference API (set `USE_INFERENCE_API=true`)
- [ ] Record demo video (60-90 seconds):
  - Scene 1: type "the sound a shadow makes" → watch three panels appear
  - Scene 2: download artifact card PNG
  - Scene 3: type second concept — show replayability and uniqueness
- [ ] Post artifact card image on Twitter/X/LinkedIn with link to Space

**Evening:**
- [ ] Write Field Notes blog post (400-600 words) — publish on HF or personal site
- [ ] Submit to Devpost: video + repo link + Space link + blog link
- [ ] Double-check Off-Brand badge eligibility — confirm no default Gradio chrome in video

---

## Definition of Done — MVP

- [x] `MOCK_MODE=true python app.py` runs without errors
- [ ] Scientist and Mythologist outputs are clearly distinct voices on any concept (partially validated; more prompt refinement needed)
- [x] FLUX prompt visibly references both text outputs
- [ ] Image feels surreal and concept-specific (not generic) (pipeline works; image quality still needs review)
- [ ] Three panels reveal sequentially (not all at once)
- [ ] Download button produces a composited PNG
- [x] `pytest tests/` — all 6 tests pass
- [ ] HF Space publicly accessible at https://huggingface.co/spaces/zanesmit29/the-seance
- [ ] Demo video recorded (60-90s) and uploaded
- [ ] Social media post drafted with artifact card image
- [ ] Devpost submission complete

---

## API Keys & Accounts Needed

| Requirement | Where | Notes |
|------------|-------|-------|
| `HF_TOKEN` | https://huggingface.co/settings/tokens | Needed for gated models |
| HF Pro account | https://huggingface.co/subscribe/pro | Required for ZeroGPU access |
| Devpost account | https://devpost.com | For hackathon submission |

---

## Known Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| FLUX.1-schnell latency or rate limits via hosted inference | Medium | High | Keep 4 inference steps; verify HF access/tier; consider fallback provider if needed |
| MiniCPM3-4B voice indistinct from Scientist | Medium | High | Tight system prompts; test on 5 concepts before any code |
| All 3 models exceed local VRAM simultaneously | Low | Medium | Dreamer now uses hosted inference; text agents still load sequentially |
| ZeroGPU cold start adds 30s+ | High | Medium | Note in demo video; show mock mode as fallback |
| Nemotron-Nano-4B custom dependencies break on Windows | High | Medium | Keep Scientist fallback model in place or move Scientist to hosted inference |

---

## Bonus Badges Checklist

- [x] **Off-Brand** — Full-screen custom dark UI. Gothic title font. No Gradio chrome visible. Sequential reveal. Violent flicker. Neon Scientist. Cloudy Dreamer. ✅ Confident target met.
- [ ] **Field Notes** — 400-600 word blog post. Draft on Day 2 evening.
- [ ] **Sharing is Caring** — Open agent trace if time allows after submission.

---

## Resource Links

- [FLUX.1-schnell on HF](https://huggingface.co/black-forest-labs/FLUX.1-schnell)
- [MiniCPM3-4B on HF](https://huggingface.co/openbmb/MiniCPM3-4B)
- [Nemotron-Nano-4B on HF](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16)
- [ZeroGPU Docs](https://huggingface.co/docs/hub/spaces-zerogpu)
- [Gradio Custom CSS Guide](https://gradio.app/guides/custom-CSS-and-JS)
- [BuildSmall Hackathon Field Guide](https://huggingface.co/spaces/build-small-hackathon/field-guide)
- [DiffusionDB dataset](https://huggingface.co/datasets/poloclub/diffusiondb) — image+prompt pairs for FLUX eval

---

*Generated by BriefForge — Base44 Superagent · Clarify → Recommend → Execute → Deliver*
