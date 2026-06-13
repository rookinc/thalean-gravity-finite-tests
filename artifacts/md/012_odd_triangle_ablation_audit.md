# Odd Triangle Ablation Audit

This audit tests whether the odd carrier triangles are causal contributors to the strongest half-flip return compression.

No physical gravity claim is made. This is a finite graph-theoretic ablation test.

## Toggle set

Carrier edges toggled to neutralize all odd carrier triangles:

- [0, 1]
- [0, 4]
- [1, 2]
- [2, 3]
- [5, 10]

## Original

- odd_triangle_count: 5
- odd_triangle_slots: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 14]
- mean_actual_delta: -0.37555555555555553
- delta_counts: {-3: 22, -1: 272, 0: 606}
- compressed_count: 294
- unchanged_count: 606
- expanded_count: 0

## Triangle neutralized

- odd_triangle_count: 0
- odd_triangle_slots: []
- mean_actual_delta: -0.057777777777777775
- delta_counts: {-2: 22, -1: 8, 0: 870}
- compressed_count: 30
- unchanged_count: 870
- expanded_count: 0

## Checks

- original_has_odd_triangles: True
- neutralized_has_no_odd_triangles: True
- return_distribution_changes_after_neutralization: True
- minus3_compression_removed_by_neutralization: True
- neutralized_mean_less_compressive_than_original: True

## Interpretation

The neutralized variant keeps the same slot graph, same local graph, and same number of carrier edges.
Only selected carrier signs are toggled so that every carrier triangle has even parity.

If the strongest return-compression class weakens or disappears after this toggle, then odd carrier triangles are not merely descriptive markers. They are causal contributors to the compression profile.

## Output

- artifacts/json/012_odd_triangle_ablation_audit.json
- artifacts/md/012_odd_triangle_ablation_audit.md
- artifacts/csv/012_odd_triangle_ablation_returns.csv
