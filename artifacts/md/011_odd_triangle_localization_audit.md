# Odd Triangle Localization Audit

This audit tests whether odd carrier triangles localize the strongest half-flip return compression.

No physical gravity claim is made. This is a finite graph-theoretic holonomy-localization test.

## Counts

- g15_edges: 30
- triangle_count: 10
- odd_triangle_count: 5
- even_triangle_count: 5
- odd_triangle_slot_count: 11
- non_odd_triangle_slot_count: 4

## Odd carrier triangles

- triangle [0, 1, 6] signs=[1, 1, 1] parity=1
- triangle [0, 4, 5] signs=[1, 1, 1] parity=1
- triangle [1, 2, 7] signs=[1, 1, 1] parity=1
- triangle [2, 3, 8] signs=[1, 1, 1] parity=1
- triangle [5, 10, 14] signs=[1, 1, 1] parity=1

## Slot classes

- odd_triangle_slots: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 14]
- non_odd_triangle_slots: [9, 11, 12, 13]

## Aggregate compression by slot class

### odd_triangle_slots

- count: 660
- mean_actual_delta: -0.5
- delta_counts: {-3: 22, -1: 264, 0: 374}

### non_odd_triangle_slots

- count: 240
- mean_actual_delta: -0.03333333333333333
- delta_counts: {-1: 8, 0: 232}

## Per-slot summary

### Slot 0

- has_odd_triangle: True
- odd_triangle_count: 2
- even_triangle_count: 0
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 1

- has_odd_triangle: True
- odd_triangle_count: 2
- even_triangle_count: 0
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 2

- has_odd_triangle: True
- odd_triangle_count: 2
- even_triangle_count: 0
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 3

- has_odd_triangle: True
- odd_triangle_count: 1
- even_triangle_count: 1
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 4

- has_odd_triangle: True
- odd_triangle_count: 1
- even_triangle_count: 1
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 5

- has_odd_triangle: True
- odd_triangle_count: 2
- even_triangle_count: 0
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 6

- has_odd_triangle: True
- odd_triangle_count: 1
- even_triangle_count: 1
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 7

- has_odd_triangle: True
- odd_triangle_count: 1
- even_triangle_count: 1
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 8

- has_odd_triangle: True
- odd_triangle_count: 1
- even_triangle_count: 1
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 9

- has_odd_triangle: False
- odd_triangle_count: 0
- even_triangle_count: 2
- best_odd_cycle_lens: [5]
- mean_actual_delta: -0.03333333333333333
- delta_counts: {-1: 2, 0: 58}

### Slot 10

- has_odd_triangle: True
- odd_triangle_count: 1
- even_triangle_count: 1
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 11

- has_odd_triangle: False
- odd_triangle_count: 0
- even_triangle_count: 2
- best_odd_cycle_lens: [5]
- mean_actual_delta: -0.03333333333333333
- delta_counts: {-1: 2, 0: 58}

### Slot 12

- has_odd_triangle: False
- odd_triangle_count: 0
- even_triangle_count: 2
- best_odd_cycle_lens: [5]
- mean_actual_delta: -0.03333333333333333
- delta_counts: {-1: 2, 0: 58}

### Slot 13

- has_odd_triangle: False
- odd_triangle_count: 0
- even_triangle_count: 2
- best_odd_cycle_lens: [5]
- mean_actual_delta: -0.03333333333333333
- delta_counts: {-1: 2, 0: 58}

### Slot 14

- has_odd_triangle: True
- odd_triangle_count: 1
- even_triangle_count: 1
- best_odd_cycle_lens: [3]
- mean_actual_delta: -0.5
- delta_counts: {-3: 2, -1: 24, 0: 34}

## Checks

- all_odd_triangle_slots_have_best_odd_len_3: True
- no_non_odd_triangle_slot_has_best_odd_len_3: True
- no_return_pair_expansion: True
- odd_triangle_slots_more_compressive_than_non_odd_triangle_slots: True

## Interpretation

Odd carrier triangles are length-3 closed slot cycles whose carrier parity is one.
Transport around such a cycle returns to the same slot with the local coordinate half-flipped.

The audit shows whether the strongest half-flip return compression is localized exactly on slots touching such odd triangles.

## Output

- artifacts/json/011_odd_triangle_localization_audit.json
- artifacts/md/011_odd_triangle_localization_audit.md
- artifacts/csv/011_slot_triangle_compression.csv
