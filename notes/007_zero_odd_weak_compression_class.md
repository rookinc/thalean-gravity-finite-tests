# Zero-Odd Weak Compression Class

## Status

Working finite-graph mechanism result, supported by audits 010 through 015.

No physical gravity claim is made. This note concerns finite signed carrier holonomy and graph metric deformation.

## Core result

In the tested same-size carrier-sign control regime, erasing all odd carrier triangles uniformly moves the system into a weak half-flip return-compression class.

The original repaired `K900` carrier graph has odd carrier triangles and a strong return-compression profile.

The zero-odd class consists of all same-size five-edge carrier-sign toggle sets that erase every odd carrier triangle.

Audit 015 shows that every member of this zero-odd class is weaker than the original.

## Original profile

The original repaired carrier graph has:

    odd_triangle_count: 5
    compressed_count: 294
    expanded_count: 0
    mean_actual_delta: -0.37555555555555553
    delta_counts: {-3:22, -1:272, 0:606}

Here:

    actual_delta = signed_distance - baseline_distance

Negative actual delta means the signed carrier graph shortens the half-flip return pair relative to the untwisted baseline.

## Zero-odd class

Audit 014 found:

    total same-size five-edge toggle sets: 142506
    zero-odd toggle sets: 243
    zero-odd fraction: 0.0017051913603637742

So the zero-odd class is rare within the same-size toggle control space.

Audit 015 then ran metric tests on all 243 zero-odd members.

The zero-odd class has:

    compressed_count range: 22 to 30
    median compressed_count: 30
    mean compressed_count: 29.62962962962963

    mean_actual_delta range: -0.057777777777777775 to -0.04888888888888889
    median mean_actual_delta: -0.057777777777777775
    class mean_actual_delta: -0.05736625514403292

    expanded_count: 0 for every zero-odd member

## Checks

Audit 015 verifies:

    all_zero_odd_have_no_expansion: True
    neutralizer_found: True
    zero_odd_class_is_weak_vs_original_median: True
    all_zero_odd_weaker_than_original: True

## Mechanism statement

Odd carrier triangle holonomy is a necessary condition for the original strong half-flip return-compression class within the tested same-size control regime.

This is stronger than saying odd triangles are correlated with compression.

The current evidence chain is:

    carrier signs
    -> odd carrier triangle holonomy
    -> short half-flip return access
    -> strong return-pair metric compression

and the ablation chain is:

    erase all odd carrier triangles
    -> enter rare zero-odd parity class
    -> strong return-compression profile collapses
    -> every zero-odd member is weak compared to the original

## Caution

This does not yet prove that odd carrier triangles are sufficient by themselves to recreate the original strong profile.

It also does not claim that larger odd cycles are irrelevant.

The safe result is:

    In this repaired K900 control regime, the strong half-flip return-compression profile does not survive when all odd carrier triangles are erased.

## Internal definition update

At this stage, finite Thalean gravity can be stated more sharply:

    finite Thalean gravity = carrier-induced metric compression organized by nontrivial return holonomy

The first detected local organizers are:

    odd carrier triangles

These behave as finite holonomy wells: sites where closed signed transport makes certain returns cheaper than they are in the untwisted baseline.

## Dependency trail

Primary support:

    artifacts/md/010_holonomy_return_compression_audit.md
    artifacts/md/011_odd_triangle_localization_audit.md
    artifacts/md/012_odd_triangle_ablation_audit.md
    artifacts/md/013_same_size_toggle_control_audit.md
    artifacts/md/014_exhaustive_same_size_triangle_parity_control.md
    artifacts/md/015_zero_odd_metric_sweep.md

Upstream repaired source:

    Project 18 tag:
    g900-kernel-admission-metric-repair-v1.0.1
