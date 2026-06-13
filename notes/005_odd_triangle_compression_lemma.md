# Odd Triangle Compression Lemma

## Status

Working finite-graph lemma, supported by audits 010 and 011.

No physical gravity claim is made. This is a finite graph-theoretic statement about signed carrier holonomy and graph metric deformation.

## Setup

Let `X_sigma` be the repaired 900-vertex signed carrier graph from Project 18, and let `X_0` be the untwisted baseline graph with the same local fibers and slot adjacency but without the signed half-flip carrier law.

A half-flip return pair is a pair of vertices of the form:

    (slot, x) -> (slot, x + 30)

where the second coordinate is taken modulo 60.

An odd carrier cycle is a closed slot cycle whose carrier signs sum to 1 modulo 2. Transport around such a cycle returns to the starting slot with the local coordinate half-flipped.

An odd carrier triangle is an odd carrier cycle of length 3.

## Lemma

In the repaired `K900` carrier graph, the strongest half-flip return compression is localized exactly on slots incident to odd carrier triangles.

More explicitly:

1. Every slot incident to an odd carrier triangle has best odd holonomy cycle length 3.

2. Every slot not incident to an odd carrier triangle has best odd holonomy cycle length 5.

3. Half-flip return pairs never expand relative to the untwisted baseline.

4. Slots incident to odd carrier triangles form the strong return-compression class.

5. Slots not incident to odd carrier triangles form the weak return-compression class.

## Witness data

The odd carrier triangles are:

    [0, 1, 6]
    [0, 4, 5]
    [1, 2, 7]
    [2, 3, 8]
    [5, 10, 14]

The odd-triangle slots are:

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 14]

The non-odd-triangle slots are:

    [9, 11, 12, 13]

Aggregate compression by slot class:

    odd triangle slots:
      count: 660
      mean_actual_delta: -0.5
      delta_counts: {-3:22, -1:264, 0:374}

    non odd triangle slots:
      count: 240
      mean_actual_delta: -0.03333333333333333
      delta_counts: {-1:8, 0:232}

Here:

    actual_delta = signed_distance - baseline_distance

Negative actual delta means the signed carrier graph shortens the half-flip return pair relative to the untwisted baseline.

## Checks

Audit 011 verifies:

    all_odd_triangle_slots_have_best_odd_len_3: True
    no_non_odd_triangle_slot_has_best_odd_len_3: True
    no_return_pair_expansion: True
    odd_triangle_slots_more_compressive_than_non_odd_triangle_slots: True

## Interpretation

Odd carrier triangles act as local holonomy wells.

They are not gravitational wells in the physical sense. They are finite graph-theoretic sites where closed signed transport creates shorter return geometry.

This gives the first clean internal meaning of "Thalean gravity" in Project 19:

    finite gravity = carrier-induced metric compression caused by nontrivial return holonomy.

In this sense, the carrier law does not merely decorate the graph. It changes the metric by making some returns cheaper than they are in the untwisted baseline.

## Dependency trail

Primary support:

    artifacts/md/010_holonomy_return_compression_audit.md
    artifacts/json/010_holonomy_return_compression_audit.json
    artifacts/csv/010_holonomy_return_pairs.csv

    artifacts/md/011_odd_triangle_localization_audit.md
    artifacts/json/011_odd_triangle_localization_audit.json
    artifacts/csv/011_slot_triangle_compression.csv

Upstream repaired source:

    Project 18 tag:
    g900-kernel-admission-metric-repair-v1.0.1
