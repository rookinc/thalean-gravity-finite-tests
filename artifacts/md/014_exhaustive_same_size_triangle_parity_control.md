# Exhaustive Same-Size Triangle Parity Control

This audit enumerates every same-size carrier-sign toggle set and counts the resulting odd carrier triangles.

No physical gravity claim is made. This is a finite sign-parity control, not a metric BFS audit.

## Settings

- carrier_edge_count: 30
- triangle_count: 10
- original_odd_triangle_count: 5
- original_odd_triangle_slots: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 14]
- toggle_size: 5
- total_same_size_combos: 142506

## Neutralizer

- toggle_edges: [[0, 1], [0, 4], [1, 2], [2, 3], [5, 10]]
- odd_triangle_count: 0
- odd_slot_count: 0

## Exhaustive distribution

- min_odd_triangle_count: 0
- max_odd_triangle_count: 10
- zero_odd_toggle_count: 243
- zero_odd_fraction: 0.0017051913603637742
- zero_odd_controls_excluding_neutralizer: 242

### Odd triangle count distribution

- 0: 243
- 2: 12015
- 4: 58995
- 6: 58995
- 8: 12015
- 10: 243

### Odd slot count distribution

- 0: 243
- 5: 4077
- 6: 7938
- 9: 20331
- 10: 20898
- 11: 16443
- 12: 21465
- 13: 21276
- 14: 20331
- 15: 9504

## Checks

- neutralizer_found: True
- neutralizer_has_zero_odd_triangles: True
- zero_odd_is_minimal_odd_triangle_count: True
- neutralizer_in_zero_odd_class: True
- zero_odd_class_is_rare_under_same_size_toggles: True

## Interpretation

This audit asks whether the odd-triangle-neutralizing toggle set belongs to a rare same-size sign-parity class.

If the zero-odd class is small, then audit 013's weak-compression result is not merely a generic five-edge sign disturbance. It belongs to a special parity regime where the odd carrier triangles have been erased.

The next metric step is to run BFS compression metrics on every zero-odd toggle set, then compare that class against the sampled and original profiles.

## Output

- artifacts/json/014_exhaustive_same_size_triangle_parity_control.json
- artifacts/md/014_exhaustive_same_size_triangle_parity_control.md
- artifacts/csv/014_zero_odd_toggle_sets.csv
- artifacts/csv/014_triangle_parity_distribution.csv
