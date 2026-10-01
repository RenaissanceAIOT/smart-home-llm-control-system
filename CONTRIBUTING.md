# Contributing

Contributions are welcome for parser coverage, safety rules, documentation, tests, and simulated integrations.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make check
```

Keep pull requests small and explain their safety impact. A new action must be declared on a device, validated by the interlock, covered by tests, and represented with synthetic examples only. Never commit API keys, addresses, voice recordings, camera data, or real household logs.

The project does not yet claim production readiness. Real-device adapters need a separate threat model, authenticated identities, acknowledgements, replay protection, and failure recovery.

