# Certificate Comparison Audit

This audit compares the fresh 003 metric-deformation computation against the existing Project 18 certificates.

## Summary

- signed_all_match: False
- baseline_all_match: True
- headline_signed_diameter_radius_match: True
- headline_baseline_diameter_radius_match: True

## Signed graph comparison

| field | match | ours | certificate |
|---|---:|---|---|
| center_count | False | `342` | `349` |
| diameter | True | `8` | `8` |
| distance_distribution | False | `{1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}` | `{1: 3600, 2: 17710, 3: 60345, 4: 131446, 5: 143177, 6: 45600, 7: 2667, 8: 5}` |
| eccentricity_counts | False | `{6: 342, 7: 526, 8: 32}` | `{6: 349, 7: 541, 8: 10}` |
| radius | True | `6` | `6` |

## Baseline comparison

| field | match | ours | certificate |
|---|---:|---|---|
| center_count | True | `900` | `900` |
| diameter | True | `9` | `9` |
| distance_distribution | True | `{1: 3600, 2: 14400, 3: 36900, 4: 72000, 5: 110700, 6: 112050, 7: 45000, 8: 9000, 9: 900}` | `{1: 3600, 2: 14400, 3: 36900, 4: 72000, 5: 110700, 6: 112050, 7: 45000, 8: 9000, 9: 900}` |
| eccentricity_counts | True | `{9: 900}` | `{9: 900}` |
| radius | True | `9` | `9` |

## Interpretation

If headline diameter/radius match but detailed distributions differ, do not treat the 003 result as theorem-identical yet.
The next audit should compare edge hashes, parse mode, source file versions, and certificate source paths.
