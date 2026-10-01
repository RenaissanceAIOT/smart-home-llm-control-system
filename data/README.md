# Synthetic command dataset

`smart_home_commands_synthetic.csv` is a reproducible **synthetic coverage fixture**. It is not the private 1,119-row dataset described in the project report and it must not be presented as real household telemetry.

The generated file intentionally matches the report's published class totals so the codebase can exercise the same category balance:

| Split | Explicit | Implicit | Total |
| --- | ---: | ---: | ---: |
| All | 526 | 593 | 1,119 |

Device categories: lighting 382, kitchen/bath 361, climate 171, doors/windows 77, curtains 52, appliances 33, media 25, security 18.

Regenerate and validate:

```bash
python scripts/generate_dataset.py
python scripts/validate_dataset.py
```

The generator seed, templates, schema fields, privacy marker, and expected command JSON are all committed. Repeated text variants are deliberate: this fixture tests pipeline coverage and data contracts, not linguistic generalization.

