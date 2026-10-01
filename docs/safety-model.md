# Safety model

This repository is a software simulation, not a certified home-control product. Its policy demonstrates defense in depth:

1. **Intent-only LLM**: the optional model returns one label from a closed vocabulary.
2. **Logical device allowlist**: unknown device IDs are rejected as hallucinations.
3. **Capability checks**: each device exposes an explicit action set.
4. **Parameter bounds**: air conditioning 16-30°C, water heating 35-55°C, percentages 0-100.
5. **Confirmation gates**: unlocking, broad leave-home scenes, and health-related context require confirmation.
6. **Fail-closed fallback**: ambiguous or unavailable classification produces no commands.
7. **Auditability**: each decision records input, intent source, plan, findings, and outcome.

Before real deployment, add authenticated identities, authorization by household role, replay protection, signed device acknowledgements, transport security, rate limits, tamper-resistant logs, physical fail-safes, and threat-model review.

