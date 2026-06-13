# First Metric Deformation Status

Project 19 has produced its first finite Thalean gravity test.

The test compares:

- canonical signed carrier graph X_sigma
- untwisted product baseline X_0

using the current Project 18 kernel payload.

## Result

Both graphs have:

- 900 vertices
- 3600 edges
- degree 8 on every vertex

The corrected direct parse of `source/kernel_payload/x_sigma_edges.csv` matches the generated signed graph.

The baseline reconstruction matches the Project 18 baseline certificate exactly.

## Headline metric separation

- signed X_sigma: diameter 8, radius 6
- untwisted X_0: diameter 9, radius 9

This reproduces the paper-level headline separation.

## Pairwise deformation

With

    delta = d_signed - d_baseline

the pairwise deformation distribution is:

- min delta: -6
- max delta: +1
- compressed pairs: 189984
- unchanged pairs: 187930
- expanded pairs: 26636
- mean delta: -0.7233938944506242

This is the first finite gravity signal:

    signed carrier transport produces measurable metric compression relative to the untwisted product baseline.

## Audit boundary

The current Project 18 detailed signed metric certificate does not match the corrected direct parse of the current `x_sigma_edges.csv`.

Observed mismatch:

- Project 19 corrected direct parse:
  - center count 342
  - eccentricity counts {6:342, 7:526, 8:32}
- Project 18 metric certificate:
  - center count 349
  - eccentricity counts {6:349, 7:541, 8:10}

The baseline certificate matches exactly.

Therefore Project 19 proceeds with corrected direct parsing and records the older detailed signed metric certificate as needing regeneration or provenance repair.

## Boundary

This is not a physical gravity claim.

It is a finite graph-theoretic result:

    Signed half-flip carrier transport induces a measurable metric deformation relative to the untwisted product baseline.
