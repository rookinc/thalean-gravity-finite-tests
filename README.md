# 19 - Thalean Gravity Finite Tests

This project tests a bounded internal claim:

Signed carrier transport in the K900 construction induces a finite metric deformation relative to controlled baselines.

This is not a physical gravity claim. It is a finite graph-theoretic test program tied to the kernel-admission theorem for the 900-vertex Thalean ring candidate.

Initial target:

Does the signed half-flip carrier law create stable, nontrivial, measurable metric deformation relative to the untwisted product baseline?

Primary test language:

- local carrier law
- metric deformation
- finite holonomy
- switching class
- baseline separation
- geodesic bending
- registered trace

Core expected comparison:

- canonical signed graph X_sigma
- untwisted product baseline X_0
- sibling signing graph
- random/sign-shuffled controls
- switch-equivalent controls

Public boundary:

This project does not assert physical gravity, GR, Newtonian gravity, or cosmological mechanism. It tests a finite gravity-like closure mechanism inside the admitted G900 kernel.

## First finite gravity test

The first test compares the canonical signed carrier graph `X_sigma` against the untwisted product baseline `X_0`.

Current local result from corrected direct parsing of Project 18 payload:

- signed graph edges: 3600
- baseline graph edges: 3600
- signed degree counts: 8 on 900 vertices
- baseline degree counts: 8 on 900 vertices
- signed diameter/radius: 8 / 6
- baseline diameter/radius: 9 / 9
- pairwise deformation count:
  - compressed pairs: 189984
  - unchanged pairs: 187930
  - expanded pairs: 26636
  - mean delta: -0.7233938944506242

Here delta means:

    delta = d_signed - d_baseline

Negative delta means the signed carrier graph shortens distance relative to the untwisted product baseline.

## Certificate boundary

Project 19 does not silently inherit every detailed Project 18 metric count.

The corrected direct parse of the current Project 18 `x_sigma_edges.csv` reproduces the headline theorem separation, but its detailed signed metric profile differs from the older Project 18 metric certificate.

Project 19 therefore treats the old Project 18 detailed signed metric certificate as requiring regeneration or provenance repair before it is used as a detailed metric source.

The safe Project 19 claim is:

Signed half-flip carrier transport induces a finite, measurable metric deformation relative to the untwisted product baseline, with reproduced headline separation 8/6 versus 9/9 on the current source payload.

No physical gravity, GR, Newtonian, cosmological, uniqueness, or census-identity claim is made.

## Project 18 metric certificate audit

Project 19 audited the Project 18 source edge file against the Project 18 metric certificate across HEAD, the manuscript tag, the bounded-QED tag, and commit 138dc5c.

The source edge file consistently recomputes to diameter 8 and radius 6, preserving the headline separation from the untwisted baseline. However, the detailed signed metric distribution recomputed from the source edge file does not match the existing Project 18 metric certificate.

Project 19 therefore treats the detailed Project 18 signed metric certificate as needing regeneration or provenance repair. The safe Project 19 result is the corrected-direct metric deformation audit on the current source edge file.
