# Full Same-Size Metric Sweep

This audit runs half-flip return metrics for every five-edge carrier-sign toggle set.

No physical gravity claim is made. This is a finite graph-theoretic metric census.

## Settings

- toggle_size: 5
- total_variants: 142506
- workers: 10
- chunk_size: 40
- runtime_seconds: 205.1774079799652

## Original

- odd_triangle_count: 5
- odd_triangle_slots: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 14]
- mean_actual_delta: -0.37555555555555553
- compressed_count: 294
- delta_counts: {-3: 22, -1: 272, 0: 606}

## Full class summaries

### odd_triangle_count 0

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.057777777777777775, 'median': -0.057777777777777775, 'max': -0.04888888888888889, 'mean': -0.05736625514403292}
- compressed_count: {'count': 243, 'min': 22, 'median': 30, 'max': 30, 'mean': 29.62962962962963}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- distinct_delta_patterns: 3

### odd_triangle_count 2

- count: 12015
- mean_actual_delta: {'count': 12015, 'min': -0.23777777777777778, 'median': -0.23333333333333334, 'max': -0.19333333333333333, 'mean': -0.22414574374624313}
- compressed_count: {'count': 12015, 'min': 146, 'median': 174, 'max': 174, 'mean': 165.77611319184354}
- expanded_count: {'count': 12015, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 12015, 'min': 5, 'median': 6, 'max': 6, 'mean': 5.6606741573033705}
- distinct_delta_patterns: 25

### odd_triangle_count 4

- count: 58995
- mean_actual_delta: {'count': 58995, 'min': -0.41333333333333333, 'median': -0.3511111111111111, 'max': -0.31333333333333335, 'mean': -0.3514046199772109}
- compressed_count: {'count': 58995, 'min': 246, 'median': 270, 'max': 318, 'mean': 269.4908043054496}
- expanded_count: {'count': 58995, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 58995, 'min': 9, 'median': 10, 'max': 12, 'mean': 9.978947368421053}
- distinct_delta_patterns: 24

### odd_triangle_count 6

- count: 58995
- mean_actual_delta: {'count': 58995, 'min': -0.5, 'median': -0.44, 'max': -0.4066666666666667, 'mean': -0.4399915247054835}
- compressed_count: {'count': 58995, 'min': 318, 'median': 342, 'max': 390, 'mean': 341.4947368421053}
- expanded_count: {'count': 58995, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 58995, 'min': 12, 'median': 13, 'max': 15, 'mean': 12.978947368421053}
- distinct_delta_patterns: 10

### odd_triangle_count 8

- count: 12015
- mean_actual_delta: {'count': 12015, 'min': -0.5, 'median': -0.5, 'max': -0.4688888888888889, 'mean': -0.48987765293383273}
- compressed_count: {'count': 12015, 'min': 366, 'median': 390, 'max': 390, 'mean': 381.8561797752809}
- expanded_count: {'count': 12015, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 12015, 'min': 14, 'median': 15, 'max': 15, 'mean': 14.66067415730337}
- distinct_delta_patterns: 3

### odd_triangle_count 10

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.5, 'median': -0.5, 'max': -0.5, 'mean': -0.5}
- compressed_count: {'count': 243, 'min': 390, 'median': 390, 'max': 390, 'mean': 390.0}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 15, 'median': 15, 'max': 15, 'mean': 15.0}
- distinct_delta_patterns: 1

## Class medians

- odd_count=0: median_mean_delta=-0.057777777777777775, median_compressed_count=30
- odd_count=2: median_mean_delta=-0.23333333333333334, median_compressed_count=174
- odd_count=4: median_mean_delta=-0.3511111111111111, median_compressed_count=270
- odd_count=6: median_mean_delta=-0.44, median_compressed_count=342
- odd_count=8: median_mean_delta=-0.5, median_compressed_count=390
- odd_count=10: median_mean_delta=-0.5, median_compressed_count=390

## Checks

- total_matches_expected: True
- zero_odd_class_weaker_than_all_positive_odd_medians: True
- compressed_median_strictly_increases_until_saturation: True
- mean_delta_median_strictly_decreases_until_saturation: True
- no_expansion_in_any_same_size_variant: True

## Interpretation

This full census upgrades audit 016 from a balanced sample to an exhaustive same-size metric result.

The central question is whether odd carrier triangle count organizes a monotone finite metric gradient for half-flip return compression.

## Output

- artifacts/json/017_full_same_size_metric_sweep.json
- artifacts/md/017_full_same_size_metric_sweep.md
- artifacts/csv/017_full_same_size_metric_sweep.csv
