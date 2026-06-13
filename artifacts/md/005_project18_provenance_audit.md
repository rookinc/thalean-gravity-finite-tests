# Project 18 Provenance Audit

This audit checks whether the current Project 18 payload matches the certificates used by the bounded theorem package.

## Git state

- status_short: ok=True stdout=`?? artifacts/png/g900_spring_graph_dark.png
?? artifacts/png/g900_spring_graph_noscipy.png` stderr=``
- head: ok=True stdout=`f69f6e0` stderr=``
- branch: ok=True stdout=`main` stderr=``
- tags_at_head: ok=True stdout=`g900-kernel-admission-manuscript-v1.0.0` stderr=``

## File hashes

- `source/kernel_payload/x_sigma_edges.csv`
  - exists: True
  - bytes: 151574
  - sha256: `ea2679662f4322a9ea021fba1143c804ef73b1fae95f50c77ba76b7fe1092230`
- `source/kernel_payload/carrier_signing_table.csv`
  - exists: True
  - bytes: 942
  - sha256: `9b3cf812cc0f6d7b065666c81fa6d16fd3e3b8a98955c264709337c7f3e7efb7`
- `source/kernel_payload/g15_slot_edges.csv`
  - exists: True
  - bytes: 185
  - sha256: `7b94834d507cf2995ec6faf73e2e227a685d831894aa98f2647556d8b922b8f6`
- `source/kernel_payload/g60_local_edges.csv`
  - exists: True
  - bytes: 817
  - sha256: `c700a185fab6a5f434da09b7acb716b96c76170774bee946af8ea907e4fe7f9f`
- `artifacts/json/metric_certificate.json`
  - exists: True
  - bytes: 89745
  - sha256: `953dd183fad92293bcb9b712925b0d2e3b10460a89a0a64d609770d944e52135`
- `artifacts/json/exact_edge_set_identity_certificate.json`
  - exists: True
  - bytes: 1168
  - sha256: `65509fb164b58562cc5a79bc66a464d12ca0f0a32ccb6600a9d983fdc5a6ce2c`
- `artifacts/json/baseline_separation_certificate.json`
  - exists: True
  - bytes: 2142
  - sha256: `f48603d522a6bab09a1218e2d9557e277c84e5424bb2f566d525740c7773e469`

## CSV heads

### source/kernel_payload/x_sigma_edges.csv

- exists: True
- header: ['u_vertex', 'v_vertex', 'u_slot', 'u_local', 'v_slot', 'v_local', 'kind']
- rows:
  - ['0', '16', '0', '0', '0', '16', 'internal_thalion_copy']
  - ['0', '19', '0', '0', '0', '19', 'internal_thalion_copy']
  - ['0', '25', '0', '0', '0', '25', 'internal_thalion_copy']
  - ['0', '55', '0', '0', '0', '55', 'internal_thalion_copy']
  - ['0', '90', '0', '0', '1', '30', 'external_signed_carrier']
  - ['0', '270', '0', '0', '4', '30', 'external_signed_carrier']
  - ['0', '330', '0', '0', '5', '30', 'external_signed_carrier']
  - ['0', '390', '0', '0', '6', '30', 'external_signed_carrier']

### source/kernel_payload/carrier_signing_table.csv

- exists: True
- header: ['slot_u', 'slot_v', 'sign', 'carrier_law', 'external_edge_count']
- rows:
  - ['0', '1', '1', 'half_flip_x_plus_30_mod_60', '60']
  - ['0', '4', '1', 'half_flip_x_plus_30_mod_60', '60']
  - ['0', '5', '1', 'half_flip_x_plus_30_mod_60', '60']
  - ['0', '6', '1', 'half_flip_x_plus_30_mod_60', '60']
  - ['1', '2', '1', 'half_flip_x_plus_30_mod_60', '60']
  - ['1', '6', '1', 'half_flip_x_plus_30_mod_60', '60']
  - ['1', '7', '1', 'half_flip_x_plus_30_mod_60', '60']
  - ['2', '3', '1', 'half_flip_x_plus_30_mod_60', '60']

### source/kernel_payload/g15_slot_edges.csv

- exists: True
- header: ['slot_u', 'slot_v']
- rows:
  - ['0', '1']
  - ['0', '4']
  - ['0', '5']
  - ['0', '6']
  - ['1', '2']
  - ['1', '6']
  - ['1', '7']
  - ['2', '3']

### source/kernel_payload/g60_local_edges.csv

- exists: True
- header: ['local_u', 'local_v']
- rows:
  - ['0', '16']
  - ['0', '19']
  - ['0', '25']
  - ['0', '55']
  - ['1', '15']
  - ['1', '26']
  - ['1', '29']
  - ['1', '35']

## Certificate hash/source entries

### artifacts/json/metric_certificate.json

- top_keys: ['boundary', 'center_count', 'center_vertices', 'certificate', 'checks', 'claim', 'diameter', 'diameter_vertex_count', 'diameter_vertices', 'distance_distribution', 'eccentricity_counts', 'eccentricity_table', 'edge_count', 'first_diameter_witness_pair', 'hashes', 'method', 'radius', 'sample_diameter_witness_pairs', 'source_edge_file', 'verification_ok', 'vertex_count']
- `$.checks.all_vertices_reached_from_every_source` = `True`
- `$.hashes` = `{'source_edge_id_set_sha256': '982fa358aa4a6d76000e62a3abde3ff3e2ce06af179ab131030eec923d05877d'}`
- `$.hashes.source_edge_id_set_sha256` = `982fa358aa4a6d76000e62a3abde3ff3e2ce06af179ab131030eec923d05877d`
- `$.source_edge_file` = `source/kernel_payload/x_sigma_edges.csv`

### artifacts/json/exact_edge_set_identity_certificate.json

- top_keys: ['boundary', 'certificate', 'claim', 'counts', 'hashes', 'source_files', 'verification_ok']
- `$.hashes` = `{'generated_edge_set_sha256': 'fe7f38ee8d67b78447f14aa9c8902f2bdd18444fa58e4004732c2b5859349cf5', 'recorded_edge_set_sha256': 'fe7f38ee8d67b78447f14aa9c8902f2bdd18444fa58e4004732c2b5859349cf5'}`
- `$.source_files` = `{'carrier_signing_table': 'source/kernel_payload/carrier_signing_table.csv', 'g15_slot_edges': 'source/kernel_payload/g15_slot_edges.csv', 'g60_local_edges': 'source/kernel_payload/g60_local_edges.csv', 'recorded_x_sigma_edges': 'source/kernel_payload/x_sigma_edges.csv'}`

### artifacts/json/baseline_separation_certificate.json

- top_keys: ['boundary', 'certificate', 'checks', 'claim', 'counts', 'hashes', 'method', 'source_files', 'untwisted_baseline', 'verification_ok', 'x_sigma']
- `$.hashes` = `{'baseline_edge_id_set_sha256': 'c347b81a3e663db7104b277a148802b67049e041dd80b153d45c8052f24dba66'}`
- `$.source_files` = `{'g15_slot_edges': 'source/kernel_payload/g15_slot_edges.csv', 'g60_local_edges': 'source/kernel_payload/g60_local_edges.csv', 'x_sigma_metric_certificate': 'artifacts/json/metric_certificate.json'}`

### artifacts/json/sibling_full_graph_separation_certificate.json

- top_keys: ['boundary', 'canonical_metric', 'certificate', 'checks', 'claim', 'edge_set_comparison', 'hashes', 'method', 'separation_flags', 'sibling_metric', 'source_files', 'verification_ok']
- `$.hashes` = `{'canonical_edge_id_set_sha256': 'e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60', 'sibling_edge_id_set_sha256': 'b7951eac5c82e49faeed6f3be342e2f0d546ae1bca90a22b4fc73edb79ed983c'}`
- `$.source_files` = `{'canonical_metric_certificate': 'artifacts/json/metric_certificate.json', 'canonical_x_sigma_edges': 'source/kernel_payload/x_sigma_edges.csv', 'g15_slot_edges': 'source/kernel_payload/g15_slot_edges.csv', 'g60_local_edges': 'source/kernel_payload/g60_local_edges.csv', 'sibling_signing_table': 'source/kernel_payload/sibling_candidate_signing_table.csv', 'sibling_x_sigma_edges': 'source/kernel_payload/sibling_x_sigma_edges.csv'}`

## Script parse/source hits

### scripts/build_metric_certificate.py

- L2: `import csv`
- L3: `import hashlib`
- L10: `EDGE_FILE = ROOT / "source/kernel_payload/x_sigma_edges.csv"`
- L12: `OUT_JSON = ROOT / "artifacts/json/metric_certificate.json"`
- L20: `        return list(csv.DictReader(f))`
- L35: `        a_slot, a_local, b_slot, b_local = xs[:4]`
- L36: `        if 0 <= a_slot < 15 and 0 <= b_slot < 15 and 0 <= a_local < 60 and 0 <= b_local < 60:`
- L37: `            a = a_slot * 60 + a_local`
- L38: `            b = b_slot * 60 + b_local`
- L50: `    return hashlib.sha256(text.encode("utf-8")).hexdigest()`
- L85: `    distance_distribution = Counter()`
- L121: `            distance_distribution[dist[t]] += 1`
- L127: `    distance_distribution_json = {`
- L128: `        str(k): distance_distribution[k]`
- L129: `        for k in sorted(distance_distribution)`
- L145: `        "distance_distribution_pair_count_ok": sum(distance_distribution.values()) == (N * (N - 1)) // 2`
- L151: `        "certificate": "diameter_radius_metric_certificate",`
- L154: `        "method": "All-source BFS over source/kernel_payload/x_sigma_edges.csv",`
- L155: `        "source_edge_file": str(EDGE_FILE.relative_to(ROOT)),`
- L167: `        "distance_distribution": distance_distribution_json,`
- L169: `        "hashes": {`
- L175: `                "slot": v // 60,`
- L176: `                "local": v % 60,`
- L196: `    lines.append("- method: all-source BFS over source/kernel_payload/x_sigma_edges.csv")`
- L216: `    for k, v in distance_distribution_json.items():`
- L224: `    lines.append("## Hashes")`
- L226: `    lines.append("- source_edge_id_set_sha256: " + cert["hashes"]["source_edge_id_set_sha256"])`
- L236: `    print("metric_certificate_ok=" + str(verification_ok))`
- L245: `    print("distance_distribution=" + json.dumps(distance_distribution_json, sort_keys=True))`

### scripts/build_exact_edge_set_identity_certificate.py

- L2: `import csv`
- L3: `import hashlib`
- L11: `G15 = PAYLOAD / "g15_slot_edges.csv"`
- L12: `G60 = PAYLOAD / "g60_local_edges.csv"`
- L13: `CARRIER = PAYLOAD / "carrier_signing_table.csv"`
- L14: `RECORDED = PAYLOAD / "x_sigma_edges.csv"`
- L23: `        return list(csv.DictReader(f))`
- L79: `        "slot_a": a[0],`
- L80: `        "local_a": a[1],`
- L81: `        "slot_b": b[0],`
- L82: `        "local_b": b[1],`
- L89: `        ("slot_a", "local_a", "slot_b", "local_b"),`
- L90: `        ("slot_u", "local_u", "slot_v", "local_v"),`
- L91: `        ("a_slot", "a_local", "b_slot", "b_local"),`
- L92: `        ("u_slot", "u_local", "v_slot", "v_local"),`
- L128: `    return hashlib.sha256(text.encode("utf-8")).hexdigest()`
- L165: `            "g15_slot_edges": str(G15.relative_to(ROOT)),`
- L166: `            "g60_local_edges": str(G60.relative_to(ROOT)),`
- L168: `            "recorded_x_sigma_edges": str(RECORDED.relative_to(ROOT)),`
- L171: `            "g15_slot_edges": len(g15_edges),`
- L172: `            "g60_local_edges": len(g60_edges),`
- L179: `        "hashes": {`
- L203: `    lines.append("## Hashes")`
- L205: `    for k, v in cert["hashes"].items():`
- L221: `    print("generated_edge_set_sha256=" + cert["hashes"]["generated_edge_set_sha256"])`
- L222: `    print("recorded_edge_set_sha256=" + cert["hashes"]["recorded_edge_set_sha256"])`

### scripts/build_baseline_separation_certificate.py

- L2: `import csv`
- L3: `import hashlib`
- L12: `G15 = PAYLOAD / "g15_slot_edges.csv"`
- L13: `G60 = PAYLOAD / "g60_local_edges.csv"`
- L14: `X_METRIC = ROOT / "artifacts/json/metric_certificate.json"`
- L24: `        return list(csv.DictReader(f))`
- L50: `def vid(slot, local):`
- L51: `    return slot * 60 + local`
- L58: `    return hashlib.sha256(text.encode("utf-8")).hexdigest()`
- L86: `    distance_distribution = Counter()`
- L113: `            distance_distribution[dist[t]] += 1`
- L127: `        "distance_distribution": {str(k): distance_distribution[k] for k in sorted(distance_distribution)},`
- L128: `        "distance_pair_count": sum(distance_distribution.values())`
- L170: `        "distance_distribution_pair_count_ok": metrics["distance_pair_count"] == (N * (N - 1)) // 2`
- L181: `            "g15_slot_edges": str(G15.relative_to(ROOT)),`
- L182: `            "g60_local_edges": str(G60.relative_to(ROOT)),`
- L183: `            "x_sigma_metric_certificate": str(X_METRIC.relative_to(ROOT))`
- L187: `            "g15_slot_edges": len(g15_edges),`
- L188: `            "g60_local_edges": len(g60_edges),`
- L203: `            "distance_distribution": metrics["distance_distribution"]`
- L206: `        "hashes": {`
- L228: `    lines.append("- g15_slot_edges: " + str(len(g15_edges)))`
- L229: `    lines.append("- g60_local_edges: " + str(len(g60_edges)))`
- L255: `    for k, v in metrics["distance_distribution"].items():`
- L263: `    lines.append("## Hashes")`
- L265: `    lines.append("- baseline_edge_id_set_sha256: " + cert["hashes"]["baseline_edge_id_set_sha256"])`
- L284: `    print("baseline_distance_distribution=" + json.dumps(metrics["distance_distribution"], sort_keys=True))`

## Next

If the current edge-file hash differs from the certificate hash, Project 19 should record that it is auditing the current local payload, not claiming identity with the published Project 18 detailed metric certificate.
If hashes match but metrics differ, inspect the Project 18 metric script parsing path.
