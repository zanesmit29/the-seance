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
| `agents/scientist.py` | ✅ Scaffolded | Nemotron-Nano-4B + mock mode |
| `agents/mythologist.py` | ✅ Scaffolded | MiniCPM3-4B + mock mode |
| `agents/dreamer.py` | ✅ Scaffolded | FLUX.1-schnell + placeholder mock |
| `pipeline/seance_pipeline.py` | ✅ Scaffolded | Full chain + partial failure handling |
| `prompts/scientist.txt` | ✅ Scaffolded | System prompt v1 — needs testing |
| `prompts/mythologist.txt` | ✅ Scaffolded | System prompt v1 — needs testing |
| `prompts/flux_constructor.py` | ✅ Scaffolded | Chained prompt builder |
| `app.py` | ✅ Scaffolded | Custom dark Gradio UI, sequential reveal |
| `tests/test_pipeline.py` | ✅ Scaffolded | 5 pytest tests |
| `docs/architecture.md` | ✅ Scaffolded | Pipeline diagram + ZeroGPU notes |
| `Dockerfile` | ✅ Scaffolded | |
| `requirements.txt` | ✅ Scaffolded | |
| `.env.example` | ✅ Scaffolded | |
| Prompt testing & refinement | ❌ Not started | Issue #2 — critical path |
| FLUX prompt chaining validation | ❌ Not started | Issue #3 |
| Real model inference (live mode) | ❌ Not started | Issue #1 |
| HF Spaces deployment | ❌ Not started | Issue #5 |
| Demo video | ❌ Not started | Issue #5 |
| Field Notes blog post | ❌ Not started | Issue #5 |

---

## Day-by-Day Sprint Plan

### Day 1 — Core pipeline working locally in mock mode

**Morning (Issues #1, #2):**
- [x] Clone repo: `git clone https://github.com/zanesmit29/the-seance`
- [x] Install: `pip install -r requirements.txt`
- [x] Run in mock mode: `MOCK_MODE=true python app.py` — confirm UI opens
- [x] Run tests: `pytest tests/` — all 5 must pass
- [ ] Test system prompts on 5 concepts (see Issue #2)
- [ ] Iterate prompts until Scientist and Mythologist voices are clearly distinct
- [ ] Commit final prompts to `prompts/scientist.txt` and `prompts/mythologist.txt`

**Afternoon (Issues #2, #3):**
- [ ] Test FLUX prompt constructor on 5 concepts — print outputs, review quality
- [ ] Confirm chained prompt references both text outputs visibly
- [ ] Add your HF_TOKEN to `.env` (copy from `.env.example`)
- [ ] Set `MOCK_MODE=false`, test live MiniCPM3-4B inference first (smallest model)
- [ ] Test live Nemotron-Nano-4B inference
- [ ] Note actual latency for each model

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
- [ ] Scientist and Mythologist outputs are clearly distinct voices on any concept
- [ ] FLUX prompt visibly references both text outputs
- [ ] Image feels surreal and concept-specific (not generic)
- [ ] Three panels reveal sequentially (not all at once)
- [ ] Download button produces a composited PNG
- [ ] `pytest tests/` — all 5 tests pass
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
| FLUX.1-schnell latency >30s on ZeroGPU | Medium | High | Use 4 inference steps (schnell optimal); pre-test on Space |
| MiniCPM3-4B voice indistinct from Scientist | Medium | High | Tight system prompts; test on 5 concepts before any code |
| All 3 models exceed ZeroGPU VRAM simultaneously | Low | High | Lazy sequential loading already implemented in agents |
| ZeroGPU cold start adds 30s+ | High | Medium | Note in demo video; show mock mode as fallback |
| Nemotron-Nano-4B not available via HF Inference API | Medium | Medium | Load locally with lazy unloading; or substitute Llama-3.2-1B-Instruct |

---

## Bonus Badges Checklist

- [ ] **Off-Brand** — No default Gradio chrome. Custom dark CSS. Sequential reveal. Target confirmed.
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
