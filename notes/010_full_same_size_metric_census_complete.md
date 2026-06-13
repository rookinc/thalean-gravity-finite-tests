# Full Same-Size Metric Census Complete

## Status

The full same-size five-edge carrier-sign toggle metric census is complete.

No physical gravity claim is made. This is a finite graph-theoretic metric census.

## Scope

The completed audit is:

    scripts/017_full_same_size_metric_sweep.py

It evaluates all five-edge carrier-sign toggle sets:

    C(30,5) = 142506

Each variant is grouped by resulting odd carrier triangle count, then tested against the untwisted baseline for half-flip return compression.

## Runtime

The Mac multiprocessing run completed with:

    workers: 10
    chunk_size: 40
    runtime_seconds: 205.1774079799652
    total_variants: 142506

## Original repaired graph

The original repaired carrier graph has:

    odd_triangle_count: 5
    odd_triangle_slots: [0,1,2,3,4,5,6,7,8,10,14]
    mean_actual_delta: -0.37555555555555553
    compressed_count: 294
    delta_counts: {-3:22, -1:272, 0:606}

## Full census median gradient

The full census gives:

    odd_count 0:
      median_mean_delta: -0.057777777777777775
      median_compressed_count: 30

    odd_count 2:
      median_mean_delta: -0.23333333333333334
      median_compressed_count: 174

    odd_count 4:
      median_mean_delta: -0.3511111111111111
      median_compressed_count: 270

    odd_count 6:
      median_mean_delta: -0.44
      median_compressed_count: 342

    odd_count 8:
      median_mean_delta: -0.5
      median_compressed_count: 390

    odd_count 10:
      median_mean_delta: -0.5
      median_compressed_count: 390

## Checks

Audit 017 verifies:

    total_matches_expected: True
    zero_odd_class_weaker_than_all_positive_odd_medians: True
    compressed_median_strictly_increases_until_saturation: True
    mean_delta_median_strictly_decreases_until_saturation: True
    no_expansion_in_any_same_size_variant: True

## Result

The balanced-sample result from audit 016 is now upgraded to a full same-size metric census.

Within the full five-edge toggle space, odd carrier triangle count organizes a monotone finite metric gradient for half-flip return compression.

The gradient saturates at odd carrier triangle counts 8 and 10.

## Project meaning

This is the strongest Project 19 mechanism statement so far:

    carrier signs
    -> odd carrier triangle count
    -> finite holonomy-density gradient
    -> half-flip return compression
    -> metric deformation

In internal project language:

    odd carrier triangles behave as finite holonomy wells,
    and odd carrier triangle count behaves as a holonomy-density control.

This remains a finite graph-theoretic statement, not a physical gravity claim.

## Dependency trail

Primary support:

    artifacts/md/017_full_same_size_metric_sweep.md
    artifacts/json/017_full_same_size_metric_sweep.json
    artifacts/csv/017_full_same_size_metric_sweep.csv

Upstream repaired source:

    Project 18 tag:
    g900-kernel-admission-metric-repair-v1.0.1
