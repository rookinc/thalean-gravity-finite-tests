# Odd Triangle Metric Gradient

## Status

Working finite-graph mechanism result, supported by audit 016 and the prior chain 010 through 015.

No physical gravity claim is made. This note concerns finite signed carrier holonomy and graph metric deformation.

## Core result

In the same-size five-edge toggle control regime, half-flip return compression strengthens as odd carrier triangle count increases.

The zero-odd class is sharply separated from every positive-odd class.

The trend saturates in the high odd-triangle classes.

## Median gradient

Audit 016 sampled 243 variants from each odd carrier triangle count class.

The class medians were:

    odd_count 0:
      median_mean_delta: -0.057777777777777775
      median_compressed_count: 30

    odd_count 2:
      median_mean_delta: -0.2311111111111111
      median_compressed_count: 174

    odd_count 4:
      median_mean_delta: -0.3488888888888889
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

Here:

    actual_delta = signed_distance - baseline_distance

More negative mean delta means stronger return compression. Higher compressed count means more half-flip return pairs are shortened relative to the untwisted baseline.

## Original repaired graph

The original repaired carrier graph has:

    odd_triangle_count: 5
    odd_triangle_slots: [0,1,2,3,4,5,6,7,8,10,14]
    mean_actual_delta: -0.37555555555555553
    compressed_count: 294
    delta_counts: {-3:22, -1:272, 0:606}

The original sits naturally between the sampled odd_count 4 and odd_count 6 classes.

## Checks

Audit 016 verifies:

    zero_odd_class_weaker_than_all_positive_odd_medians: True
    compressed_median_increases_after_zero_odd: True
    original_is_stronger_than_zero_odd_median: True

## Mechanism statement

Odd carrier triangle count behaves like a finite holonomy-density control for half-flip return compression.

In the tested same-size control regime:

    0 odd triangles -> weak compression
    positive odd triangles -> stronger compression
    high odd triangle count -> saturated strong compression

This strengthens the Project 19 mechanism chain:

    carrier signs
    -> odd carrier triangle holonomy
    -> holonomy-density gradient
    -> half-flip return compression
    -> finite metric deformation

## Caution

This is a finite graph-theoretic result, not a physical gravity result.

The audit used a balanced sample of 243 variants per odd-count class, not a full metric sweep of all 142506 same-size toggles.

The safe claim is:

    In the balanced same-size toggle sample, median half-flip return compression strengthens with odd carrier triangle count, with saturation at the 8 and 10 odd-triangle classes.

## Internal definition update

Finite Thalean gravity can now be stated as:

    carrier-induced metric compression organized by return holonomy, with odd carrier triangles acting as local holonomy wells and odd-triangle count behaving as a finite holonomy-density control.

## Dependency trail

Primary support:

    artifacts/md/010_holonomy_return_compression_audit.md
    artifacts/md/011_odd_triangle_localization_audit.md
    artifacts/md/012_odd_triangle_ablation_audit.md
    artifacts/md/013_same_size_toggle_control_audit.md
    artifacts/md/014_exhaustive_same_size_triangle_parity_control.md
    artifacts/md/015_zero_odd_metric_sweep.md
    artifacts/md/016_odd_triangle_count_gradient_metric_audit.md

Upstream repaired source:

    Project 18 tag:
    g900-kernel-admission-metric-repair-v1.0.1
