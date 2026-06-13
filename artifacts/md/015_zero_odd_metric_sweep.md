# Zero-Odd Metric Sweep

This audit runs half-flip return metric tests on every same-size toggle set that erases all odd carrier triangles.

No physical gravity claim is made. This is a finite graph-theoretic metric control.

## Original

- mean_actual_delta: -0.37555555555555553
- compressed_count: 294
- expanded_count: 0
- delta_counts: {-3: 22, -1: 272, 0: 606}

## Zero-odd class summary

- zero_odd_count: 243
- runtime_seconds: 6.0602850914001465
- distinct_delta_patterns: 3
- mean_actual_delta: {'min': -0.057777777777777775, 'median': -0.057777777777777775, 'max': -0.04888888888888889, 'mean': -0.05736625514403292}
- compressed_count: {'min': 22, 'median': 30, 'max': 30, 'mean': 29.62962962962963}
- expanded_count: {'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}

## Neutralizer

- name: zero_odd_000
- mean_actual_delta: -0.057777777777777775
- compressed_count: 30
- expanded_count: 0
- delta_counts: {-2: 22, -1: 8, 0: 870}
- same_delta_pattern_as_neutralizer_count: 207

## Most compressive zero-odd member

- name: zero_odd_000
- mean_actual_delta: -0.057777777777777775
- compressed_count: 30
- delta_counts: {-2: 22, -1: 8, 0: 870}
- toggle_edges: [[0, 1], [0, 4], [1, 2], [2, 3], [5, 10]]

## Least compressive zero-odd member

- name: zero_odd_035
- mean_actual_delta: -0.04888888888888889
- compressed_count: 22
- delta_counts: {-2: 22, 0: 878}
- toggle_edges: [[0, 1], [0, 5], [1, 2], [3, 8], [10, 14]]

## Checks

- all_zero_odd_have_no_expansion: True
- neutralizer_found: True
- neutralizer_is_weakest_or_tied: False
- zero_odd_class_is_weak_vs_original_median: True
- all_zero_odd_weaker_than_original: True

## Interpretation

This audit asks whether erasing all odd carrier triangles generally weakens half-flip return compression.

If the zero-odd class is uniformly weaker than the original, the causal mechanism becomes stronger: odd triangle holonomy is not merely correlated with the strong profile; removing it moves the system into a weak-compression metric class.

## Output

- artifacts/json/015_zero_odd_metric_sweep.json
- artifacts/md/015_zero_odd_metric_sweep.md
- artifacts/csv/015_zero_odd_metric_sweep.csv
