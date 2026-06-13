# Aletheos Source Probe

aletheos_root: `/data/data/com.termux/files/home/dev/cori/aletheos.ai`
exists: `True`

## Counts

- interesting_files: 34
- json_files: 14
- text_hit_files: 32

## Interesting files

- `public_html/json/p900/manifest.json` (1486 bytes)
- `public_html/json/p900/p900_phase13_candidate_orbit_families.json` (4239 bytes)
- `public_html/json/p900/p900_phase15_local_balance_score.json` (4650 bytes)
- `public_html/json/p900/p900_phase16_preferred_representative_edge_law.json` (10114 bytes)
- `public_html/json/p900/p900_phase17_external_edge_list.json` (181689 bytes)
- `public_html/json/p900/p900_phase18_component_structure.json` (71404 bytes)
- `public_html/json/p900/p900_phase19_doubled_g15_sheet_audit.json` (92739 bytes)
- `public_html/json/p900/p900_phase20_checkpoint_summary.json` (3841 bytes)
- `public_html/json/p900/p900_phase30_combined_graph_export.json` (5595831 bytes)
- `public_html/json/p900/p900_stub_summary.json` (530 bytes)
- `public_html/labs/constructor/kernel/p900_external_renderer.js` (7404 bytes)
- `public_html/labs/p900_observatory/kernel/camera.js` (1305 bytes)
- `public_html/labs/p900_observatory/kernel/local_storage_lenses.js` (4368 bytes)
- `public_html/labs/p900_observatory/kernel/p900_data.js` (5196 bytes)
- `public_html/labs/p900_observatory/kernel/p900_geometry.js` (2446 bytes)
- `public_html/labs/p900_observatory/kernel/renderer.js` (4601 bytes)
- `public_html/labs/g900_admission/kernel/g900_data.js` (4168 bytes)
- `public_html/labs/g900_admission/kernel/renderer.js` (3858 bytes)
- `notes/900conjecture.md` (3892 bytes)
- `notes/900conjecture_v2.md` (5553 bytes)
- `notes/lift_signed_mode_bridge_note.md` (6963 bytes)
- `notes/p900_camera_defaults_autorotate.md` (449 bytes)
- `notes/p900_external_overdrive.md` (584 bytes)
- `notes/p900_external_play_reveal.md` (465 bytes)
- `notes/p900_external_render_mode.md` (464 bytes)
- `notes/p900_lab_boot_syntax_fix.md` (307 bytes)
- `notes/p900_public_json_bridge.md` (511 bytes)
- `notes/p900_start_view_autorotate_off.md` (387 bytes)
- `notes/p900_yaw_11_clear_stage_text.md` (276 bytes)
- `notes/remove_exact_p900_canvas_text.md` (301 bytes)
- `reports/derived/edge_column_assignment.json` (6345 bytes)
- `reports/derived/edge_column_signatures.json` (42968 bytes)
- `reports/derived/edge_column_signatures_colored.json` (113588 bytes)
- `reports/overlap9_graph.json` (5623 bytes)

## JSON summaries

### public_html/json/p900/manifest.json

- bytes: 1486
- sha256: `631f181cde39ae64f7d655746f1c3de71b05ef7a22e6af30a23da55339f22df3`
- ok: True
- type: dict
- size: 10
- keys: ['do_not_claim_yet', 'files', 'generated_utc', 'name', 'primary_renderer_inputs', 'public_path', 'source_repo', 'status', 'strongest_current_statement', 'warning']
- candidate_arrays:
  - key: do_not_claim_yet
    size: 5
    sample_types: ['str', 'str', 'str']
    sample: ['P900 is a fully constructed thalion-cluster graph.', 'The preferred representative is the final P900 law.']
  - key: files
    size: 8
    sample_types: ['str', 'str', 'str']
    sample: ['p900_stub_summary.json', 'p900_phase13_candidate_orbit_families.json']

### public_html/json/p900/p900_phase13_candidate_orbit_families.json

- bytes: 4239
- sha256: `ce805e14a5c37a1b5cf95b99567be0dd19cf6a98fdd9e3ca0b4911b1551cf818`
- ok: True
- type: dict
- size: 12
- keys: ['best_balance_gap', 'candidate_families', 'candidate_family_count', 'demoted_baseline', 'generated_utc', 'name', 'next_tests', 'selection_rule', 'source', 'status', 'warning', 'working_position']
- candidate_arrays:
  - key: candidate_families
    size: 2
    sample_types: ['dict', 'dict']
    sample: [{'edge_label_counts': {'half_turn': 15, 'identity': 15}, 'family_id': 'gap1_orbit_1', 'half_turn_closure_count': 279, 'identity_closure_count': 278, 'identity_half_turn_balance_gap': 1, 'orbit_size': 60, 'orientation_drift_count': 0, 'representative_half_turn_set': [0, 1, 2, 3, 5], 'sample_sets': [[0, 1, 2, 3, 5], [0, 1, 2, 3, 8], [0, 1, 2, 4, 7], [0, 1, 2, 4, 9], [0, 1, 2, 5, 8], [0, 1, 2, 7, 9], [0, 1, 3, 4, 6], [0, 1, 3, 4, 8], [0, 1, 3, 5, 8
  - key: next_tests
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['choose one representative from each gap-1 orbit and build explicit edge-law tables', 'compare orbit 1 and orbit 2 cycle length closure profiles']
  - key: working_position
    size: 5
    sample_types: ['str', 'str', 'str']
    sample: ['P900 binary consonance is currently best treated as an orbit-family problem.', 'The preferred candidates are the two Petersen split orbits with balance gap 1.']

### public_html/json/p900/p900_phase15_local_balance_score.json

- bytes: 4650
- sha256: `f84a9f55aa295e51f4416afc4248e3ed3266655ced82d5beb08746b71ee58b37`
- ok: True
- type: dict
- size: 9
- keys: ['first_read', 'name', 'preferred_by_local_balance', 'ranked_families', 'ranking_rule', 'scoring_rule', 'source', 'status', 'warning']
- candidate_arrays:
  - key: first_read
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['Both preferred orbit representatives remain tied at total balance gap 1 with zero drift.', 'Phase 15 breaks the tie using local balance by cycle length.']
  - key: ranked_families
    size: 2
    sample_types: ['dict', 'dict']
    sample: [{'family': 'gap1_orbit_2_representative', 'half_turn_set': [0, 1, 2, 3, 9], 'local_balance_score': 13, 'max_length_gap': 7, 'per_length_scores': {'3': {'half_turn_closure': 5, 'identity_closure': 5, 'length_balance_gap': 0, 'orientation_drift': 0}, '5': {'half_turn_closure': 6, 'identity_closure': 6, 'length_balance_gap': 0, 'orientation_drift': 0}, '6': {'half_turn_closure': 32, 'identity_closure': 38, 'length_balance_gap': 6, 'orientation_drif
  - key: ranking_rule
    size: 5
    sample_types: ['str', 'str', 'str']
    sample: ['minimize orientation drift', 'minimize total identity/half-turn balance gap']

### public_html/json/p900/p900_phase16_preferred_representative_edge_law.json

- bytes: 10114
- sha256: `a76402a881cb2bfa5c4a5556688570d69e247f04a824901efe5c30f213e267e1`
- ok: True
- type: dict
- size: 16
- keys: ['edge_label_counts', 'edge_records', 'g15_edges', 'generated_utc', 'name', 'next_tests', 'phase15_support', 'preferred_family', 'preferred_half_turn_set', 'preferred_identity_set', 'rule', 'source', 'status', 'surface_counts', 'warning', 'working_position']
- candidate_arrays:
  - key: edge_records
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'g15_edge': [0, 1], 'interface_label': 'half_turn', 'petersen_edge_a': [0, 1], 'petersen_edge_b': [1, 2], 'shared_petersen_vertex': 1, 'shift_mod_60': 30}, {'g15_edge': [0, 4], 'interface_label': 'half_turn', 'petersen_edge_a': [0, 1], 'petersen_edge_b': [4, 0], 'shared_petersen_vertex': 0, 'shift_mod_60': 30}]
  - key: next_tests
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['build explicit P900 external edge list for this representative', 'audit connectedness and degree distribution of the external-only surface']
  - key: preferred_half_turn_set
    size: 5
    sample_types: ['int', 'int', 'int']
    sample: [0, 1]
  - key: preferred_identity_set
    size: 5
    sample_types: ['int', 'int', 'int']
    sample: [4, 5]
  - key: working_position
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['This representative is selected from one of the two best gap-1 Petersen split orbits.', 'It is preferred over the other tested representative by local balance score.']

### public_html/json/p900/p900_phase17_external_edge_list.json

- bytes: 181689
- sha256: `0b7f1d238a978a3f38b8350bb7092191fb9c307e05a8831837e83109930adfed`
- ok: True
- type: dict
- size: 14
- keys: ['component_count', 'component_sizes', 'connected', 'degree_histogram', 'external_edge_count', 'external_edges', 'first_read', 'name', 'p900_vertex_count', 'preferred_family', 'preferred_half_turn_set', 'source', 'status', 'warning']
- candidate_arrays:
  - key: component_sizes
    size: 30
    sample_types: ['int', 'int', 'int']
    sample: [30, 30]
  - key: external_edges
    size: 1800
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'a': [0, 0], 'b': [1, 30]}, {'a': [0, 1], 'b': [1, 31]}]
  - key: first_read
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['The preferred representative external law materializes as 1800 inter-thalion edges.', 'Each P900 state has external degree 4.']
  - key: preferred_half_turn_set
    size: 5
    sample_types: ['int', 'int', 'int']
    sample: [0, 1]

### public_html/json/p900/p900_phase18_component_structure.json

- bytes: 71404
- sha256: `8360741e6a17ee4efbf9ea928e9267d35121647ab3e22d9272ae8a430be2ea0a`
- ok: True
- type: dict
- size: 14
- keys: ['all_components_have_15_sectors', 'all_components_single_mod30_residue', 'all_components_size_30', 'all_components_two_per_sector', 'component_count', 'component_records', 'component_size_histogram', 'first_read', 'local_residue_mod_30_count_histogram', 'name', 'sector_count_pattern_histogram', 'source', 'status', 'warning']
- candidate_arrays:
  - key: component_records
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'component_index': 0, 'local_max': 30, 'local_min': 0, 'local_parity_counts': {'0': 30}, 'local_residue_mod_30_count': 1, 'local_residues_mod_30': [0], 'local_values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30], 'members': [[0, 0], [0, 30], [1, 0], [1, 30], [2, 0], [2, 30], [3, 0], [3, 30], [4, 0], [4, 30], [5, 0], [5, 30], [6, 0], [6, 30], [7, 0], [7, 30], [8, 0], [8, 30], [9, 0], 
  - key: first_read
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['The external-only P900 surface decomposes into 30 equal components.', 'Each component should be checked for sector coverage and local-index organization.']

### public_html/json/p900/p900_phase19_doubled_g15_sheet_audit.json

- bytes: 92739
- sha256: `d322d24da9f534ced9110befc5f98fd538bd8d64b6d485eeae7172d08c3fd5db`
- ok: True
- type: dict
- size: 14
- keys: ['all_sheets_2_lifts_of_g15', 'all_sheets_4_regular', 'all_sheets_have_60_edges', 'all_sheets_same_type', 'first_read', 'name', 'preferred_half_turn_set', 'preferred_identity_set', 'sheet_count', 'sheet_records', 'sheet_type_histogram', 'source', 'status', 'warning']
- candidate_arrays:
  - key: first_read
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['Each Phase 18 component is a doubled G15 sheet indexed by one residue mod 30.', 'Within a sheet, shift 0 gives parallel edges between the two bit layers.']
  - key: preferred_half_turn_set
    size: 5
    sample_types: ['int', 'int', 'int']
    sample: [0, 1]
  - key: preferred_identity_set
    size: 5
    sample_types: ['int', 'int', 'int']
    sample: [4, 5]
  - key: sheet_records
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'bit_edge_counts': {'cross': 15, 'parallel': 15}, 'degree_histogram': {'4': 30}, 'edge_count': 60, 'is_2_lift_of_g15': True, 'sample_edges': [{'a': [0, 0], 'b': [1, 1]}, {'a': [0, 1], 'b': [1, 0]}, {'a': [0, 0], 'b': [4, 1]}, {'a': [0, 1], 'b': [4, 0]}, {'a': [0, 0], 'b': [5, 1]}, {'a': [0, 1], 'b': [5, 0]}, {'a': [0, 0], 'b': [6, 1]}, {'a': [0, 1], 'b': [6, 0]}, {'a': [1, 0], 'b': [2, 1]}, {'a': [1, 1], 'b': [2, 0]}, {'a': [1, 0], 'b': [6, 1]}
  - key: source
    size: 3
    sample_types: ['str', 'str', 'str']
    sample: ['p900_phase16_preferred_representative_edge_law.json', 'p900_phase17_external_edge_list.json']

### public_html/json/p900/p900_phase20_checkpoint_summary.json

- bytes: 3841
- sha256: `b774815cf0a7b0070530b65d8a1302f9781fb6327d636beb1065d83f5f33b005`
- ok: True
- type: dict
- size: 11
- keys: ['checkpoint_ok', 'checks', 'current_claim_ladder', 'do_not_claim_yet', 'generated_utc', 'key_artifacts', 'name', 'next_steps', 'numeric_summary', 'status', 'warning']
- candidate_arrays:
  - key: current_claim_ladder
    size: 11
    sample_types: ['str', 'str', 'str']
    sample: ['P900 is currently treated as a candidate consonance surface, not a proven graph identity.', 'The address space is 15 x 60 = 900 states.']
  - key: do_not_claim_yet
    size: 5
    sample_types: ['str', 'str', 'str']
    sample: ['Do not claim P900 is a fully constructed thalion-cluster graph.', 'Do not claim the preferred representative is the final P900 law.']
  - key: next_steps
    size: 5
    sample_types: ['str', 'str', 'str']
    sample: ['write a README checkpoint section', 'prepare internal G60 import strategy']

### public_html/json/p900/p900_phase30_combined_graph_export.json

- bytes: 5595831
- sha256: `609720792931d5e90fb9d49d12fd2c5390e02afcc1a19976fd95c119ae95d900`
- ok: True
- type: dict
- size: 11
- keys: ['candidates', 'checks', 'first_read', 'name', 'phase', 'purpose', 'renderer_defaults', 'source_artifacts', 'status', 'vertices', 'warning']
- candidate_arrays:
  - key: candidates
    size: 2
    sample_types: ['dict', 'dict']
    sample: [{'combined_edges': [{'class': 'internal_g60', 'edge_class': 'internal_same_sector', 'local_a': 0, 'local_b': 16, 'residue_a': 0, 'residue_b': 16, 'sector_a': 0, 'sector_b': 0, 'shared_petersen_vertex': None, 'shift_mod60': None, 'source': 0, 'target': 16}, {'class': 'internal_g60', 'edge_class': 'internal_same_sector', 'local_a': 0, 'local_b': 19, 'residue_a': 0, 'residue_b': 19, 'sector_a': 0, 'sector_b': 0, 'shared_petersen_vertex': None, 'shi
  - key: first_read
    size: 5
    sample_types: ['str', 'str', 'str']
    sample: ['Phase 30 exports both closure-bearing P900 candidates.', 'Orbit 2 remains the provisional selector from Phase 27.']
  - key: vertices
    size: 900
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'bit': 0, 'id': 0, 'local': 0, 'residue_mod30': 0, 'sector': 0}, {'bit': 0, 'id': 1, 'local': 1, 'residue_mod30': 1, 'sector': 0}]

### public_html/json/p900/p900_stub_summary.json

- bytes: 530
- sha256: `3b47569f234aff31c127f09b3da7776bd09b976510f365b5676645cbaa18bfec`
- ok: True
- type: dict
- size: 10
- keys: ['address_form', 'construction_layers', 'core_slogan', 'g15_edges', 'g15_model', 'g15_positions', 'name', 'p900_state_count', 'status', 'thalion_states_per_position']
- candidate_arrays:
  - key: construction_layers
    size: 4
    sample_types: ['str', 'str', 'str']
    sample: ['address_space_only', 'internal_g60_edges_later']

### reports/derived/edge_column_assignment.json

- bytes: 6345
- sha256: `31b478e740554f4f2f233d4df2c7a1a88990595c12db2b4454b5f7d61548fbfc`
- ok: True
- type: dict
- size: 1
- keys: ['assignment']
- candidate_arrays:
  - key: assignment
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'edge': [0, 1], 'cocycle_value': 0, 'column': 1, 'support': [6, 7, 8, 9, 10, 11, 12]}, {'edge': [0, 2], 'cocycle_value': 1, 'column': 2, 'support': [4, 6, 7, 9, 11, 12, 14]}]

### reports/derived/edge_column_signatures.json

- bytes: 42968
- sha256: `4ab614d0fb8b7471b33d2fbde061dc2ff109de4980dd1f096a6df34b79214d7d`
- ok: True
- type: dict
- size: 2
- keys: ['columns', 'edges']
- candidate_arrays:
  - key: edges
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'idx': 0, 'edge': [0, 1], 'hist': [[[0, 1, 1, 1], 2], [[0, 1, 1, 2], 4], [[1, 1, 2, 2], 4], [[1, 2, 2, 2], 4], [[1, 2, 2, 3], 4], [[2, 2, 2, 2], 1], [[2, 2, 2, 3], 8], [[2, 2, 3, 3], 2]]}, {'idx': 1, 'edge': [0, 2], 'hist': [[[0, 1, 1, 1], 2], [[0, 1, 1, 2], 4], [[1, 1, 2, 2], 4], [[1, 2, 2, 2], 4], [[1, 2, 2, 3], 4], [[2, 2, 2, 2], 1], [[2, 2, 2, 3], 8], [[2, 2, 3, 3], 2]]}]
  - key: columns
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'idx': 0, 'support': [6, 7, 8, 9, 10, 11, 12], 'hist': [[1, 1], [2, 10], [3, 8], [4, 4], [5, 6]]}, {'idx': 1, 'support': [4, 6, 7, 9, 11, 12, 14], 'hist': [[1, 3], [2, 6], [3, 8], [4, 8], [5, 4]]}]

### reports/derived/edge_column_signatures_colored.json

- bytes: 113588
- sha256: `a435477c6053dabbf17ca6fb2d2744fea385ac1d5b2aa7fa505c6b0b30f31532`
- ok: True
- type: dict
- size: 2
- keys: ['columns', 'edges']
- candidate_arrays:
  - key: edges
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'idx': 0, 'edge': [0, 1], 'value': 0, 'hist': [[[0, 0, [0, [1, 1, 2, 2]]], 1], [[0, 0, [0, [1, 2, 2, 3]]], 2], [[0, 0, [0, [2, 2, 2, 3]]], 4], [[0, 0, [1, [0, 1, 1, 2]]], 2], [[0, 1, [0, [1, 1, 2, 2]]], 3], [[0, 1, [0, [1, 2, 2, 2]]], 4], [[0, 1, [0, [1, 2, 2, 3]]], 2], [[0, 1, [0, [2, 2, 2, 2]]], 1], [[0, 1, [0, [2, 2, 2, 3]]], 4], [[0, 1, [0, [2, 2, 3, 3]]], 2], [[0, 1, [1, [0, 1, 1, 1]]], 2], [[0, 1, [1, [0, 1, 1, 2]]], 2]]}, {'idx': 1, 'edg
  - key: columns
    size: 30
    sample_types: ['dict', 'dict', 'dict']
    sample: [{'idx': 0, 'support': [6, 7, 8, 9, 10, 11, 12], 'hist': [[1, 1], [2, 10], [3, 8], [4, 4], [5, 6]]}, {'idx': 1, 'support': [4, 6, 7, 9, 11, 12, 14], 'hist': [[1, 3], [2, 6], [3, 8], [4, 8], [5, 4]]}]

### reports/overlap9_graph.json

- bytes: 5623
- sha256: `6d0019afc29a94033410491f05acb837124da9a457de66e19b11b4e91dd7fe58`
- ok: True
- type: dict
- size: 9
- keys: ['adjacency_list', 'adjacency_matrix', 'adjacency_rule', 'degrees', 'derived_from', 'diameter', 'distance_matrix', 'graph_name', 'vertex_count']
- candidate_arrays:
  - key: degrees
    size: 15
    sample_types: ['int', 'int', 'int']
    sample: [4, 4]
  - key: adjacency_matrix
    size: 15
    sample_types: ['list', 'list', 'list']
    sample: [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]]
  - key: distance_matrix
    size: 15
    sample_types: ['list', 'list', 'list']
    sample: [[0, 1, 1, 3, 2, 2, 3, 2, 2, 2, 2, 1, 2, 2, 1], [1, 0, 1, 2, 3, 2, 2, 2, 1, 3, 2, 2, 2, 1, 2]]

## Text hits

### public_html/json/p900/manifest.json

- L3: `    "P900 is a fully constructed thalion-cluster graph.",`
- L4: `    "The preferred representative is the final P900 law.",`
- L5: `    "The external layer alone is connected.",`
- L7: `    "P900 has been identified with AT4val[60,6] or any known graph census object."`
- L10: `    "p900_stub_summary.json",`
- L11: `    "p900_phase13_candidate_orbit_families.json",`
- L12: `    "p900_phase15_local_balance_score.json",`
- L13: `    "p900_phase16_preferred_representative_edge_law.json",`
- L14: `    "p900_phase17_external_edge_list.json",`
- L15: `    "p900_phase18_component_structure.json",`
- L16: `    "p900_phase19_doubled_g15_sheet_audit.json",`
- L17: `    "p900_phase20_checkpoint_summary.json"`

### public_html/json/p900/p900_phase13_candidate_orbit_families.json

- L5: `      "edge_label_counts": {`
- L6: `        "half_turn": 15,`
- L10: `      "half_turn_closure_count": 279,`
- L12: `      "identity_half_turn_balance_gap": 1,`
- L15: `      "representative_half_turn_set": [`
- L96: `      "edge_label_counts": {`
- L97: `        "half_turn": 15,`
- L101: `      "half_turn_closure_count": 279,`
- L103: `      "identity_half_turn_balance_gap": 1,`
- L106: `      "representative_half_turn_set": [`
- L195: `  "name": "P900 Phase 13 Candidate Orbit Families",`
- L197: `    "choose one representative from each gap-1 orbit and build explicit edge-law tables",`

### public_html/json/p900/p900_phase15_local_balance_score.json

- L5: `    "The lower local balance score is preferred as a representative for the next external-surface tests.",`
- L8: `  "name": "P900 Phase 15 Local Balance Score",`
- L11: `    "half_turn_set": [`
- L22: `        "half_turn_closure": 5,`
- L28: `        "half_turn_closure": 6,`
- L34: `        "half_turn_closure": 32,`
- L40: `        "half_turn_closure": 90,`
- L46: `        "half_turn_closure": 146,`
- L54: `    "total_half_turn_closures": 279,`
- L61: `      "half_turn_set": [`
- L72: `          "half_turn_closure": 5,`
- L78: `          "half_turn_closure": 6,`

### public_html/json/p900/p900_phase16_preferred_representative_edge_law.json

- L2: `  "edge_label_counts": {`
- L3: `    "half_turn": 15,`
- L6: `  "edge_records": [`
- L8: `      "g15_edge": [`
- L12: `      "interface_label": "half_turn",`
- L13: `      "petersen_edge_a": [`
- L17: `      "petersen_edge_b": [`
- L25: `      "g15_edge": [`
- L29: `      "interface_label": "half_turn",`
- L30: `      "petersen_edge_a": [`
- L34: `      "petersen_edge_b": [`
- L42: `      "g15_edge": [`

### public_html/json/p900/p900_phase17_external_edge_list.json

- L37: `    "4": 900`
- L39: `  "external_edge_count": 1800,`
- L40: `  "external_edges": [`
- L18043: `    "The preferred representative external law materializes as 1800 inter-thalion edges.",`
- L18044: `    "Each P900 state has external degree 4.",`
- L18045: `    "This graph is the external surface layer only.",`
- L18046: `    "Internal G60 edges are not included yet."`
- L18048: `  "name": "P900 Phase 17 External Edge List",`
- L18049: `  "p900_vertex_count": 900,`
- L18051: `  "preferred_half_turn_set": [`
- L18058: `  "source": "p900_phase16_preferred_representative_edge_law.json",`
- L18059: `  "status": "external_surface_checkpoint",`

### public_html/json/p900/p900_phase18_component_structure.json

- L5623: `    "The external-only P900 surface decomposes into 30 equal components.",`
- L5626: `    "If each component is organized by one residue mod 30, the external surface is explicitly G30-indexed."`
- L5631: `  "name": "P900 Phase 18 Component Structure Audit",`
- L5635: `  "source": "p900_phase17_external_edge_list.json",`
- L5636: `  "status": "external_surface_audit",`
- L5637: `  "warning": "This audits the external inter-thalion surface only. It does not include internal G60 edges."`

### public_html/json/p900/p900_phase19_doubled_g15_sheet_audit.json

- L4: `  "all_sheets_have_60_edges": true,`
- L8: `    "Within a sheet, shift 0 gives parallel edges between the two bit layers.",`
- L9: `    "Within a sheet, shift 30 gives cross edges between the two bit layers.",`
- L10: `    "The preferred external P900 layer is therefore a G30-indexed family of identical 2-lifts of G15."`
- L12: `  "name": "P900 Phase 19 Doubled-G15 Sheet Audit",`
- L13: `  "preferred_half_turn_set": [`
- L30: `      "bit_edge_counts": {`
- L37: `      "edge_count": 60,`
- L39: `      "sample_edges": [`
- L245: `      "bit_edge_counts": {`
- L252: `      "edge_count": 60,`
- L254: `      "sample_edges": [`

### public_html/json/p900/p900_phase20_checkpoint_summary.json

- L4: `    "address_space_is_900": true,`
- L9: `    "external_component_count_is_30": true,`
- L10: `    "external_degree_uniform_4": true,`
- L11: `    "external_edge_count_is_1800": true,`
- L12: `    "external_layer_not_connected": true,`
- L15: `    "sheets_have_60_edges": true,`
- L19: `    "P900 is currently treated as a candidate consonance surface, not a proven graph identity.",`
- L20: `    "The address space is 15 x 60 = 900 states.",`
- L22: `    "Binary 0/30 sign grammar eliminates orientation drift in the audited cycle holonomy tests.",`
- L24: `    "The current preferred representative is gap1_orbit_2 with half-turn set [0,1,2,3,9].",`
- L25: `    "The preferred external edge law produces 1800 inter-thalion edges and uniform external degree 4.",`
- L26: `    "The external-only layer decomposes into 30 components of size 30.",`

### public_html/json/p900/p900_phase30_combined_graph_export.json

- L4: `      "combined_edges": [`
- L7: `          "edge_class": "internal_same_sector",`
- L21: `          "edge_class": "internal_same_sector",`
- L35: `          "edge_class": "internal_same_sector",`
- L48: `          "class": "external_p900",`
- L49: `          "edge_class": "external_half_turn_mod30",`
- L62: `          "class": "external_p900",`
- L63: `          "edge_class": "external_half_turn_mod30",`
- L76: `          "class": "external_p900",`
- L77: `          "edge_class": "external_half_turn_mod30",`
- L91: `          "edge_class": "internal_same_sector",`
- L104: `          "class": "external_p900",`

### public_html/json/p900/p900_stub_summary.json

- L5: `    "internal_g60_edges_later",`
- L9: `  "core_slogan": "P900 is the surface where thalions become vertices without ceasing to be bodies.",`
- L10: `  "g15_edges": 30,`
- L13: `  "name": "P900 Consonance Surface Stub",`
- L14: `  "p900_state_count": 900,`

### public_html/labs/constructor/kernel/p900_external_renderer.js

- L1: `const P900_EDGE_URL = "/json/p900/p900_phase17_external_edge_list.json";`
- L2: `const P900_CHECKPOINT_URL = "/json/p900/p900_phase20_checkpoint_summary.json";`
- L12: `function buildP900Point(sector, local, modelTick = 0, echoLayer = 0) {`
- L16: `  const overdrive = Math.max(0, Number(modelTick) - 900);`
- L79: `  const artifactVisible = Math.min(900, Math.max(0, Math.floor(Number(simStateCount) || 0)));`
- L94: `  const overdrive = Math.max(0, Math.floor(Number(simStateCount) || 0) - 900);`
- L95: `  const fullEchoLayers = Math.floor(overdrive / 900);`
- L96: `  const partialEchoStates = overdrive % 900;`
- L106: `export async function loadP900ExternalData() {`
- L107: `  const [edgeRes, checkpointRes] = await Promise.all([`
- L108: `    fetch(P900_EDGE_URL, { cache: "no-store" }),`
- L109: `    fetch(P900_CHECKPOINT_URL, { cache: "no-store" }),`

### public_html/labs/p900_observatory/kernel/local_storage_lenses.js

- L1: `const P900_LENS_STORAGE_KEY = "p900_saved_lenses_v1";`
- L2: `const P900_LENS_SCHEMA_VERSION = 1;`
- L29: `    schemaVersion: Number(raw.schemaVersion || P900_LENS_SCHEMA_VERSION),`
- L35: `    return storage.getItem(P900_LENS_STORAGE_KEY);`
- L43: `    storage.setItem(P900_LENS_STORAGE_KEY, value);`
- L53: `  const testKey = P900_LENS_STORAGE_KEY + "_test";`
- L106: `    schemaVersion: P900_LENS_SCHEMA_VERSION,`
- L163: `    storage.removeItem(P900_LENS_STORAGE_KEY);`

### public_html/labs/p900_observatory/kernel/p900_data.js

- L1: `const PHASE30_URL = "/json/p900/p900_phase30_combined_graph_export.json";`
- L19: `function normalizeEdge(e) {`
- L31: `    kind: e.edge_class || e.class || "edge",`
- L32: `    class: e.class || e.edge_class || "edge",`
- L48: `  const internalEdges = Array.isArray(raw.internal_edges)`
- L49: `    ? raw.internal_edges.map(normalizeEdge)`
- L52: `  const externalEdges = Array.isArray(raw.external_edges)`
- L53: `    ? raw.external_edges.map(normalizeEdge)`
- L56: `  const combinedEdges = Array.isArray(raw.combined_edges)`
- L57: `    ? raw.combined_edges.map(normalizeEdge)`
- L58: `    : internalEdges.concat(externalEdges);`
- L65: `    half_turn_set: raw.half_turn_set || [],`

### public_html/labs/p900_observatory/kernel/p900_geometry.js

- L69: `export function buildEdges(candidate, view) {`
- L70: `  const lists = candidate.edge_lists || {};`
- L76: `  if (view === "external_p900" || view === "residue_sheets") {`
- L77: `    return lists.external_p900 || [];`

### public_html/labs/p900_observatory/kernel/renderer.js

- L43: `function edgeColor(kind, alpha) {`
- L45: `  if (kind === "external_half_turn_mod30") return "rgba(217, 184, 108, " + alpha + ")";`
- L46: `  if (kind === "external_identity_same_local") return "rgba(120, 170, 255, " + alpha + ")";`
- L54: `  if (view === "external_p900") {`
- L81: `  const edgeAlpha = Math.max(0, Math.min(1, Number(options.edgeAlpha ?? 0.38)));`
- L84: `  const edgeEnabled = options.showEdges ?? true;`
- L98: `  if (edgeEnabled && edgeAlpha > 0) {`
- L99: `    const edgeItems = [];`
- L101: `    for (const e of scene.edges) {`
- L106: `      edgeItems.push({`
- L107: `        edge: e,`
- L114: `    edgeItems.sort((a, b) => b.depth - a.depth);`

### public_html/labs/g900_admission/kernel/g900_data.js

- L1: `window.G900_DATA = {`
- L5: `      caption: "The finite construction kernel: G15, G60, signed carriers, and half-flip.",`
- L7: `        "The G900 candidate begins with a bounded kernel: a 15-slot graph, a 60-state fiber graph, a carrier signing, and a half-flip involution h(x) = x + 30 mod 60.",`
- L11: `        ["G15", "15 slot vertices and 30 slot edges."],`
- L12: `        ["G60", "60 fiber states and 120 fiber edges."],`
- L13: `        ["Carrier law", "Slot edges couple fibers by identity or half-flip."],`
- L14: `        ["Half-flip", "h pairs local states into 30 opposite pairs and satisfies h^2 = id."]`
- L19: `      caption: "The generated graph has 900 vertices, 3600 edges, and degree split 4 + 4.",`
- L21: `        "The vertex set is V(G15) x V(G60), giving 15 x 60 = 900 vertices.",`
- L22: `        "The edge set combines internal fiber edges with carrier edges. Each vertex receives four internal neighbors and four carrier neighbors, so the graph is 8-regular."`
- L25: `        ["Vertices", "900"],`
- L26: `        ["Edges", "3600 total: 1800 internal and 1800 carrier."],`

### public_html/labs/g900_admission/kernel/renderer.js

- L2: `  function drawG900(canvas, viewName) {`
- L29: `    drawLedgerPulse(ctx, cx, cy, min, viewName);`
- L104: `  function drawLedgerPulse(ctx, cx, cy, min, viewName) {`
- L107: `      object: "900 / 3600 / 8",`
- L108: `      receipts: "QED LEDGER CLOSED",`
- L118: `    ctx.fillText(labels[viewName] || "G900", cx, cy);`
- L129: `  window.G900_RENDERER = {`
- L130: `    drawG900: drawG900`

### notes/900conjecture.md

- L1: `# 900 Resonance Conjecture`
- L19: `The primary incidence rectangle on the core is the sector-edge matrix M of size`
- L29: `The conjectural claim is that 900 is the first genuinely overdetermined resonance point in the current Thalean arithmetic.`
- L32: `900 is a privileged resonance number because it has multiple native realizations:`
- L34: `- 900 = 15 * 60`
- L35: `- 900 = 30^2`
- L36: `- 900 = 2 * (15 * 30)`
- L44: `Among composites generated from the native Thalean scales and primary incidence dimensions, 900 is the lowest value with at least three independent native realizations.`
- L49: `900 is not only the first overdetermined resonance number, but marks a genuine cross-phase threshold between the G15, G30, and G60 strata.`
- L53: `## Why 900 is favored over arbitrary numbers`
- L54: `900 is structurally near the organism's own arithmetic.`
- L64: `So 900 is not favored because it is round or visually pleasing.`

### notes/900conjecture_v2.md

- L1: `# 900 Resonance Conjecture v2`
- L10: `The center of gravity is no longer just that 900 appears multiple times.`
- L16: `- 900 is the scalar that witnesses that balance`
- L42: `900 = 15 * 60 = 30^2`
- L46: `- 900 is the balance witness of the ladder`
- L51: `The importance of 900 is no longer just that it is a round number or that it can be decomposed in several ways.`
- L57: `So 900 appears as the scalar that certifies multiplicative balance between:`
- L63: `The primary incidence rectangle on the quotient-visible core is the sector-edge matrix M of size`
- L69: `900 = 2 * (15 * 30)`
- L75: `This route is currently treated as strengthening evidence, not as the foundational reason for 900.`
- L87: `The same witness 900 reappears through the doubled legibility rectangle:`
- L89: `900 = 2 * (15 * 30)`

### notes/lift_signed_mode_bridge_note.md

- L1: `# Lift-Signed Mode Bridge Note`
- L8: `- the signed lift / cocycle layer`
- L14: `The goal is to define the first natural operator that carries the signed-lift data into the centered Q-arena.`
- L21: `On the quotient core G15, the sector-edge incidence matrix is`
- L29: `This is the unsigned sector-overlap Gram matrix.`
- L31: `### Signed lift / cocycle data`
- L36: `is a signed 2-lift.`
- L38: `Each edge of G15 is classified as either:`
- L42: `Equivalently, the lift carries a sign function`
- L44: `sigma : E(G15) -> {+1, -1}`
- L70: `How do we convert the signed edge data of the lift into an operator acting on the centered sector-mode space?`
- L76: `## 3. Edge-sign diagonal operator`

### notes/p900_camera_defaults_autorotate.md

- L1: `# P900 Camera Defaults and Auto Rotate`
- L20: `    It does not alter P900 artifact data or simulator overdrive semantics.`

### notes/p900_external_overdrive.md

- L1: `# P900 Simulator Overdrive`
- L5: `The simulator intentionally breaks the 900-state artifact boundary after the checkpoint.`
- L9: `    0..900:`
- L12: `    at 900:`
- L17: `        sim_states continues beyond 900`
- L18: `        overdrive = sim_states - 900`
- L19: `        visual renders post-900 echo layers`
- L23: `    artifact_states remains 900`
- L24: `    post-900 states are simulated, not theorem-backed P900 states`
- L25: `    internal G60 thalion edges are still not added`

### notes/p900_external_play_reveal.md

- L1: `# P900 External Play Reveal`
- L5: `P900 External now uses the existing play/tick controls as a reveal animation.`
- L9: `    The D4 growth engine is still not treated as the source of P900.`
- L14: `    tick 0 shows no P900 states`
- L15: `    tick N shows the first N P900 states and edges whose endpoints are visible`
- L16: `    tick 900 shows the full external P900 scaffold`

### notes/p900_external_render_mode.md

- L1: `# P900 External Render Mode`
- L5: `Adds a separate `P900 External` render mode to the existing constructor lab.`
- L9: `    This mode loads public P900 JSON artifacts.`
- L11: `    It renders the external P900 scaffold only.`
- L12: `    It does not include internal G60 thalion edges.`
- L16: `    /json/p900/p900_phase17_external_edge_list.json`
- L17: `    /json/p900/p900_phase20_checkpoint_summary.json`

### notes/p900_lab_boot_syntax_fix.md

- L1: `# P900 Lab Boot Syntax Fix`
- L5: `Fixed malformed template literal lines in the P900 console readout.`

### notes/p900_public_json_bridge.md

- L1: `# P900 Public JSON Bridge`
- L5: `Selected P900 external-surface sandbox artifacts have been copied into:`
- L7: `    public_html/json/p900/`
- L11: `    make P900 checkpoint data available to browser-side renderer code`
- L15: `    The preferred external P900 layer is a G30-indexed family`
- L20: `    this is external-surface data only`
- L22: `    no final P900 law is claimed`

### notes/p900_start_view_autorotate_off.md

- L1: `# P900 Start View and Auto Rotate Off`
- L5: `The constructor now opens on the preferred P900 view:`
- L7: `    mode: P900 External Scaffold`
- L8: `    tick: 900`
- L17: `    It does not change P900 artifact data.`

### notes/p900_yaw_11_clear_stage_text.md

- L1: `# P900 Yaw 11 and Clear Stage Text`
- L8: `    P900 stage overlay text has been removed`

### notes/remove_exact_p900_canvas_text.md

- L1: `# Remove Exact P900 Canvas Text`
- L5: `Removed the exact P900 canvas overlay text block from p900_external_renderer.js.`
- L9: `    P900 Simulator: ...`
- L10: `    artifact 900, overdrive ...`
- L11: `    post-900 echo beyond checkpoint`

### reports/derived/edge_column_assignment.json

- L2: `  "assignment": [`
- L4: `      "edge": [`
- L21: `      "edge": [`
- L38: `      "edge": [`
- L55: `      "edge": [`
- L72: `      "edge": [`
- L89: `      "edge": [`
- L106: `      "edge": [`
- L123: `      "edge": [`
- L140: `      "edge": [`
- L157: `      "edge": [`
- L174: `      "edge": [`

### reports/derived/edge_column_signatures.json

- L2: `  "edges": [`
- L5: `      "edge": [`
- L86: `      "edge": [`
- L167: `      "edge": [`
- L248: `      "edge": [`
- L329: `      "edge": [`
- L410: `      "edge": [`
- L491: `      "edge": [`
- L572: `      "edge": [`
- L653: `      "edge": [`
- L734: `      "edge": [`
- L815: `      "edge": [`

### reports/derived/edge_column_signatures_colored.json

- L2: `  "edges": [`
- L5: `      "edge": [`
- L207: `      "edge": [`
- L457: `      "edge": [`
- L675: `      "edge": [`
- L925: `      "edge": [`
- L1175: `      "edge": [`
- L1409: `      "edge": [`
- L1643: `      "edge": [`
- L1877: `      "edge": [`
- L2095: `      "edge": [`
- L2313: `      "edge": [`

## Next

Use this to identify whether Aletheos contains an earlier or alternate P900/G900 edge source.
