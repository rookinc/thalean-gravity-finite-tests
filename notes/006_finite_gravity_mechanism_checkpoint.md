# Finite Gravity Mechanism Checkpoint

## Status

Project 19 now has a first finite-graph mechanism for "Thalean gravity."

No physical gravity claim is made. The claim is internal to the repaired finite carrier graph.

## Mechanism chain

The current evidence chain is:

    carrier signs
    -> odd holonomy
    -> half-flip return paths
    -> return-pair metric compression
    -> localization on odd carrier triangles
    -> ablation collapse when odd triangles are neutralized

## Audits

Audit 010 shows that half-flip return compression exists.

    return pairs: 900
    compressed: 294
    unchanged: 606
    expanded: 0

Audit 011 shows that strongest compression localizes exactly on slots incident to odd carrier triangles.

    odd triangle slots:
      [0,1,2,3,4,5,6,7,8,10,14]

    non odd triangle slots:
      [9,11,12,13]

    odd triangle slot mean delta:
      -0.5

    non odd triangle slot mean delta:
      -0.03333333333333333

Audit 012 shows that neutralizing all odd carrier triangles destroys the strong compression profile.

    original:
      compressed_count: 294
      delta_counts: {-3:22, -1:272, 0:606}
      mean_actual_delta: -0.37555555555555553

    triangle neutralized:
      compressed_count: 30
      delta_counts: {-2:22, -1:8, 0:870}
      mean_actual_delta: -0.057777777777777775

## Cautious claim

Odd carrier triangles are causal contributors to the strong half-flip return-compression profile.

This does not yet prove they are the only possible source of compression. Toggling carrier signs also changes larger-cycle holonomy. The safe claim is that the original strong compression profile does not survive the odd-triangle-neutralizing ablation.

## Internal definition

At this stage, "finite Thalean gravity" means:

    carrier-induced metric compression caused by nontrivial return holonomy

More specifically, in the repaired K900 carrier graph:

    odd carrier triangles behave as local holonomy wells

A holonomy well is not a physical gravitational well. It is a finite graph-theoretic site where closed signed transport makes certain returns cheaper than they are in the untwisted baseline.

## Next tests

The next tests should distinguish odd-triangle causality from generic sign-toggle disturbance.

Recommended next audit:

    same-size toggle controls

Compare the odd-triangle-neutralizing toggle set against other five-edge carrier sign toggles. The question is whether the observed collapse of strong compression is specific to triangle neutralization or typical of any five sign changes.

