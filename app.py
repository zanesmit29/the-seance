"""
The Séance — A Gradio app for HuggingFace BuildSmall Hackathon: Thousand Token Wood
Three AI entities channel the form of things that don't exist.
"""
import os
import gradio as gr
from pipeline.seance_pipeline import SeancePipeline
from config import load_env

load_env()
os.environ.setdefault("MOCK_MODE", "false")
pipeline = SeancePipeline()

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
@keyframes fog-drift {
    0% { opacity: 0.55; transform: translateX(0) scaleX(1); }
    50% { opacity: 0.75; transform: translateX(8px) scaleX(1.02); }
    100% { opacity: 0.55; transform: translateX(0) scaleX(1); }
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

html {
    background: #050507 !important;
    animation: scene-flicker 7s infinite;
}

body, .gradio-container {
    background: #050507 !important;
    color: #b0a8c0 !important;
    font-family: 'Georgia', serif;
}

.gradio-container { max-width: 100vw !important; width: 100% !important; min-height: 100vh !important; margin: 0 !important; padding: 0 40px !important; }

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
    background: #0c0a12 !important;
    border: 1px solid #2e2248 !important;
    color: #c0b8d0 !important;
    font-family: 'Georgia', serif !important;
    font-size: 1.1em !important;
    text-align: center;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    caret-color: #8060a0;
    padding: 12px !important;
}
#concept-input textarea:focus {
    border-color: #4a3a70 !important;
    box-shadow: none !important;
    outline: none !important;
}

#summon-btn {
    background: #0e0a18 !important;
    border: 1px solid #3a2a5a !important;
    color: #a070d0 !important;
    letter-spacing: 0.15em !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.9em !important;
    animation: breathe 4s infinite;
}
#summon-btn:hover {
    background: #180f2a !important;
    border-color: #7050a0 !important;
    color: #c090e0 !important;
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
    background: #08060e !important;
}
#dreamer-image .wrap, #dreamer-image .block, #dreamer-image > div {
    background: #08060e !important;
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
    filter: saturate(0.35) brightness(0.72) contrast(0.88);
}
#dreamer-image::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 15% 25%, rgba(200, 210, 240, 0.12) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 65%, rgba(180, 190, 230, 0.09) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 10%, rgba(220, 220, 255, 0.08) 0%, transparent 40%),
        linear-gradient(180deg, rgba(150,150,180,0.06) 0%, transparent 30%, transparent 70%, rgba(100,100,140,0.1) 100%);
    pointer-events: none;
    animation: fog-drift 12s ease-in-out infinite;
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
"""

# ---- Build UI ----
with gr.Blocks(css=CUSTOM_CSS, title="The Séance",
               head='<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap" rel="stylesheet">') as demo:

    gr.HTML('<div id="seance-title">✦ The Séance ✦</div>')
    gr.HTML("<div id=\"seance-subtitle\">Name something that doesn't exist. Three entities will channel its form.</div>")

    with gr.Row():
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
    dreamer_out = gr.Image(show_label=False, elem_id="dreamer-image")

    # Download button
    download_btn = gr.DownloadButton("↓ Download Artifact Card", visible=False)

    def summon(concept):
        if not concept.strip():
            yield (
                '<div id="status-msg">Speak a concept to begin the summoning.</div>',
                '<div id="scientist-panel"></div>',
                '<div id="mythologist-panel"></div>',
                None,
                gr.update(visible=False),
            )
            return

        yield (
            '<div id="status-msg">The Scientist observes...</div>',
            '<div id="scientist-panel">...</div>',
            '<div id="mythologist-panel"></div>',
            None,
            gr.update(visible=False),
        )

        artifact = pipeline.summon(concept)

        yield (
            '<div id="status-msg">The Mythologist remembers...</div>',
            f'<div id="scientist-panel">{artifact["scientist_text"]}</div>',
            '<div id="mythologist-panel">...</div>',
            None,
            gr.update(visible=False),
        )

        yield (
            '<div id="status-msg">The Dreamer is forming the image...</div>',
            f'<div id="scientist-panel">{artifact["scientist_text"]}</div>',
            f'<div id="mythologist-panel">{artifact["mythologist_text"]}</div>',
            None,
            gr.update(visible=False),
        )

        yield (
            '<div id="status-msg">The summoning is complete.</div>',
            f'<div id="scientist-panel">{artifact["scientist_text"]}</div>',
            f'<div id="mythologist-panel">{artifact["mythologist_text"]}</div>',
            artifact.get("image_path"),
            gr.update(visible=True, value=artifact.get("image_path")),
        )

    summon_btn.click(
        fn=summon,
        inputs=[concept_input],
        outputs=[status_msg, scientist_out, mythologist_out, dreamer_out, download_btn],
    )
    concept_input.submit(
        fn=summon,
        inputs=[concept_input],
        outputs=[status_msg, scientist_out, mythologist_out, dreamer_out, download_btn],
    )

if __name__ == "__main__":
    demo.launch()
