# Full Same-Size Metric Sweep Deferred

## Status

The full exhaustive same-size metric sweep was attempted on Termux and deferred.

No physical gravity claim is made. This note records compute scope.

## Attempted audit

The proposed audit was:

    scripts/017_full_same_size_metric_sweep.py

Goal:

    run half-flip return metrics for all C(30,5) = 142506 five-edge carrier-sign toggle sets

The run reached approximately:

    4000 / 142506 variants

with elapsed time approximately:

    888 seconds

Projected full Termux runtime:

    about 8.8 hours

This is too long for the phone workflow.

## Current evidence level

Audit 016 remains the current gradient result.

Audit 016 ran a balanced sample:

    243 variants per odd-triangle-count class

and found the median gradient:

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

## Decision

The full exhaustive metric census is deferred to the Mac or to a later optimized implementation.

Project 19 should not treat the full 142506-variant metric census as completed.

The safe current claim remains:

    In the balanced same-size toggle sample, median half-flip return compression strengthens with odd carrier triangle count, with saturation at the 8 and 10 odd-triangle classes.

## Next recommended paths

Option A:

    move the full 017 metric census to the Mac

Option B:

    optimize 017 before rerunning

Option C:

    keep 016 as the current result and proceed to manuscript-style synthesis
