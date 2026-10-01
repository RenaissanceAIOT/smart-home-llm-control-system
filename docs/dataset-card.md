# Dataset card: `smart_home_commands_synthetic`

## Summary

A Chinese-language synthetic fixture containing 1,119 smart-home commands. It exists to make the repository runnable after the original private records and per-example predictions were not published with the report.

## Intended uses

- Data-contract and pipeline tests.
- Demonstrating explicit vs. implicit instruction handling.
- Reproducing the class-count tables in the report.
- Tutorial examples and regression tests.

## Out-of-scope uses

- Claims about real-world intent-recognition accuracy.
- Training or evaluating a production model.
- Representing household demographics, speech variation, dialects, or ASR noise.
- Reproducing the report's historical performance numbers.

## Generation and provenance

The file is generated from `scripts/generate_dataset.py` with seed `20260606`. Every row carries `source=synthetic_template_v1` and `privacy=contains_no_real_user_data`. Templates are deliberately repeated with deterministic variation.

## Limitations

The data has low linguistic diversity, no recorded speech, no annotator disagreement, no real device feedback, and labels share the same intent vocabulary as the implementation. Treat evaluation on this fixture as a coverage check only.

