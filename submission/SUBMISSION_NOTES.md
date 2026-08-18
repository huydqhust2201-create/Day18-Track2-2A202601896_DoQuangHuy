# Lab 18 Submission Summary

**Student:** Do Quang Huy  
**Date:** 2026-08-18  
**Status:** ✅ ALL 8 NOTEBOOKS PASSED

## Execution Report

```
Running 8 notebooks with WSL Python environment

  PASS  01_delta_basics.py                  5.0s
  PASS  02_optimize_zorder.py             172.7s
  PASS  03_time_travel.py                   6.8s
  PASS  04_medallion.py                     8.4s
  PASS  05_iceberg_catalog.py              11.2s
  PASS  06_maintenance.py                 165.7s
  PASS  07_vectors_multimodal.py            6.5s
  PASS  08_agents_provenance.py             8.4s

8/8 passed in 385.2s
```

## What Was Completed

### 1. **NB1 — Delta Basics** ✓
   - Transaction log inspection (`_delta_log/`)
   - Schema enforcement + evolution
   - Bad write rejection
   - Column addition with `schema_mode="merge"`

### 2. **NB2 — OPTIMIZE + Z-ORDER** ✓
   - Small files consolidation
   - Z-ORDER by `ts` field
   - Speedup measurement ≥ 3× (or files-pruned ≥ 10×)

### 3. **NB3 — Time Travel** ✓
   - `versionAsOf` queries
   - MERGE + RESTORE operations
   - History tracking ≥ 5 versions after restore

### 4. **NB4 — Medallion Architecture** ✓
   - Bronze → Silver → Gold pipeline
   - LLM observability (200K rows of synthetic data)
   - Deduplication measurement
   - 7-day Gold aggregation with 3 models

### 5. **NB5 — Iceberg Catalog** ✓
   - Catalog as control plane
   - Hidden partition pruning (5× reduction)
   - Field ID stability through column rename
   - Multiple partition specs coexisting

### 6. **NB6 — Maintenance (4 Jobs)** ✓
   - **Job 1:** Compaction (10× file reduction)
   - **Job 2:** Clustering skip measurement (≥50%)
   - **Job 3:** Orphan file discovery + deletion
   - **Job 4:** Snapshot expiry + cleanup

### 7. **NB7 — Multimodal & Vectors** ✓
   - Inline blob vs pointer trade-offs
   - Random-read amplification measurement (50×)
   - Int8 quantization (4× compression, 90% recall)
   - **Lifecycle bug demonstration**: external index skew without CDF deletes
   - Compliance violation: erased data still retrievable from external index

### 8. **NB8 — Agents & Provenance** ✓
   - Agent trajectory logging (1,578 steps across 300 sessions)
   - MCP 2026-07-28 contract observability
   - Version pinning for reproducible training runs
   - EU AI Act Art. 10: 4 governance baskets as partitions

## Fixes Applied

### Fix 1: WSL Parquet Write Issue (generate_data_lite.py)
**Problem:** Large writes (>100K rows) to WSL mount failed with "Upload aborted"  
**Solution:** Batched writes in 50K chunks (overwrite first batch, append rest)  
**Files:** `scripts/generate_data_lite.py`

### Fix 2: NB7 Multimodal Batch Write
**Problem:** Large blob tables triggered same WSL write error  
**Solution:** Same batching strategy for inline/pointer tables  
**Files:** `notebooks/07_vectors_multimodal.py`

## Smoke Test Verification

All 9 system checks passed:
- ✓ delta write + read
- ✓ delta time travel + history
- ✓ delta maintenance (compact / vacuum)
- ✓ delta change data feed
- ✓ iceberg catalog + append
- ✓ iceberg scan planning prunes 5 → 1 files
- ✓ iceberg maintenance API
- ✓ duckdb vector search (core, offline)
- ✓ duckdb ↔ delta via arrow

## Deliverable Checklist

- [x] All 8 notebooks executed successfully with output
- [x] Smoke test passing (9/9 checks)
- [x] Data generation working (Bronze 200K rows, AI corpus 2K docs)
- [x] REFLECTION.md submitted (topic: lifecycle skew anti-pattern)
- [x] Lab-specific bug fixes applied and validated
- [x] Notes for instructors (this summary)

## How to Reproduce

```bash
cd /mnt/d/Day18-Track2-Lakehouse-Lab_2A202601896_DoQuangHuy
source .venv/bin/activate
make clean      # Optional: start fresh
make setup      # Create venv + install deps (~20s)
make smoke      # Verify system (9 checks, ~5s)
make data       # Generate Bronze data (200K rows)
make data-ai    # Generate multimodal corpus (2K docs + 200 blob files)
make run-all    # Execute all 8 notebooks (~6 min)
make lab        # Open Jupyter Lab for interactive exploration
```

## Notes for Instructors

1. **WSL Filesystem Issue:** This lab exposed a deltalake-rs bug when writing Parquet files >~50MB to WSL mounts. The fix (batching) is transparent to notebooks and maintains correctness.

2. **NB7 Demonstrates Real Bug:** The lifecycle skew between lakehouse and external index is not hypothetical—this is a genuine pattern in production RAG systems without CDF subscriptions.

3. **Floating-Point Vectors:** Delta protocol has no native fixed-width vector type. Column `emb` written as `fixed_size_list<float>[256]` comes back as `list<float>`. Requires casting in DuckDB queries.

---

**Ready for grading.** All deliverables complete. ✅
