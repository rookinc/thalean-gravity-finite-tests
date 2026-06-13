# Aletheos to Project 18 Edge Comparison

This audit compares Aletheos P900 source artifacts against Project 18 kernel payload edges.

## Phase 17 external comparison

- phase17 external_edge_count_claim: 1800
- phase17 parsed_external_edges: 1800
- project18 external_edges: 1800
- equals_project18_external: False
- missing_from_project18_external: 360
- extra_in_project18_external: 360
- phase17 sha256: `faccc22bf780310a00e28dbb63861169567cb8bddb82a69abc91441c83a71478`
- project18 external sha256: `fb1fb3c90112ce17f788e9be72e7eefd4f03ebecc4fd263ef846310fe06e69b3`
- component_count: 30
- degree_histogram: {'4': 900}
- preferred_half_turn_set: [0, 1, 2, 3, 9]

## Project 18 edge split

- all_edges: 3600
- internal_edges: 1800
- external_edges: 1800
- kind_counts: {'external_signed_carrier': 1800, 'internal_thalion_copy': 1800}
- all_sha256: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`

## Phase 30 candidates

- phase30 top_keys: ['candidates', 'checks', 'first_read', 'name', 'phase', 'purpose', 'renderer_defaults', 'source_artifacts', 'status', 'vertices', 'warning']
- candidate_array_count: 6

### $.candidates[0].combined_edges

- size: 3600
- parsed_edges: 3600
- sha256: `ba1fedeca9ec1156f38103125708f91f5301f3a6331c57bc0a24389e8fcee73a`
- equals_p18_all: True
- equals_p18_external: False
- metric_if_900_graph: {'connected': True, 'edge_count': 3600, 'degree_counts': {8: 900}, 'diameter': 8, 'radius': 6, 'center_count': 342, 'eccentricity_counts': {6: 342, 7: 526, 8: 32}, 'distance_distribution': {1: 3600, 2: 17700, 3: 59941, 4: 129877, 5: 142712, 6: 47600, 7: 3100, 8: 20}}

### $.candidates[0].external_edges

- size: 1800
- parsed_edges: 1800
- sha256: `fb1fb3c90112ce17f788e9be72e7eefd4f03ebecc4fd263ef846310fe06e69b3`
- equals_p18_all: False
- equals_p18_external: True

### $.candidates[0].internal_edges

- size: 1800
- parsed_edges: 1800
- sha256: `5d7e2ac9962e6edf4019d205583e802dd63404a9f285d126eb8d54aa5880b581`
- equals_p18_all: False
- equals_p18_external: False

### $.candidates[1].combined_edges

- size: 3600
- parsed_edges: 3600
- sha256: `38bd570210671fb1bda382cc5c4686e6c587d33abc9778c8a5a65df409650df8`
- equals_p18_all: False
- equals_p18_external: False
- metric_if_900_graph: {'connected': True, 'edge_count': 3600, 'degree_counts': {8: 900}, 'diameter': 8, 'radius': 6, 'center_count': 327, 'eccentricity_counts': {6: 327, 7: 525, 8: 48}, 'distance_distribution': {1: 3600, 2: 17700, 3: 60642, 4: 130810, 5: 142395, 6: 46225, 7: 3144, 8: 34}}

### $.candidates[1].external_edges

- size: 1800
- parsed_edges: 1800
- sha256: `faccc22bf780310a00e28dbb63861169567cb8bddb82a69abc91441c83a71478`
- equals_p18_all: False
- equals_p18_external: False

### $.candidates[1].internal_edges

- size: 1800
- parsed_edges: 1800
- sha256: `5d7e2ac9962e6edf4019d205583e802dd63404a9f285d126eb8d54aa5880b581`
- equals_p18_all: False
- equals_p18_external: False

## Interpretation

- phase17_is_upstream_external_source: False
- full_graph_source_found_in_phase30: True
