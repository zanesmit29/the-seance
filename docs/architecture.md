# The Séance — Architecture

## Pipeline

```
User Input (strange concept)
        │
        ▼
┌─────────────────┐
│  The Scientist  │  nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16
│  (Nemotron-4B)  │  Cold, clinical field-note voice
└────────┬────────┘
         │ scientist_text
         ▼
┌─────────────────┐
│ The Mythologist │  openbmb/MiniCPM3-4B  (40K downloads, Apache 2.0)
│  (MiniCPM3-4B)  │  Ancient, folkloric, feeling-forward voice
└────────┬────────┘
         │ mythologist_text
         ▼
┌─────────────────┐
│ FLUX Constructor│  prompts/flux_constructor.py
│ (prompt chain)  │  Synthesises both text outputs → FLUX prompt
└────────┬────────┘
         │ flux_params
         ▼
┌─────────────────┐
│   The Dreamer   │  black-forest-labs/FLUX.1-schnell
│  (FLUX-schnell) │  301K downloads, Apache 2.0, ~12B params
└────────┬────────┘
         │ image_path
         ▼
   Artifact Card
  (3 panels + image)
```

## Model Loading Strategy

**Lazy sequential loading** — never load all models simultaneously.

```
Load Nemotron → run → unload → (VRAM free)
Load MiniCPM3 → run → unload → (VRAM free)
Load FLUX     → run → unload → (VRAM free)
```

Combined peak VRAM usage: ~8GB (single model at a time in bfloat16).
ZeroGPU limit: 40GB — well within budget.

## FLUX Prompt Chaining

The image prompt is NOT written independently. It is constructed from:
1. Key noun phrases extracted from Scientist output
2. Dominant creature/image from Mythologist output
3. Fixed style suffix: `dreamlike atmospheric surreal dark watercolor cinematic lighting no text`

This ensures the image feels like a visual synthesis of both voices.

## ZeroGPU Notes

- Each model load/unload cycle takes ~10-20 seconds cold, ~2-5 seconds warm
- FLUX.1-schnell inference: ~5-10 seconds at 4 steps on H200
- Total expected latency: 30-60 seconds per summoning
- Use `@spaces.GPU` decorator on the summon function for ZeroGPU allocation
