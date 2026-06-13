# Same-Size Toggle Control Audit

This audit compares the odd-triangle-neutralizing toggle set against random same-size carrier-sign toggle controls.

No physical gravity claim is made. This is a finite graph-theoretic control test.

## Settings

- seed: 90013
- control_samples: 60
- toggle_size: 5

## Original

- odd_triangle_count: 5
- mean_actual_delta: -0.37555555555555553
- compressed_count: 294
- delta_counts: {-3: 22, -1: 272, 0: 606}

## Triangle neutralized

- toggle_edges: [[0, 1], [0, 4], [1, 2], [2, 3], [5, 10]]
- odd_triangle_count: 0
- mean_actual_delta: -0.057777777777777775
- compressed_count: 30
- delta_counts: {-2: 22, -1: 8, 0: 870}

## Control summary

- control_count: 60
- attempts: 60
- mean_actual_delta_min: -0.5
- mean_actual_delta_median: -0.39555555555555555
- mean_actual_delta_max: -0.057777777777777775
- compressed_count_min: 30
- compressed_count_median: 306.0
- compressed_count_max: 390
- odd_triangle_count_min: 0
- odd_triangle_count_median: 5.0
- odd_triangle_count_max: 8
- controls_less_or_equal_compressive_than_neutralized_count: 1
- controls_with_no_odd_triangles_count: 1

## Checks

- neutralized_has_no_odd_triangles: True
- neutralized_removes_minus3_class: True
- neutralized_less_compressive_than_original: True
- some_controls_preserve_stronger_compression_than_neutralized: True

## Interpretation

The triangle-neutralized variant changes five carrier signs, exactly like each random control.
This test asks whether the weakening seen in audit 012 is specific to removing odd carrier triangles, or whether it is typical of arbitrary five-edge sign toggles.

A strong specificity signal occurs if the triangle-neutralized variant has no odd triangles and is much less compressive than most same-size controls.

## Output

- artifacts/json/013_same_size_toggle_control_audit.json
- artifacts/md/013_same_size_toggle_control_audit.md
- artifacts/csv/013_same_size_toggle_controls.csv
