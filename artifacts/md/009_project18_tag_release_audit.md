# Project 18 Tag/Release Audit

This audit compares Project 18 HEAD and release refs without checking out or modifying Project 18.

## Current Project 18 git state

- head: ok=True stdout=`f69f6e0` stderr=``
- branch: ok=True stdout=`main` stderr=``
- tags_at_head: ok=True stdout=`g900-kernel-admission-manuscript-v1.0.0` stderr=``
- status_short: ok=True stdout=`?? artifacts/png/g900_spring_graph_dark.png
?? artifacts/png/g900_spring_graph_noscipy.png` stderr=``

## Ref comparisons

### HEAD

- rev_parse_ok: True
- rev: `f69f6e0`
- edge_file_ok: True
- cert_file_ok: True
- edge_headers: ['u_vertex', 'v_vertex', 'u_slot', 'u_local', 'v_slot', 'v_local', 'kind']
- edge_count: 3600
- edge_sha256: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`
- edge_metric_matches_certificate: False

Edge-file metric:
- connected: True
- diameter: 8
- radius: 6
- center_count: 342
- eccentricity_counts: {6: 342, 7: 526, 8: 32}
- distance_distribution: {1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}

Certificate metric:
- diameter: 8
- radius: 6
- center_count: 349
- eccentricity_counts: {6: 349, 7: 541, 8: 10}
- distance_distribution: {1: 3600, 2: 17710, 3: 60345, 4: 131446, 5: 143177, 6: 45600, 7: 2667, 8: 5}
- hashes: {'source_edge_id_set_sha256': '982fa358aa4a6d76000e62a3abde3ff3e2ce06af179ab131030eec923d05877d'}

### g900-kernel-admission-manuscript-v1.0.0

- rev_parse_ok: True
- rev: `10e1430`
- edge_file_ok: True
- cert_file_ok: True
- edge_headers: ['u_vertex', 'v_vertex', 'u_slot', 'u_local', 'v_slot', 'v_local', 'kind']
- edge_count: 3600
- edge_sha256: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`
- edge_metric_matches_certificate: False

Edge-file metric:
- connected: True
- diameter: 8
- radius: 6
- center_count: 342
- eccentricity_counts: {6: 342, 7: 526, 8: 32}
- distance_distribution: {1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}

Certificate metric:
- diameter: 8
- radius: 6
- center_count: 349
- eccentricity_counts: {6: 349, 7: 541, 8: 10}
- distance_distribution: {1: 3600, 2: 17710, 3: 60345, 4: 131446, 5: 143177, 6: 45600, 7: 2667, 8: 5}
- hashes: {'source_edge_id_set_sha256': '982fa358aa4a6d76000e62a3abde3ff3e2ce06af179ab131030eec923d05877d'}

### g900-kernel-admission-bounded-qed-v1.0.0

- rev_parse_ok: True
- rev: `222c13a`
- edge_file_ok: True
- cert_file_ok: True
- edge_headers: ['u_vertex', 'v_vertex', 'u_slot', 'u_local', 'v_slot', 'v_local', 'kind']
- edge_count: 3600
- edge_sha256: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`
- edge_metric_matches_certificate: False

Edge-file metric:
- connected: True
- diameter: 8
- radius: 6
- center_count: 342
- eccentricity_counts: {6: 342, 7: 526, 8: 32}
- distance_distribution: {1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}

Certificate metric:
- diameter: 8
- radius: 6
- center_count: 349
- eccentricity_counts: {6: 349, 7: 541, 8: 10}
- distance_distribution: {1: 3600, 2: 17710, 3: 60345, 4: 131446, 5: 143177, 6: 45600, 7: 2667, 8: 5}
- hashes: {'source_edge_id_set_sha256': '982fa358aa4a6d76000e62a3abde3ff3e2ce06af179ab131030eec923d05877d'}

### 138dc5c

- rev_parse_ok: True
- rev: `138dc5c`
- edge_file_ok: True
- cert_file_ok: True
- edge_headers: ['u_vertex', 'v_vertex', 'u_slot', 'u_local', 'v_slot', 'v_local', 'kind']
- edge_count: 3600
- edge_sha256: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`
- edge_metric_matches_certificate: False

Edge-file metric:
- connected: True
- diameter: 8
- radius: 6
- center_count: 342
- eccentricity_counts: {6: 342, 7: 526, 8: 32}
- distance_distribution: {1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}

Certificate metric:
- diameter: 8
- radius: 6
- center_count: 349
- eccentricity_counts: {6: 349, 7: 541, 8: 10}
- distance_distribution: {1: 3600, 2: 17710, 3: 60345, 4: 131446, 5: 143177, 6: 45600, 7: 2667, 8: 5}
- hashes: {'source_edge_id_set_sha256': '982fa358aa4a6d76000e62a3abde3ff3e2ce06af179ab131030eec923d05877d'}

## Interpretation

If the bounded-QED tag exists and its edge-file metric matches its certificate, then the paper release is internally consistent and Project 19 should cite that release separately from local HEAD.
If the bounded-QED tag does not exist locally, fetch tags or inspect the remote before making a stronger claim.
