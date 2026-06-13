# Holonomy Return Compression Audit

This audit tests whether nontrivial signed carrier cycles create half-flip return paths and measurable metric deformation.

No physical gravity claim is made. This is a finite graph-theoretic holonomy and metric test.

## Counts

- g15_edges: 30
- g60_edges: 120
- signed_edges: 3600
- baseline_edges: 3600
- simple_cycle_count: 7514
- odd_holonomy_cycle_count: 3765
- even_holonomy_cycle_count: 3749
- return_pair_count: 900

## Cycle parity

- (3, 0): 5
- (3, 1): 5
- (5, 0): 6
- (5, 1): 6
- (6, 0): 32
- (6, 1): 38
- (7, 0): 94
- (7, 1): 86
- (8, 0): 141
- (8, 1): 144
- (9, 0): 196
- (9, 1): 204
- (10, 0): 372
- (10, 1): 360
- (11, 0): 694
- (11, 1): 686
- (12, 0): 927
- (12, 1): 958
- (13, 0): 810
- (13, 1): 810
- (14, 0): 400
- (14, 1): 380
- (15, 0): 72
- (15, 1): 88

## Best odd holonomy cycle length by slot

- slot 0: 3
- slot 1: 3
- slot 2: 3
- slot 3: 3
- slot 4: 3
- slot 5: 3
- slot 6: 3
- slot 7: 3
- slot 8: 3
- slot 9: 5
- slot 10: 3
- slot 11: 5
- slot 12: 5
- slot 13: 5
- slot 14: 3

## Return-pair metric deformation

Return pairs are pairs of the form `(slot,x)` to `(slot,x+30)`.

- actual_delta_counts: {-3: 22, -1: 272, 0: 606}
- shortcut_delta_counts: {-3: 22, -1: 272, 0: 220, 1: 250, 2: 80, 3: 56}

Here `actual_delta = signed_distance - baseline_distance`.

- negative actual delta means signed carrier holonomy shortens the half-flip return pair.
- zero means no change for that pair.
- positive means the signed carrier graph lengthens that pair.

## By slot

### Slot 0

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2930
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 1

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2930
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 2

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2898
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 3

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2913
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 4

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2913
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 5

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2898
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 6

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2913
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 7

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2913
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 8

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2909
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 9

- best_odd_cycle_len: 5
- odd_cycle_count_containing_slot: 2908
- mean_actual_delta: -0.03333333333333333
- actual_delta_counts: {-1: 2, 0: 58}

### Slot 10

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2913
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

### Slot 11

- best_odd_cycle_len: 5
- odd_cycle_count_containing_slot: 2908
- mean_actual_delta: -0.03333333333333333
- actual_delta_counts: {-1: 2, 0: 58}

### Slot 12

- best_odd_cycle_len: 5
- odd_cycle_count_containing_slot: 2908
- mean_actual_delta: -0.03333333333333333
- actual_delta_counts: {-1: 2, 0: 58}

### Slot 13

- best_odd_cycle_len: 5
- odd_cycle_count_containing_slot: 2912
- mean_actual_delta: -0.03333333333333333
- actual_delta_counts: {-1: 2, 0: 58}

### Slot 14

- best_odd_cycle_len: 3
- odd_cycle_count_containing_slot: 2909
- mean_actual_delta: -0.5
- actual_delta_counts: {-3: 2, -1: 24, 0: 34}

## Interpretation

An odd carrier cycle is a finite holonomy witness: transport around the closed slot cycle returns to the same slot with local coordinate shifted by 30.

The audit asks whether those half-flip return paths are metric-active relative to the untwisted baseline.

## Output

- artifacts/json/010_holonomy_return_compression_audit.json
- artifacts/md/010_holonomy_return_compression_audit.md
- artifacts/csv/010_holonomy_return_pairs.csv
