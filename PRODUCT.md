# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Python and Streamlit, as specified by the project report. The core control logic remains framework-independent so it can also be exercised through a CLI, tests, and future API adapters.

## Users

- Primary: course reviewers and research readers evaluating whether the reported hybrid LLM-and-rules approach is understandable and reproducible.
- Secondary: IoT and AI developers exploring a safe natural-language control architecture before connecting real devices.

These audiences are inferred from the supplied report and the request to turn the repository into a complete, credible project.

## Product Purpose

Demonstrate an end-to-end smart-home control pipeline that converts explicit or implicit Chinese natural-language requests into constrained device commands. Success means a visitor can understand the safety model, run the demo without an API key, inspect a reproducible synthetic benchmark, and verify behavior through tests and evaluation scripts.

## Positioning

The LLM never directly controls devices. It is limited to intent classification; deterministic rules own device mapping, parameter bounds, confirmation policy, and execution.

## Operating Context

Users enter Chinese household requests, inspect the recognized intent and planned actions, review safety findings, confirm high-risk operations, observe simulated device state, and save simple recurring automations. The repository is both a research artifact and a runnable engineering demo.

## Capabilities and Constraints

- Rule-first intent recognition with optional OpenAI-compatible LLM classification.
- Device and action allowlists, parameter bounds, high-risk confirmation, and conservative fallback.
- Simulated execution, CSV/JSONL audit logs, scheduled habit storage, and reproducible evaluation.
- No real Home Assistant, MQTT, Xiaomi IoT, or physical-device integration is claimed.
- The original 1,119 private samples and per-example predictions were not included in the source report. Any included replacement benchmark must be explicitly labeled synthetic and reproducible.
- Reported historical metrics must be distinguished from metrics produced by the included code.

## Evidence on Hand

- `基于自然语言意图识别的智能家居LLM控制系统.pdf`: 12-page project report containing architecture, sample counts, historical experimental results, constraints, and implementation direction.
- No original raw user dataset, original source code, model run logs, or real-device evidence was provided. Future work must not fabricate these assets.

## Product Principles

1. Safety decisions are deterministic and auditable.
2. Synthetic demonstration data is labeled honestly and generated reproducibly.
3. The no-key local path remains fully runnable.
4. Every control decision exposes intent, actions, validation, and outcome.
5. Research claims and newly reproduced measurements remain visibly separate.

## Accessibility & Inclusion

The web demo should preserve keyboard navigation, visible focus, sufficient contrast, responsive layouts, and Chinese-language clarity. Color is not the sole carrier of execution state.
