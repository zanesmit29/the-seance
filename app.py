"""
The Séance — A Gradio app for HuggingFace BuildSmall Hackathon: Thousand Token Wood
Three AI entities channel the form of things that don't exist.
"""
import os
import gradio as gr
from pathlib import Path
from urllib.parse import quote
from pipeline.seance_pipeline import SeancePipeline
from config import load_env

try:
    import spaces  # type: ignore[import-not-found]
except ImportError:
    spaces = None

load_env()
os.environ.setdefault("MOCK_MODE", "false")

# Use the app's directory so audio works regardless of launch cwd.
BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
AUDIO_FILE = AUDIO_DIR / "ambiance.MP3"
if AUDIO_DIR.exists():
    gr.set_static_paths(paths=[AUDIO_DIR])

audio_file_web = str(AUDIO_FILE).replace("\\", "/")
AUDIO_SRC = f"/gradio_api/file={quote(audio_file_web)}" if AUDIO_FILE.exists() else ""
pipeline = SeancePipeline()

if spaces is not None:
    @spaces.GPU(duration=90)
    def _summon_on_gpu(concept: str):
        return pipeline.summon(concept)
else:
    def _summon_on_gpu(concept: str):
        return pipeline.summon(concept)

# ---- Custom CSS: dark, eerie, uneasy ----
CUSTOM_CSS = """@keyframes flicker {
    0%, 8%, 12%, 16%, 20%, 50%, 54%, 58%, 80%, 84%, 100% { opacity: 1; }
    10%, 14% { opacity: 0.15; }
    18% { opacity: 0.6; }
    52%, 56% { opacity: 0.1; }
    82% { opacity: 0.5; }
}
@keyframes scene-flicker {
    0%, 88%, 92%, 96%, 100% { opacity: 1; }
    89%, 93% { opacity: 0.25; }
    90%, 94% { opacity: 0.85; }
    97% { opacity: 0.4; }
    98% { opacity: 0.9; }
}
@keyframes breathe {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.88; }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 10px rgba(100, 50, 180, 0.3), inset 0 0 20px rgba(100, 50, 180, 0.1); }
    50% { box-shadow: 0 0 25px rgba(100, 50, 180, 0.5), inset 0 0 30px rgba(100, 50, 180, 0.2); }
}
@keyframes smoke-plume-a {
    0% { transform: translate3d(-5%, 2%, 0) scale(1.05) rotate(0.2deg); opacity: 0.24; }
    33% { transform: translate3d(4%, -2%, 0) scale(1.13) rotate(-0.2deg); opacity: 0.4; }
    66% { transform: translate3d(-2%, -1%, 0) scale(1.09) rotate(0.2deg); opacity: 0.31; }
    100% { transform: translate3d(-5%, 2%, 0) scale(1.05) rotate(0.2deg); opacity: 0.24; }
}
@keyframes smoke-plume-b {
    0% { transform: translate3d(3%, 1%, 0) scale(1.02); opacity: 0.2; }
    40% { transform: translate3d(-4%, -2%, 0) scale(1.12); opacity: 0.34; }
    80% { transform: translate3d(2%, 2%, 0) scale(1.08); opacity: 0.27; }
    100% { transform: translate3d(3%, 1%, 0) scale(1.02); opacity: 0.2; }
}
@keyframes smoke-plume-c {
    0% { transform: translate3d(-1%, 3%, 0) scale(1); opacity: 0.16; }
    45% { transform: translate3d(3%, -2%, 0) scale(1.07); opacity: 0.28; }
    100% { transform: translate3d(-1%, 3%, 0) scale(1); opacity: 0.16; }
}
@keyframes grain-drift {
    0% { transform: translate(0, 0); }
    25% { transform: translate(-1.2%, 0.8%); }
    50% { transform: translate(0.8%, -1%); }
    75% { transform: translate(-0.6%, -0.8%); }
    100% { transform: translate(0, 0); }
}
@keyframes ritual-surge {
    0% { opacity: 0; }
    40% { opacity: 0.35; }
    100% { opacity: 0; }
}
@keyframes fog-drift {
    0% { opacity: 0.55; transform: translateX(0) scaleX(1); }
    50% { opacity: 0.75; transform: translateX(8px) scaleX(1.02); }
    100% { opacity: 0.55; transform: translateX(0) scaleX(1); }
}
@keyframes panel-reveal {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
@keyframes loading-pulse {
    0%, 100% { opacity: 0.45; }
    50% { opacity: 1; }
}
@keyframes loading-dots {
    0% { width: 0; }
    100% { width: 3ch; }
}

* { box-sizing: border-box; outline: none !important; }
*:focus, *:focus-visible, *:focus-within { outline: none !important; box-shadow: none !important; }
.block, .block:focus, .block:focus-within { outline: none !important; box-shadow: none !important; border-color: transparent !important; }

/* Kill Gradio component container borders everywhere */
.gradio-container .block,
.gradio-container [class*="block"],
.gradio-container label,
.gradio-container .wrap,
.gradio-container .container,
.gradio-container > div > div,
.gradio-container form,
.svelte-1f354aw,
.svelte-1gfkn6j {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
}

/* Override Gradio 6 CSS variables for the input component */
:root, .gradio-container {
    --block-border-color: transparent !important;
    --block-border-width: 0px !important;
    --input-border-color: #2e2248 !important;
    --input-border-color-focus: #4a3a70 !important;
    --border-color-primary: transparent !important;
    --block-background-fill: transparent !important;
    --input-background-fill: #0c0a12 !important;
    --block-shadow: none !important;
    --input-shadow: none !important;
    --input-shadow-focus: none !important;
}

:root {
    --smoke-violet: rgba(130, 100, 182, 0.48);
    --smoke-indigo: rgba(58, 76, 132, 0.38);
    --smoke-char: rgba(18, 16, 26, 0.62);
    --smoke-speed-a: 32s;
    --smoke-speed-b: 46s;
    --smoke-speed-c: 58s;
}

html {
    background: #050507 !important;
    animation: scene-flicker 7s infinite;
}

body, .gradio-container {
    background: #050507 !important;
    color: #b0a8c0 !important;
    font-family: 'Georgia', serif;
}

.gradio-container::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 2;
    background:
        radial-gradient(120vmax 75vmax at 50% 12%, transparent 0%, rgba(0, 0, 0, 0.22) 48%, rgba(0, 0, 0, 0.72) 100%),
        linear-gradient(180deg, transparent 0%, var(--smoke-char) 100%);
    box-shadow: inset 0 0 180px rgba(0, 0, 0, 0.75);
}

.gradio-container { max-width: 100vw !important; width: 100% !important; min-height: 100vh !important; margin: 0 !important; padding: 0 40px !important; }

.gradio-container > * {
    position: relative;
    z-index: 4;
}

#smoke-layer {
    position: fixed;
    inset: -12%;
    z-index: 1;
    pointer-events: none;
    overflow: hidden;
}

#smoke-layer .smoke {
    position: absolute;
    border-radius: 50%;
    filter: blur(36px);
    mix-blend-mode: screen;
    will-change: transform, opacity;
}

#smoke-layer .smoke-a {
    width: 78vmax;
    height: 54vmax;
    top: -10vmax;
    left: -18vmax;
    background: radial-gradient(ellipse at center, var(--smoke-violet) 0%, rgba(90, 66, 130, 0.18) 46%, transparent 75%);
    animation: smoke-plume-a var(--smoke-speed-a) ease-in-out infinite;
}

#smoke-layer .smoke-b {
    width: 84vmax;
    height: 58vmax;
    right: -20vmax;
    top: 12vmax;
    background: radial-gradient(ellipse at center, var(--smoke-indigo) 0%, rgba(60, 72, 118, 0.2) 44%, transparent 74%);
    animation: smoke-plume-b var(--smoke-speed-b) ease-in-out infinite;
}

#smoke-layer .smoke-c {
    width: 96vmax;
    height: 52vmax;
    left: 4vmax;
    bottom: -22vmax;
    background: radial-gradient(ellipse at center, rgba(94, 77, 126, 0.24) 0%, rgba(60, 52, 82, 0.14) 42%, transparent 74%);
    animation: smoke-plume-c var(--smoke-speed-c) ease-in-out infinite;
}

/* Hide all default Gradio chrome */
footer, .share-button, .duplicate-button, .built-with { display: none !important; }
.svelte-1ipelgc { display: none !important; }

/* Title — eerie gothic, violent flicker */
#seance-title {
    text-align: center;
    padding: 40px 0 10px;
    font-size: 3em;
    letter-spacing: 0.08em;
    color: #d0c8e0;
    font-family: 'UnifrakturMaguntia', 'Palatino Linotype', serif;
    animation: flicker 2.8s infinite;
    text-shadow: 0 0 30px rgba(100, 50, 180, 0.6), 0 0 60px rgba(100, 50, 180, 0.3), 0 0 2px #fff;
}
#seance-subtitle {
    text-align: center;
    color: #6a5880;
    font-size: 0.95em;
    letter-spacing: 0.06em;
    margin-bottom: 36px;
    font-style: italic;
    animation: breathe 6s infinite;
    text-shadow: 0 0 15px rgba(80, 30, 120, 0.3);
}

/* Input area — kill ALL Gradio default borders and glows */
#ritual-input-shell {
    position: relative;
    padding: 14px;
    border: 1px solid rgba(118, 84, 172, 0.32) !important;
    background: linear-gradient(160deg, rgba(20, 16, 33, 0.85), rgba(10, 9, 16, 0.7)) !important;
    box-shadow: inset 0 0 0 1px rgba(173, 129, 237, 0.08), 0 0 28px rgba(48, 28, 74, 0.34);
    backdrop-filter: blur(4px);
}

#ritual-input-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(120deg, transparent 35%, rgba(181, 140, 240, 0.1) 50%, transparent 65%);
    opacity: 0.5;
}

#concept-input, #concept-input *, #concept-input *:focus, #concept-input *:active, #concept-input *:hover {
    outline: none !important;
}
#concept-input > *, #concept-input label, #concept-input .block, #concept-input .wrap, #concept-input > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
#concept-input textarea {
    background: linear-gradient(180deg, rgba(11, 9, 18, 0.94), rgba(15, 11, 25, 0.92)) !important;
    border: 1px solid rgba(95, 72, 141, 0.75) !important;
    color: #d8d0e7 !important;
    font-family: 'Palatino Linotype', 'Georgia', serif !important;
    font-size: 1.05em !important;
    text-align: left;
    border-radius: 2px !important;
    box-shadow: inset 0 0 18px rgba(95, 58, 150, 0.15), 0 0 0 1px rgba(166, 124, 232, 0.1) !important;
    outline: none !important;
    caret-color: #b88ef3;
    letter-spacing: 0.02em;
    line-height: 1.45;
    padding: 14px 16px !important;
    transition: border-color 0.18s ease, box-shadow 0.2s ease, transform 0.2s ease;
}
#concept-input textarea::placeholder {
    color: rgba(184, 167, 216, 0.58) !important;
    font-style: italic;
    letter-spacing: 0.05em;
}
#concept-input textarea:focus {
    border-color: rgba(188, 143, 248, 0.92) !important;
    box-shadow: inset 0 0 22px rgba(112, 73, 182, 0.22), 0 0 24px rgba(146, 102, 214, 0.26) !important;
    outline: none !important;
    transform: translateY(-1px);
}

#ritual-input-shell:focus-within {
    border-color: rgba(184, 138, 248, 0.78) !important;
    box-shadow: inset 0 0 0 1px rgba(190, 146, 248, 0.14), 0 0 36px rgba(110, 62, 184, 0.42);
}

#summon-btn {
    position: relative;
    overflow: hidden;
    background: #0e0a18 !important;
    border: 1px solid #3a2a5a !important;
    color: #a070d0 !important;
    letter-spacing: 0.15em !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.9em !important;
    animation: breathe 4s infinite;
    transition: transform 0.18s ease, box-shadow 0.25s ease;
}
#summon-btn:hover {
    background: #180f2a !important;
    border-color: #7050a0 !important;
    color: #c090e0 !important;
    transform: translateY(-1px);
    box-shadow: 0 0 18px rgba(130, 84, 190, 0.28);
}
#summon-btn:active {
    transform: translateY(1px) scale(0.995);
}
#summon-btn.is-channeling {
    box-shadow: 0 0 22px rgba(146, 99, 201, 0.36), inset 0 0 10px rgba(146, 99, 201, 0.12);
}
#summon-btn.is-channeling::after {
    content: "";
    position: absolute;
    inset: -35% -10%;
    background: linear-gradient(110deg, transparent 35%, rgba(200, 155, 255, 0.22) 50%, transparent 65%);
    animation: grain-drift 1.6s linear infinite;
}

/* Scientist panel — rigid, cold, neon green terminal */
#scientist-panel {
    background: #030a04 !important;
    border-top: 1px solid #1a3a1a !important;
    border-right: 1px solid #1a3a1a !important;
    border-bottom: 1px solid #1a3a1a !important;
    border-left: 3px solid #00ff41 !important;
    border-radius: 0;
    padding: 20px;
    font-family: 'Courier New', monospace !important;
    color: #00ff41 !important;
    font-size: 1.1em;
    line-height: 1.7;
    min-height: 100px;
    letter-spacing: 0.04em;
    box-shadow: 0 0 12px rgba(0, 255, 65, 0.15), inset 0 0 8px rgba(0, 255, 65, 0.05);
    text-shadow: 0 0 6px rgba(0, 255, 65, 0.6);
}
#scientist-label {
    color: #00cc33;
    font-family: 'Courier New', monospace;
    font-size: 0.75em;
    letter-spacing: 0.28em;
    margin-bottom: 8px;
    text-transform: uppercase;
    text-shadow: 0 0 8px rgba(0, 255, 65, 0.5);
}

/* Mythologist panel — amber, breathing, eerie */
#mythologist-panel {
    background: linear-gradient(135deg, #0f0815 0%, #1a0f25 100%) !important;
    border: 2px solid #4a3a7a !important;
    border-radius: 2px;
    padding: 20px;
    font-family: 'Georgia', serif !important;
    color: #d8a0ff !important;
    font-size: 1.15em;
    line-height: 1.9;
    font-style: italic;
    min-height: 100px;
    animation: breathe 5s ease-in-out infinite;
    box-shadow: 0 0 20px rgba(180, 100, 255, 0.2), inset 0 0 15px rgba(180, 100, 255, 0.1);
    text-shadow: 0 0 10px rgba(180, 100, 255, 0.3);
}
#mythologist-label {
    color: #7a5a9a;
    font-family: 'Georgia', serif;
    font-size: 0.75em;
    letter-spacing: 0.2em;
    margin-bottom: 8px;
    text-transform: uppercase;
    font-style: normal;
    animation: flicker 4s infinite;
    text-shadow: 0 0 8px rgba(180, 100, 255, 0.4);
}

/* Dreamer — cloudy, desaturated, fog overlay */
#dreamer-image {
    position: relative;
    overflow: hidden;
    background: transparent !important;
}
#dreamer-image .wrap, #dreamer-image .block, #dreamer-image > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#dreamer-image button, #dreamer-image .icon-button {
    background: transparent !important;
    border: none !important;
    opacity: 0.4;
}
#dreamer-image img {
    border-radius: 0;
    border: 2px solid #201828;
    width: 100%;
    display: block;
    position: relative;
    z-index: 1;
    filter: none;
}
#dreamer-label {
    color: #5a4a7a;
    font-size: 0.75em;
    letter-spacing: 0.2em;
    margin-bottom: 8px;
    text-transform: uppercase;
    animation: breathe 5s infinite;
}

/* Status message */
#status-msg {
    color: #6a5880;
    font-size: 0.8em;
    text-align: center;
    font-style: italic;
    animation: flicker 3s infinite;
    letter-spacing: 0.05em;
}

body[data-seance-state="channeling"] #status-msg {
    color: #aa86d6;
    text-shadow: 0 0 10px rgba(152, 102, 214, 0.3);
}
body[data-seance-state="channeling"] {
    --smoke-speed-a: 20s;
    --smoke-speed-b: 31s;
    --smoke-speed-c: 38s;
}
body[data-seance-state="complete"] {
    --smoke-speed-a: 15s;
    --smoke-speed-b: 24s;
    --smoke-speed-c: 29s;
}
body[data-seance-state="complete"] .gradio-container::after {
    animation: ritual-surge 1.1s ease-out;
}

.panel-reveal {
    opacity: 0;
    animation: panel-reveal 0.55s ease forwards;
}
.reveal-1 { animation-delay: 0.03s; }
.reveal-2 { animation-delay: 0.17s; }
.reveal-3 { animation-delay: 0.31s; }

.entity-loading {
    display: inline-flex;
    align-items: baseline;
    gap: 0;
    animation: loading-pulse 1.4s ease-in-out infinite;
}
.loading-dots {
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;
    width: 0;
    animation: loading-dots 1.1s steps(4, end) infinite;
}
.scientist-loading {
    color: #00ff41;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.mythologist-loading {
    color: #d8a0ff;
    font-style: italic;
}
.dreamer-loading {
    color: #8f84b0;
}
#dreamer-loading-panel {
    min-height: 56px;
    display: flex;
    align-items: center;
    color: #8f84b0;
    font-style: italic;
    letter-spacing: 0.04em;
}
/* Mute button style */
#mute-btn {
    position: fixed !important;
    bottom: 20px !important;
    right: 20px !important;
    background: #0e0a18 !important;
    border: 1px solid #3a2a5a !important;
    color: #a070d0 !important;
    padding: 10px 20px !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.9em !important;
    letter-spacing: 0.1em !important;
    cursor: pointer !important;
    z-index: 10000 !important;
    animation: breathe 4s infinite !important;
    border-radius: 2px !important;
}
#mute-btn:hover {
    background: #180f2a !important;
    border-color: #7050a0 !important;
    color: #c090e0 !important;
}

@media (max-width: 900px) {
    .gradio-container {
        padding: 0 16px !important;
    }
    #ritual-input-shell {
        padding: 10px;
    }
    #seance-title {
        font-size: 2.2em;
        padding-top: 28px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
"""
BACKGROUND_AUDIO = f"""
<audio id="seance-bg-audio" loop preload="auto">
    <source src="{AUDIO_SRC}" type="audio/mpeg">
</audio>

<button id="enable-audio-btn" style="position: fixed; bottom: 70px; right: 20px; background: #0e0a18; border: 1px solid #3a2a5a; color: #a070d0; padding: 10px 20px; font-family: 'Georgia', serif; font-size: 0.9em; letter-spacing: 0.1em; cursor: pointer; z-index: 10000;">
    🔊 Enable Sound
</button>

<button id="mute-btn" style="position: fixed; bottom: 20px; right: 20px; background: #0e0a18; border: 1px solid #3a2a5a; color: #a070d0; padding: 10px 20px; font-family: 'Georgia', serif; font-size: 0.9em; letter-spacing: 0.1em; cursor: pointer; z-index: 10000;">
    🔇 Mute
</button>
"""

HEAD_SNIPPET = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap" rel="stylesheet">
<script>
(() => {
    const setSceneState = (state) => {
        document.body.setAttribute('data-seance-state', state);
        const summonBtn = document.querySelector('#summon-btn button, #summon-btn');
        if (summonBtn) {
            summonBtn.classList.toggle('is-channeling', state === 'channeling');
        }
    };

    const observeSummonState = () => {
        const resolveStatusNode = () => document.querySelector('#status-msg');
        const node = resolveStatusNode();
        if (!node) return false;

        const applyStateFromText = () => {
            const text = (node.textContent || '').toLowerCase();
            if (text.includes('channeling')) {
                setSceneState('channeling');
                return;
            }
            if (text.includes('complete')) {
                setSceneState('complete');
                return;
            }
            setSceneState('idle');
        };

        applyStateFromText();
        const obs = new MutationObserver(applyStateFromText);
        obs.observe(node, { childList: true, subtree: true, characterData: true });
        return true;
    };

    const bindAudio = () => {
        const audio = document.getElementById('seance-bg-audio');
        const enableBtn = document.getElementById('enable-audio-btn');
        const muteBtn = document.getElementById('mute-btn');
        if (!audio || !enableBtn || !muteBtn) return false;

        if (audio.dataset.bound === '1') return true;
        audio.dataset.bound = '1';
        audio.volume = 0.35;

        let started = false;
        let muted = false;

        enableBtn.addEventListener('click', async () => {
            try {
                await audio.play();
                started = true;
                enableBtn.style.display = 'none';
            } catch (e) {
                console.error('Audio play failed:', e);
            }
        });

        muteBtn.addEventListener('click', async () => {
            if (!started) {
                try {
                    await audio.play();
                    started = true;
                    enableBtn.style.display = 'none';
                } catch (e) {
                    console.error('Audio play failed:', e);
                    return;
                }
            }
            muted = !muted;
            audio.muted = muted;
            muteBtn.textContent = muted ? '🔊 Unmute' : '🔇 Mute';
        });

        // Best effort autoplay: if browser allows, hide enable button; otherwise keep fallback.
        (async () => {
            try {
                await audio.play();
                started = true;
                enableBtn.style.display = 'none';
            } catch (e) {
                // Expected on browsers that block autoplay with sound.
                enableBtn.style.display = 'block';
            }
        })();

        return true;
    };

    const startBinding = () => {
        setSceneState('idle');
        if (!observeSummonState()) {
            const statusObserver = new MutationObserver(() => {
                if (observeSummonState()) statusObserver.disconnect();
            });
            statusObserver.observe(document.body, { childList: true, subtree: true });
            setTimeout(() => statusObserver.disconnect(), 15000);
        }

        if (bindAudio()) return;
        const observer = new MutationObserver(() => {
            if (bindAudio()) observer.disconnect();
        });
        observer.observe(document.body, { childList: true, subtree: true });
        setTimeout(() => observer.disconnect(), 15000);
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startBinding, { once: true });
    } else {
        startBinding();
    }
})();
</script>
"""

# ---- Build UI ----
with gr.Blocks(title="The Séance", css=CUSTOM_CSS, head=HEAD_SNIPPET) as demo:

    # Add background audio
    gr.HTML(BACKGROUND_AUDIO)
    gr.HTML(
        '<div id="smoke-layer" aria-hidden="true">'
        '<span class="smoke smoke-a"></span>'
        '<span class="smoke smoke-b"></span>'
        '<span class="smoke smoke-c"></span>'
        '</div>'
    )

    gr.HTML('<div id="seance-title">✦ The Séance ✦</div>')
    gr.HTML("<div id=\"seance-subtitle\">Name something that doesn't exist. Three entities will channel its form.</div>")

    with gr.Row(elem_id="ritual-input-shell"):
        concept_input = gr.Textbox(
            placeholder="the last color light ever made...",
            show_label=False,
            elem_id="concept-input",
            scale=4,
        )
        summon_btn = gr.Button("— SUMMON —", elem_id="summon-btn", scale=1)

    status_msg = gr.HTML('<div id="status-msg"></div>')

    # Scientist panel
    gr.HTML('<div id="scientist-label">✦ The Scientist</div>')
    scientist_out = gr.HTML('<div id="scientist-panel"></div>')

    # Mythologist panel
    gr.HTML('<div id="mythologist-label">✦ The Mythologist</div>')
    mythologist_out = gr.HTML('<div id="mythologist-panel"></div>')

    # Dreamer image
    gr.HTML('<div id="dreamer-label">✦ The Dreamer</div>')
    dreamer_loading_out = gr.HTML('<div id="dreamer-loading-panel"></div>')
    dreamer_out = gr.Image(show_label=False, elem_id="dreamer-image")

    # Download button
    download_btn = gr.DownloadButton("↓ Download Artifact Card", visible=False)

    def summon(concept):
        if not concept.strip():
            yield (
                '<div id="status-msg">Speak a concept to begin the summoning.</div>',
                '<div id="scientist-panel"></div>',
                '<div id="mythologist-panel"></div>',
                '<div id="dreamer-loading-panel"></div>',
                None,
                gr.update(visible=False),
            )
            return

        yield (
            '<div id="status-msg"><span class="entity-loading">The entities are channeling<span class="loading-dots">...</span></span></div>',
            '<div id="scientist-panel"><span class="entity-loading scientist-loading">Calculating spectral residue<span class="loading-dots">...</span></span></div>',
            '<div id="mythologist-panel"><span class="entity-loading mythologist-loading">Gathering echoes from the elder tongue<span class="loading-dots">...</span></span></div>',
            '<div id="dreamer-loading-panel"><span class="entity-loading dreamer-loading">Condensing the fog into form<span class="loading-dots">...</span></span></div>',
            None,
            gr.update(visible=False),
        )

        artifact = _summon_on_gpu(concept)

        yield (
            '<div id="status-msg">The summoning is complete.</div>',
            f'<div id="scientist-panel" class="panel-reveal reveal-1">{artifact["scientist_text"]}</div>',
            f'<div id="mythologist-panel" class="panel-reveal reveal-2">{artifact["mythologist_text"]}</div>',
            '<div id="dreamer-loading-panel" class="panel-reveal reveal-3"></div>',
            artifact.get("image_path"),
            gr.update(visible=True, value=artifact.get("image_path")),
        )

    summon_btn.click(
        fn=summon,
        inputs=[concept_input],
        outputs=[status_msg, scientist_out, mythologist_out, dreamer_loading_out, dreamer_out, download_btn],
    )
    concept_input.submit(
        fn=summon,
        inputs=[concept_input],
        outputs=[status_msg, scientist_out, mythologist_out, dreamer_loading_out, dreamer_out, download_btn],
    )

if __name__ == "__main__":
    demo.launch()
