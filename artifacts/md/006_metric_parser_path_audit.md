# Metric Parser Path Audit

This audit compares three ways of reading Project 18 `x_sigma_edges.csv`.

## Edge counts

- correct_direct: 3600
- slot_local_named: 3600
- project18_metric_style: 56
- project18_metric_style_skipped_rows: 3544

## Hashes

- correct_direct: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`
- slot_local_named: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`
- project18_metric_style: `ebcce58c2a8aa90ba4b0fd918f6292a7be72f5a348c7debc32f467f0c65fb88f`
- certificate_source_edge_id_set_sha256: `982fa358aa4a6d76000e62a3abde3ff3e2ce06af179ab131030eec923d05877d`

## Edge-set equalities

- correct_direct_equals_slot_local_named: True
- correct_direct_equals_project18_metric_style: False

## Certificate match

- correct_direct: False
- project18_metric_style: False

## Correct direct metric

- diameter: 8
- radius: 6
- center_count: 342
- eccentricity_counts: {6: 342, 7: 526, 8: 32}
- distance_distribution: {1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}

## Project 18 metric-style parse

- connected: False
- edge_count: None
- degree_counts: {0: 829, 1: 56, 2: 1, 3: 2, 4: 12}
- diameter: None
- radius: None
- center_count: None
- eccentricity_counts: None
- distance_distribution: None

## Skip examples

- {'reason': 'bounds_fail', 'row': {'u_vertex': '0', 'v_vertex': '90', 'u_slot': '0', 'u_local': '0', 'v_slot': '1', 'v_local': '30', 'kind': 'external_signed_carrier'}, 'xs4': [0, 90, 0, 0]}
- {'reason': 'bounds_fail', 'row': {'u_vertex': '0', 'v_vertex': '270', 'u_slot': '0', 'u_local': '0', 'v_slot': '4', 'v_local': '30', 'kind': 'external_signed_carrier'}, 'xs4': [0, 270, 0, 0]}
- {'reason': 'bounds_fail', 'row': {'u_vertex': '0', 'v_vertex': '330', 'u_slot': '0', 'u_local': '0', 'v_slot': '5', 'v_local': '30', 'kind': 'external_signed_carrier'}, 'xs4': [0, 330, 0, 0]}
- {'reason': 'bounds_fail', 'row': {'u_vertex': '0', 'v_vertex': '390', 'u_slot': '0', 'u_local': '0', 'v_slot': '6', 'v_local': '30', 'kind': 'external_signed_carrier'}, 'xs4': [0, 390, 0, 0]}
- {'reason': 'bounds_fail', 'row': {'u_vertex': '1', 'v_vertex': '91', 'u_slot': '0', 'u_local': '1', 'v_slot': '1', 'v_local': '31', 'kind': 'external_signed_carrier'}, 'xs4': [1, 91, 0, 1]}
- {'reason': 'bounds_fail', 'row': {'u_vertex': '1', 'v_vertex': '271', 'u_slot': '0', 'u_local': '1', 'v_slot': '4', 'v_local': '31', 'kind': 'external_signed_carrier'}, 'xs4': [1, 271, 0, 1]}
- {'reason': 'bounds_fail', 'row': {'u_vertex': '1', 'v_vertex': '331', 'u_slot': '0', 'u_local': '1', 'v_slot': '5', 'v_local': '31', 'kind': 'external_signed_carrier'}, 'xs4': [1, 331, 0, 1]}
- {'reason': 'bounds_fail', 'row': {'u_vertex': '1', 'v_vertex': '391', 'u_slot': '0', 'u_local': '1', 'v_slot': '6', 'v_local': '31', 'kind': 'external_signed_carrier'}, 'xs4': [1, 391, 0, 1]}

## Interpretation

If `correct_direct` fails to match the old certificate while the source edge file is correct, Project 19 should proceed with corrected direct parsing and record the Project 18 detailed metric certificate as needing regeneration.
