# Topic configuration — template (read-only)

This file is a **read-only template**: it documents the available fields and ships the
example defaults the skill offers on first run. It is **not** where your live settings
are stored. Your per-user config lives in your Google Drive at
`Claude/skill-config/news-digest.config.json` (written by the skill's guided setup); the skill
reads that file — not this one — at the start of every run. Editing this template does
not change your runs; edit the Drive config instead, or ask the skill to re-run setup.
If you name topics directly in a request, those take priority for that run.

## Default time window

14 days (2 weeks). Override per run if the user specifies a different window.

## Topics

Each topic has a short name, optional keywords/synonyms to broaden web and inbox
searches, and optional preferred sources. Keywords are search aids, not filters —
an item is relevant if it clearly concerns the topic, regardless of exact wording.

- name: Runtime inference
  keywords: inference engine, on-device inference, edge inference, inference runtime, ONNX Runtime, TensorRT, llama.cpp, ExecuTorch, quantization, latency, throughput
  sources:

- name: On-device AI
  keywords: edge AI, on-device machine learning, local AI, offline AI, private on-device, edge ML
  sources:

- name: NPUs and AI chips for end devices
  keywords: NPU, neural processing unit, AI accelerator, Apple Neural Engine, Qualcomm Hexagon, Snapdragon NPU, Intel NPU, AMD XDNA, Google Tensor, mobile SoC AI, edge accelerator, TOPS
  sources:

- name: New models (emphasis on smaller models)
  keywords: small language model, SLM, compact model, distilled model, quantized model, on-device model, sub-3B, edge model, efficient model, model release
  sources:

- name: Computer vision and world understanding
  keywords: computer vision, scene understanding, spatial understanding, depth estimation, object detection, segmentation, visual perception, world model
  sources:

- name: Speech (TTS and STT)
  keywords: text-to-speech, TTS, speech-to-text, STT, ASR, automatic speech recognition, voice synthesis, on-device speech, streaming transcription
  sources:

- name: LLMs on device
  keywords: on-device LLM, local LLM, edge LLM, mobile LLM, phone-run model, laptop LLM, browser LLM, WebGPU inference
  sources:

- name: Pose detection
  keywords: pose estimation, pose detection, body tracking, hand tracking, skeletal tracking, keypoint detection, human pose
  sources:

## Events to watch

Major industry events/conferences that get their own digest section when their
announcement days fall inside the window. Dates shift each year, so these are watch
cues, not fixed dates — the skill verifies the actual dates before featuring an event.
Edit freely; add your domain's events (and remove ones you don't care about).

- CES (early January)
- Nvidia GTC (March)
- Mobile World Congress / MWC (late February – early March)
- Google I/O (May)
- Microsoft Build (May)
- Apple WWDC (June)
- Computex (June)
- CVPR (June)
- Qualcomm Snapdragon Summit (autumn)
- Meta Connect (autumn)
- NeurIPS (December)

The skill should also feature any major event not listed here if it clearly occurred in
the window and is driving topic news.

## Excluded / noise to drop

Use this to suppress recurring irrelevant items (optional).

- Pure marketing/promo with no substantive development
- Generic funding-round news with no product or technical detail (unless the user wants it)
