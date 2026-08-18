"""Debug script to identify the deltalake write issue."""
import sys
import os
from pathlib import Path

# Check disk space
stat = os.statvfs('/mnt/d')
free_gb = stat.f_bavail * stat.f_frsize / (1024**3)
print(f"Disk space available on /mnt/d: {free_gb:.1f} GB")

# Check path
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from lakehouse import path, reset

bronze_path = path("bronze", "llm_calls_raw")
print(f"Target path: {bronze_path}")
print(f"Path exists: {Path(bronze_path).exists()}")

# Try creating small dataframe
import polars as pl
import pyarrow as pa
from deltalake import write_deltalake

print(f"Polars version: {pl.__version__}")
print(f"PyArrow version: {pa.__version__}")

# Create minimal test
print("\nCreating minimal test dataframe...")
df = pl.DataFrame({
    "id": [1, 2, 3],
    "value": ["a", "b", "c"]
})

print(f"DataFrame: {df}")
print(f"Arrow table schema: {df.to_arrow().schema}")

# Reset and try to write
reset(bronze_path)
print(f"\nAttempting write to {bronze_path}...")
try:
    write_deltalake(bronze_path, df.to_arrow(), mode="overwrite")
    print("✓ Write succeeded!")
except Exception as e:
    print(f"✗ Write failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
