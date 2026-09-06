"""Column discovery helper used by the probes: name, type, and the table's row count."""
from _shared.q import run
def cols(db, schema, table, label=None):
    r = run(f"select column_name, data_type from {db}.information_schema.columns where table_schema='{schema}' and table_name='{table}' order by ordinal_position", label or f"cols {table}")
    print(f"-- {db}.{schema}.{table}: {len(r)} cols"); print(", ".join(f"{x['COLUMN_NAME']}:{x['DATA_TYPE'][:4]}" for x in r)); return r
