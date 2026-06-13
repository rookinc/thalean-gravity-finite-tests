# Full Census Theorem Verification

## Verdict

- verdict_ok: True
- observed_total: 142506
- expected_total: 142506

## Class table

| odd_triangle_count | count | median_mean_actual_delta | median_compressed_count | max_expanded_count |
|---:|---:|---:|---:|---:|
| 0 | 243 | -0.057777777777777775 | 30 | 0 |
| 2 | 12015 | -0.23333333333333334 | 174 | 0 |
| 4 | 58995 | -0.3511111111111111 | 270 | 0 |
| 6 | 58995 | -0.44 | 342 | 0 |
| 8 | 12015 | -0.5 | 390 | 0 |
| 10 | 243 | -0.5 | 390 | 0 |

## Checks

- class_counts_match_expected: True
- compressed_median_strictly_increases_until_saturation: True
- csv_total_matches_expected: True
- mean_delta_median_strictly_decreases_until_saturation: True
- median_compressed_counts_match_theorem: True
- median_mean_deltas_match_theorem: True
- no_expansion_in_any_same_size_variant: True
- no_unexpected_odd_triangle_classes: True
- source_017_json_checks_all_true: True
- source_017_json_checks_found: True
- zero_odd_class_weaker_than_all_positive_odd_medians: True

## Source artifacts

- csv: artifacts/csv/017_full_same_size_metric_sweep.csv
- json: artifacts/json/017_full_same_size_metric_sweep.json
- md: artifacts/md/017_full_same_size_metric_sweep.md
- script: scripts/017_full_same_size_metric_sweep.py

## SHA-256

- 18-g900-kernel-admission/source/kernel_payload/carrier_signing_table.csv: 9b3cf812cc0f6d7b065666c81fa6d16fd3e3b8a98955c264709337c7f3e7efb7
- 18-g900-kernel-admission/source/kernel_payload/g15_slot_edges.csv: 7b94834d507cf2995ec6faf73e2e227a685d831894aa98f2647556d8b922b8f6
- 18-g900-kernel-admission/source/kernel_payload/g60_local_edges.csv: c700a185fab6a5f434da09b7acb716b96c76170774bee946af8ea907e4fe7f9f
- 18-g900-kernel-admission/source/kernel_payload/x_sigma_edges.csv: ea2679662f4322a9ea021fba1143c804ef73b1fae95f50c77ba76b7fe1092230
- 19-thalean-gravity-finite-tests/artifacts/csv/017_full_same_size_metric_sweep.csv: 408a56f2a14f7f06eba5a1f89487066aa19f50e4cc6a4772ca32d2c2acf3b9a7
- 19-thalean-gravity-finite-tests/artifacts/json/017_full_same_size_metric_sweep.json: 4d525a12c991480067858fe90016d0abd655ff1c8060cbe1f193e9a6dc78e155
- 19-thalean-gravity-finite-tests/artifacts/md/017_full_same_size_metric_sweep.md: c170097980884d407e6dd70bef93bdaedd394694537901cac4ad8f8849c0306f
- 19-thalean-gravity-finite-tests/scripts/017_full_same_size_metric_sweep.py: b4a957be8efbb91872aa6b9b0aaee7704d0e1e796a01f0251eb1eac8085a7191
