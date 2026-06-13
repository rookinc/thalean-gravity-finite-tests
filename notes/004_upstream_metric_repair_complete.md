# Upstream Metric Repair Complete

Project 18 has been repaired, merged to main, pushed, and tagged.

Upstream repaired tag:

    g900-kernel-admission-metric-repair-v1.0.1

Repair commit on Project 18 main:

    85d5027

The repair corrected the metric certificate parser so `source/kernel_payload/x_sigma_edges.csv` is read through the explicit `u_vertex,v_vertex` columns.

The corrected canonical metric is:

- diameter: 8
- radius: 6
- center_count: 342
- eccentricity_counts: {6:342, 7:526, 8:32}
- distance_distribution: {1:3600, 2:17700, 3:59941, 4:129877, 5:142712, 6:47600, 7:3100, 8:20}

The headline separation remains:

- canonical signed graph: diameter/radius 8/6
- untwisted baseline: diameter/radius 9/9

Project 19 can now treat the corrected metric profile as the repaired upstream certificate state.
