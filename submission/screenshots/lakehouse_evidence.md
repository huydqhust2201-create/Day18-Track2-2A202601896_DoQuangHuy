# Evidence — lightweight path

Per `rubric.md`, the lightweight-path substitute for a MinIO console screenshot is
`tree _lakehouse/` plus the contents of one `_delta_log/*.json`. Both captured below,
generated after `make setup && make smoke && make data && make data-ai && make run-all`.

## `tree _lakehouse/` (directories capped at 8 entries for readability; blob/parquet
counts noted where truncated)

```
_lakehouse/
├── blobs/
│   ├── frame_0000.bin
│   ├── frame_0001.bin
│   ├── frame_0002.bin
│   ├── frame_0003.bin
│   ├── frame_0004.bin
│   ├── frame_0005.bin
│   ├── frame_0006.bin
│   ├── frame_0007.bin
│   └── ... (192 more)
├── bronze/
│   ├── agent_traces/
│   │   ├── _delta_log/
│   │   │   └── 00000000000000000000.json
│   │   └── part-00000-ee20f6c8-0e8a-4bff-8dfa-a72a6cb0da89-c000.snappy.parquet
│   ├── docs_multimodal/
│   │   ├── _delta_log/
│   │   │   └── 00000000000000000000.json
│   │   └── part-00000-724f56b4-467c-4cd5-b9e2-a7198efd17ee-c000.snappy.parquet
│   └── llm_calls_raw/
│       ├── _delta_log/
│       │   ├── 00000000000000000000.json
│       │   ├── 00000000000000000001.json
│       │   ├── 00000000000000000002.json
│       │   └── 00000000000000000003.json
│       ├── part-00000-68283625-427d-4f00-9cd0-c15cbd2799c2-c000.snappy.parquet
│       ├── part-00000-7bd76ff7-10d2-4bf6-b3b3-5c4b6fc1efa3-c000.snappy.parquet
│       ├── part-00000-7ed5574b-2606-4d51-980a-6ca14f31146d-c000.snappy.parquet
│       └── part-00000-cee901e4-3871-45fa-a007-746ab9a92771-c000.snappy.parquet
├── gold/
│   ├── agent_performance/
│   │   ├── _delta_log/
│   │   │   └── 00000000000000000000.json
│   │   └── part-00000-47595e0a-8d6b-403a-9810-550d9f2f4d1f-c000.snappy.parquet
│   └── llm_daily_metrics/
│       ├── _delta_log/
│       │   ├── 00000000000000000000.json
│       │   └── 00000000000000000001.json
│       ├── date=2026-04-01/  (2 parquet parts)
│       ├── date=2026-04-02/  (2 parquet parts)
│       ├── date=2026-04-03/  (2 parquet parts)
│       ├── date=2026-04-04/  (2 parquet parts)
│       ├── date=2026-04-05/  (2 parquet parts)
│       ├── date=2026-04-06/  (2 parquet parts)
│       └── date=2026-04-07/  (2 parquet parts)
├── iceberg/           # NB5/NB6/NB8 catalogs — pyiceberg SQLite catalog + Avro/JSON metadata
├── silver/
│   ├── agent_trajectories/_delta_log/
│   └── llm_calls_clean/_delta_log/
└── vectors/
    ├── inline/_delta_log/
    └── pointer/_delta_log/
```

`bronze/gold/silver/vectors` each carry their own `_delta_log/` — the transaction log
that makes every one of these directories an ACID Delta table, not just a folder of
Parquet files.

## Contents of one `_delta_log/*.json` — `bronze/llm_calls_raw/_delta_log/00000000000000000000.json`

The file is newline-delimited JSON (one commit action per line); pretty-printed below.

**commitInfo** — this commit's operation metadata:

```json
{
  "commitInfo": {
    "timestamp": 1787068494435,
    "operation": "WRITE",
    "operationParameters": { "mode": "Overwrite" },
    "engineInfo": "delta-rs:py-1.6.2",
    "operationMetrics": {
      "execution_time_ms": 153,
      "num_added_files": 1,
      "num_added_rows": 50000,
      "num_partitions": 0,
      "num_removed_files": 0
    },
    "clientVersion": "delta-rs.py-1.6.2"
  }
}
```

**protocol** — reader/writer version the table requires:

```json
{ "protocol": { "minReaderVersion": 1, "minWriterVersion": 2 } }
```

**metaData** — table id and schema:

```json
{
  "metaData": {
    "id": "3568873f-e6d0-4ea7-bfb2-754a3121f04c",
    "format": { "provider": "parquet", "options": {} },
    "schemaString": "{\"type\":\"struct\",\"fields\":[{\"name\":\"request_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"ts\",\"type\":\"timestamp\",\"nullable\":true,\"metadata\":{}},{\"name\":\"raw_json\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]}",
    "partitionColumns": [],
    "createdTime": 1787068494289,
    "configuration": {}
  }
}
```

**add** — the Parquet file this commit added, with column-level min/max/null stats
(this is what lets a query engine skip files without opening them):

```json
{
  "add": {
    "path": "part-00000-68283625-427d-4f00-9cd0-c15cbd2799c2-c000.snappy.parquet",
    "partitionValues": {},
    "size": 3563093,
    "modificationTime": 1787068494434,
    "dataChange": true,
    "stats": "{\"numRecords\":50000,\"minValues\":{\"ts\":\"2026-04-01T00:00:00Z\",\"request_id\":\"00027712-f769-4ec7-85b5-4c04e564d490\"},\"maxValues\":{\"ts\":\"2026-04-02T17:59:56Z\",\"request_id\":\"fffeb1ec-0ef6-4656-bd0e-e96483b2eb0c\"},\"nullCount\":{\"raw_json\":0,\"request_id\":0,\"ts\":0}}"
  }
}
```

`bronze/llm_calls_raw` shows **4 commits** in `_delta_log/` (`...0000` through
`...0003`) from the batched 50K-row writes described in `SUBMISSION_NOTES.md` — visible
proof the transaction log grows one JSON file per commit, exactly as NB1 asserts.
