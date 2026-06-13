# Metric Deformation Test

This is the first finite Thalean gravity test.

It compares the canonical signed carrier graph X_sigma against the untwisted product baseline X_0.

No physical gravity claim is made here. The tested claim is finite and graph-theoretic: signed carrier transport induces a measurable metric deformation.

## Edge checks

- generated_signed_edges: 3600
- source_signed_edges: 3600
- source_parse_mode: numeric_pair:u_vertex,v_vertex
- generated_matches_source: True
- baseline_edges: 3600
- signed_degree_counts: {8: 900}
- baseline_degree_counts: {8: 900}

## Metric summaries

### signed_metric

- diameter: 8
- radius: 6
- center_count: 342
- eccentricity_counts: {6: 342, 7: 526, 8: 32}
- distance_distribution: {1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}

### baseline_metric

- diameter: 9
- radius: 9
- center_count: 900
- eccentricity_counts: {9: 900}
- distance_distribution: {1: 3600, 2: 14400, 3: 36900, 4: 72000, 5: 110700, 6: 112050, 7: 45000, 8: 9000, 9: 900}

## Deformation summary

- pair_count: 404550
- delta_counts: {-6: 114, -5: 174, -4: 6272, -3: 20295, -2: 68629, -1: 94500, 0: 187930, 1: 26636}
- mean_delta: -0.7233938944506242
- compressed_pair_count: 189984
- unchanged_pair_count: 187930
- expanded_pair_count: 26636
- min_delta: -6
- max_delta: 1

## Interpretation

- The generated signed graph matches the source X_sigma edge file.
- A negative delta means the signed carrier graph shortens a pairwise distance relative to the untwisted baseline.
- A positive delta means the signed carrier graph lengthens a pairwise distance relative to the untwisted baseline.
- The finite gravity signal is the organized deformation field d_signed - d_baseline.

## Output files

- artifacts/json/003_metric_deformation_summary.json
- artifacts/csv/003_delta_distribution.csv
- artifacts/csv/003_extreme_pairs.csv
