# Odd Triangle Count Gradient Metric Audit

This audit runs a balanced metric sample across same-size toggle classes grouped by odd carrier triangle count.

No physical gravity claim is made. This is a finite graph-theoretic metric gradient test.

## Settings

- seed: 90016
- sample_per_class: 243
- runtime_seconds: 23.43224000930786

## Original

- odd_triangle_count: 5
- odd_triangle_slots: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 14]
- mean_actual_delta: -0.37555555555555553
- compressed_count: 294
- delta_counts: {-3: 22, -1: 272, 0: 606}

## Class summaries

### odd_triangle_count 0

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.057777777777777775, 'median': -0.057777777777777775, 'max': -0.04888888888888889, 'mean': -0.05736625514403292}
- compressed_count: {'count': 243, 'min': 22, 'median': 30, 'max': 30, 'mean': 29.62962962962963}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}

### odd_triangle_count 2

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.23777777777777778, 'median': -0.2311111111111111, 'max': -0.2, 'mean': -0.22262459990855052}
- compressed_count: {'count': 243, 'min': 148, 'median': 174, 'max': 174, 'mean': 165.7037037037037}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 5, 'median': 6, 'max': 6, 'mean': 5.658436213991769}

### odd_triangle_count 4

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.4111111111111111, 'median': -0.3488888888888889, 'max': -0.31777777777777777, 'mean': -0.35335162322816643}
- compressed_count: {'count': 243, 'min': 246, 'median': 270, 'max': 318, 'mean': 273.25925925925924}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 9, 'median': 10, 'max': 12, 'mean': 10.135802469135802}

### odd_triangle_count 6

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.5, 'median': -0.44, 'max': -0.4066666666666667, 'mean': -0.44183813443072706}
- compressed_count: {'count': 243, 'min': 318, 'median': 342, 'max': 390, 'mean': 344.3703703703704}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 12, 'median': 13, 'max': 15, 'mean': 13.098765432098766}

### odd_triangle_count 8

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.5, 'median': -0.5, 'max': -0.4688888888888889, 'mean': -0.4866849565614998}
- compressed_count: {'count': 243, 'min': 366, 'median': 390, 'max': 390, 'mean': 379.7283950617284}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 14, 'median': 15, 'max': 15, 'mean': 14.572016460905349}

### odd_triangle_count 10

- count: 243
- mean_actual_delta: {'count': 243, 'min': -0.5, 'median': -0.5, 'max': -0.5, 'mean': -0.5}
- compressed_count: {'count': 243, 'min': 390, 'median': 390, 'max': 390, 'mean': 390.0}
- expanded_count: {'count': 243, 'min': 0, 'median': 0, 'max': 0, 'mean': 0.0}
- odd_slot_count: {'count': 243, 'min': 15, 'median': 15, 'max': 15, 'mean': 15.0}

## Class medians

- odd_count=0: median_mean_delta=-0.057777777777777775, median_compressed_count=30
- odd_count=2: median_mean_delta=-0.2311111111111111, median_compressed_count=174
- odd_count=4: median_mean_delta=-0.3488888888888889, median_compressed_count=270
- odd_count=6: median_mean_delta=-0.44, median_compressed_count=342
- odd_count=8: median_mean_delta=-0.5, median_compressed_count=390
- odd_count=10: median_mean_delta=-0.5, median_compressed_count=390

## Checks

- zero_odd_class_weaker_than_all_positive_odd_medians: True
- compressed_median_increases_after_zero_odd: True
- original_is_stronger_than_zero_odd_median: True

## Interpretation

This audit asks whether the weak zero-odd class is part of a broader metric gradient as odd carrier triangles return.

The key comparison is not whether every additional odd triangle monotonically increases compression. The cautious question is whether the zero-odd class is separated from the positive-odd classes.

## Output

- artifacts/json/016_odd_triangle_count_gradient_metric_audit.json
- artifacts/md/016_odd_triangle_count_gradient_metric_audit.md
- artifacts/csv/016_odd_triangle_count_gradient_metric_audit.csv
