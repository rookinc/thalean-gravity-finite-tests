# Project 18 Metric Certificate Mismatch

Project 19 audited the Project 18 G900 kernel-admission payload against the Project 18 metric certificate.

## Result

The current Project 18 source edge file:

    source/kernel_payload/x_sigma_edges.csv

is stable across the checked refs:

- HEAD
- g900-kernel-admission-manuscript-v1.0.0
- g900-kernel-admission-bounded-qed-v1.0.0
- commit 138dc5c

The edge file has:

- 3600 edges
- connected graph
- diameter 8
- radius 6

This preserves the headline signed-vs-baseline separation used by Project 19.

## Mismatch

The metric recomputed directly from `u_vertex,v_vertex` in the edge file gives:

- center_count: 342
- eccentricity_counts: {6:342, 7:526, 8:32}
- distance_distribution: {1:3600, 2:17700, 3:59941, 4:129877, 5:142712, 6:47600, 7:3100, 8:20}

The existing Project 18 metric certificate reports:

- center_count: 349
- eccentricity_counts: {6:349, 7:541, 8:10}
- distance_distribution: {1:3600, 2:17710, 3:60345, 4:131446, 5:143177, 6:45600, 7:2667, 8:5}

Therefore the existing detailed metric certificate is not synchronized with the source edge file.

## Baseline

The untwisted baseline certificate matches the Project 19 reconstruction exactly:

- diameter 9
- radius 9
- center_count 900
- eccentricity_counts {9:900}
- matching distance distribution

## Aletheos provenance

Aletheos Phase 30 candidate 0 matches the Project 18 full graph exactly.

Aletheos Phase 30 candidate 1 matches the sibling-style metric profile.

Aletheos Phase 17 external edge list does not match the Project 18 canonical external edge set. Phase 17 appears to correspond to a different candidate/source stage.

## Safe Project 19 claim

Project 19 may safely claim:

    The signed carrier graph represented by the current Project 18 edge file produces a finite metric deformation relative to the untwisted product baseline, with headline separation 8/6 versus 9/9.

Project 19 should not claim the old Project 18 detailed metric distribution as canonical until Project 18 regenerates or repairs its metric certificate.

## Boundary

This is not a physical gravity claim. It is a finite graph-theoretic audit of carrier-induced metric deformation.
